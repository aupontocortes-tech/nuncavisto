"""Vídeo longo Nunca Visto (16:9). python3 rl.py  -> out/video_mudo.mp4 + out/fx.wav"""
import json, os, sys, subprocess, math, random, re
import numpy as np
from PIL import Image, ImageDraw, ImageFont
H='/home/claude/insetos'; N='/home/claude/nuncavisto'; OUT=H+'/long/out8'; W,Hh,FPS=1920,1080,30
spec=json.load(open(H+'/long/spec.json'))
sys.path.insert(0,H+'/long'); import ill as ILL1, ill2 as ILL2M
ILLM=type('X',(),{'ILL':{**ILL1.ILL,**ILL2M.ILL2}}); T=json.load(open(OUT+'/timing.json')); segs=T['segs']; words=T['words']; DUR=T['dur']
R=H+'/raw/'; C=H+'/clips/'
# footage por capítulo: (arquivo, [(ini,fim)...]) ; se o arquivo não existir, usa fundo desenhado
R2=H+'/raw2/'
FOOT={
 'gancho':[(C+'bomb1.mov',[(12.0,19.5)])],
 'bombardeiro':[(C+'bomb1.mov',[(3.3,8.2),(19.5,25.7)]),(C+'bomb2.mov',[(3.3,9.7),(14.3,28)])],
 'formigaleao':[(R2+'ant5.mp4',[(0,6),(30,36)]),(R2+'ant2.mp4',[(0,7)]),(R2+'ant3.mp4',[(0,4.5)]),(R2+'ant1.mp4',[(0,3)])],
 'cortadeira':[(R+'leaf.mp4',[(0,7),(20,27),(45,52)])],
 'cigarras':[(H+'/raw3/c5h.mp4',[(0,12)]),(R+'cic2c.mp4',[(0,10)]),(R+'cic1c.mp4',[(0,8)])],
 'rolabosta':[(R+'dung1.mp4',[(0,24)])],
 'final':[(R+'dung1.mp4',[(20,42)])]}
import glob
for _g in ['bombardeiro','formigaleao','cortadeira','cigarras','rolabosta']:
    FOOT[_g]=FOOT[_g]+[(p,[(0,5.9)]) for p in sorted(glob.glob(H+'/fotoclip/'+_g+'_*.mp4'))]
FOOT['final']=[(R+'dung1.mp4',[(0,42)])]+[(p,[(0,5.9)]) for p in sorted(glob.glob(H+'/fotoclip/rolabosta_*.mp4'))]
# abertura: cada frase da apresentação mostra o bicho certo
FP=H+'/fotoclip/'
GANCHO={'Um besouro, que atira':(FP+'bombardeiro_10.mp4',0),'Uma larva':(FP+'formigaleao_02.mp4',0),'Formigas, que plantam':(R+'leaf.mp4',8),'Cigarras, que passam':(H+'/raw3/c5h.mp4',4),'E um besouro':(R+'dung1.mp4',2),'E hoje':(FP+'bombardeiro_02.mp4',0)}
NOME={'bombardeiro':'BESOURO-BOMBARDEIRO','vespa':'VESPA CAÇADORA DE TARÂNTULA','formigaleao':'FORMIGA-LEÃO','rolabosta':'BESOURO ROLA-BOSTA','cortadeira':'FORMIGA CORTADEIRA','tecela':'FORMIGA TECELÃ','cigarras':'CIGARRAS DA NINHADA X','aguape':'CAÇADOR-D’ÁGUA GIGANTE','escorpiao':'MOSCA-ESCORPIÃO'}
COR={'bombardeiro':(255,120,40),'vespa':(255,200,30),'formigaleao':(230,190,110),'rolabosta':(120,200,255),'cortadeira':(110,220,90),'tecela':(90,220,160),'cigarras':(255,70,70),'aguape':(60,190,255),'escorpiao':(200,120,255),'gancho':(255,200,30),'final':(255,200,30)}
IMP=[("Quando é agarrado","ELE NÃO FOGE. ELE ATIRA","fogo"),("O resultado é uma explosão","QUASE 100 °C","fogo"),("E não sai de uma vez","ATÉ 735 PULSOS POR SEGUNDO","raio"),("Em quarenta e três","43% ESCAPARAM VIVOS","estrela"),("O recorde","107 MINUTOS DENTRO DO SAPO","relogio"),
("E tem um detalhe de engenharia","ÂNGULO CALCULADO","seta"),("Se tenta fugir","JOGA AREIA NELA","seta"),("Quando agarra","TOXINA + ENZIMAS","raio"),("Essa fase de larva","1 A 3 ANOS COMO LARVA","relogio"),
("Isso é agricultura","AGRICULTURA","folha"),("Elas fazem isso há","50 MILHÕES DE ANOS","relogio"),("Cada formiga pode","20X O PRÓPRIO PESO","seta"),("A solução delas","BACTÉRIAS = ANTIBIÓTICO","estrela"),
("Dezessete anos","17 ANOS NO ESCURO","calendario"),("Mas por que dezessete","13 E 17 = NÚMEROS PRIMOS","estrela"),("Em dois mil e vinte e quatro","JUNTAS: 1ª VEZ DESDE 1803","calendario"),
("De vez em quando","DANÇA = BÚSSOLA","seta"),("À noite, ele usa","LUA: 1 MILHÃO X MAIS FRACA","estrela"),("Sem o boné","VIA LÁCTEA = BÚSSOLA","galaxia")]
KW=set("vivo viva saiu vomitado vomitou quente canhão paralisada armadilha areia via láctea fungo agricultura costurando corrente bilhões dezessete quarenta três cento sete cinquenta milhões trinta centímetros elétrica galáxia bússola presente roubam impossíveis gigante cem mil milhão ninhos 2038 dois mil trinta oito".split())
F=lambda p,s:ImageFont.truetype(N+'/'+p,s)
fc=F('Mont900.ttf',66); fi=F('Anton.ttf',120); fn=F('Anton.ttf',64); ft=F('Mont800.ttf',40); fb=F('Anton.ttf',230)
# ---------- linha do tempo dos capítulos ----------
sc=spec['scenes']; chap=[]  # (ins,t0,t1)
for i,s in enumerate(sc):
    a,b=segs[i]
    if chap and chap[-1][0]==s['ins']: chap[-1][2]=b+0.3
    else: chap.append([s['ins'],a if chap else 0,b+0.3])
for k in range(len(chap)-1): chap[k][2]=chap[k+1][1]
chap[-1][2]=DUR
# ---------- cortes ----------
def avail(ins):
    L=[]
    for f,rs in FOOT[ins]:
        if os.path.exists(f) and os.path.getsize(f)>20000: L.append((f,rs))
    return L
cuts=[]  # (t0,t1,file|None,src_in,ins,dir,ill)
PLAN={'bombardeiro':[('bomba','Dentro do abdômen',7.0)],'formigaleao':[('leao','E tem um detalhe',8.0)],'cortadeira':[('corta','Elas usam a folha',7.0)],'cigarras':[('cigarra','Dezessete anos',6.0)],'rolabosta':[('rola','E sem lua',7.0)]}
def _st(p): return next(segs[i][0] for i,x in enumerate(sc) if x['text'].startswith(p))
random.seed(7)
GPH={'bombardeiro_02.mp4','bombardeiro_10.mp4','formigaleao_02.mp4'}
SW=_st('Pesquisadores deixaram'); SW2=_st('O recorde')
SPAN={}   # trechos ainda não usados de cada arquivo
def spans(f,rs):
    if f not in SPAN: SPAN[f]=[list(r) for r in rs]
    return SPAN[f]
def consume(f,rs,a,b):
    out=[]
    for x,y in spans(f,rs):
        if b<=x or a>=y: out.append([x,y])
        else:
            if a-x>=1.0: out.append([x,a])
            if y-b>=1.0: out.append([b,y])
    SPAN[f]=out
def take(f,rs,d):
    for sp in spans(f,rs):
        if sp[1]-sp[0]>=d-0.01: p=sp[0]; sp[0]+=d; return p
    return None
for ins,t0,t1 in chap:   # reserva o que a abertura usa
    if ins=='gancho':
        for i,x in enumerate(sc):
            for p_,(f,pp) in GANCHO.items():
                if x['ins']=='gancho' and x['text'].startswith(p_):
                    rs=next((r for ff,r in sum(FOOT.values(),[]) if ff==f),[(0,6)]); consume(f,rs,pp,pp+(segs[i+1][0]-segs[i][0]) if i+1<len(segs) else pp+5)
consume(C+'bomb1.mov',FOOT['bombardeiro'][0][1],12.0,25.0)
for ins,t0,t1 in chap:
    L=avail(ins)
    if ins=='gancho':
        fix=sorted((segs[i][0],segs[i+1][0] if i+1<len(segs) else t1,GANCHO[p]) for i,x in enumerate(sc) for p in GANCHO if x['ins']=='gancho' and x['text'].startswith(p))
        t=t0; k=0
        while t<fix[0][0]-0.05:
            d=min(random.uniform(1.8,2.6),fix[0][0]-t)
            if fix[0][0]-t-d<1.0: d=fix[0][0]-t
            cuts.append((t,t+d,C+'bomb1.mov',12.0+(t-t0),ins,k%2,None)); t+=d; k+=1
        for j,(a_,b_,(f,p)) in enumerate(fix):
            cuts.append((a_,t1 if j==len(fix)-1 else b_,f,p,ins,k%2,None)); k+=1
        continue
    vids=[x for x in L if '/fotoclip/' not in x[0]]; fot=[x for x in L if '/fotoclip/' in x[0] and x[0].split('/')[-1] not in GPH]
    iv=[(_st(p),_st(p)+ln,n) for n,p,ln in PLAN.get(ins,[])]; k=0; t=t0; vi=0; fi=0
    while t<t1-0.05:
        hit=next((x for x in iv if x[0]<=t+0.01<x[1]),None)
        if hit: d=hit[1]-t; il=hit[2]
        else:
            nxt=min([x[0] for x in iv if x[0]>t]+[t1]); d=min(random.uniform(1.8,2.8),nxt-t); il=None
            if nxt-t-d<1.2: d=nxt-t
        JT=[_st(p_) for p_ in ('O resultado é uma explosão','E não sai de uma vez','Isso alcança')]
        jt=next((j for j,a_ in enumerate(JT) if a_-0.05<=t<a_+2.2),None) if ins=='bombardeiro' and not hit else None
        if jt is not None:
            cuts.append((t,t+d,C+'bomb1.mov',[14.0,17.5,20.5][jt],ins,2,None)); t+=d; k+=1; continue
        if ins=='bombardeiro': V=[x for x in vids if ('bomb2' in x[0])==(SW<=t<SW2)]
        else: V=vids
        F_=[] if (ins=='bombardeiro' and SW<=t<SW2) else fot
        got=None
        order=(['v','f'] if (k%2==0 or ins=='bombardeiro') else ['f','v'])
        for kind in order:
            P=V if kind=='v' else F_
            for j in range(len(P)):
                f,rs=P[((vi if kind=='v' else fi)+j)%len(P)]
                if kind=='f' and f in SPAN and SPAN[f]==[]: continue
                p=take(f,rs,min(d,5.8) if kind=='f' else d) if kind=='v' else (None if f in SPAN else 0.0)
                if p is not None:
                    if kind=='f': SPAN[f]=[]; fi+=j+1
                    else: vi+=j+1
                    got=(f,p); break
            if got: break
        if not got:   # acabou material novo: reaproveita vídeo com outro enquadramento
            f,rs=V[vi%len(V)]; SPAN[f]=[list(r) for r in rs]; p=take(f,rs,d) or rs[0][0]; got=(f,p); vi+=1
            print('reuso',ins,round(t),f.split('/')[-1])
        cuts.append((t,t+d,got[0],got[1],ins,k%2,il)); t+=d; k+=1
if '--dry' in sys.argv: json.dump(cuts,open('/tmp/dry.json','w')); sys.exit()
if '--bg' in sys.argv: json.dump(cuts,open(OUT+'/cuts.json','w'))
else: cuts=[tuple(c) for c in json.load(open(OUT+'/cuts.json'))]
# ---------- fundo ----------
os.makedirs(OUT+'/seg',exist_ok=True)
def mk(i,c):
    t0,t1,f,ss,ins,dr,il=c; nf=round(t1*FPS)-round(t0*FPS); d=nf/FPS+0.1; o=f'{OUT}/seg/{i:03d}.mp4'
    if os.path.exists(o): return o
    if f:
        z=0.07 if dr==0 else 0.0
        var=['','hflip,crop=iw/1.35:ih/1.35:0:ih*0.2,','crop=iw/1.4:ih/1.4:iw*0.3:ih*0.1,','hflip,'][i%4] if ('bomb1' in f or 'bomb2' in f) else ''
        if dr==2: var='hflip,crop=iw/1.6:ih/1.6:iw*0.30:ih*0.15,'; dr=0
        pre=var+('crop=iw:ih*0.84:0:0,' if 'dung1' in f else ('crop=873:491:486:240,' if 'ant5' in f else ''))
        vf=pre+(f"scale={W}:{Hh}:force_original_aspect_ratio=increase,scale=w='trunc({W}*(1+{0.08}*t/{d:.3f})/2)*2':h='trunc({Hh}*(1+{0.08}*t/{d:.3f})/2)*2':eval=frame,crop={W}:{Hh}")
        if dr: vf=pre+(f"scale={W*1.08:.0f}:{Hh*1.08:.0f}:force_original_aspect_ratio=increase,crop={W}:{Hh}:x='(iw-{W})*t/{d:.3f}':y='(ih-{Hh})/2'")
        cmd=['ffmpeg','-loglevel','error','-y','-stream_loop','-1','-ss',f'{ss:.2f}','-i',f,'-t',f'{d:.3f}','-an','-vf',vf+f',fps={FPS},format=yuv420p','-frames:v',str(nf),'-c:v','libx264','-bf','0','-preset','veryfast','-crf','20',o]
    else:
        col='0x%02x%02x%02x'%tuple(int(x*0.25) for x in COR[ins])
        cmd=['ffmpeg','-loglevel','error','-y','-f','lavfi','-i',f'color=c={col}:s={W}x{Hh}:r={FPS}:d={d:.3f}','-vf','format=yuv420p','-frames:v',str(nf),'-c:v','libx264','-bf','0','-preset','veryfast','-crf','20',o]
    subprocess.run(cmd,check=True); return o
if __name__=='__main__' and '--bg' in sys.argv:
    fl=[mk(i,c) for i,c in enumerate(cuts)]
    open(OUT+'/list.txt','w').write(''.join(f"file '{x}'\n" for x in fl))
    subprocess.run(['ffmpeg','-loglevel','error','-y','-f','concat','-safe','0','-i',OUT+'/list.txt','-c','copy',OUT+'/bg.mp4'],check=True)
    print('bg ok',len(cuts),'cortes'); sys.exit()
# ---------- overlays ----------
def ease(x): x=max(0,min(1,x)); return 1-(1-x)**3
def txt(d,xy,s,f,fill,stroke=0,anchor='la'): d.text(xy,s,font=f,fill=fill,stroke_width=stroke,stroke_fill=(0,0,0,255),anchor=anchor)
def bug(d,cx,cy,s,col,ph=0):
    d.ellipse([cx-.5*s,cy-.28*s,cx+.5*s,cy+.28*s],fill=col+(255,),outline=(0,0,0,255),width=max(3,int(s/25)))
    d.ellipse([cx+.4*s,cy-.2*s,cx+.75*s,cy+.2*s],fill=col+(255,),outline=(0,0,0,255),width=max(3,int(s/25)))
    for k,x in enumerate((-.25,0,.25)):
        w=math.sin(ph*6+k)*.08*s
        for sg in(-1,1): d.line([cx+x*s,cy+sg*.25*s,cx+x*s+w,cy+sg*.6*s],fill=(0,0,0,255),width=max(4,int(s/18)))
    d.line([cx+.7*s,cy-.15*s,cx+.95*s,cy-.4*s],fill=(0,0,0,255),width=max(3,int(s/25))); d.line([cx+.7*s,cy+.15*s,cx+.95*s,cy+.4*s],fill=(0,0,0,255),width=max(3,int(s/25)))
    d.ellipse([cx+.55*s,cy-.08*s,cx+.65*s,cy+.02*s],fill=(255,255,255,255))
def icon(d,nome,cx,cy,s,col):
    k=(255,255,255,255); o=(0,0,0,255); c=col+(255,)
    if nome=='fogo':
        d.polygon([(cx,cy-s*.5),(cx+.35*s,cy+.1*s),(cx+.2*s,cy+.45*s),(cx-.2*s,cy+.45*s),(cx-.35*s,cy+.1*s),(cx-.1*s,cy-.1*s)],fill=c,outline=o)
        d.polygon([(cx,cy),(cx+.15*s,cy+.3*s),(cx-.15*s,cy+.3*s)],fill=(255,240,120,255))
    elif nome=='estrela':
        P=[(cx+(.5 if i%2==0 else .22)*s*math.sin(i*math.pi/5),cy-(.5 if i%2==0 else .22)*s*math.cos(i*math.pi/5)) for i in range(10)]; d.polygon(P,fill=c,outline=o)
    elif nome=='relogio':
        d.ellipse([cx-.45*s,cy-.45*s,cx+.45*s,cy+.45*s],fill=k,outline=o,width=6); d.line([cx,cy,cx,cy-.3*s],fill=o,width=7); d.line([cx,cy,cx+.2*s,cy+.1*s],fill=c,width=7)
    elif nome=='raio':
        d.polygon([(cx+.1*s,cy-.5*s),(cx-.3*s,cy+.05*s),(cx-.02*s,cy+.05*s),(cx-.12*s,cy+.5*s),(cx+.3*s,cy-.08*s),(cx+.02*s,cy-.08*s)],fill=c,outline=o)
    elif nome=='seta':
        d.polygon([(cx-.5*s,cy-.15*s),(cx+.1*s,cy-.15*s),(cx+.1*s,cy-.4*s),(cx+.5*s,cy),(cx+.1*s,cy+.4*s),(cx+.1*s,cy+.15*s),(cx-.5*s,cy+.15*s)],fill=c,outline=o)
    elif nome=='galaxia':
        d.ellipse([cx-.5*s,cy-.5*s,cx+.5*s,cy+.5*s],fill=(20,10,60,255),outline=o,width=5)
        for i in range(60):
            a=i*.35; r=.02*i*s*.8; d.ellipse([cx+r*math.cos(a)-3,cy+r*math.sin(a)-3,cx+r*math.cos(a)+3,cy+r*math.sin(a)+3],fill=(200,210,255,255))
    elif nome=='folha':
        d.polygon([(cx-.45*s,cy+.4*s),(cx-.3*s,cy-.2*s),(cx+.1*s,cy-.5*s),(cx+.45*s,cy-.45*s),(cx+.4*s,cy),(cx,cy+.35*s)],fill=(80,200,80,255),outline=o); d.line([cx-.45*s,cy+.4*s,cx+.3*s,cy-.35*s],fill=o,width=5)
    elif nome=='calendario':
        d.rectangle([cx-.45*s,cy-.4*s,cx+.45*s,cy+.45*s],fill=k,outline=o,width=6); d.rectangle([cx-.45*s,cy-.4*s,cx+.45*s,cy-.15*s],fill=c,outline=o,width=6)
        for r in range(2):
            for q in range(3): d.rectangle([cx-.32*s+q*.25*s,cy-.05*s+r*.25*s,cx-.2*s+q*.25*s,cy+.05*s+r*.25*s],fill=o)
    elif nome=='regua':
        d.rectangle([cx-.5*s,cy-.18*s,cx+.5*s,cy+.18*s],fill=c,outline=o,width=6)
        for q in range(9): d.line([cx-.45*s+q*.11*s,cy-.18*s,cx-.45*s+q*.11*s,cy+(.0 if q%2 else .08)*s],fill=o,width=4)
    elif nome=='presente':
        d.rectangle([cx-.4*s,cy-.1*s,cx+.4*s,cy+.45*s],fill=c,outline=o,width=6); d.rectangle([cx-.45*s,cy-.3*s,cx+.45*s,cy-.1*s],fill=c,outline=o,width=6); d.rectangle([cx-.07*s,cy-.3*s,cx+.07*s,cy+.45*s],fill=k)
def wrapchunks(ws):
    ch=[];cur=[]
    for i,w in enumerate(ws):
        cur.append(i)
        if len(cur)>=5 or w['w'][-1] in '.?!,:': ch.append(cur);cur=[]
    if cur: ch.append(cur)
    return ch
CH={}  # seg -> chunks
for s in range(len(sc)):
    ws=[w for w in words if w['seg']==s]; CH[s]=(ws,wrapchunks(ws))
SEGI=lambda t: next((i for i,(a,b) in enumerate(segs) if a-0.2<=t<=b+0.4),None)
impt={}
for i,s in enumerate(sc):
    for p,ph,ic in IMP:
        if s['text'].startswith(p): impt[i]=(ph,ic,segs[i][0])
chapn=[c for c in chap if c[0] not in('gancho','final')]
def frame_overlay(t):
    ov=Image.new('RGBA',(W,Hh),(0,0,0,0)); d=ImageDraw.Draw(ov)
    ins=next(c[0] for c in chap if c[1]<=t<c[2]) if t<DUR else 'final'
    col=COR[ins]
    cc=next((c for c in cuts if c[0]<=t<c[1]),None); ilb=bool(cc and cc[6])
    if ilb:
        dim=Image.new('RGBA',(W,Hh),(0,0,0,140)); ov.alpha_composite(dim)
        cv=Image.new('RGBA',(W,Hh),(14,18,30,255)); ILLM.ILL[cc[6]](ImageDraw.Draw(cv),(t-cc[0])/(cc[1]-cc[0]),t,lambda z:F('Anton.ttf',z),col)
        sc_=0.88+0.12*ease((t-cc[0])/0.22); cw,ch=int(1440*sc_),int(810*sc_); cv=cv.resize((cw,ch),Image.LANCZOS)
        mk_=Image.new('L',(cw,ch),0); ImageDraw.Draw(mk_).rounded_rectangle([0,0,cw-1,ch-1],34,fill=255); px,py=(W-cw)//2,(Hh-ch)//2-30
        ov.paste(cv,(px,py),mk_); ImageDraw.Draw(ov).rounded_rectangle([px,py,px+cw,py+ch],34,outline=col+(255,),width=6)
    # barra de vinheta embaixo
    g=Image.new('RGBA',(W,360),(0,0,0,0)); gd=ImageDraw.Draw(g)
    for y in range(360): gd.line([0,y,W,y],fill=(0,0,0,int(190*(y/360)**1.5)))
    ov.alpha_composite(g,(0,Hh-360))
    # legenda
    si=SEGI(t)
    if si is not None:
        ws,chs=CH[si]
        for ci in chs:
            if ws[ci[0]]['s']-0.05<=t<=ws[ci[-1]]['e']+0.35 or (ci is chs[-1] and t>=ws[ci[0]]['s']):
                cur=[j for j in ci if ws[j]['s']<=t]; 
                if not cur: continue
                line=[(ws[j]['w'],re.sub(r'\W','',ws[j]['w']).lower() in KW) for j in cur]
                full=' '.join(w for w,_ in line); tw=d.textlength(full,font=fc); x=(W-tw)/2; y=Hh-170
                last=ws[cur[-1]]; pop=ease((t-last['s'])/0.12)
                for k,(w,hl) in enumerate(line):
                    f=fc; wv=d.textlength(w+' ',font=f)
                    txt(d,(x,y-(14*(1-pop) if k==len(line)-1 else 0)),w,f,(255,225,40,255) if hl else (255,255,255,255),8)
                    x+=wv
                break
    # selo do capítulo (entra de lado, depois vira etiqueta)
    if ins in NOME:
        a=[c for c in chap if c[0]==ins][0]; n=[c[0] for c in chapn].index(ins)+1; lt=t-a[1]
        if lt<3.2:
            p=ease(lt/0.28) if lt<2.8 else 1-ease((lt-2.8)/0.4)
            x=-900+p*(900+60); d.rounded_rectangle([x,70,x+1000,330],28,fill=(0,0,0,215),outline=col+(255,),width=8)
            txt(d,(x+30,60),str(n),fb,col+(255,),6); txt(d,(x+210,120),NOME[ins],fn if len(NOME[ins])<22 else F('Anton.ttf',52),(255,255,255,255),4)
            txt(d,(x+215,215),f'INSETO {n} DE {len(chapn)}',ft,(220,220,220,255),3); bug(d,x+900,220,120,col,lt)
        else:
            d.rounded_rectangle([40,40,40+int(d.textlength(NOME[ins][:24],font=ft))+170,112],22,fill=(0,0,0,170),outline=col+(255,),width=4); txt(d,(66,48),f'{n}/{len(chapn)}',fn,col+(255,),3); txt(d,(180,62),NOME[ins][:24],ft,(255,255,255,255),3)
    for i,(ph,ic,t0) in impt.items():
        lt=t-t0
        if 0<=lt<3.4 and not ilb:
            p=ease(lt/0.22) if lt<3.0 else 1-ease((lt-3.0)/0.4); wds=ph.split(' '); half=(len(wds)+1)//2; ls=[' '.join(wds[:half]),' '.join(wds[half:])] if len(ph)>14 else [ph]
            fz=F('Anton.ttf',62); bw=int(max(d.textlength(l,font=fz) for l in ls))+150; bh=40+len(ls)*72; x0=W-bw-30+(1-p)*(bw+60); y0=130
            d.rounded_rectangle([x0,y0,x0+bw,y0+bh],22,fill=(0,0,0,205),outline=col+(255,),width=6)
            icon(d,ic,x0+70,y0+bh/2,100,col)
            for q,l in enumerate(ls): txt(d,(x0+135,y0+20+q*72),l,fz,(255,255,255,255),4)
    return ov
if __name__=='__main__' and '--fx' in sys.argv:
    sys.path.insert(0,N); import sfx, soundfile as sf
    SR=48000; y=np.zeros(int((DUR+3)*SR),np.float32)
    def put(x,t,g):
        i=int(t*SR); x=x[:len(y)-i]*g; y[i:i+len(x)]+=x
    for ins,t0,t1 in chap[1:]: put(sfx.impacto(),t0,0.25); put(sfx.whoosh(0.6),t0-0.25,0.45)
    for c in cuts:
        if c[6]: put(sfx.whoosh(0.35),c[0]-0.12,0.35); put(sfx.whoosh(0.35),c[1]-0.12,0.3)
    for i,(ph,ic,t0) in impt.items(): put(sfx.brilho(),t0,0.35)
    sf.write(OUT+'/fx.wav',y,SR); print('fx ok'); sys.exit()
if __name__=='__main__' and '--ov' in sys.argv:
    dec=subprocess.Popen(['ffmpeg','-loglevel','error','-i',OUT+'/bg.mp4','-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE)
    enc=subprocess.Popen(['ffmpeg','-loglevel','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{Hh}','-r',str(FPS),'-i','-','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p',OUT+'/video_mudo.mp4'],stdin=subprocess.PIPE)
    n=0; lim=int(os.environ.get('LIM',0)); fs=W*Hh*3
    while True:
        b=dec.stdout.read(fs)
        if len(b)<fs: break
        t=n/FPS; im=Image.frombytes('RGB',(W,Hh),b).convert('RGBA'); im.alpha_composite(frame_overlay(t)); enc.stdin.write(im.convert('RGB').tobytes()); n+=1
        if lim and n>=lim: break
        if n%900==0: print(n,flush=True)
    enc.stdin.close(); enc.wait(); print('ov ok',n)
