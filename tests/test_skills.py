"""Bundle/frontmatter and offline CLI smoke checks; not provider integration tests."""
from pathlib import Path
import ast
import re
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]

class SkillTests(unittest.TestCase):
    def test_skill_names_and_frontmatter(self):
        for path in (ROOT/'skills').iterdir():
            text = (path/'SKILL.md').read_text()
            self.assertTrue(text.startswith('---\n'))
            front = text.split('---', 2)[1]
            self.assertIn('name: ' + path.name, front)
            self.assertRegex(front, r'\ndescription: .+')
            self.assertRegex(path.name, r'^[a-z0-9-]+$')
            self.assertNotIn('TODO', text)

    def test_local_references_exist(self):
        for name in ('handoff', 'resume'):
            folder = ROOT/'skills'/name
            for ref in re.findall(r'`(references/[^`]+)`', (folder/'SKILL.md').read_text()):
                self.assertTrue((folder/ref).is_file(), ref)

    def test_thabto_scripts_parse_and_help(self):
        for path in (ROOT/'skills/thabto/scripts').glob('*.py'):
            ast.parse(path.read_text())
            result = subprocess.run(['python3', str(path), '--help'], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn('usage:', result.stdout.lower())

if __name__ == '__main__':
    unittest.main()
