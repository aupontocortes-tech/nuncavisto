"""Efeitos sonoros do Nunca Visto (gerados por código, sem direitos autorais).
Uso: python3 sfx.py spec.json out  -> out/fx.wav  (o render.py mistura com a narração se existir)
- "whoosh" suave em toda troca de cena;
- "efeito" opcional por cena: impacto | explosao | trovao | agua | vento | coracao | grave | brilho;
- "impacto": true na cena do fato mais surpreendente (pancada grave)."""
import sys, os, json
import numpy as np, soundfile as sf
SR = 48000; R = np.random.default_rng(3)
def t(d): return np.arange(int(d * SR)) / SR
def ruido(d): return R.standard_normal(int(d * SR)).astype(np.float32)
def banda(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0
    return np.fft.irfft(X, len(x)).astype(np.float32)
def norm(x, g=1.0): return (x / (np.max(np.abs(x)) + 1e-9) * g).astype(np.float32)
def whoosh(d=0.45):
    x = banda(ruido(d), 300, 5000) * np.sin(np.linspace(0, np.pi, int(d * SR))) ** 2
    return norm(x)
def impacto():
    d = 1.8; f = np.linspace(75, 30, int(d * SR)); boom = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t(d) * 2.2)
    return norm(boom + banda(ruido(d), 60, 3000) * np.exp(-t(d) * 18) * 0.8)
def explosao(): d = 2.2; return norm(banda(ruido(d), 30, 900) * np.exp(-t(d) * 2.0) * (1 + 0.4 * np.sin(2 * np.pi * 5 * t(d))))
def trovao(): d = 2.8; return norm(banda(ruido(d), 30, 300) * np.exp(-t(d) * 1.3))
def agua(): d = 2.0; return norm(banda(ruido(d), 200, 1500) * np.sin(np.linspace(0, np.pi, int(d * SR))))
def vento(): d = 2.0; return norm(banda(ruido(d), 80, 700) * np.sin(np.linspace(0, np.pi, int(d * SR))))
def coracao():
    th = np.sin(2 * np.pi * 52 * t(0.18)) * np.exp(-t(0.18) * 28); y = np.zeros(int(3.4 * SR), np.float32)
    for b in range(4):
        for dd, g in ((0, 1), (0.22, 0.7)): i = int((b * 0.85 + dd) * SR); y[i:i + len(th)] += th * g
    return norm(y)
def grave(): d = 2.5; return norm(np.sin(2 * np.pi * 45 * t(d)) * np.sin(np.linspace(0, np.pi, int(d * SR))))
def brilho():
    y = np.zeros(int(1.2 * SR), np.float32)
    for k, f in enumerate([1320, 1760, 2093, 2637]):
        i = int(k * 0.07 * SR); n = int(0.9 * SR); y[i:i + n] += np.sin(2 * np.pi * f * t(0.9)) * np.exp(-t(0.9) * 5)
    return norm(y)
EF = dict(impacto=impacto, explosao=explosao, trovao=trovao, agua=agua, vento=vento, coracao=coracao, grave=grave, brilho=brilho)
VOL = dict(impacto=0.5, explosao=0.45, trovao=0.4, agua=0.18, vento=0.15, coracao=0.35, grave=0.3, brilho=0.12)
def main():
    spec = json.load(open(sys.argv[1], encoding='utf-8')); out = sys.argv[2]
    T = json.load(open(os.path.join(out, 'timing.json'), encoding='utf-8'))
    n = int((T['dur'] + 1) * SR); y = np.zeros(n, np.float32); w = whoosh() * 0.10
    def add(x, s):
        i = max(0, int(s * SR)); y[i:i + len(x)] += x[:max(0, n - i)]
    for k, (sc, (s, e)) in enumerate(zip(spec['scenes'], T['segs'])):
        if k > 0: add(w, s - 0.32)                       # troca de cena
        if sc.get('impacto'): add(impacto() * VOL['impacto'], s - 0.05)
        if sc.get('efeito') in EF: add(EF[sc['efeito']]() * VOL[sc['efeito']], s)
    sf.write(os.path.join(out, 'fx.wav'), np.clip(y, -1, 1), SR); print('efeitos ok')
if __name__ == '__main__':
    main()
