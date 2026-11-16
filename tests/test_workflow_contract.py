"""Guard the handoff/resume procedural contract and keep public skills generic."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
HANDOFF = (ROOT/'skills/handoff/SKILL.md').read_text()
RESUME = (ROOT/'skills/resume/SKILL.md').read_text()

def flat(text):
    return re.sub(r'\s+', ' ', text).lower()

class WorkflowContractTests(unittest.TestCase):
    def assertSays(self, text, *phrases):
        for phrase in phrases:
            self.assertIn(phrase.lower(), flat(text), phrase)

    def test_handoff_triggers_and_batching(self):
        self.assertSays(HANDOFF, 'meaningful milestones', 'before switching',
                        'failure or blocker', 'not commit a record for every trivial tool result',
                        'never a raw transcript')

    def test_handoff_capture_fields(self):
        self.assertSays(HANDOFF, 'goal and scope', 'decisions with rationale', 'HEAD, checks',
                        'observation times', 'blockers', 'one exact next action',
                        'source links', 'active owner/writer', 'durable artifact pointers')

    def test_handoff_bounded_size_and_pruning(self):
        self.assertSays(HANDOFF, 'replace superseded state', 'link history',
                        'keep the rationale', 'prune or split')

    def test_concurrent_writers(self):
        self.assertSays(HANDOFF, 'writes only its own run record', 'coordinator',
                        'fetch and read the record immediately before',
                        'never silently drop', 'stop after three attempts',
                        'report the conflict', 'never force push')

    def test_publication_and_enforcement_honesty(self):
        self.assertSays(HANDOFF, "verify the destination's visibility",
                        'never put credentials', 'public repository',
                        'procedure, not enforcement', 'actually configured and observed')

    def test_resume_reads_canonical_record_and_claims_run(self):
        self.assertSays(RESUME, 'fetch the latest canonical record', 'run records',
                        'not depend on one transcript', 'active writer',
                        'create or claim your own run record')

    def test_run_record_template_fields(self):
        text = (ROOT/'skills/handoff/references/run-record-template.md').read_text()
        self.assertSays(text, 'owner:', 'writer:', 'last verified:', 'exact head',
                        'exact next action', 'durable artifacts', 'one writer per run record')

    def test_public_skills_have_no_private_markers(self):
        patterns = [r'atlassian\.net', r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}',
                    r'gh[pousr]_[A-Za-z0-9]{20,}', r'github_pat_', r'xox[abpr]-', r'AKIA[0-9A-Z]{16}',
                    r'BEGIN [A-Z ]*PRIVATE KEY', r'VantaInc/', r'nikhil-work-context', r'/workspaces/']
        for name in ('handoff', 'resume'):
            for path in (ROOT/'skills'/name).rglob('*.md'):
                text = path.read_text()
                for pattern in patterns:
                    self.assertIsNone(re.search(pattern, text), f'{path}: {pattern}')

if __name__ == '__main__':
    unittest.main()
