"""Ilustrações v3 (mais detalhadas e animadas). Mesmas assinaturas de ill.py."""
import math, random
from ill import *
def vg(d,x0,y0,x1,y1,c0,c1):
    n=max(1,int(y1-y0))
    for i in range(0,n,2):
        k=i/n; d.rectangle([x0,y0+i,x1,y0+i+2],fill=tuple(int(c0[j]+(c1[j]-c0[j])*k) for j in range(3))+(255,))
def formiga(d,x,y,s,t=0,ang=0,col=(40,25,20)):
    c=(*col,255)
    for k in range(3):
        for sg in(-1,1):
            w=math.sin(t*14+k*2+sg)*.18*s; px=x+(k-1)*.28*s
            d.line([px,y,px+sg*.1*s,y-sg*.45*s+w],fill=c,width=max(2,int(s/9)))
    d.ellipse([x-.62*s,y-.2*s,x-.2*s,y+.2*s],fill=c); d.ellipse([x-.2*s,y-.14*s,x+.1*s,y+.14*s],fill=c); d.ellipse([x+.1*s,y-.18*s,x+.45*s,y+.18*s],fill=c)
    d.line([x+.4*s,y-.1*s,x+.7*s,y-.3*s],fill=c,width=max(2,int(s/12))); d.line([x+.4*s,y+.1*s,x+.7*s,y+.3*s],fill=c,width=max(2,int(s/12)))
def leao(d,p,t,F,col):
    vg(d,0,0,1920,330,(120,170,215),(215,230,240)); vg(d,0,330,1920,1080,(205,170,110),(120,85,50))
    R=random.Random(4)
    for i in range(500):
        x=R.randint(0,1920); y=R.randint(335,1080); d.point([x,y],fill=(110,80,45,255)); d.ellipse([x,y,x+3,y+3],fill=(150+R.randint(-20,20),115,70,255))
    cx=960; top=330
    fun=[(cx-640,top),(cx+640,top),(cx+170,880),(cx-170,880)]
    # interior do funil (corte)
    vg(d,cx-640,top,cx+640,880,(95,70,42),(55,38,22))
    d.polygon([(cx-640,top),(cx-170,880),(cx-170,1080),(0,1080),(0,top)],fill=(176,138,86,255)); d.polygon([(cx+640,top),(cx+170,880),(cx+170,1080),(1920,1080),(1920,top)],fill=(176,138,86,255))
    for i in range(260):
        y=top+R.random()*(880-top); xl=cx-640+(y-top)/(880-top)*470; xr=cx+640-(y-top)/(880-top)*470; x=xl+R.random()*(xr-xl)
        d.ellipse([x,y,x+4,y+4],fill=(215,180,120,255))
    d.line([cx-640,top,cx-170,880],fill=(60,40,22,255),width=6); d.line([cx+640,top,cx+170,880],fill=(60,40,22,255),width=6)
    # larva (corpo enterrado + mandíbulas)
    snap=ph(p,.62,.7); jaw=40-snap*34
    d.ellipse([cx-90,845,cx+90,960],fill=(120,100,80,255),outline=(40,28,18,255),width=4)
    d.ellipse([cx-60,815,cx+60,880],fill=(145,120,90,255),outline=(40,28,18,255),width=4)
    for sg in(-1,1): d.polygon([(cx+sg*30,830),(cx+sg*(jaw+70),740),(cx+sg*(jaw+90),735),(cx+sg*(jaw+48),835)],fill=(80,45,25,255),outline=(30,20,12,255))
    d.ellipse([cx-30,832,cx-14,846],fill=(10,10,10,255)); d.ellipse([cx+14,832,cx+30,846],fill=(10,10,10,255))
    # formiga: caminha, escorrega, tenta fugir, é puxada
    if p<.22: ax=cx-900+ph(p,0,.22)*(900-560); ay=top-22; ang=0; vis=1
    elif p<.62:
        q=ph(p,.22,.62); e=ea(q); ax=cx-560+e*(560-60); ay=top-22+e*(880-top-40)*1.0; vis=1
        if q>.45 and q<.7: ax-=math.sin(q*40)*24; ay-=abs(math.sin(q*30))*18
    else: ax=cx-60+ph(p,.62,.7)*60; ay=800+ph(p,.62,.7)*70; vis=1-ph(p,.72,.9)
    if vis>.02 and p<.9: formiga(d,ax,ay,130*(0.4+0.6*vis),t)
    # areia arremessada (p .42-.62)
    if .4<p<.64:
        for i in range(26):
            r=((t*2.6+i*.19)%1); xx=cx+(-200+i*16)*(1-r*.1)-r*(ax-cx)*-.2; yy=800-r*(780-ay+40)*(0.9+0.2*math.sin(i)); d.ellipse([cx-60+(ax-cx+60)*r-6,830+(ay-830)*r-6-math.sin(r*3.1)*170,cx-60+(ax-cx+60)*r+6,830+(ay-830)*r+6-math.sin(r*3.1)*170],fill=(225,190,130,255))
    # casca arremessada
    if p>.9:
        q=ph(p,.9,1); xx=cx+q*520; yy=830-math.sin(q*math.pi)*520+q*300; d.ellipse([xx-26,yy-14,xx+26,yy+14],outline=(40,25,20,255),width=4)
    # rótulos
    steps=[(0,.22,'1  A FORMIGA CHEGA NA BORDA'),(.22,.42,'2  A AREIA SOLTA CEDE'),(.42,.62,'3  ELA JOGA AREIA PARA DERRUBAR'),(.62,.9,'4  JATO DE TOXINA + ENZIMAS'),(.9,1.01,'5  A CASCA VAZIA É ARREMESSADA')]
    s=next(x for x in steps if x[0]<=p<x[1]); 
    d.rounded_rectangle([cx-520,80,cx+520,170],24,fill=(10,10,14,215),outline=(240,200,120,255),width=5); lab(d,F,cx,125,s[2],(255,235,170,255),50)
def corta(d,p,t,F,col):
    vg(d,0,0,1920,600,(140,200,230),(200,230,210)); vg(d,0,600,1920,1080,(110,76,48),(60,40,26))
    d.line([0,600,1920,600],fill=(50,35,22,255),width=6)
    R=random.Random(2)
    # árvore
    d.polygon([(220,600),(250,230),(330,230),(360,600)],fill=(95,62,36,255),outline=(50,32,18,255))
    for i in range(40):
        x=120+R.random()*330; y=50+R.random()*230; el(d,x,y,60+R.random()*40,34+R.random()*20,(60+R.randint(0,40),150+R.randint(0,50),55,255),3)
    # trilha curva e formigas com pedaços de folha
    def pt(u): return (360+u*900, 580+math.sin(u*math.pi*2)*18-u*0)
    for i in range(9):
        u=((t*.09+i/9)%1); x,y=pt(u); formiga(d,x,y,80,t+i,0,(120,45,25)); d.polygon([(x+10,y-70),(x+70,y-110),(x+90,y-60),(x+30,y-40)],fill=(70,185,60,255),outline=(30,90,30,255))
    # ninho subterrâneo
    d.rounded_rectangle([1180,680,1860,1030],40,fill=(70,46,30,255),outline=(35,22,14,255),width=6)
    d.polygon([(1180,600),(1260,600),(1260,690),(1200,690)],fill=(70,46,30,255)); 
    g=ph(p,.35,.8)
    for i in range(16):
        cx2=1260+(i%8)*78; cy2=770+(i//8)*120; r=(18+30*g)*(0.75+0.25*math.sin(i*2.1))
        for k in range(5): el(d,cx2+math.cos(k*1.3)*r*.6,cy2+math.sin(k*1.3)*r*.5,r*.7,r*.6,(250,248,238,255),2)
    for i in range(4): formiga(d,1300+i*130+math.sin(t*2+i)*14,985,56,t+i,0,(150,60,35))
    steps=[(0,.28,'1  CORTAM A FOLHA',(90,220,90,255)),(.28,.55,'2  CARREGAM ATÉ O NINHO',(255,210,90,255)),(.55,.8,'3  USAM COMO ADUBO PARA O FUNGO',(255,255,255,255)),(.8,1.01,'4  A COLÔNIA COME O FUNGO',(255,235,170,255))]
    s=next(x for x in steps if x[0]<=p<x[1]); d.rounded_rectangle([420,70,1500,160],24,fill=(10,10,14,215),outline=s[3],width=5); lab(d,F,960,115,s[2],s[3],50)
def rola(d,p,t,F,col):
    vg(d,0,0,1920,1080,(4,6,26),(20,16,48)); R=random.Random(9)
    for i in range(330):
        x=R.randint(0,1920); y=R.randint(0,540); dd=abs((x*.2)-y+160)
        if dd<150 or i%6==0: tw=0.5+0.5*math.sin(t*2+i); c=int(150+90*tw); d.ellipse([x,y,x+4,y+4],fill=(c,c,min(255,c+30),255))
    for i in range(14):
        d.polygon([(0,230-i*7),(1920,-90-i*7),(1920,-60-i*7+18),(0,260-i*7+18)],fill=(130,110,200,12))
    lab(d,F,960,110,'VIA LÁCTEA',(210,205,255,255),52)
    d.rectangle([0,540,1920,1080],fill=(52,34,22,255)); d.line([0,540,1920,540],fill=(20,12,8,255),width=6)
    def faixa(y,reto,boné):
        x=140+((t*.2+p*.9)%1)*1300 if False else 140+p*1500
        yy=y+(0 if reto else math.sin(p*22)*34)
        for k in range(14): d.line([100+k*110,y+62,150+k*110,y+62],fill=(120,90,60,255),width=4)
        rr=62; ang=x*.04
        el(d,x+130,yy,rr,rr,(110,76,44,255),4); d.line([x+130,yy,x+130+rr*math.cos(ang),yy+rr*math.sin(ang)],fill=(70,48,28,255),width=5)
        bichinho(d,x-30,yy+8,130,(30,34,48),t,1)
        if boné: d.polygon([(x-85,yy-58),(x+20,yy-82),(x+36,yy-30),(x-70,yy-6)],fill=(205,175,120,255),outline=(60,40,20,255),width=3); lab(d,F,x-20,yy-130,'?',(255,90,90,255),70)
        if reto: arrow(d,x+250,yy-120,x+470,yy-120,(110,255,130,255),10) if x<1200 else None
    faixa(680,True,False); faixa(900,False,True)
    lab(d,F,1500,640,'COM O CÉU À VISTA',(120,255,140,255),44,'mm'); lab(d,F,1500,860,'COM O BONÉ DE PAPELÃO',(255,110,110,255),44,'mm')
def cigarra(d,p,t,F,col):
    vg(d,0,0,1920,430,(10,14,40),(30,28,62)); vg(d,0,430,1920,1080,(88,58,36),(40,26,18))
    d.line([0,430,1920,430],fill=(20,12,8,255),width=6); R=random.Random(5)
    for i in range(14): x=120+i*130; d.line([x,430,x+R.randint(-80,80),1040],fill=(125,86,52,255),width=5)
    for i in range(80): x=R.randint(0,1920); y=R.randint(0,360); d.ellipse([x,y,x+3,y+3],fill=(220,225,255,255))
    # tronco
    d.polygon([(1600,430),(1625,-20),(1700,-20),(1720,430)],fill=(70,46,30,255),outline=(25,16,10,255))
    prog=min(p/.72,1); yr=int(prog*17)
    x=160+prog*1380; y=700+math.sin(prog*8)*50 if p<.72 else 700
    muda=[3,6,9,12,15]; n=sum(1 for m in muda if yr>=m)
    for i,m in enumerate(muda):
        if yr>=m: xm=160+m/17*1380; d.ellipse([xm-18,820-0,xm+18,860],outline=(255,225,100,255),width=4); lab(d,F,xm,885,f'MUDA {i+1}',(255,225,100,255),30)
    if p<.72: bichinho(d,x,y,150,(150,100,55),t,1)
    else:
        q=ph(p,.72,1); bichinho(d,1560+q*80,700-q*540,150,(150,100,55) if q<.6 else (130,200,70),t,1)
        if q>.6: d.polygon([(1640,170),(1760,100),(1790,200),(1660,230)],fill=(200,230,255,150),outline=(120,150,190,255))
    lab(d,F,960,170,f'ANO {yr}' if p<.72 else 'SAEM TODAS DE UMA VEZ',(255,110,110,255) if p<.72 else (255,225,100,255),110 if p<.72 else 84)
    lab(d,F,960,300,'17 ANOS DEBAIXO DA TERRA',WH,52) if p<.72 else lab(d,F,960,300,'PRÓXIMA VEZ: 2038',WH,52)
ILL2=dict(leao=leao,corta=corta,rola=rola,cigarra=cigarra)
