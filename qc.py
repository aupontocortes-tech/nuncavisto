"""Revisão automática antes de publicar (Nunca Visto).
Uso: python3 qc.py spec.json out   -> imprime APROVADO ou a lista do que corrigir (e sai com erro)."""
import sys, os, json, subprocess
import numpy as np
spec = json.load(open(sys.argv[1], encoding='utf-8')); out = sys.argv[2]
T = json.load(open(os.path.join(out, 'timing.json'), encoding='utf-8'))
erros = []
SC = spec['scenes']; pal = sum(len(s['text'].split()) for s in SC)
wps = pal / max(T['dur'], 1)   # palavras por segundo do vídeo inteiro (com as pausas)
if wps > 2.85: erros.append(f'fala rápida demais: {wps:.2f} palavras/s no vídeo (máx. 2,8). Corte palavras ou divida frases.')
if not (25 <= T['dur'] <= 52): erros.append(f'duração {T["dur"]:.1f}s fora de 25-50s.')
if not (6 <= len(SC) <= 12): erros.append(f'{len(SC)} cenas (use 8 a 10).')
if not SC[-1]['text'].strip().endswith('?'): erros.append('a última cena tem que terminar com uma pergunta para comentar.')
if not any(s.get('impacto') for s in SC): erros.append('marque "impacto": true na cena do fato mais surpreendente.')
for i, s in enumerate(SC):
    if len(s['text'].split()) > 22: erros.append(f'cena {i + 1} longa demais ({len(s["text"].split())} palavras): divida em duas.')
if not SC[0].get('title'): erros.append('a 1ª cena precisa de título amarelo (o choque em 2 linhas).')
final = os.path.join(out, 'final.mp4')
if os.path.exists(final):
    pr = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height', '-of', 'csv=p=0', final],
                        capture_output=True, text=True).stdout.strip()
    if pr != '1080,1920': erros.append(f'vídeo {pr}, precisa ser 1080x1920.')
    if os.path.getsize(final) > 18e6: erros.append('vídeo maior que 18 MB.')
    # tela preta: confere 1 quadro por segundo
    raw = subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', final, '-vf', 'fps=1,scale=54:96', '-f', 'rawvideo', '-pix_fmt', 'gray', '-'],
                         capture_output=True).stdout
    q = np.frombuffer(raw, np.uint8).reshape(-1, 96 * 54)
    pretos = [k for k, f in enumerate(q) if f.mean() < 12]
    if pretos: erros.append(f'tela preta nos segundos {pretos}.')
else: erros.append('out/final.mp4 não existe.')
if erros:
    print('REPROVADO — corrija e renderize de novo:'); [print(' -', e) for e in erros]; sys.exit(1)
print(f'APROVADO ({T["dur"]:.1f}s, {wps:.2f} palavras/s, {len(SC)} cenas)')
