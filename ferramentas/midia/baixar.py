import json,urllib.parse,urllib.request,time,os,sys,re
UA={'User-Agent':'NuncaVistoBot/1.0 (https://github.com/aupontocortes-tech/nuncavisto)'}
def get(u,bin=False):
    for i in range(6):
        try:
            r=urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=120).read()
            return r if bin else json.loads(r)
        except Exception as e: print('retry',e,flush=True); time.sleep(5*(i+1))
def api(**p):
    p.update(action='query',format='json'); return get('https://commons.wikimedia.org/w/api.php?'+urllib.parse.urlencode(p)) or {}
Q=json.load(open('consultas.json'))
os.makedirs('midia',exist_ok=True); man=[]
for chave,qs in Q.items():
    n=0
    for q in qs:
        vid=q.startswith('V:'); qq=q[2:] if vid else q
        if qq.startswith('File:'): ts=[qq]
        else:
            r=api(list='search',srsearch=qq+(' filetype:video' if vid else ' filetype:bitmap'),srnamespace=6,srlimit=6)
            ts=[x['title'] for x in r.get('query',{}).get('search',[])]
        if not ts: continue
        r=api(titles='|'.join(ts),prop='imageinfo|videoinfo',iiprop='url|size|extmetadata|mime',iiurlwidth=1920,viprop='url|size|derivatives|extmetadata')
        for p in r.get('query',{}).get('pages',{}).values():
            ii=(p.get('videoinfo') or p.get('imageinfo') or [None])[0]
            if not ii: continue
            m=ii.get('extmetadata',{}); lic=m.get('LicenseShortName',{}).get('value','')
            if 'NC' in lic or 'ND' in lic: continue
            art=re.sub('<[^>]+>','',m.get('Artist',{}).get('value',''))[:80]
            if vid:
                ders=[d for d in ii.get('derivatives',[]) if d.get('type','').startswith('video/webm') and d.get('height',0) and d['height']<=1080]
                if not ders: continue
                d=max(ders,key=lambda d:d['height']); url=d['src']; ext='webm'
            else:
                url=ii.get('thumburl') or ii['url']; ext='jpg'
            n+=1; fn=f'midia/{chave}_{n:02d}.{ext}'
            data=get(url,bin=True)
            if data: open(fn,'wb').write(data); man.append(dict(arq=fn,titulo=p['title'],licenca=lic,autor=art)); print(fn,p['title'],lic,flush=True)
            time.sleep(1)
        time.sleep(1)
json.dump(man,open('midia/manifesto.json','w'),ensure_ascii=False,indent=1)
