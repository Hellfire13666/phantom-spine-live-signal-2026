import hashlib
import html.parser
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parent.parent
APPROVED_SHA256 = "5c903ba9d080a5ac1efc1f7fc49618832346b8e16e8fed0bc31421d6f1559541"

class PageParser(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(); self.refs = []; self.buttons = 0; self.codes = 0
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in ('a', 'link', 'img', 'script'):
            value = attrs.get({'a': 'href', 'link': 'href', 'img': 'src', 'script': 'src'}[tag])
            if value: self.refs.append(value)
        if tag == 'button' and attrs.get('class') == 'copy': self.buttons += 1
        if tag == 'pre' and attrs.get('class') == 'cmd': self.codes += 1

class PublicPagesTests(unittest.TestCase):
    def test_selected_art_is_preserved(self):
        self.assertEqual(hashlib.sha256((ROOT/'assets/rosie-phantom-spine-approved.png').read_bytes()).hexdigest(), APPROVED_SHA256)
    def test_five_live_pages_have_real_links(self):
        for name in ['index.html','examples.html','connections.html','adapter-guide.html','troubleshooting.html']:
            with self.subTest(page=name):
                p = PageParser(); p.feed((ROOT/name).read_text())
                for ref in p.refs:
                    if '://' not in ref and not ref.startswith(('#','mailto:')):
                        self.assertTrue((ROOT/ref.split('#')[0]).exists(), f'{name}: {ref}')
                self.assertGreaterEqual(p.buttons, 1)
                self.assertEqual(p.buttons, p.codes)
    def test_no_legacy_version_in_user_ui(self):
        for name in ['index.html','examples.html','connections.html','adapter-guide.html','troubleshooting.html']:
            body = (ROOT/name).read_text().lower()
            self.assertNotIn('live checks pending',body)
            self.assertNotIn('field check is pending',body)
            self.assertNotIn('still unverified',body)
    def test_dated_results_are_not_guarantees(self):
        body = (ROOT/'index.html').read_text()
        self.assertIn('113',body)
        self.assertIn('6',body)
        self.assertIn('dated',body.lower())
        self.assertIn('assets/rosie-phantom-spine-approved.png',body)

if __name__ == '__main__': unittest.main()
