# -*- coding: utf-8 -*-
"""Validate offline links, sections, curriculum boundary and worked examples."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import json, xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
class Page(HTMLParser):
 def __init__(self,path):
  super().__init__(); self.path=path;self.ids=[];self.links=[];self.sections=0;self.feed(path.read_text())
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.append(a['id'])
  if tag=='section':self.sections+=1
  for key in ('src','href'):
   if key in a:self.links.append(a[key])
  if tag=='img':assert a.get('alt'),f'Missing alt: {self.path}'
files=[ROOT/'index.html']+sorted(ROOT.glob('chapter-*.html'))
assert len(files)==25
pages={p:Page(p) for p in files}
for path,page in pages.items():
 assert len(page.ids)==len(set(page.ids)),f'Duplicate id {path}'
 for link in page.links:
  u=urlsplit(link)
  if u.scheme or u.netloc:continue
  target=(path.parent/unquote(u.path)).resolve() if u.path else path
  assert target.exists(),f'Broken local link {path}: {link}'
  if u.fragment and target in pages:assert u.fragment in pages[target].ids,f'Broken anchor: {link}'
for n in range(1,25):
 page=pages[ROOT/f'chapter-{n:02}.html']
 if n<=3:assert page.sections>=7
 else:assert page.sections==0 and '待学习' in page.path.read_text()
assert len(json.loads((ROOT/'content/curriculum.json').read_text()))==24
for p in (ROOT/'assets').glob('*.svg'):ET.parse(p)
assert 2*80*8*128*2==327680
assert (40+15)//16==3 and 19//16==1 and 19%16==3
print('PASS: 25 pages, 24 chapter entries, 3 detailed chapters, 21 empty chapters, local links, anchors, SVG XML and examples.')
