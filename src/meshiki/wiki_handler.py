# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "html2text>=2025.4.15",
#     "wikitextparser>=3.0.0",
# ]
# ///

#Script to fetch, decompress and format wiki pages 

import bz2
import xml.etree.ElementTree as ET
import wikitextparser as wtp
from html2text import html2text as htt

INDEX_FILE = "/mnt/hgfs/D/enwiki-20260101-pages-articles-multistream-index.txt"
DATA_FILE = "/mnt/hgfs/D/enwiki-20260101-pages-articles-multistream.xml.bz2"

class WikiHandler:

    def __init__(self, index_file=INDEX_FILE, data_file=DATA_FILE):
        self.index_file = index_file
        self.data_file = data_file
    

    def find_index(self, target):
        with open(self.index_file, "r") as index:
            for line in index:
                listed = (line.split(":"))
                title = listed[2].strip()

                if target.lower() == title.lower(): 
                    offset = int(listed[0])
                    return offset, title

    def decompress_page(self, offset, title):
        with open(self.data_file, "rb") as f:
            f.seek(int(offset))

            decompressor = bz2.BZ2Decompressor()

            data = b""

            while not decompressor.eof:
                chunk = f.read(1024 * 1024)
                if not chunk:
                    break

                data += decompressor.decompress(chunk)
                xml = data.decode("utf-8", errors="ignore")

                return xml


    def find_target(self, target, xml): 
        inside_page = False
        page_lines = ["<page>"]

        for line in xml.splitlines():
            if f"<title>{target}</title>" in line:
                inside_page = True 
            if inside_page:
                page_lines.append(line.strip())
                if "</page>" in line:
                    break

        parse_me = "".join(page_lines)
        root = ET.fromstring(parse_me)
        redirect = root.find("redirect")
        if redirect != None:
            redirect = redirect.attrib["title"]

        for item in root.iter("text"):
            text = item.text

        return text, redirect


    def format_text(self, wiki_page):  

        wiki_page = wtp.parse(wiki_page)#.plain_text()

        description = None
        for template in wiki_page.templates:
            if template.name.lower() == "short description":
                if template.arguments:
                    description = template.arguments[0].value.strip()
                    break

        wiki_page = wiki_page.plain_text()
        wiki_page = htt(wiki_page)
        wiki_page = wiki_page.replace('==' or '===', '\n\n')
        wiki_page = wiki_page.replace('*', '')    

        return wiki_page, description



    def handle(self, msg):

        offset, title = self.find_index(msg)

        xml = self.decompress_page(offset, title)

        text, redirect = self.find_target(title, xml)

        if redirect != None:
            offset, title = self.find_index(redirect)
            xml = self.decompress_page(offset, title)
            text, redirect = self.find_target(title, xml)

        wiki_page, short_des = self.format_text(text)

        return wiki_page, short_des
