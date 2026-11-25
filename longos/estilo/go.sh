cd /home/claude/insetos/long
python3 rl.py --bg > out8/bg.log 2>&1 && python3 rl.py --fx >> out8/bg.log 2>&1
M=/home/claude/nuncavisto/musica; D=$(python3 -c "import json;print(json.load(open('out8/timing.json'))['dur'])")
cd out8
ffmpeg -loglevel error -y -i $M/hidden_past.mp3 -i $M/dreamy_flashback.mp3 -i $M/constancy_part_three.mp3 -i $M/floating_cities.mp3 -i narr.wav -i fx.wav -filter_complex "[0:a][1:a]acrossfade=d=4[m1];[m1][2:a]acrossfade=d=4[m2];[m2][3:a]acrossfade=d=4,atrim=0:$D,asetpts=PTS-STARTPTS,volume=0.32,afade=t=in:d=1.5,afade=t=out:st=$(python3 -c "print($D-3)"):d=3,aformat=sample_rates=48000:channel_layouts=stereo[mus];[4:a]aformat=sample_rates=48000:channel_layouts=stereo,asplit=2[nv][ns];[mus][ns]sidechaincompress=threshold=0.015:ratio=14:attack=15:release=500:makeup=1[duck];[5:a]aformat=sample_rates=48000:channel_layouts=stereo[fx];[nv][duck][fx]amix=inputs=3:duration=first:normalize=0,alimiter=limit=0.95[o]" -map "[o]" -ar 48000 audio.wav
cd ..
python3 rl.py --ov > out8/ov.log 2>&1
cd out8 && ffmpeg -loglevel error -y -i video_mudo.mp4 -i audio.wav -c:v libx264 -preset veryfast -crf 26 -vf scale=1280:-2 -c:a aac -b:a 128k -shortest -movflags +faststart insetos_v8.mp4 && echo PRONTO > done.txt
