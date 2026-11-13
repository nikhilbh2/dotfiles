"""Offline installer regression tests using temporary homes, never the real home."""
import os
from pathlib import Path
import subprocess
import shutil
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ('handoff', 'resume', 'thabto')

class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='skills test ')
        self.home = Path(self.tmp.name) / 'home'
        self.home.mkdir()
        self.env = dict(os.environ, HOME=str(self.home))
        for key in ('XDG_DATA_HOME', 'CODEX_HOME'):
            self.env.pop(key, None)

    def tearDown(self):
        self.tmp.cleanup()

    def run_install(self, *args, ok=True):
        result = subprocess.run(['bash', str(ROOT/'install-skills.sh'), *args],
                                env=self.env, capture_output=True, text=True)
        self.assertEqual(result.returncode == 0, ok, result.stdout + result.stderr)
        return result

    def test_fresh_and_repeat(self):
        self.run_install()
        self.run_install()
        for name in SKILLS:
            for directory in ('.local/share', '.agents', '.claude', '.codex'):
                p = self.home / directory / 'skills' / name
                self.assertEqual(p.resolve(), ROOT/'skills'/name)

    def test_dry_run_creates_nothing(self):
        self.run_install('--dry-run')
        self.assertEqual(list(self.home.iterdir()), [])

    def test_legacy_dangling_link_migration(self):
        shared = self.home/'.local/share/skills/thabto'
        shared.parent.mkdir(parents=True)
        shared.symlink_to(ROOT/'skills/.local/share/skills/thabto')
        discovery = self.home/'.claude/skills/thabto'
        discovery.parent.mkdir(parents=True)
        discovery.symlink_to(shared)
        self.run_install('--dry-run')
        self.assertEqual(os.readlink(shared), str(ROOT/'skills/.local/share/skills/thabto'))
        self.run_install()
        self.assertEqual(discovery.resolve(), ROOT/'skills/thabto')

    def test_direct_legacy_discovery_link(self):
        target = self.home/'.agents/skills/thabto'
        target.parent.mkdir(parents=True)
        target.symlink_to(ROOT/'skills/.local/share/skills/thabto')
        self.run_install()
        self.assertEqual(target.resolve(), ROOT/'skills/thabto')

    def test_broken_unmanaged_discovery_link(self):
        target = self.home/'.claude/skills/resume'
        target.parent.mkdir(parents=True)
        target.symlink_to('/missing/user/skill')
        self.run_install(ok=False)
        self.assertEqual(os.readlink(target), '/missing/user/skill')
        self.assertFalse((self.home/'.local').exists())

    def test_source_checkout_with_spaces(self):
        root = Path(self.tmp.name)/'source checkout'
        root.mkdir()
        shutil.copy2(ROOT/'install-skills.sh', root/'install-skills.sh')
        shutil.copytree(ROOT/'skills', root/'skills')
        result = subprocess.run(['bash', str(root/'install-skills.sh')], env=self.env,
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((self.home/'.agents/skills/handoff').resolve(), root/'skills/handoff')

    def test_conflict_preflight_leaves_no_partial_install(self):
        conflict = self.home/'.codex/skills/thabto'
        conflict.mkdir(parents=True)
        (conflict/'user-data').write_text('keep me')
        self.run_install(ok=False)
        self.assertFalse((self.home/'.local').exists())
        self.assertEqual((conflict/'user-data').read_text(), 'keep me')

    def test_other_checkout_symlink_preserved(self):
        conflict = self.home/'.local/share/skills/thabto'
        conflict.parent.mkdir(parents=True)
        conflict.symlink_to('/another/checkout/skills/.local/share/skills/thabto')
        self.run_install(ok=False)
        self.assertEqual(os.readlink(conflict), '/another/checkout/skills/.local/share/skills/thabto')
        self.assertFalse((self.home/'.agents').exists())

    def test_custom_paths_and_duplicate_discovery(self):
        self.env['XDG_DATA_HOME'] = str(self.home/'shared data')
        self.env['CODEX_HOME'] = str(self.home/'.agents')
        self.run_install()
        self.run_install()
        self.assertEqual((self.home/'shared data/skills/handoff').resolve(), ROOT/'skills/handoff')

    def test_custom_codex_home(self):
        self.env['CODEX_HOME'] = str(self.home/'custom codex')
        self.run_install()
        self.assertEqual((self.home/'custom codex/skills/resume').resolve(), ROOT/'skills/resume')

    def test_alias_discovery_directory(self):
        (self.home/'.claude').mkdir()
        (self.home/'.agents').symlink_to(self.home/'.claude')
        self.run_install()
        self.assertEqual((self.home/'.agents/skills/resume').resolve(), ROOT/'skills/resume')

    def test_parent_file_preflight(self):
        (self.home/'.codex').write_text('not a directory')
        self.run_install(ok=False)
        self.assertFalse((self.home/'.local').exists())

    def test_unknown_option(self):
        self.run_install('--overwrite', ok=False)
        self.assertEqual(list(self.home.iterdir()), [])

if __name__ == '__main__':
    unittest.main()
