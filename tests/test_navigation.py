from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote
from collections import Counter
import unittest

class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.ids = []
        self.links = []
        self.feed(text)
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        if tag == 'a' and attrs.get('href', '').startswith('#'):
            self.links.append(unquote(attrs['href'][1:]))

class NavigationTests(unittest.TestCase):
    def test_all_sidebar_links_resolve_to_unique_targets(self):
        page = Page((Path(__file__).resolve().parents[1] / 'index.html').read_text(encoding='utf-8'))
        self.assertTrue(page.links, 'The course directory must have navigation links')
        duplicates = {key for key, count in Counter(page.ids).items() if count > 1}
        self.assertEqual(duplicates, set(), 'Repeated course titles need distinct anchors')
        self.assertEqual(set(page.links) - set(page.ids), set())
        self.assertNotIn('', page.links)

if __name__ == '__main__':
    unittest.main()
