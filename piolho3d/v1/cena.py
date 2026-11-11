"""Cena 3D: "Você é o piolho que derrotou Napoleão".
uso: python3 cena.py shots.json <ini> <fim> <saida> [preview f1,f2,...]"""
import bpy, math, sys, json, os, random
from mathutils import Vector
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, '..'))
args = sys.argv[1:]
SHOTS = json.load(open(args[0])); F0, F1 = int(args[1]), int(args[2]); OUT = args[3]
PREVIEW = len(args) > 4 and args[4] == 'preview'
bpy.ops.wm.read_factory_settings(use_empty=True)
import personagens as P
sc = bpy.context.scene; sc.render.fps = SHOTS['fps']
R = math.radians
def p(x, y, z): return Vector((x, y, z))
mat = P.mat
random.seed(7)

def plano(loc, tam, m, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_plane_add(size=1, location=loc, rotation=rot); o = bpy.context.object; o.scale = (tam[0], tam[1], 1); o.data.materials.append(m); return o
def caixa(loc, tam, m):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc); o = bpy.context.object; o.scale = tam; o.data.materials.append(m); return o
def ruido(m, cor2, escala=8, forca=0.35):
    """mistura uma segunda cor com textura de ruído (chão, tecido)"""
    nt = m.node_tree; b = nt.nodes['Principled BSDF']
    n = nt.nodes.new('ShaderNodeTexNoise'); n.inputs['Scale'].default_value = escala
    mx = nt.nodes.new('ShaderNodeMix'); mx.data_type = 'RGBA'; mx.inputs['Factor'].default_value = forca
    mx.inputs[6].default_value = b.inputs['Base Color'].default_value; mx.inputs[7].default_value = (*cor2, 1)
    nt.links.new(n.outputs['Fac'], mx.inputs['Factor']); nt.links.new(mx.outputs[2], b.inputs['Base Color'])
    bump = nt.nodes.new('ShaderNodeBump'); bump.inputs['Strength'].default_value = 0.3; nt.links.new(n.outputs['Fac'], bump.inputs['Height']); nt.links.new(bump.outputs['Normal'], b.inputs['Normal'])
    return m
VISIVEL = {}
def mostra(o, a, b): VISIVEL.setdefault(o, set()).update(range(a, b + 1))
def kf(o, f, loc=None, rot=None, esc=None):
    if loc is not None: o.location = loc; o.keyframe_insert('location', frame=f)
    if rot is not None: o.rotation_euler = rot; o.keyframe_insert('rotation_euler', frame=f)
    if esc is not None: o.scale = esc; o.keyframe_insert('scale', frame=f)
def hold(o, a, b, loc, rot=(0, 0, 0)): kf(o, a, loc, rot); kf(o, b, loc, rot)
LONGE = p(0, -300, -50)

# ================= SETS =================
# 1) estrada de verão (x=0): terra, grama, árvores
GRAMA = ruido(mat('grama', (0.3, 0.45, 0.15), 0.9), (0.45, 0.5, 0.2), 3)
TERRA = ruido(mat('terra', (0.45, 0.33, 0.2), 0.9), (0.35, 0.25, 0.15), 6)
plano((0, 0, 0), (80, 80), GRAMA); plano((0, 0, 0.005), (4, 80), TERRA)
TRONCO = mat('tronco', (0.3, 0.2, 0.12), 0.8); FOLHA = mat('folha', (0.18, 0.35, 0.12), 0.8)
for i in range(30):
    x = random.choice((-1, 1)) * random.uniform(4, 14); y = random.uniform(-15, 40)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.15, depth=2, location=(x, y, 1)); bpy.context.object.data.materials.append(TRONCO)
    bpy.ops.mesh.primitive_cone_add(radius1=1.3, depth=3.5, location=(x, y, 3.2)); bpy.context.object.data.materials.append(FOLHA)
# acampamento (verão, à noite): fogueira e barracas
FOGO = mat('fogo', (1, 0.5, 0.1), 0.5, emis=((1.0, 0.45, 0.08), 30))
CAMP = p(8, -6, 0)
bpy.ops.mesh.primitive_cone_add(radius1=0.25, depth=0.5, location=CAMP + p(0, 0, 0.25)); FOGUEIRA = bpy.context.object; FOGUEIRA.data.materials.append(FOGO)
LONA = mat('lona', (0.85, 0.8, 0.68), 0.9)
for k, (dx, dy) in enumerate(((-2.5, 2), (2.5, 2.4), (0, 3.5))):
    bpy.ops.mesh.primitive_cone_add(vertices=4, radius1=1.4, depth=1.6, location=CAMP + p(dx, dy, 0.8)); t = bpy.context.object; t.rotation_euler = (0, 0, R(45)); t.data.materials.append(LONA)

# 2) estrada de inverno (x=100): neve
SI = p(100, 0, 0)
NEVE = ruido(mat('neve', (0.9, 0.93, 1.0), 0.75), (0.75, 0.8, 0.9), 2, 0.25)
plano(SI, (80, 80), NEVE)
GALHO = mat('galho', (0.18, 0.14, 0.12), 0.8)
for i in range(30):
    x = SI.x + random.choice((-1, 1)) * random.uniform(4, 14); y = random.uniform(-15, 40)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.12, depth=3, location=(x, y, 1.5)); bpy.context.object.data.materials.append(GALHO)
    bpy.ops.mesh.primitive_cone_add(radius1=1.0, depth=3.0, location=(x, y, 3.2)); bpy.context.object.data.materials.append(NEVE)
MONTES = []      # soldados caídos cobertos de neve
for i in range(18):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=(SI.x + random.uniform(-3, 3), random.uniform(-2, 30), 0)); m_ = bpy.context.object
    m_.scale = (0.35, 0.9, 0.22); m_.rotation_euler = (0, 0, random.uniform(-1, 1)); m_.data.materials.append(NEVE)
FLOCOS = []
NEVE_MAT = mat('floco', (1, 1, 1), 0.5, emis=((1, 1, 1), 0.6))
for i in range(260):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=0.025, location=(0, 0, 0)); f_ = bpy.context.object; f_.data.materials.append(NEVE_MAT)
    FLOCOS.append((f_, random.uniform(-6, 6), random.uniform(-6, 12), random.uniform(0, 1)))

# 3) Moscou (x=200): prédios e cúpulas de cebola, fogo e fumaça
SM = p(200, 0, 0)
plano(SM, (80, 80), ruido(mat('chao_m', (0.4, 0.38, 0.35), 0.9), (0.3, 0.28, 0.25), 4))
CORES = [(0.75, 0.3, 0.25), (0.85, 0.8, 0.65), (0.55, 0.6, 0.7), (0.9, 0.7, 0.4)]
PREDIOS = []
for i in range(16):
    lado = 1 if i % 2 else -1; y = (i // 2) * 4.5; h = random.uniform(4, 8)
    pr = caixa(SM + p(lado * random.uniform(4.5, 6), y, h / 2), (3, 3.5, h), mat(f'pr{i}', random.choice(CORES), 0.8)); PREDIOS.append((pr, h))
for k, (dx, dy, hh) in enumerate(((0, 30, 9), (-5, 36, 7), (5, 36, 7))):
    caixa(SM + p(dx, dy, hh / 2), (2.2, 2.2, hh), mat(f'torre{k}', (0.9, 0.88, 0.82), 0.7))
    bpy.ops.mesh.primitive_uv_sphere_add(radius=1.3, location=SM + p(dx, dy, hh + 1.0)); c_ = bpy.context.object; c_.scale = (1, 1, 1.25)
    c_.data.materials.append(mat(f'cupula{k}', [(0.9, 0.7, 0.2), (0.2, 0.55, 0.35), (0.15, 0.35, 0.75)][k], 0.3, 0.8 if k == 0 else 0)); bpy.ops.object.shade_smooth()
    bpy.ops.mesh.primitive_cone_add(radius1=0.3, depth=1.4, location=SM + p(dx, dy, hh + 2.9)); bpy.context.object.data.materials.append(mat(f'ponta{k}', (0.9, 0.7, 0.2), 0.3, 1))
CHAMAS = []
FUMACA = mat('fumaca', (0.08, 0.08, 0.08), 1.0)
for pr, h in PREDIOS:
    for j in range(3):
        bpy.ops.mesh.primitive_cone_add(radius1=1.0, depth=2.8, location=pr.location + p(random.uniform(-1, 1), random.uniform(-1, 1), h / 2 + 1.2)); ch = bpy.context.object; ch.data.materials.append(FOGO)
        CHAMAS.append(ch)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=1.6, location=pr.location + p(0, 0, h / 2 + 3)); fu = bpy.context.object; fu.data.materials.append(FUMACA); CHAMAS.append(fu)

# 4) vala de 2001 (x=300): terra escura com ossos
SV = p(300, 0, 0)
plano(SV, (60, 60), ruido(mat('terra_v', (0.32, 0.24, 0.17), 0.95), (0.22, 0.16, 0.11), 5))
OSSO = mat('osso', (0.9, 0.86, 0.75), 0.6)
for i in range(70):
    x, y = random.uniform(-2.2, 2.2), random.uniform(-1.4, 1.4)
    if random.random() < 0.25:
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.11, location=SV + p(x, y, 0.06)); o = bpy.context.object; o.scale = (1, 1.15, 1)
    else:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.025, depth=random.uniform(0.25, 0.5), location=SV + p(x, y, 0.03), rotation=(R(90), 0, random.uniform(0, 3.14))); o = bpy.context.object
    o.data.materials.append(OSSO)
caixa(SV + p(0, 1.6, 0.3), (5, 0.1, 0.6), mat('borda', (0.4, 0.3, 0.2), 0.9)); caixa(SV + p(2.6, 0, 0.3), (0.1, 3.2, 0.6), mat('borda2', (0.4, 0.3, 0.2), 0.9))
for i, (dx, dy) in enumerate(((-2.6, -1.7), (2.6, -1.7), (-2.6, 1.7), (2.6, 1.7))):
    bpy.ops.mesh.primitive_cylinder_add(radius=0.03, depth=0.9, location=SV + p(dx, dy, 0.45)); bpy.context.object.data.materials.append(mat(f'estaca{i}', (0.8, 0.6, 0.2), 0.6))
# hélice de DNA brilhando (aparece na "prova")
DNA = []
for i in range(40):
    a_ = i * 0.45; z = 0.15 + i * 0.035
    for sgn, cor in ((1, (0.2, 0.9, 1.0)), (-1, (1.0, 0.3, 0.6))):
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.025, location=SV + p(0.6 + sgn * 0.15 * math.cos(a_), 0.15 * math.sin(a_) * sgn - 0.6, z)); d_ = bpy.context.object
        d_.data.materials.append(mat(f'dna{i}{sgn}', cor, 0.3, emis=(cor, 4))); DNA.append(d_)

# 5) macro (x=400): tecido azul da farda gigante, pele e bolinhas de cocô
SX = p(400, 0, 0)
TECIDO = mat('tecido', (0.08, 0.13, 0.42), 0.9)
nt = TECIDO.node_tree; b_ = nt.nodes['Principled BSDF']; wv = nt.nodes.new('ShaderNodeTexWave'); wv.inputs['Scale'].default_value = 6; wv.inputs['Distortion'].default_value = 2
bump = nt.nodes.new('ShaderNodeBump'); bump.inputs['Strength'].default_value = 0.8; nt.links.new(wv.outputs['Fac'], bump.inputs['Height']); nt.links.new(bump.outputs['Normal'], b_.inputs['Normal'])
plano(SX, (20, 20), TECIDO)
bpy.ops.mesh.primitive_cylinder_add(radius=2.5, depth=20, location=SX + p(-4.5, 0, 0.0), rotation=(R(90), 0, 0)); bpy.context.object.data.materials.append(TECIDO)   # outra manga (pulo)
PELE = ruido(mat('pele', (0.86, 0.6, 0.5), 0.55), (0.75, 0.45, 0.4), 4, 0.3)
SP = p(400, 30, 0); plano(SP, (20, 20), PELE)
MORDIDAS = []
for i in range(3):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.18, location=SP + p(-0.6 + i * 0.45, 0.4 + 0.1 * i, 0)); m_ = bpy.context.object; m_.scale = (1, 1, 0.35)
    m_.data.materials.append(mat(f'mordida{i}', (0.85, 0.25, 0.22), 0.5)); MORDIDAS.append(m_)
COCO = []
for i in range(7):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.035, location=SP + p(0.0, -0.4 - i * 0.07, 0.03)); c_ = bpy.context.object; c_.scale = (1, 1.4, 0.8)
    c_.data.materials.append(mat(f'coco{i}', (0.15, 0.08, 0.05), 0.6)); COCO.append(c_)
# 6) bactérias do tifo (x=500): bastonetes roxos num fundo vermelho
SB = p(500, 0, 0)
FUNDO = mat('fundo_b', (0.5, 0.05, 0.08), 0.7, emis=((0.35, 0.02, 0.05), 0.6))
bpy.ops.mesh.primitive_uv_sphere_add(radius=15, location=SB); FB = bpy.context.object; FB.data.materials.append(FUNDO)
BACT = []
BM = mat('bacteria', (0.55, 0.35, 0.9), 0.4, emis=((0.35, 0.2, 0.7), 0.6))
for i in range(40):
    loc = SB + p(random.uniform(-2.5, 2.5), random.uniform(-1, 5), random.uniform(-2, 2))
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.18, location=loc); o = bpy.context.object; o.scale = (1, 1, 2.4); o.rotation_euler = (random.uniform(0, 3), random.uniform(0, 3), 0)
    o.data.materials.append(BM); bpy.ops.object.shade_smooth(); BACT.append(o)

# ================= PERSONAGENS =================
PIO = P.piolho(1.0)          # em macro: 1 m de comprimento sobre tecido gigante
SOLD = [P.soldado() for _ in range(12)]
NAP = P.soldado(cor_casaco=mat('cinza', (0.45, 0.45, 0.47), 0.7), napoleao=True)
def acao(arm, acts, nome, a, b, vel=1.0):
    act = [x for x in acts if x.name.split('.')[0] == nome][0]; ln = act.frame_range[1] - act.frame_range[0]
    tr = arm.animation_data.nla_tracks.new(); st = tr.strips.new(f'{nome}_{a}', a, act)
    st.scale = vel; st.repeat = max(1.0, (b - a) / (ln * vel)) if nome != 'Death' else 1.0
    st.extrapolation = 'HOLD_FORWARD' if nome == 'Death' else 'NOTHING'
    # a próxima cena desliga a "morte" com uma faixa por cima
    return st
def tropa(a, b, base, n=12, anim='Walk', vel=1.0, sep=1.1, avanco=0.0, rot=0.0, mortos=()):
    """forma os soldados em colunas de 3 andando para -Y (em direção à câmera)."""
    for i, (raiz, arm, acts) in enumerate(SOLD):
        if i >= n: hold(raiz, a, b, LONGE); continue
        col, lin = i % 3, i // 3
        pos = base + p((col - 1) * sep, lin * sep * 1.2 + random.uniform(-0.15, 0.15), 0)
        kf(raiz, a, pos, (0, 0, rot)); kf(raiz, b, pos + p(0, -avanco, 0), (0, 0, rot))
        acao(arm, acts, 'Death' if i in mortos else anim, a + (random.randint(0, 20) if i in mortos else 0), b, vel)
def sem_napoleao(a, b): hold(NAP[0], a, b, LONGE)
def sem_tropa(a, b):
    for raiz, arm, acts in SOLD: hold(raiz, a, b, LONGE)
def sem_piolho(a, b): hold(PIO, a, b, LONGE)

# ================= LUZ / CÉU =================
w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True; BG = w.node_tree.nodes['Background']
SOL = bpy.data.objects.new('sol', bpy.data.lights.new('sol', 'SUN')); sc.collection.objects.link(SOL); SOL.rotation_euler = (R(50), 0, R(-35))
LUZF = bpy.data.objects.new('luzfogo', bpy.data.lights.new('luzfogo', 'POINT')); sc.collection.objects.link(LUZF); LUZF.data.color = (1, 0.5, 0.15)
def modo(f, m):
    ceu, forca, sol, cor = {'dia': ((0.5, 0.65, 0.9), 1.0, 3.5, (1, 0.95, 0.85)), 'noite': ((0.08, 0.1, 0.22), 0.9, 0.5, (0.6, 0.7, 1)),
                            'inverno': ((0.62, 0.66, 0.72), 1.1, 1.2, (0.85, 0.9, 1)), 'fogo': ((0.35, 0.15, 0.08), 0.8, 1.0, (1, 0.6, 0.35)),
                            'macro': ((0.5, 0.55, 0.65), 0.8, 3.0, (1, 0.97, 0.9)), 'bact': ((0.2, 0.02, 0.04), 0.4, 1.5, (1, 0.8, 0.85)),
                            'vala': ((0.6, 0.6, 0.62), 1.0, 2.5, (1, 0.95, 0.88))}[m]
    BG.inputs[0].default_value = (*ceu, 1); BG.inputs[1].default_value = forca; SOL.data.energy = sol; SOL.data.color = cor
    for s_ in (BG.inputs[0], BG.inputs[1]): s_.keyframe_insert('default_value', frame=f)
    SOL.data.keyframe_insert('energy', frame=f); SOL.data.keyframe_insert('color', frame=f)
    LUZF.data.energy = {'noite': 2500, 'fogo': 8000}.get(m, 0); LUZF.data.keyframe_insert('energy', frame=f)
    LUZF.location = {'noite': CAMP + p(0, 0, 0.8), 'fogo': SM + p(0, 12, 6)}.get(m, LONGE); LUZF.keyframe_insert('location', frame=f)
def neve(a, b, centro, vel=1.0):
    for f_, x, y, fase in FLOCOS:
        dur = int(60 / vel); t0 = a - int(fase * dur); k = t0
        while k < b:
            kf(f_, k, centro + p(x, y, 5)); kf(f_, k + dur, centro + p(x + 0.8, y, -0.2)); k += dur
        mostra(f_, a, b)

# ================= CÂMERA =================
camd = bpy.data.cameras.new('cam'); CAM = bpy.data.objects.new('cam', camd); sc.collection.objects.link(CAM); sc.camera = CAM
camd.clip_start = 0.01; camd.dof.use_dof = True; camd.sensor_width = 36
FOCO = bpy.data.objects.new('foco', None); sc.collection.objects.link(FOCO); camd.dof.focus_object = FOCO
def mira(cl, alvo, f, lens=35, fstop=8):
    CAM.location = cl; CAM.rotation_euler = (Vector(alvo) - Vector(cl)).to_track_quat('-Z', 'Y').to_euler(); FOCO.location = alvo
    CAM.keyframe_insert('location', frame=f); CAM.keyframe_insert('rotation_euler', frame=f); FOCO.keyframe_insert('location', frame=f)
    camd.lens = lens; camd.keyframe_insert('lens', frame=f); camd.dof.aperture_fstop = fstop; camd.dof.keyframe_insert('aperture_fstop', frame=f)

# piolho doente: brilho verde na cena da ironia
CUERPO = [m for m in bpy.data.materials if m.name.startswith('Cuerpo')]
def doente(f, on):
    for m in CUERPO:
        b = m.node_tree.nodes.get('Principled BSDF')
        if not b: continue
        b.inputs['Emission Color'].default_value = (0.3, 0.9, 0.1, 1); b.inputs['Emission Strength'].default_value = 0.8 if on else 0.0
        b.inputs['Emission Strength'].keyframe_insert('default_value', frame=f)
doente(0, False)

# ================= CENAS =================
def esconde_tudo(a, b, menos=()):
    if 'tropa' not in menos: sem_tropa(a, b)
    if 'nap' not in menos: sem_napoleao(a, b)
    if 'pio' not in menos: sem_piolho(a, b)
EST = p(0, 0, 0)           # estrada de verão
def s_abre(a, b):        # tropa enorme vindo; vários caem
    modo(a, 'dia'); esconde_tudo(a, b, ('tropa', 'nap'))
    tropa(a, b, EST + p(0, 4, 0), 12, 'Walk', 1.0, avanco=2.0, rot=0, mortos=(1, 5, 9))
    hold(NAP[0], a, b, EST + p(-2.2, 2, 0), (0, 0, R(-20))); acao(NAP[1], NAP[2], 'Idle', a, b)
    mira(EST + p(1.2, -1.5, 0.9), EST + p(0, 5, 1.3), a, 24, 11); mira(EST + p(1.0, -1.0, 0.9), EST + p(0, 5, 1.3), b, 24, 11)
MAC = SX + p(0, 0, 0)       # tecido da farda
def s_piolho(a, b):      # close do piolho no tecido
    modo(a, 'macro'); esconde_tudo(a, b, ('pio',)); hold(PIO, a, b, MAC, (0, 0, R(200)))
    mira(MAC + p(0.4, -1.8, 0.45), MAC + p(0, 0.2, 0.25), a, 35, 4); mira(MAC + p(0.3, -1.5, 0.4), MAC + p(0, 0.2, 0.25), b, 35, 4)
def s_marcha(a, b):      # 1812: Napoleão na frente da tropa
    modo(a, 'dia'); esconde_tudo(a, b, ('tropa', 'nap'))
    tropa(a, b, EST + p(0, 3, 0), 12, 'Walk', 1.0, avanco=3.0)
    kf(NAP[0], a, EST + p(0, 1.2, 0)); kf(NAP[0], b, EST + p(0, -1.8, 0)); acao(NAP[1], NAP[2], 'Walk', a, b)
    mira(EST + p(-3.5, -4, 1.6), EST + p(0, 1, 1.2), a, 24, 11); mira(EST + p(-2.5, -5.5, 1.5), EST + p(0, -1, 1.2), b, 24, 11)
def deitados(a, b):      # soldados dormindo grudados perto da fogueira
    for i, (raiz, arm, acts) in enumerate(SOLD):
        if i >= 6: hold(raiz, a, b, LONGE); continue
        hold(raiz, a, b, CAMP + p(-1.5 + i * 0.55, 1.2, 0.12), (R(-90), 0, R(180)))
        acao(arm, acts, 'Idle', a, b, 0.6)
def s_sujeira(a, b):
    modo(a, 'noite'); esconde_tudo(a, b, ('tropa',)); deitados(a, b)
    mira(CAMP + p(0.3, -1.6, 2.4), CAMP + p(-0.2, 1.1, 0.2), a, 26, 10); mira(CAMP + p(0.2, -1.3, 2.3), CAMP + p(-0.2, 1.1, 0.2), b, 26, 10)
def s_paraiso(a, b):     # piolho feliz pulando no tecido
    modo(a, 'macro'); esconde_tudo(a, b, ('pio',))
    for k in range(0, b - a, 12):
        kf(PIO, a + k, MAC, (0, 0, R(160))); kf(PIO, a + k + 6, MAC + p(0, 0, 0.35), (0, 0, R(180)))
    kf(PIO, b, MAC, (0, 0, R(160)))
    mira(MAC + p(-0.8, -2.0, 0.6), MAC + p(0, 0, 0.35), a, 30, 6); mira(MAC + p(-0.6, -1.8, 0.55), MAC + p(0, 0, 0.35), b, 30, 6)
def s_pula(a, b):        # salta de uma manga para outra
    modo(a, 'macro'); esconde_tudo(a, b, ('pio',))
    m = (a + b) // 2
    kf(PIO, a, MAC + p(0, 0, 0), (0, 0, R(90))); kf(PIO, a + 10, MAC + p(0, 0, 0), (0, 0, R(90)))
    kf(PIO, m, MAC + p(-2.2, 0, 3.2), (0, R(-30), R(90))); kf(PIO, b - 10, MAC + p(-4.5, 0, 2.55), (0, R(-80), R(90))); kf(PIO, b, MAC + p(-4.5, 0, 2.55), (0, R(-80), R(90)))
    mira(MAC + p(-2.0, -7.5, 2.0), MAC + p(-2.0, 0, 1.4), a, 30, 11); mira(MAC + p(-2.6, -7.0, 2.2), MAC + p(-3.0, 0, 1.8), b, 30, 11)
def s_tifo(a, b):        # bactérias do tifo
    modo(a, 'bact'); esconde_tudo(a, b)
    mira(SB + p(0, -3.2, 0.3), SB + p(0, 1.5, 0), a, 30, 16); mira(SB + p(0, -2.6, 0.2), SB + p(0, 1.5, 0), b, 30, 16)
def s_coco(a, b):        # piolho na pele soltando bolinhas
    modo(a, 'macro'); esconde_tudo(a, b, ('pio',)); hold(PIO, a, b, SP + p(0, 0.2, 0), (0, 0, R(0))); ve(a, b, *COCO)
    for i, c_ in enumerate(COCO):
        t = a + 8 + i * 10; kf(c_, a, esc=(0.0001,) * 3); kf(c_, t, esc=(0.0001,) * 3); kf(c_, t + 4, esc=(1, 1.4, 0.8))
    mira(SP + p(2.0, -0.4, 0.7), SP + p(0, -0.1, 0.2), a, 35, 6); mira(SP + p(1.8, -0.5, 0.6), SP + p(0, -0.2, 0.15), b, 35, 6)
def s_coca(a, b):        # soldado coçando o braço no acampamento
    modo(a, 'noite'); esconde_tudo(a, b, ('tropa',))
    for i, (raiz, arm, acts) in enumerate(SOLD):
        if i == 0: hold(raiz, a, b, CAMP + p(0.9, -0.5, 0), (0, 0, R(-25))); acao(arm, acts, 'Interact', a, b, 0.7)
        elif i < 5: hold(raiz, a, b, CAMP + p(-1.5 + i * 0.55, 1.2, 0.12), (R(-90), 0, R(180))); acao(arm, acts, 'Idle', a, b, 0.6)
        else: hold(raiz, a, b, LONGE)
    mira(CAMP + p(1.9, -2.4, 1.5), CAMP + p(0.9, -0.5, 1.1), a, 35, 8); mira(CAMP + p(1.7, -2.1, 1.45), CAMP + p(0.9, -0.5, 1.15), b, 35, 8)
def s_febre(a, b):       # soldados caindo pela estrada
    modo(a, 'dia'); esconde_tudo(a, b, ('tropa',))
    tropa(a, b, EST + p(0, 2, 0), 12, 'Walk', 0.6, avanco=1.0, mortos=(0, 2, 4, 7, 10))
    mira(EST + p(3.5, -3.5, 1.2), EST + p(0, 3, 0.7), a, 26, 11); mira(EST + p(3.0, -3.0, 1.1), EST + p(0, 3, 0.6), b, 26, 11)
def s_moscou(a, b):      # chegam em Moscou vazia
    modo(a, 'dia'); esconde_tudo(a, b, ('tropa', 'nap'))
    tropa(a, b, SM + p(0, 4, 0), 6, 'Walk', 0.8, avanco=-3.0, rot=R(180))
    kf(NAP[0], a, SM + p(0, 2.5, 0), (0, 0, R(180))); kf(NAP[0], b, SM + p(0, 5.5, 0), (0, 0, R(180))); acao(NAP[1], NAP[2], 'Walk', a, b, 0.8)
    mira(SM + p(1.5, -3, 1.6), SM + p(0, 20, 4), a, 24, 16); mira(SM + p(1.3, -1.5, 1.6), SM + p(0, 22, 4), b, 24, 16)
def s_fogo(a, b):
    modo(a, 'fogo'); esconde_tudo(a, b, ('nap',)); ve(a, b, *CHAMAS)
    hold(NAP[0], a, b, SM + p(0, 6, 0), (0, 0, R(180))); acao(NAP[1], NAP[2], 'Idle', a, b)
    for k, ch in enumerate(CHAMAS):
        if ch.data.materials[0] == FOGO:
            for t in range(a, b + 1, 6): kf(ch, t, esc=(1, 1, 0.8 + 0.5 * random.random()))
    mira(SM + p(-1.5, 1, 1.3), SM + p(0, 18, 6), a, 22, 16); mira(SM + p(-1.2, 2.5, 1.2), SM + p(0, 20, 7), b, 22, 16)
def s_volta(a, b):       # retirada na neve
    modo(a, 'inverno'); esconde_tudo(a, b, ('tropa', 'nap')); neve(a, b, SI + p(0, 0, 0))
    tropa(a, b, SI + p(0, 3, 0), 9, 'Walk', 0.5, avanco=1.2)
    kf(NAP[0], a, SI + p(-1.5, 1.5, 0)); kf(NAP[0], b, SI + p(-1.5, 0.3, 0)); acao(NAP[1], NAP[2], 'Walk', a, b, 0.5)
    mira(SI + p(2.5, -4.5, 1.4), SI + p(0, 3, 1.0), a, 26, 11); mira(SI + p(2.0, -4.0, 1.3), SI + p(0, 3, 1.0), b, 26, 11)
def s_combo(a, b):       # um soldado cai na neve
    modo(a, 'inverno'); esconde_tudo(a, b, ('tropa',)); neve(a, b, SI + p(0, 0, 0), 1.6)
    tropa(a, b, SI + p(0, 3, 0), 6, 'Walk', 0.4, avanco=0.6, mortos=(1,))
    mira(SI + p(-1.8, 0.5, 1.2), SI + p(0, 3.5, 0.6), a, 30, 8); mira(SI + p(-1.5, 1.0, 1.0), SI + p(0, 3.5, 0.4), b, 30, 8)
def s_poucos(a, b):      # campo de neve com montes e só 3 de pé
    modo(a, 'inverno'); esconde_tudo(a, b, ('tropa',)); neve(a, b, SI + p(0, 8, 0))
    tropa(a, b, SI + p(0, 6, 0), 3, 'Walk', 0.4, sep=1.6, avanco=0.8)
    mira(SI + p(0, -3, 5), SI + p(0, 10, 0), a, 22, 16); mira(SI + p(0, -2, 5.5), SI + p(0, 11, 0), b, 22, 16)
def s_culpa(a, b):       # soldado congelado sozinho, nevasca
    modo(a, 'inverno'); esconde_tudo(a, b, ('tropa',)); neve(a, b, SI + p(0, 0, 0), 2.0)
    for i, (raiz, arm, acts) in enumerate(SOLD):
        if i == 0: hold(raiz, a, b, SI + p(0, 2, 0), (0, 0, R(10))); acao(arm, acts, 'Idle', a, b, 0.3)
        else: hold(raiz, a, b, LONGE)
    mira(SI + p(0.8, -1.5, 1.0), SI + p(0, 2, 1.3), a, 30, 8); mira(SI + p(0.5, -0.5, 1.4), SI + p(0, 2, 1.5), b, 30, 8)
def s_vala(a, b):        # 2001: a vala com ossos
    modo(a, 'vala'); esconde_tudo(a, b)
    mira(SV + p(0, -5, 4.5), SV, a, 26, 16); mira(SV + p(0.5, -3.5, 3.5), SV, b, 26, 16)
def s_prova(a, b):       # DNA brilhando na vala
    modo(a, 'vala'); esconde_tudo(a, b); ve(a, b, *DNA)
    for i, d_ in enumerate(DNA):
        t = a + int(i * (b - a) / len(DNA) * 0.6); kf(d_, a, esc=(0.0001,) * 3); kf(d_, t, esc=(0.0001,) * 3); kf(d_, t + 3, esc=(1, 1, 1))
    mira(SV + p(1.4, -2.0, 0.9), SV + p(0.6, -0.6, 0.6), a, 35, 8); mira(SV + p(1.2, -1.7, 1.0), SV + p(0.6, -0.6, 0.8), b, 35, 8)
def s_ironia(a, b):      # piolho doente, tremendo
    modo(a, 'macro'); doente(a, True); doente(b + 1, False); esconde_tudo(a, b, ('pio',))
    for k in range(0, b - a, 3): kf(PIO, a + k, MAC + p(0.02 * ((k // 3) % 2), 0, 0), (0, 0, R(200)))
    mira(MAC + p(0.6, -2.0, 0.6), MAC + p(0, 0.2, 0.25), a, 35, 5); mira(MAC + p(0.4, -1.6, 0.5), MAC + p(0, 0.2, 0.25), b, 35, 5)
def s_empate(a, b):      # piolho de barriga pra cima na neve
    modo(a, 'inverno'); esconde_tudo(a, b, ('pio',)); neve(a, b, SI + p(0, 0, 0), 0.5)
    kf(PIO, a, SI + p(0, 0, 0.6), (0, R(150), R(30))); kf(PIO, a + 10, SI + p(0, 0, 0.3), (0, R(180), R(30))); kf(PIO, b, SI + p(0, 0, 0.3), (0, R(180), R(30)))
    mira(SI + p(1.4, -2.2, 1.0), SI + p(0, 0, 0.3), a, 35, 6); mira(SI + p(1.1, -1.8, 0.9), SI + p(0, 0, 0.3), b, 35, 6)
def s_final(a, b):       # herói: câmera baixa
    modo(a, 'macro'); esconde_tudo(a, b, ('pio',)); hold(PIO, a, b, MAC, (0, 0, R(180)))
    mira(MAC + p(0.0, -1.6, 0.15), MAC + p(0, 0.3, 0.35), a, 24, 5); mira(MAC + p(0.0, -1.2, 0.12), MAC + p(0, 0.3, 0.35), b, 24, 5)
def ve(a, b, *objs):
    for o in objs: mostra(o, a, b)

FUN = {k[2:]: v for k, v in globals().items() if k.startswith('s_')}
for s in SHOTS['shots']:
    FUN[s['id']](s['ini'], s['fim'])
def fcurves(ad):
    try: return ad.action.fcurves
    except AttributeError:
        from bpy_extras import anim_utils
        cb = anim_utils.action_get_channelbag_for_slot(ad.action, ad.action_slot); return cb.fcurves if cb else []
FIMS = {s['fim'] for s in SHOTS['shots']}
IDS = list(bpy.data.objects) + list(bpy.data.lights) + list(bpy.data.cameras) + [w.node_tree] + [m.node_tree for m in bpy.data.materials if m.node_tree]
for o in IDS:
    ad = getattr(o, 'animation_data', None)
    if ad and ad.action:
        for fc in fcurves(ad):
            for k in fc.keyframe_points:
                k.interpolation = 'CONSTANT' if int(round(k.co.x)) in FIMS or 'default_value' in fc.data_path or fc.data_path in ('energy', 'color') else 'LINEAR'
def visibilidade(f):
    for o, fs in VISIVEL.items(): o.hide_render = f not in fs
sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'
sc.cycles.samples = 6 if PREVIEW else 16; sc.cycles.use_denoising = True
sc.cycles.max_bounces = 4; sc.cycles.diffuse_bounces = 2; sc.cycles.glossy_bounces = 2
sc.cycles.use_adaptive_sampling = True; sc.cycles.adaptive_threshold = 0.05
sc.render.resolution_x = 360 if PREVIEW else 720; sc.render.resolution_y = 640 if PREVIEW else 1280
sc.render.image_settings.file_format = 'JPEG'; sc.render.image_settings.quality = 92
sc.view_settings.view_transform = 'AgX'; sc.view_settings.look = 'AgX - Punchy'
os.makedirs(OUT, exist_ok=True)
fr = list(range(F0, F1 + 1)) if not PREVIEW else [int(x) for x in args[5].split(',')]
for f in fr:
    sc.frame_set(f); visibilidade(f)
    sc.render.filepath = os.path.join(OUT, f'{f:05d}.jpg'); bpy.ops.render.render(write_still=True)
print('ok', len(fr))
