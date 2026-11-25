"""Narração por parágrafos (prosódia natural) com tempos reais das palavras. python3 tts2.py VOZ RATE"""
import asyncio,ssl,os,sys,json,subprocess,tempfile,time
ca='/root/.ccr/ca-bundle.crt'; _o=ssl.create_default_context
def _c(*a,**k):
    c=_o(*a,**k); c.load_verify_locations(ca); return c
ssl.create_default_context=_c
import edge_tts, numpy as np, soundfile as sf
VOZ=sys.argv[1]; RATE=sys.argv[2] if len(sys.argv)>2 else '+0%'
sc=json.load(open('spec.json'))['scenes']; SR=24000
# parágrafos: até 3 frases do mesmo inseto
P=[]; 
for i,s in enumerate(sc):
    if P and sc[P[-1][0]]['ins']==s['ins'] and len(P[-1])<3: P[-1].append(i)
    else: P.append([i])
async def one(text):
    ws=[]; data=b''
    for t in range(6):
        try:
            ws=[];data=b''
            async for ch in edge_tts.Communicate(text,VOZ,rate=RATE,boundary='WordBoundary').stream():
                if ch['type']=='audio': data+=ch['data']
                elif ch['type']=='WordBoundary': ws.append((ch['offset']/1e7,(ch['offset']+ch['duration'])/1e7,ch['text']))
            if len(data)>1000: return data,ws
        except Exception as e: print('retry',str(e)[:50]); await asyncio.sleep(3+t*2)
    raise RuntimeError('voz falhou')
audio=[np.zeros(int(.2*SR),np.float32)]; t=0.2; words=[]; segs=[None]*len(sc); tmp=tempfile.mkdtemp()
for pi,p in enumerate(P):
    text=' '.join(sc[i]['text'] for i in p)
    data,bw=asyncio.run(one(text)); mp3=f'{tmp}/{pi}.mp3'; open(mp3,'wb').write(data)
    subprocess.run(['ffmpeg','-y','-loglevel','error','-i',mp3,'-ac','1','-ar',str(SR),mp3[:-4]+'.wav'],check=True)
    x,_=sf.read(mp3[:-4]+'.wav',dtype='float32'); nz=np.where(np.abs(x)>0.01)[0]; lead=nz[0]; x=x[max(0,lead-200):nz[-1]+800]; shift=max(0,lead-200)/SR
    dur=len(x)/SR; toks=[(i,w) for i in p for w in sc[i]['text'].split()]
    # alinha palavras do texto com as marcas do serviço (mesma ordem)
    if abs(len(bw)-len(toks))>len(toks)*0.3: bw=[(dur*k/len(toks),dur*(k+1)/len(toks),'') for k in range(len(toks))]; shift=0
    for k,(i,w) in enumerate(toks):
        b=bw[min(k*len(bw)//len(toks),len(bw)-1)] if len(bw)!=len(toks) else bw[k]
        s0=max(0,b[0]-shift); e0=max(s0+.05,b[1]-shift); words.append({'w':w,'s':round(t+s0,3),'e':round(t+e0,3),'seg':i})
    for i in p:
        ws=[w for w in words if w['seg']==i]; segs[i]=[ws[0]['s'],ws[-1]['e']]
    audio.append(x); t+=dur; gap=.6; audio.append(np.zeros(int(gap*SR),np.float32)); t+=gap
    print(pi+1,len(P),round(t),flush=True)
audio.append(np.zeros(int(.6*SR),np.float32)); t+=.6
y=np.concatenate(audio); y=y/np.max(np.abs(y))*.89; os.makedirs('out4',exist_ok=True); sf.write('out4/narr.wav',y,SR)
json.dump({'words':words,'segs':segs,'dur':t},open('out4/timing.json','w')); print('dur',t)
