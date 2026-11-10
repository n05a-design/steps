#!/usr/bin/env python3
"""Respektvoller Ableton-Blog-METADATEN-Indexer. Keine Artikeltextkopien oder Assetdownloads.
Abhängigkeiten: pip install requests beautifulsoup4
Beispiel: python index_ableton_blog.py --max-pages 150 --delay 2.5 --out ableton_index.csv
Kein gesetzter Rechte- oder robots-Override. Exakter Vollcrawlnachweis nur bei Abschluss der Paginierung.
"""
import argparse,csv,time,re,sys,json
from urllib.parse import urljoin,urlparse,urlunparse,parse_qs
from urllib.robotparser import RobotFileParser
import requests
from bs4 import BeautifulSoup
BASE='https://www.ableton.com'
UA='STEPS-Library-ResearchIndexer/0.1 (metadata-only; polite)' 
CATS=['/de/blog/','/de/blog/categories/tutorials/','/de/blog/categories/downloads/',
      '/de/blog/categories/artists/','/de/blog/categories/videos/',
      '/de/blog/categories/news/','/de/blog/categories/podcasts/']
def canonical(u):
 p=urlparse(u)
 if p.hostname not in ('www.ableton.com','ableton.com'):return ''
 path=p.path
 if not re.fullmatch(r'/de/blog/[a-zA-Z0-9-]+/',path):return ''
 if path in ['/de/blog/categories/','/de/blog/tags/']:return ''
 return BASE+path

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--max-pages',type=int,default=150)
 ap.add_argument('--delay',type=float,default=2.5);ap.add_argument('--out',default='ableton_blog_metadata.csv')
 ap.add_argument('--fetch-article-metadata',action='store_true');a=ap.parse_args()
 s=requests.Session();s.headers['User-Agent']=UA
 rob=RobotFileParser();rob.set_url(BASE+'/robots.txt')
 try:rob.read()
 except Exception as exc:sys.exit('robots.txt nicht verfügbar; aus Sicherheitsgründen abgebrochen: '+str(exc))
 fetched=0;seen=set();rows={};errors=[];stopped={}
 def get(u):
  nonlocal fetched
  if not rob.can_fetch(UA,u):raise PermissionError('robots disallows '+u)
  time.sleep(max(1.0,a.delay))
  r=s.get(u,timeout=22);r.raise_for_status();fetched+=1
  if not r.url.startswith(BASE):raise ValueError('Redirect außerhalb der Domain')
  return BeautifulSoup(r.text,'html.parser')
 for cat in CATS:
  last_new=0;empty=0;page=1;status='max_pages'
  while page<=a.max_pages:
   u=BASE+cat+(('?page='+str(page)) if page>1 else '')
   try:soup=get(u)
   except Exception as exc:
    errors.append({'url':u,'error':str(exc)});status='fetch_error';break
   current=set()
   for link in soup.select('a[href]'):
    full=urljoin(u,link['href']);c=canonical(full)
    if not c:continue
    parent=link.find_parent(['h1','h2','h3','h4'])
    if not parent:continue
    title=parent.get_text(' ',strip=True)
    if len(title)<8:continue
    current.add(c)
    row=rows.setdefault(c,{'url':c,'title':title,'listing_category':cat,'article_title':'','article_description':'','article_date':'','status':'listing_only'})
   # If site repeats old posts or returns no items, stop rather than assuming endless pagination.
   new=current-seen
   if not new:empty+=1
   else:empty=0
   seen|=current
   if empty>=2:status='terminal_repeated_pages';break
   page+=1
  stopped[cat]={'last_page_attempted':page,'stop_reason':status}
 if a.fetch_article_metadata:
  for c,row in list(rows.items()):
   try:
    soup=get(c)
    title=soup.find('meta',property='og:title');desc=soup.find('meta',attrs={'name':'description'})
    date=soup.find('meta',property='article:published_time')
    if title:row['article_title']=title.get('content','')
    if desc:row['article_description']=desc.get('content','')[:280]
    if date:row['article_date']=date.get('content','')
    row['status']='article_html_seen'
   except Exception as exc:errors.append({'url':c,'error':str(exc)})
 with open(a.out,'w',newline='',encoding='utf-8-sig') as f:
  cols=['url','title','listing_category','article_title','article_description','article_date','status']
  w=csv.DictWriter(f,fieldnames=cols);w.writeheader();w.writerows(sorted(rows.values(),key=lambda x:x['url']))
 with open(a.out+'.audit.json','w',encoding='utf8') as f:
  json.dump({'count':len(rows),'fetched':fetched,'stops':stopped,'errors':errors,'complete':all(v['stop_reason']=='terminal_repeated_pages' for v in stopped.values()) and not errors},f,ensure_ascii=False,indent=2)
 print(f'Artikel: {len(rows)}; Seitenabrufe: {fetched}; Fehler: {len(errors)}; Dateien: {a.out}')
if __name__=='__main__':main()
