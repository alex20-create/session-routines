"""Tests for obsidian-project-sync/scripts/vault.py.

Run from the repository root:

    python -m unittest discover -s tests

Every test builds a throwaway vault in a temporary folder; nothing outside
it is read or written.
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile
import textwrap
import unittest

SCRIPT = os.path.join(os.path.dirname(__file__), "..", "obsidian-project-sync", "scripts", "vault.py")
SCRIPT = os.path.abspath(SCRIPT)

NOTE = textwrap.dedent("""\
    ---
    type: project
    status: draft
    updated: 2026-01-01
    topic:
      - demo
    ---
    # Demo

    ## 🚀 Deploy

    Old deploy text.

    ## Recent changes

    ```ad-note
    - First change.
    ```

    ## State

    Draft.

    [[Home]]
    """)


def run(*args, stdin=None, env=None, cwd=None):
    full_env = dict(os.environ)
    for name in ("OBSIDIAN_VAULT", "OBSIDIAN_VAULT_CLAUDE"):
        full_env.pop(name, None)
    full_env.update(env or {})
    r = subprocess.run([sys.executable, "-X", "utf8", SCRIPT] + list(args),
                       input=stdin, capture_output=True, text=True,
                       encoding="utf-8", env=full_env, cwd=cwd)
    return r.returncode, r.stdout, r.stderr


class VaultTest(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.vault = os.path.join(self.tmp, "vault")
        self.project = os.path.join(self.vault, "Projects", "Demo")
        os.makedirs(self.project)
        os.makedirs(os.path.join(self.vault, "Projects", ".space"))
        self.note = os.path.join(self.project, "Demo.md")
        self.write(self.note, NOTE)
        self.write(os.path.join(self.vault, "Conventions.md"), "# Conventions\n")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def write(self, path, text):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(text)

    def read(self, path):
        with open(path, encoding="utf-8") as f:
            return f.read()

    def content(self, text):
        path = os.path.join(self.tmp, "content.md")
        self.write(path, text)
        return path

    def scan(self, *extra):
        code, out, err = run("scan", "--vault", self.vault, *extra)
        self.assertEqual(code, 0, err)
        return json.loads(out)

    # ------------------------------------------------------------ vault

    def test_no_vault_is_an_error_not_a_guess(self):
        code, out, err = run("scan")
        self.assertEqual(code, 1)
        self.assertIn("OBSIDIAN_VAULT", err)

    def test_vault_from_environment(self):
        code, out, _ = run("scan", env={"OBSIDIAN_VAULT": self.vault})
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(out)["projects"][0]["name"], "Demo")

    def test_old_environment_variable_still_works(self):
        code, _, _ = run("scan", env={"OBSIDIAN_VAULT_CLAUDE": self.vault})
        self.assertEqual(code, 0)

    def test_vault_before_the_subcommand(self):
        code, out, err = run("--vault", self.vault, "scan")
        self.assertEqual(code, 0, err)

    def test_missing_vault_folder(self):
        code, _, err = run("scan", "--vault", os.path.join(self.tmp, "nope"))
        self.assertEqual(code, 1)
        self.assertIn("does not exist", err)

    # ----------------------------------------------------------- config

    def test_defaults_are_reported(self):
        data = self.scan()
        self.assertEqual(data["config"]["source"], "defaults")
        self.assertIsNotNone(data["config"]["conventions"])

    def test_hidden_folders_are_not_projects(self):
        names = [p["name"] for p in self.scan()["projects"]]
        self.assertEqual(names, ["Demo"])

    def test_english_config(self):
        os.rename(os.path.join(self.vault, "Projects"), os.path.join(self.vault, "1 Work"))
        self.write(os.path.join(self.vault, ".claude-vault.json"),
                   json.dumps({"projects": "1 Work", "logs": "Logs"}))
        data = self.scan()
        self.assertEqual(data["config"]["source"], ".claude-vault.json")
        self.assertEqual([p["name"] for p in data["projects"]], ["Demo"])
        self.assertNotIn("warning", data["config"])

    def test_spanish_config_keys_are_aliases(self):
        os.rename(os.path.join(self.vault, "Projects"), os.path.join(self.vault, "2 Projects"))
        self.write(os.path.join(self.vault, ".claude-vault.json"),
                   json.dumps({"proyectos": "2 Projects", "registros": "Logs"}))
        data = self.scan()
        self.assertEqual(data["config"]["projects"], "2 Projects")
        self.assertEqual(data["config"]["logs"], "Logs")
        self.assertNotIn("warning", data["config"])

    def test_english_key_wins_over_alias(self):
        self.write(os.path.join(self.vault, ".claude-vault.json"),
                   json.dumps({"projects": "Projects", "proyectos": "Elsewhere"}))
        self.assertEqual(self.scan()["config"]["projects"], "Projects")

    def test_unknown_key_warns(self):
        self.write(os.path.join(self.vault, ".claude-vault.json"),
                   json.dumps({"projects": "Projects", "colour": "blue"}))
        self.assertIn("colour", self.scan()["config"]["warning"])

    def test_broken_config_warns_and_falls_back(self):
        self.write(os.path.join(self.vault, ".claude-vault.json"), "{not json")
        data = self.scan()
        self.assertEqual(data["config"]["source"], "defaults")
        self.assertIn("could not be read", data["config"]["warning"])

    def test_missing_conventions(self):
        os.remove(os.path.join(self.vault, "Conventions.md"))
        data = self.scan()
        self.assertIsNone(data["config"]["conventions"])
        self.assertIn("ask", data["config"]["conventions_warning"])

    def test_project_scan_lists_headings(self):
        card = self.scan("--project", "demo")["projects"][0]
        self.assertIn("## 🚀 Deploy", card["headings"])
        self.assertEqual(card["frontmatter"]["topic"], ["demo"])
        self.assertEqual(card["files"]["notes"], ["Demo.md"])

    def test_unknown_project_warns(self):
        self.assertIn("Ask before creating", self.scan("--project", "Nope")["warning"])

    # ---------------------------------------------------------- section

    def test_replace_dry_run_writes_nothing(self):
        code, out, _ = run("section", "--vault", self.vault, "--note", self.note,
                           "--heading", "Deploy", "--content", self.content("New."),
                           "--dry-run")
        self.assertEqual(code, 0)
        self.assertIn("+New.", out)
        self.assertIn("[DRY RUN]", out)
        self.assertEqual(self.read(self.note), NOTE)

    def test_replace_matches_heading_without_emoji(self):
        run("section", "--note", self.note, "--heading", "Deploy",
            "--content", self.content("New deploy."))
        text = self.read(self.note)
        self.assertIn("## 🚀 Deploy\n\nNew deploy.\n", text)
        self.assertNotIn("Old deploy text.", text)
        self.assertIn("## Recent changes", text)

    def test_last_section_is_protected(self):
        code, _, err = run("section", "--note", self.note, "--heading", "State",
                           "--content", self.content("Done."))
        self.assertEqual(code, 2)
        self.assertIn("last section", err)
        self.assertEqual(self.read(self.note), NOTE)

    def test_append_keeps_footer_last(self):
        run("section", "--note", self.note, "--heading", "State", "--mode", "append",
            "--content", self.content("Shipped."))
        text = self.read(self.note)
        self.assertTrue(text.rstrip().endswith("Shipped.\n\n[[Home]]"), text)

    def test_append_goes_inside_a_callout(self):
        run("section", "--note", self.note, "--heading", "Recent changes",
            "--mode", "append", "--content", self.content("- Second change."))
        text = self.read(self.note)
        self.assertIn("```ad-note\n- First change.\n\n- Second change.\n```", text)

    def test_append_joins_a_native_callout(self):
        self.write(self.note, NOTE.replace("```ad-note\n- First change.\n```",
                                           "> [!note]\n> - First change."))
        run("section", "--note", self.note, "--heading", "Recent changes",
            "--mode", "append", "--content", self.content("- Second change."))
        self.assertIn("> [!note]\n> - First change.\n>\n> - Second change.\n", self.read(self.note))

    def test_new_section_after(self):
        run("section", "--note", self.note, "--heading", "Testing", "--after", "Deploy",
            "--content", self.content("Unit tests."))
        text = self.read(self.note)
        self.assertLess(text.index("## Testing"), text.index("## Recent changes"))

    def test_missing_heading_lists_existing(self):
        code, _, err = run("section", "--note", self.note, "--heading", "Nowhere",
                           "--content", self.content("x"))
        self.assertEqual(code, 1)
        self.assertIn("## Recent changes", err)

    def test_touch_updated(self):
        run("section", "--note", self.note, "--heading", "Deploy",
            "--content", self.content("x"), "--touch-updated")
        self.assertNotIn("updated: 2026-01-01", self.read(self.note))

    # ------------------------------------------------------ frontmatter

    def test_frontmatter_scalar(self):
        run("frontmatter", "--note", self.note, "--set", "status=solid")
        text = self.read(self.note)
        self.assertIn("status: solid", text)
        self.assertIn("topic:\n  - demo", text)

    def test_frontmatter_refuses_block_list(self):
        code, _, err = run("frontmatter", "--note", self.note, "--set", "topic=x")
        self.assertEqual(code, 1)
        self.assertIn("block list", err)

    # ----------------------------------------------------------- canvas

    def canvas(self):
        path = os.path.join(self.project, "Map.canvas")
        self.write(path, json.dumps({"nodes": [
            {"id": "g1", "type": "group", "label": "draft", "x": 0, "y": 0, "width": 500, "height": 500},
            {"id": "n1", "type": "file", "file": "Projects/Demo/Demo.md", "x": 10, "y": 10, "width": 100, "height": 100},
            {"id": "n2", "type": "file", "file": "Projects/Demo/Gone.md", "x": 600, "y": 0, "width": 100, "height": 100},
        ], "edges": []}))
        return path

    def test_canvas_report(self):
        code, out, _ = run("canvas", "--vault", self.vault, "--file", self.canvas(), "--report")
        data = json.loads(out)
        self.assertEqual(data["broken_links"], ["Projects/Demo/Gone.md"])
        self.assertEqual(data["state_outside_its_group"], [])

    def test_canvas_add_dry_run_and_real(self):
        path = self.canvas()
        before = self.read(path)
        code, out, _ = run("canvas", "--file", path, "--add-file", "Projects/Demo/New.md", "--dry-run")
        self.assertIn("[DRY RUN]", out)
        self.assertEqual(self.read(path), before)
        run("canvas", "--file", path, "--add-file", "Projects/Demo/New.md", "--color", "4")
        nodes = json.loads(self.read(path))["nodes"]
        self.assertEqual(nodes[1]["x"], 10)  # existing nodes untouched
        self.assertEqual(nodes[-1]["y"], 580)

    # -------------------------------------------------------------- log

    def git_repo(self):
        repo = os.path.join(self.tmp, "demo")
        os.makedirs(repo)
        for args in (["init", "-q"], ["config", "user.email", "t@example.com"],
                     ["config", "user.name", "t"], ["commit", "-q", "--allow-empty", "-m", "one"]):
            subprocess.run(["git", "-C", repo] + args, check=True)
        return repo

    def test_log_without_vault_is_silent(self):
        code, out, err = run("log", "--quiet", "--repo", self.git_repo())
        self.assertEqual((code, out, err), (0, "", ""))

    def test_log_skips_non_repositories(self):
        run("log", "--vault", self.vault, "--repo", self.tmp)
        self.assertFalse(os.path.exists(os.path.join(self.vault, "Claude Sync")))

    def test_log_from_stdin(self):
        repo = self.git_repo()
        code, _, _ = run("log", "--vault", self.vault, "--quiet", "--stdin",
                         stdin=json.dumps({"cwd": repo}))
        self.assertEqual(code, 0)
        log = json.loads(self.read(os.path.join(self.vault, "Claude Sync", "demo.json")))
        self.assertEqual(log["sessions"][0]["commits"][0][-3:], "one")
        self.assertEqual(log["project"], "demo")

    def test_log_migrates_spanish_keys(self):
        repo = self.git_repo()
        head = subprocess.run(["git", "-C", repo, "rev-parse", "HEAD"],
                              capture_output=True, text=True).stdout.strip()
        old = {"sesiones": [{"fecha": "2026-01-01", "hora": "10:00", "rama": "main",
                             "commits": [], "archivos": [], "sin_commitear": 0}],
               "proyecto": "demo", "ruta": repo, "ultimo_commit": head,
               "ultima_sesion": "2026-01-01",
               "carpetas": {repo: {"rama": "main", "ultimo_commit": head}}}
        path = os.path.join(self.vault, "Claude Sync", "demo.json")
        self.write(path, json.dumps(old))
        subprocess.run(["git", "-C", repo, "commit", "-q", "--allow-empty", "-m", "two"], check=True)
        run("log", "--vault", self.vault, "--repo", repo, "--quiet")
        log = json.loads(self.read(path))
        self.assertNotIn("sesiones", log)
        self.assertEqual(len(log["sessions"]), 2)
        self.assertEqual(log["sessions"][0]["date"], "2026-01-01")
        self.assertEqual([c[-3:] for c in log["sessions"][1]["commits"]], ["two"])
        self.assertIn(repo, log["folders"])

    def test_log_from_a_subfolder_is_not_a_worktree(self):
        repo = self.git_repo()
        sub = os.path.join(repo, "src", "ui")
        os.makedirs(sub)
        run("log", "--vault", self.vault, "--repo", sub, "--quiet")
        log = json.loads(self.read(os.path.join(self.vault, "Claude Sync", "demo.json")))
        self.assertNotIn("worktree", log["sessions"][0])
        self.assertEqual(list(log["folders"]), [os.path.abspath(repo)])

    def test_scan_finds_the_log_through_the_note_path(self):
        self.write(self.note, NOTE.replace("status: draft", "status: draft\npath: C:/code/my-app"))
        self.write(os.path.join(self.vault, "Claude Sync", "my-app.json"),
                   json.dumps({"sessions": [{"date": "2026-01-02", "time": "09:00"}]}))
        card = self.scan("--project", "Demo")["projects"][0]
        self.assertEqual(card["session_log_file"], "my-app.json")
        self.assertEqual(len(card["session_log"]["sessions"]), 1)

    def test_scan_reports_sessions_since_note_changed(self):
        self.write(os.path.join(self.vault, "Claude Sync", "demo.json"), json.dumps({
            "sessions": [{"date": "2000-01-01", "time": "10:00"},
                         {"date": "2999-01-01", "time": "10:00"}]}))
        card = self.scan("--project", "Demo")["projects"][0]
        self.assertEqual([s["date"] for s in card["sessions_since_note_changed"]], ["2999-01-01"])


if __name__ == "__main__":
    unittest.main()
