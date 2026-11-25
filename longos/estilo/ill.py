"""Ilustrações explicativas desenhadas por código (estilo desenho animado). ill(nome,d,p,t,F) desenha em 1920x1080; p=0..1 progresso do bloco."""
import math
K=(0,0,0,255); WH=(255,255,255,255)
def cl(x): return max(0.,min(1.,x))
def ph(p,a,b): return cl((p-a)/(b-a))
def ea(x): x=cl(x); return 1-(1-x)**3
def arrow(d,x1,y1,x2,y2,col,w=14):
    d.line([x1,y1,x2,y2],fill=col,width=w); a=math.atan2(y2-y1,x2-x1)
    d.polygon([(x2,y2),(x2-38*math.cos(a-.5),y2-38*math.sin(a-.5)),(x2-38*math.cos(a+.5),y2-38*math.sin(a+.5))],fill=col)
def lab(d,F,x,y,s,col=WH,size=54,anchor='mm'):
    d.text((x,y),s,font=F(size),fill=col,stroke_width=5,stroke_fill=K,anchor=anchor)
def el(d,cx,cy,rx,ry,fill,w=6): d.ellipse([cx-rx,cy-ry,cx+rx,cy+ry],fill=fill,outline=K,width=w)
def bichinho(d,cx,cy,s,col,t=0,fl=1):
    for k,x in enumerate((-.25,0,.25)):
        w=math.sin(t*8+k*2)*.07*s
        for sg in(-1,1): d.line([cx+fl*x*s,cy+sg*.2*s,cx+fl*x*s+w,cy+sg*.55*s],fill=K,width=max(4,int(s/16)))
    el(d,cx,cy,.5*s,.27*s,col+(255,),max(3,int(s/24))); el(d,cx+fl*.52*s,cy,.2*s,.17*s,col+(255,),max(3,int(s/24)))
    d.ellipse([cx+fl*.55*s-6,cy-.07*s-6,cx+fl*.55*s+6,cy-.07*s+6],fill=WH)
    d.line([cx+fl*.65*s,cy-.1*s,cx+fl*.9*s,cy-.35*s],fill=K,width=max(3,int(s/26)))
def aranha(d,cx,cy,s,col,t=0,mov=True):
    for k in range(4):
        for sg in(-1,1):
            w=math.sin(t*5+k)*.05*s if mov else 0; x0=cx+(k-1.5)*.18*s
            d.line([x0,cy,x0+sg*.0*s+(k-1.5)*.1*s,cy+sg*.55*s+w,x0+(k-1.5)*.35*s,cy+sg*.8*s],fill=K,width=max(5,int(s/14)))
    el(d,cx,cy,.45*s,.32*s,col+(255,)); el(d,cx+.5*s,cy,.22*s,.2*s,col+(255,)); d.ellipse([cx+.55*s-7,cy-.07*s-7,cx+.55*s+7,cy-.07*s+7],fill=(255,60,60,255))
def jato(d,x,y,p,t,n=14,L=420):
    for i in range(n):
        a=-.5+i/(n-1); r=((t*5+i*.37)%1)*L
        d.ellipse([x+r*math.cos(a)-12,y+r*math.sin(a)-12,x+r*math.cos(a)+12,y+r*math.sin(a)+12],fill=(255,200-i*6,80,int(255*(1-r/L))))

def bomba(d,p,t,F,col):
    cx,cy=860,470; el(d,cx,cy,520,230,(60,50,45,255),9); el(d,cx-480,cy,110,90,(90,70,50,255),8)
    a=ea(ph(p,0,.2)); b=ph(p,.33,.6)
    for k,(x,c,n) in enumerate(((cx-240,(60,140,255),'SUBSTÂNCIA 1'),(cx-240,(255,70,90),'SUBSTÂNCIA 2'))):
        yy=cy-70+k*140; mx=x+b*210
        d.ellipse([mx-80*a,yy-60*a,mx+80*a,yy+60*a],fill=c+(255,),outline=K,width=6)
        if p<.5: lab(d,F,x-250,yy,n,WH,44)
    if p>.33:
        r=60+25*math.sin(t*12)*ph(p,.5,1); el(d,cx+30,cy,r*1.4,r*1.2,(255,150,30,255),8); lab(d,F,cx+30,cy-170,'CÂMARA DE REAÇÃO',WH,44)
    if p>.62:
        d.polygon([(cx+420,cy-40),(cx+520,cy-70),(cx+520,cy+70),(cx+420,cy+40)],fill=(255,200,70,255),outline=K); jato(d,cx+520,cy,p,t)
        lab(d,F,1560,330,'JATO QUENTE',(255,200,70,255),64)
    lab(d,F,960,760,'DENTRO DO CORPO DO BESOURO',WH,46) if p<.33 else None
def sapo(d,p,t,F,col):
    el(d,780,520,520,300,(90,150,70,255),9); el(d,1180,320,150,110,(110,170,80,255),8)
    for ex in (1120,1240): el(d,ex,230,34,34,WH,6); d.ellipse([ex-12,218,ex+12,242],fill=K)
    d.arc([1040,320,1320,460],0,180,fill=K,width=8)
    el(d,700,560,230,170,(230,170,140,255),7); lab(d,F,700,380,'ESTÔMAGO',WH,42)
    if p<.25: bx=1250-ph(p,0,.25)*550; by=400+ph(p,0,.25)*150
    elif p<.75: bx,by=700,560
    else: q=ph(p,.75,1); bx=700+q*520; by=560-q*190*math.sin(q*math.pi/2)
    bichinho(d,bx,by,150,(255,140,50),t,1)
    if .25<=p<.75: jato(d,bx+60,by,p,t,8,200); lab(d,F,780,740,'DISPARA DE DENTRO!',(255,200,70,255),56)
    if p>=.75: lab(d,F,1300,160,'VÔMITO',(120,255,120,255),64)
    a=ph(p,.45,1); d.pieslice([1500,420,1800,720],-90,-90+360*.43*a,fill=(255,200,70,255),outline=K,width=6); d.ellipse([1500,420,1800,720],outline=WH,width=6)
    lab(d,F,1650,570,f'{int(43*a)}%',WH,80); lab(d,F,1650,770,'ESCAPARAM',WH,44)
def vespa(d,p,t,F,col):
    d.rectangle([0,760,1920,1080],fill=(90,60,40,255))
    if p<.5:
        sx=960; aranha(d,sx,600,360,(70,50,40),t,p<.25 or p>.4); wx=300+ea(ph(p,0,.2))*500; wy=420-ea(ph(p,0,.2))*60
        bichinho(d,wx,wy,130,(255,200,30),t,1); d.line([wx+80,wy+10,wx+170,wy+50],fill=K,width=10)
        if p<.25: lab(d,F,1500,300,'PICA ENTRE AS PERNAS',(255,200,30,255),54)
        else: lab(d,F,960,300,'PARALISADA EM SEGUNDOS',(255,90,90,255),60); lab(d,F,1200,430,'Zzz',WH,70)
    elif p<.78:
        q=ph(p,.5,.78); d.ellipse([1380,730,1640,820],fill=(20,12,8,255)); sx=1000+q*480
        aranha(d,sx,640,280,(70,50,40),t,False); bichinho(d,sx-330,640,120,(255,200,30),t,1); lab(d,F,960,260,'ARRASTA ATÉ A TOCA',(255,200,30,255),60)
    else:
        q=ph(p,.78,1); d.ellipse([760,700,1160,860],fill=(20,12,8,255)); aranha(d,960,540,420,(70,50,40),t,False)
        el(d,1010,500,36,46,(255,250,220,255),6); lab(d,F,960,230,'1 OVO',WH,64)
        if q>.5: el(d,1010,520,50*(q-.5)*2+10,22*(q-.5)*2+8,(240,240,150,255),6); lab(d,F,960,300,'A LARVA COME A ARANHA VIVA',(255,90,90,255),52)
def leao(d,p,t,F,col):
    d.rectangle([0,380,1920,1080],fill=(190,150,90,255)); d.line([0,380,1920,380],fill=K,width=8)
    d.polygon([(260,380),(1660,380),(1180,900),(740,900)],fill=(235,205,140,255),outline=K); d.polygon([(260,380),(1660,380),(1560,380),(1100,880),(820,880)],fill=(235,205,140,255))
    for i in range(4): d.arc([700-i*40,420+i*100,1220+i*40,900],200,340,fill=(160,120,70,255),width=5)
    el(d,960,880,70,45,(120,80,50,255),7); d.polygon([(900,845),(860,790),(890,800)],fill=K); d.polygon([(1020,845),(1060,790),(1030,800)],fill=K)
    q=ph(p,0,.6); ax=300+q*400 if q<1 else 700
    if p<.6: ay=380-30+ph(p,.35,.6)*0; bx=ax+ph(p,.35,.6)*260; by=350+ph(p,.35,.6)*480
    else: bx,by=960,830
    if p<.7: bichinho(d,bx if p>=.35 else ax,by if p>=.35 else 350,110,(60,60,60),t,1)
    if .45<p<.75:
        for i in range(10):
            r=((t*3+i*.2)%1); d.ellipse([960+r*(-250+i*50)-9,860-r*500-9,960+r*(-250+i*50)+9,860-r*500+9],fill=(235,205,140,255),outline=K)
        lab(d,F,1500,240,'JOGA AREIA NELA!',(255,200,70,255),56)
    if p>=.8: lab(d,F,960,200,'ELA SUGA A PRESA E JOGA A CASCA FORA',WH,50)
    else: lab(d,F,960,200,'ARMADILHA DE AREIA',WH,56)
def rola(d,p,t,F,col):
    d.rectangle([0,0,1920,1080],fill=(8,10,34,255))
    for i in range(160):
        x=(i*97)%1920; y=(i*53)%520; dd=abs((x*.26)-(y)+160)
        if dd<140 or i%5==0: d.ellipse([x,y,x+5,y+5],fill=(230,235,255,255) if dd<140 else (140,150,200,255))
    d.polygon([(0,200),(1920,-100),(1920,160),(0,460)],fill=(120,110,200,60))
    lab(d,F,960,110,'VIA LÁCTEA',(200,205,255,255),56)
    d.rectangle([0,760,1920,1080],fill=(120,85,50,255)); d.line([0,760,1920,760],fill=K,width=8)
    if p<.55:
        x=200+ph(p,0,.55)*1500; y=700; arrow(d,x+120,y-110,x+420,y-110,(120,255,120,255),12) if x<1400 else None
        el(d,x+130,y,70,70,(100,70,40,255),7); bichinho(d,x-40,y+10,140,(40,40,50),t,1); lab(d,F,960,830,'LINHA RETA = NÃO PERDE A BOLA',(120,255,120,255),56)
    else:
        q=ph(p,.55,1); x=500+q*800; y=700+math.sin(q*14)*40; el(d,x+130,y,70,70,(100,70,40,255),7); bichinho(d,x-40,y+10,140,(40,40,50),t,1)
        d.polygon([(x-80,y-80),(x+10,y-110),(x+30,y-50),(x-60,y-30)],fill=(200,170,110,255),outline=K); lab(d,F,x,y-170,'?',(255,90,90,255),90); lab(d,F,960,830,'COM O CÉU COBERTO: SE PERDE',(255,90,90,255),56)
def corta(d,p,t,F,col):
    d.rectangle([0,620,1920,1080],fill=(110,75,45,255)); d.line([0,620,1920,620],fill=K,width=8)
    d.polygon([(200,620),(240,200),(300,200),(340,620)],fill=(90,60,30,255),outline=K); el(d,270,200,210,120,(70,170,60,255))
    d.rectangle([980,700,1800,1000],fill=(80,50,30,255),outline=K,width=8)
    for i in range(14): el(d,1030+(i%7)*110,760+(i//7)*130,38,30,(245,245,235,255),5)
    q=(p*3)%1; x=380+q*620; y=520+q*0; el(d,x+20,y-50,60,36,(70,190,60,255),5); bichinho(d,x,y,120,(150,50,30),t,1)
    if x>940: pass
    lab(d,F,520,420,'FOLHA',(90,220,90,255),48); lab(d,F,1390,660,'JARDIM DE FUNGO',WH,48); arrow(d,950,640,1100,730,(255,200,70,255),12)
    if p>.5: lab(d,F,960,230,'ELAS NÃO COMEM A FOLHA… COMEM O FUNGO',(255,225,40,255),56)
    else: lab(d,F,960,230,'FOLHA → ADUBO → FUNGO → COMIDA',WH,56)
def tecela(d,p,t,F,col):
    g=ea(ph(p,.1,.7)); lx=420+g*330; rx=1500-g*330
    d.polygon([(lx-380,320),(lx,300),(lx,760),(lx-380,700)],fill=(70,170,60,255),outline=K); d.polygon([(rx+380,320),(rx,300),(rx,760),(rx+380,700)],fill=(70,190,70,255),outline=K)
    n=7; gap=rx-lx
    for i in range(n):
        x=lx+gap*i/(n-1); y=520+math.sin(i*1.3+t*2)*14; el(d,x,y,40,28,(90,230,170,255),5)
        if i: d.line([lx+gap*(i-1)/(n-1),520,x,y],fill=K,width=7)
    if p>.7:
        q=ph(p,.7,1)
        for k in range(8):
            y=360+k*45; d.line([lx,y,lx+(rx-lx)*q,y+(k%2)*20],fill=(250,250,250,255),width=5)
        lab(d,F,960,220,'LARVA = TUBO DE COLA (SEDA)',(255,240,150,255),56)
    else: lab(d,F,960,220,'FORMAM UMA CORRENTE VIVA E PUXAM',(90,230,170,255),56)
def cigarra(d,p,t,F,col):
    d.rectangle([0,520,1920,1080],fill=(95,62,38,255)); d.line([0,520,1920,520],fill=K,width=8)
    for i in range(18):
        x=120+i*98; d.line([x,520,x,560],fill=WH,width=5)
        if i%2==0: lab(d,F,x,600,str(i),WH,34) if i<=16 else None
    x=120+min(p/.8,1)*1632; dep=p<.8
    if dep: bichinho(d,x,760,130,(120,70,40),t,1)
    else:
        q=ph(p,.8,1); bichinho(d,1752,760-q*520,130,(255,70,70),t,1)
    yr=int(min(p/.8,1)*17); lab(d,F,960,210,f'ANO {yr}' if p<.8 else 'ELAS SAEM!',(255,90,90,255),110)
    lab(d,F,960,350,'17 ANOS DEBAIXO DA TERRA',WH,56); lab(d,F,1650,900,'PRÓXIMA: 2038',(255,225,40,255),54)
def aguape(d,p,t,F,col):
    d.rectangle([0,640,1920,1080],fill=(30,110,190,255)); d.line([0,640,1920,640],fill=(170,225,255,255),width=8)
    hop=math.sin(p*math.pi*3)**2*160 if p>.45 else 0; cy=560-hop; cx=960
    for k in range(3):
        for sg in(-1,1):
            x2=cx+sg*(150+k*130); d.line([cx+sg*30,cy,x2,640-(hop*.3)],fill=K,width=9)
            if hop<5: d.ellipse([x2-40,640-8,x2+40,640+14],outline=(190,235,255,255),width=5)
    el(d,cx,cy,150,34,(70,70,60,255),7)
    d.line([cx-480,770,cx+480,770],fill=WH,width=10); d.line([cx-480,740,cx-480,800],fill=WH,width=10); d.line([cx+480,740,cx+480,800],fill=WH,width=10)
    lab(d,F,960,840,'CERCA DE 30 CENTÍMETROS COM AS PERNAS ABERTAS',WH,50); lab(d,F,960,240,'O MAIOR DO GRUPO',(120,220,255,255),70)
def escorpiao(d,p,t,F,col):
    d.rectangle([0,700,1920,1080],fill=(60,90,40,255)); d.line([0,700,1920,700],fill=K,width=8)
    bichinho(d,640,600,260,(200,120,255),t,1); d.arc([300,420,520,640],150,330,fill=K,width=16)
    bichinho(d,1360,640,260,(255,170,200),t,-1)
    gx=840+ea(ph(p,.1,.5))*260; sz=1+ph(p,.5,.8)*.7
    d.rectangle([gx-40*sz,650-60*sz,gx+40*sz,650],fill=(255,225,60,255),outline=K,width=6)
    d.rectangle([420,790,420+1080*.35*sz/1.7,840],fill=(255,225,60,255),outline=K,width=5); d.rectangle([420,790,1500,840],outline=WH,width=6)
    lab(d,F,960,250,'O PRESENTE: INSETO MORTO OU SALIVA',WH,56); lab(d,F,960,740,'MAIOR PRESENTE = MAIS TEMPO JUNTOS',(255,225,60,255),50)
ILL=dict(bomba=bomba,sapo=sapo,vespa=vespa,leao=leao,rola=rola,corta=corta,tecela=tecela,cigarra=cigarra,aguape=aguape,escorpiao=escorpiao)
