import json,sys,urllib.request,urllib.parse,os
OUT='/home/claude/insetos/fotos'
Q={'bombardeiro':dict(taxon_id='122211,251460'),
   'formigaleao':dict(taxon_id='49358',term_id=1,term_value_id=6),
   'rolabosta':dict(taxon_id='199919,49104')}
cred=json.load(open(OUT+'/creditos.json'))
for ins,q in Q.items():
    p=dict(q,photo_license='cc-by,cc0',quality_grade='research',per_page=60,order_by='votes',photos='true')
    u='https://api.inaturalist.org/v1/observations?'+urllib.parse.urlencode(p)
    d=json.load(urllib.request.urlopen(u,timeout=30)); n=0
    for o in d['results']:
        ph=o['photos'][0]; dim=ph.get('original_dimensions') or {}
        if ph.get('license_code') not in('cc-by','cc0'): continue
        if dim and dim.get('width',0)<dim.get('height',1)*1.15: continue
        url=ph['url'].replace('square','large'); fn=f'{OUT}/{ins}_{n:02d}.jpg'
        try: urllib.request.urlretrieve(url,fn)
        except Exception as e: continue
        cred[os.path.basename(fn)]=dict(autor=(o['user'].get('name') or o['user']['login']),lic=ph['license_code'],obs=f"https://www.inaturalist.org/observations/{o['id']}",tax=o['taxon']['name'])
        n+=1
        if n>=12: break
    print(ins,n,d['total_results'])
json.dump(cred,open(OUT+'/creditos.json','w'),ensure_ascii=False,indent=1)
