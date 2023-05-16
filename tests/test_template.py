import glob
import html5lib
from html5lib import HTMLParser
from lxml import etree
import os
import unittest

class HTMLFormattingTest(unittest.TestCase):

    def setUp(self):
        self.template_dir = 'templates'
        self.template_files = glob.glob(os.path.join(self.template_dir, '*.html')) 

    def test_html_formatting(self):
        for template_file in self.template_files:
            print(template_file)
            with open(template_file, 'r') as file:
                html_content = file.read()

            try:
                parser = HTMLParser(strict=True)
                parser.parse(html_content)
            except (etree.ParseError, html5lib.html5parser.ParseError, AssertionError) as e:
                self.fail("HTML formatting error in {}: {}".format(template_file, str(e)))

if __name__ == "__main__":
    unittest.main()

