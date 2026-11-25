import subprocess,sys,os
SEL={'formigaleao':[12,14,15,17,18,19,20,21,22,23,25,26,29,30],'cortadeira':[12,14,15,16,17,18,22,23,24,25,26,28,30],'cigarras':[13,14,15,16,17,18,19,20,21,22,24,25,26,27,29,30]}
I='/home/claude/insetos/fotos/'; O='/home/claude/insetos/fotoclip/'
jobs=[]
for g,ix in SEL.items():
    for k,i in enumerate(ix):
        src=f'{I}{g}_{i:02d}.jpg'; dst=f'{O}{g}_{i:02d}.mp4'
        if os.path.exists(dst): continue
        # fundo desfocado + foto inteira por cima, com zoom lento alternando direção
        z="1+0.10*on/180" if k%2==0 else "1.10-0.10*on/180"
        vf=(f"[0]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,boxblur=30:3,eq=brightness=-0.15[b];"
            f"[0]scale=1920:1080:force_original_aspect_ratio=decrease[f];[b][f]overlay=(W-w)/2:(H-h)/2,"
            f"scale=3840:2160,zoompan=z='{z}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1920x1080:fps=30,format=yuv420p")
        jobs.append(subprocess.Popen(['ffmpeg','-loglevel','error','-y','-loop','1','-i',src,'-filter_complex',vf,'-frames:v','180','-c:v','libx264','-preset','veryfast','-crf','19',dst]))
        if len(jobs)>=4: [j.wait() for j in jobs]; jobs=[]
[j.wait() for j in jobs]
print(len(os.listdir(O)))
