"""Cena 3D: "Você é um tubarão-branco" — cada fato com a sua demonstração.
uso: python3 cena.py shots.json <ini> <fim> <saida> [preview f1,f2,...]"""
import bpy, math, sys, json, os, random
from mathutils import Vector
AQUI = os.path.dirname(os.path.abspath(__file__))
ASSET = os.path.join(AQUI, '..')
args = sys.argv[1:]
SHOTS = json.load(open(args[0])); F0, F1 = int(args[1]), int(args[2]); OUT = args[3]
PREVIEW = len(args) > 4 and args[4] == 'preview'
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene; sc.render.fps = SHOTS['fps']
R = math.radians
def p(x, y, z): return Vector((x, y, z))
random.seed(11)

def mat(n, c, r=0.5, metal=0.0, emis=None, alpha=1.0):
    m = bpy.data.materials.new(n); m.use_nodes = True; b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*c, 1); b.inputs['Roughness'].default_value = r; b.inputs['Metallic'].default_value = metal
    if emis: b.inputs['Emission Color'].default_value = (*emis[0], 1); b.inputs['Emission Strength'].default_value = emis[1]
    if alpha < 1: b.inputs['Alpha'].default_value = alpha
    return m
def brilho(n, cor, forca, alpha):
    m = bpy.data.materials.new(n); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    o = nt.nodes.new('ShaderNodeOutputMaterial'); e = nt.nodes.new('ShaderNodeEmission'); t = nt.nodes.new('ShaderNodeBsdfTransparent'); mx = nt.nodes.new('ShaderNodeMixShader')
    e.inputs['Color'].default_value = (*cor, 1); e.inputs['Strength'].default_value = forca; mx.inputs['Fac'].default_value = alpha
    nt.links.new(t.outputs[0], mx.inputs[1]); nt.links.new(e.outputs[0], mx.inputs[2]); nt.links.new(mx.outputs[0], o.inputs['Surface']); return m
def esf(loc, esc, m, liso=True, seg=24):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=seg, ring_count=seg // 2, location=loc); o = bpy.context.object; o.scale = esc if hasattr(esc, '__len__') else (esc,) * 3
    o.data.materials.append(m)
    if liso: bpy.ops.object.shade_smooth()
    return o
def caixa(loc, tam, m, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=rot); o = bpy.context.object; o.scale = tam; o.data.materials.append(m); return o
def cone(loc, r1, r2, h, m, rot=(0, 0, 0), v=24):
    bpy.ops.mesh.primitive_cone_add(vertices=v, radius1=r1, radius2=r2, depth=h, location=loc, rotation=rot); o = bpy.context.object; o.data.materials.append(m); return o
def plano(loc, tam, m, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_plane_add(size=1, location=loc, rotation=rot); o = bpy.context.object; o.scale = (tam[0], tam[1], 1); o.data.materials.append(m); return o
def vazio(nome, pai=None):
    o = bpy.data.objects.new(nome, None); sc.collection.objects.link(o)
    if pai: o.parent = pai
    return o
def pai_de(o, pai): o.parent = pai; return o
VISIVEL = {}
def mostra(o, a, b): VISIVEL.setdefault(o, set()).update(range(a, b + 1))
def ve(a, b, *objs):
    for o in objs: mostra(o, a, b)
def kf(o, f, loc=None, rot=None, esc=None):
    if loc is not None: o.location = loc; o.keyframe_insert('location', frame=f)
    if rot is not None: o.rotation_euler = rot; o.keyframe_insert('rotation_euler', frame=f)
    if esc is not None: o.scale = esc if hasattr(esc, '__len__') else (esc,) * 3; o.keyframe_insert('scale', frame=f)
def hold(o, a, b, loc, rot=(0, 0, 0)): kf(o, a, loc, rot); kf(o, b, loc, rot)
LONGE = p(0, -900, -300)

# ================= personagens importados =================
def importa(arq):
    antes = set(bpy.data.objects); a0 = set(bpy.data.actions)
    bpy.ops.import_scene.gltf(filepath=os.path.join(ASSET, arq))
    novos = [o for o in bpy.data.objects if o not in antes]
    g = vazio(arq + '_g')
    for o in novos:
        if o.parent is None: o.parent = g
    return g, novos, [a for a in bpy.data.actions if a not in a0]
def normaliza(g, novos, comprimento, cabeca=None):
    """centraliza, escala para o comprimento (m) e deixa a cabeça apontando para +Y. Devolve o vazio de controle."""
    bpy.context.view_layer.update(); dg = bpy.context.evaluated_depsgraph_get(); pts = []
    for o in novos:
        if o.type == 'MESH' and not o.hide_render:
            me = o.evaluated_get(dg).to_mesh(); pts += [o.matrix_world @ v.co for v in list(me.vertices)[::7]]
    lo = Vector([min(q[i] for q in pts) for i in range(3)]); hi = Vector([max(q[i] for q in pts) for i in range(3)])
    c = (lo + hi) / 2; s = comprimento / (hi.y - lo.y)
    vira = cabeca is not None and cabeca.y < c.y
    ctrl = vazio('ctrl'); g.parent = ctrl
    g.scale = (s, s, s); g.rotation_euler = (0, 0, math.pi if vira else 0)
    g.location = (c.x * s, c.y * s, -c.z * s) if vira else (-c.x * s, -c.y * s, -c.z * s)
    return ctrl
def tubarao(xray=False):
    g, novos, acts = importa('tubarao.glb')
    arm = [o for o in novos if o.type == 'ARMATURE'][0]
    for o in novos:
        if o.type == 'MESH' and any(m and m.name.startswith('Border_mat') for m in o.data.materials): o.hide_render = True
        if o.name.startswith('Icosphere'): o.hide_render = True
    bpy.context.view_layer.update()
    cab = arm.matrix_world @ arm.pose.bones['Head_end_029'].head
    ctrl = normaliza(g, novos, 4.6, cab)
    arm.animation_data_create()
    for t in list(arm.animation_data.nla_tracks): arm.animation_data.nla_tracks.remove(t)
    arm.animation_data.action = None
    if xray:
        vid = brilho('raiox', (0.45, 0.8, 1.0), 0.9, 0.2)
        for o in novos:
            if o.type == 'MESH' and not o.hide_render:
                o.data.materials.clear(); o.data.materials.append(vid)
    return ctrl, arm, acts, novos
TUB, TARM, TACTS, TOBJS = tubarao()
XR, XARM, XACTS, XOBJS = tubarao(xray=True)
def nada(arm, acts, a, b, vel=1.0):
    act = acts[0]; ln = act.frame_range[1] - act.frame_range[0]
    tr = arm.animation_data.nla_tracks.new(); st = tr.strips.new(f'n{a}', a, act)
    st.scale = vel; st.repeat = max(1.0, (b - a + 1) / (ln * vel)); st.extrapolation = 'NOTHING'
OG, ONOV, _ = importa('orca.glb')
ORCA = normaliza(OG, ONOV, 6.5, p(0, 99, 0))
# fígado (dentro do raio-x) e X onde ficaria a bexiga
FIGADO = esf((0, 0.2, -0.2), (0.22, 0.75, 0.2), mat('figado', (1.0, 0.4, 0.12), 0.4, emis=((1.0, 0.35, 0.08), 3.0))); FIGADO.parent = XR
XIS = [caixa((-0.5, 0.3, 0.15), (0.09, 0.09, 0.9), mat('xis', (1, 0.1, 0.1), 0.4, emis=((1, 0.05, 0.05), 4)), rot=(0, R(45 * s_), 0)) for s_ in (1, -1)]
for x_ in XIS: x_.parent = XR

# ================= mar =================
w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True; BG = w.node_tree.nodes['Background']
SOL = bpy.data.objects.new('sol', bpy.data.lights.new('sol', 'SUN')); sc.collection.objects.link(SOL); SOL.rotation_euler = (R(25), 0, R(20)); SOL.data.angle = R(8)
ENCH = bpy.data.objects.new('ench', bpy.data.lights.new('ench', 'SUN')); sc.collection.objects.link(ENCH); ENCH.rotation_euler = (R(120), 0, R(-40))
def modo(f, m):
    ceu, forca, sol, ench = {'azul': ((0.02, 0.22, 0.5), 1.0, 4.0, 0.8), 'fundo': ((0.02, 0.12, 0.3), 0.9, 3.0, 0.6), 'fundoA': ((0.02, 0.22, 0.5), 0.8, 2.5, 0.5), 'verde': ((0.03, 0.3, 0.22), 1.0, 3.0, 0.7),
                             'lab': ((0.75, 0.82, 0.86), 1.0, 3.0, 1.0), 'raiox': ((0.01, 0.06, 0.16), 0.8, 1.0, 0.3), 'escuro': ((0.01, 0.04, 0.1), 0.6, 1.5, 0.4),
                             'claro': ((0.02, 0.22, 0.5), 1.15, 5.0, 1.1)}[m]
    BG.inputs[0].default_value = (*ceu, 1); BG.inputs[1].default_value = forca; SOL.data.energy = sol; ENCH.data.energy = ench
    BG.inputs[0].keyframe_insert('default_value', frame=f); BG.inputs[1].keyframe_insert('default_value', frame=f)
    SOL.data.keyframe_insert('energy', frame=f); ENCH.data.keyframe_insert('energy', frame=f)
# raios de luz e partículas acompanham a câmera (ficam presos nela)
camd = bpy.data.cameras.new('cam'); CAM = bpy.data.objects.new('cam', camd); sc.collection.objects.link(CAM); sc.camera = CAM
camd.clip_start = 0.005; camd.clip_end = 120; camd.dof.use_dof = True; camd.sensor_width = 36
FOCO = vazio('foco'); camd.dof.focus_object = FOCO
def mira(cl, alvo, f, lens=35, fstop=8):
    CAM.location = cl; CAM.rotation_euler = (Vector(alvo) - Vector(cl)).to_track_quat('-Z', 'Y').to_euler(); FOCO.location = alvo
    CAM.keyframe_insert('location', frame=f); CAM.keyframe_insert('rotation_euler', frame=f); FOCO.keyframe_insert('location', frame=f)
    camd.lens = lens; camd.keyframe_insert('lens', frame=f); camd.dof.aperture_fstop = fstop; camd.dof.keyframe_insert('aperture_fstop', frame=f)
RAIO = brilho('raio_luz', (0.7, 0.9, 1.0), 0.6, 0.022)
def nevoa(m, cor, d0=6.0, d1=55.0):
    """some na cor da água conforme a distância da câmera (dá profundidade e esconde a linha do horizonte)"""
    nt = m.node_tree; out = [n for n in nt.nodes if n.type == 'OUTPUT_MATERIAL'][0]; sh = out.inputs['Surface'].links[0].from_socket
    cd = nt.nodes.new('ShaderNodeCameraData'); mr = nt.nodes.new('ShaderNodeMapRange'); mr.inputs['From Min'].default_value = d0; mr.inputs['From Max'].default_value = d1
    em = nt.nodes.new('ShaderNodeEmission'); em.inputs['Color'].default_value = (*cor, 1); mx = nt.nodes.new('ShaderNodeMixShader')
    nt.links.new(cd.outputs['View Z Depth'], mr.inputs['Value']); nt.links.new(mr.outputs['Result'], mx.inputs['Fac'])
    nt.links.new(sh, mx.inputs[1]); nt.links.new(em.outputs[0], mx.inputs[2]); nt.links.new(mx.outputs[0], out.inputs['Surface']); return m
def areia(cor_agua):
    m = mat('areia', (0.86, 0.78, 0.58), 0.95); nt = m.node_tree; b = nt.nodes['Principled BSDF']
    wv = nt.nodes.new('ShaderNodeTexWave'); wv.inputs['Scale'].default_value = 1.3; wv.inputs['Distortion'].default_value = 3.0; wv.inputs['Detail'].default_value = 2
    bp = nt.nodes.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = 0.5; nt.links.new(wv.outputs['Fac'], bp.inputs['Height']); nt.links.new(bp.outputs['Normal'], b.inputs['Normal'])
    # cáusticas: rede de luz do sol no fundo
    vo = nt.nodes.new('ShaderNodeTexVoronoi'); vo.feature = 'DISTANCE_TO_EDGE'; vo.inputs['Scale'].default_value = 0.9
    cr = nt.nodes.new('ShaderNodeValToRGB'); cr.color_ramp.elements[0].position = 0.0; cr.color_ramp.elements[0].color = (1, 1, 1, 1); cr.color_ramp.elements[1].position = 0.09; cr.color_ramp.elements[1].color = (0, 0, 0, 1)
    nt.links.new(vo.outputs['Distance'], cr.inputs['Fac'])
    b.inputs['Emission Color'].default_value = (0.75, 0.95, 1.0, 1); nt.links.new(cr.outputs['Color'], b.inputs['Emission Strength'])
    mu = nt.nodes.new('ShaderNodeMath'); mu.operation = 'MULTIPLY'; mu.inputs[1].default_value = 0.55; nt.links.new(cr.outputs['Color'], mu.inputs[0]); nt.links.new(mu.outputs[0], b.inputs['Emission Strength'])
    return nevoa(m, cor_agua)
def pedra(loc, tam, m):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=3, radius=1, location=loc); o = bpy.context.object; o.scale = tam; o.rotation_euler = (0, 0, random.uniform(0, 6))
    tx = bpy.data.textures.new('ruido', 'CLOUDS'); tx.noise_scale = 0.8; d = o.modifiers.new('d', 'DISPLACE'); d.texture = tx; d.strength = 0.5
    o.data.materials.append(m); bpy.ops.object.shade_smooth(); return o
def coral(loc, m, h=1.0, n=6):
    """coral de galhos"""
    for i in range(n):
        a_ = random.uniform(0, 6.28); inc = random.uniform(0.15, 0.6); hh = h * random.uniform(0.6, 1.2)
        d = p(math.cos(a_) * math.sin(inc), math.sin(a_) * math.sin(inc), math.cos(inc))
        o = cone(loc + d * hh / 2, 0.09 * h, 0.05 * h, hh, m, v=7); o.rotation_euler = d.to_track_quat('Z', 'Y').to_euler()
        topo = loc + d * hh; esf(topo, 0.07 * h, m, True, 8)
        for k in range(2):
            a2 = a_ + random.uniform(-1, 1); d2 = p(math.cos(a2) * 0.6, math.sin(a2) * 0.6, 0.7).normalized(); h2 = hh * 0.45
            o2 = cone(loc + d * hh * random.uniform(0.4, 0.8) + d2 * h2 / 2, 0.05 * h, 0.03 * h, h2, m, v=6); o2.rotation_euler = d2.to_track_quat('Z', 'Y').to_euler()
def esponja(loc, m, h=0.8):
    for i in range(random.randint(2, 4)):
        hh = h * random.uniform(0.6, 1.3); o = cone(loc + p(random.uniform(-0.25, 0.25), random.uniform(-0.25, 0.25), hh / 2), 0.12, 0.2, hh, m, v=10)
def alga(loc, m, h=2.0):
    for i in range(random.randint(3, 6)):
        cu = bpy.data.curves.new('alga', 'CURVE'); cu.dimensions = '3D'; cu.bevel_depth = 0.035; cu.bevel_resolution = 2
        sp = cu.splines.new('BEZIER'); sp.bezier_points.add(3); x0, y0 = random.uniform(-0.3, 0.3), random.uniform(-0.3, 0.3); hh = h * random.uniform(0.6, 1.2)
        for k in range(4):
            bp_ = sp.bezier_points[k]; bp_.co = (x0 + 0.18 * math.sin(k * 1.7 + i), y0 + 0.1 * math.cos(k * 1.3 + i), hh * k / 3); bp_.handle_left_type = bp_.handle_right_type = 'AUTO'; bp_.radius = 1.6 - 0.45 * k
        o = bpy.data.objects.new('alga', cu); sc.collection.objects.link(o); o.location = loc; o.scale = (2.2, 0.5, 1); cu.materials.append(m)
def estrela(loc, m):
    for k in range(5):
        a_ = k * 1.2566; o = cone(loc + p(math.cos(a_) * 0.13, math.sin(a_) * 0.13, 0.03), 0.07, 0.01, 0.3, m, rot=(0, R(90), a_), v=6); o.scale = (0.5, 1, 1)
def bolhas(base, n=10):
    bm = mat('bolha', (0.9, 0.97, 1.0), 0.05, emis=((0.8, 0.95, 1.0), 1.2))
    for i in range(n): esf(base + p(random.uniform(-0.12, 0.12), random.uniform(-0.12, 0.12), i * random.uniform(0.35, 0.6)), random.uniform(0.02, 0.06), bm, True, 8)
def mar(base, cor_agua, fundo=-6.0, raios=7, raio_=16, livre=3.0):
    """um pedaço de mar com fundo detalhado: areia com ondas e rede de luz, pedras, corais, esponjas, algas, estrelas, cardumes e bolhas"""
    plano(base + p(0, 0, fundo), (260, 260), areia(cor_agua))
    for i in range(raios):
        cone(base + p(random.uniform(-raio_, raio_), random.uniform(-raio_ * 0.4, raio_ * 1.4), 3), 0.25, 1.6, 26, RAIO, rot=(R(random.uniform(-12, -4)), R(random.uniform(8, 16)), 0), v=12)
    pm = mat('particula', (0.8, 0.9, 1.0), 0.5, emis=((0.7, 0.85, 1.0), 0.6))
    for i in range(110):
        esf(base + p(random.uniform(-raio_, raio_), random.uniform(-raio_ * 0.6, raio_ * 1.6), random.uniform(fundo + 0.3, 6)), random.uniform(0.012, 0.03), pm, False, 6)
    fx = lambda m: nevoa(m, cor_agua)
    PED = fx(mat('pedra', (0.4, 0.4, 0.43), 0.9)); PED2 = fx(mat('pedra2', (0.3, 0.33, 0.3), 0.9))
    COR = [fx(mat(f'coral{k}', c_, 0.6)) for k, c_ in enumerate(((0.95, 0.35, 0.3), (0.98, 0.6, 0.15), (0.85, 0.3, 0.6), (0.95, 0.85, 0.3), (0.5, 0.35, 0.8)))]
    VERDE = [fx(mat(f'algam{k}', c_, 0.7)) for k, c_ in enumerate(((0.1, 0.45, 0.2), (0.25, 0.55, 0.15), (0.12, 0.4, 0.35)))]
    def lugar(rmin=livre):
        while True:
            x, y = random.uniform(-raio_, raio_), random.uniform(-6, raio_ * 1.7)
            if math.hypot(x, y - 1) > rmin: return base + p(x, y, fundo)
    for i in range(16):
        l = lugar(); t = random.uniform(0.5, 1.8); pedra(l + p(0, 0, t * 0.25), (t, t * random.uniform(0.7, 1.2), t * random.uniform(0.4, 0.8)), random.choice((PED, PED2)))
        if random.random() < 0.6: coral(l + p(random.uniform(-0.4, 0.4), random.uniform(-0.4, 0.4), t * 0.45), random.choice(COR), random.uniform(0.6, 1.2))
    for i in range(14): coral(lugar(), random.choice(COR), random.uniform(0.5, 1.3))
    for i in range(10): esponja(lugar(), random.choice(COR))
    for i in range(22): alga(lugar(), random.choice(VERDE), random.uniform(1.2, 3.2))
    for i in range(9): estrela(lugar(1.0) + p(0, 0, 0.02), random.choice(COR))
    for i in range(5): bolhas(lugar() + p(0, 0, 0.3), 12)
    for i in range(4):   # cardumes coloridos perto do fundo
        g = cardume(lugar(5) + p(0, 0, random.uniform(1.0, 3.0)), 18, 1.4, random.choice(((1.0, 0.75, 0.1), (1.0, 0.45, 0.1), (0.3, 0.7, 1.0))))
        g.rotation_euler = (0, 0, random.uniform(0, 6))
PEIXE_M = mat('peixinho', (0.75, 0.8, 0.85), 0.3, 0.6)
def cardume(base, n=40, espalha=3.0, cor=None):
    m = PEIXE_M if cor is None else mat('peixe_cor', cor, 0.4, emis=((cor), 0.25))
    g = vazio('cardume'); g.location = base
    for i in range(n):
        o = esf((random.uniform(-espalha, espalha), random.uniform(-espalha * 1.5, espalha * 1.5), random.uniform(-1, 1)), (0.05, 0.16, 0.08), m, True, 8); o.parent = g
        t = cone((o.location.x, o.location.y - 0.17, o.location.z), 0.07, 0.0, 0.1, m, rot=(R(-90), 0, 0), v=4); t.parent = g; t.scale = (0.3, 1, 1)
    return g
AGUA_A, AGUA_B, AGUA_C = (0.02, 0.22, 0.5), (0.02, 0.12, 0.3), (0.03, 0.3, 0.22)
A = p(0, 0, 0); mar(A, AGUA_A, fundo=-5.0)                 # mar aberto azul
B = p(300, 0, 0); mar(B, AGUA_B, fundo=-1.6, raios=4)       # fundo de areia (sentido elétrico)
C = p(600, 0, 0); mar(C, AGUA_C, fundo=-6.0)                # água verde (orca)
CARD = cardume(A + p(3, 8, 1.5))
# carro para a comparação de tamanho + régua
CARRO = vazio('carro')
cm = mat('lataria', (0.85, 0.15, 0.12), 0.3, 0.3)
pai_de(caixa((0, 0, 0.55), (1.7, 4.2, 0.6), cm), CARRO); pai_de(caixa((0, -0.2, 1.05), (1.5, 2.2, 0.55), mat('vidro_c', (0.15, 0.2, 0.25), 0.1)), CARRO)
for sx in (-1, 1):
    for sy in (-1.3, 1.3):
        bpy.ops.mesh.primitive_cylinder_add(radius=0.36, depth=0.25, location=(0.85 * sx, sy, 0.36), rotation=(0, R(90), 0)); r_ = bpy.context.object; r_.data.materials.append(mat('pneu', (0.03, 0.03, 0.03), 0.8)); r_.parent = CARRO
REGUA = vazio('regua'); rm = mat('regua', (1.0, 0.8, 0.1), 0.4, emis=((1.0, 0.75, 0.05), 3))
pai_de(caixa((0, 0, 0), (0.05, 4.6, 0.05), rm), REGUA); pai_de(caixa((0, 2.3, 0), (0.05, 0.05, 0.5), rm), REGUA); pai_de(caixa((0, -2.3, 0), (0.05, 0.05, 0.5), rm), REGUA)

# ================= raio-x: peixe comum com bexiga de ar =================
PX = vazio('peixe_x'); vidro = brilho('raiox_p', (1.0, 0.85, 0.4), 0.9, 0.3)
pai_de(esf((0, 0, 0), (0.28, 1.0, 0.5), vidro), PX); pai_de(cone((0, -1.2, 0), 0.5, 0.0, 0.5, vidro, rot=(R(-90), 0, 0), v=4), PX).scale = (0.25, 1, 1)
BEXIGA = pai_de(esf((0, 0.1, 0.12), (0.14, 0.42, 0.16), mat('bexiga', (0.9, 0.97, 1.0), 0.2, emis=((0.8, 0.95, 1.0), 4))), PX)

# ================= zoom na pele (laboratório) =================
SK = p(0, 300, 0)
plano(SK, (30, 30), mat('pele_fundo', (0.42, 0.46, 0.5), 0.6))
DM = mat('denticulo', (0.82, 0.85, 0.88), 0.25, 0.2)
for ix in range(-9, 10):
    for iy in range(-4, 24):
        d_ = cone(SK + p(ix * 0.5 + (0.25 if iy % 2 else 0), iy * 0.42, 0.07), 0.27, 0.02, 0.6, DM, rot=(R(72), 0, 0), v=5); d_.scale = (1, 0.35, 1)
LISA = plano(SK + p(40, 4, 0), (12, 14), mat('pele_lisa', (0.75, 0.6, 0.55), 0.5))
AGUA_M = mat('agua', (0.5, 0.8, 1.0), 0.05, emis=((0.3, 0.6, 1.0), 0.8))
GOTAS = [esf(SK, 0.09, AGUA_M, True, 12) for _ in range(46)]
GOTAS2 = [esf(SK, 0.09, AGUA_M, True, 12) for _ in range(30)]

# ================= mito do sangue =================
SANGUE = [esf(A + p(random.uniform(-1.2, 1.2), 6 + random.uniform(-1, 1), random.uniform(-0.8, 0.8)), random.uniform(0.3, 0.8), brilho(f'sg{i}', (0.8, 0.02, 0.05), 0.7, 0.35), True, 12) for i in range(14)]

# ================= sentido elétrico =================
PRESA = B + p(0, 4.5, -1.6)
pai_presa = vazio('presa'); pai_presa.location = PRESA
pai_de(esf((0, 0, 0.02), (0.3, 0.7, 0.2), mat('linguado', (0.7, 0.62, 0.42), 0.9)), pai_presa)
CORACAO = pai_de(esf((0, 0.15, 0.2), 0.09, mat('coracao', (1, 0.1, 0.2), 0.3, emis=((1.0, 0.05, 0.15), 8))), pai_presa)
ANEIS = []
ROSA = brilho('campo', (1.0, 0.25, 0.9), 5.0, 0.8)
for i in range(6):
    bpy.ops.mesh.primitive_torus_add(major_radius=1, minor_radius=0.018, location=PRESA + p(0, 0, 0.1), rotation=(R(90 if i % 2 else 60), 0, R(i * 30))); t = bpy.context.object; t.data.materials.append(ROSA); ANEIS.append(t)
# poros no focinho (bolinhas pretas grudadas na cabeça do tubarão)
from mathutils.bvhtree import BVHTree
def poros():
    # calcula com o tubarão na pose de nado (a pose de descanso do modelo é outra)
    TARM.animation_data.action = TACTS[0]; sc.frame_set(1); bpy.context.view_layer.update(); dg = bpy.context.evaluated_depsgraph_get()
    corpo = [o for o in TOBJS if o.type == 'MESH' and o.data.materials and o.data.materials[0].name.startswith('body_mat')][0]
    bvh = BVHTree.FromObject(corpo, dg); mw_c = corpo.matrix_world; inv = mw_c.inverted()
    pm = mat('poro', (0.02, 0.02, 0.02), 0.3); out = []
    for i in range(320):
        alvo = p(random.uniform(-0.35, 0.35), random.uniform(1.85, 2.4), random.uniform(-0.05, 0.35))
        hit = bvh.find_nearest(inv @ alvo)
        if not hit or hit[0] is None: continue
        pos = mw_c @ hit[0]
        if pos.y < 1.8 or pos.z < -0.1: continue
        o = esf(pos, 0.0055, pm, False, 6); bpy.context.view_layer.update(); mw = o.matrix_world.copy()
        o.parent = TARM; o.parent_type = 'BONE'; o.parent_bone = 'Head_05'; bpy.context.view_layer.update(); o.matrix_world = mw; out.append(o)
    TARM.animation_data.action = None
    return out
POROS = poros()

# ================= esteira de dentes (mandíbula em corte) =================
MD = p(0, 600, 0)
plano(MD + p(0, 3, -1.2), (40, 40), mat('mesa', (0.82, 0.86, 0.9), 0.4))
plano(MD + p(0, 8, 4), (40, 14), mat('fundo_md', (0.55, 0.78, 0.9), 0.6), rot=(R(90), 0, 0))
GENG = mat('gengiva', (0.95, 0.45, 0.5), 0.35)
esf(MD, (1.25, 1.5, 1.125), GENG, True, 48)
caixa(MD + p(0, 0, -0.85), (2.3, 2.8, 0.7), GENG)
DENTE_M = mat('dente', (0.97, 0.96, 0.9), 0.2)
DENTES = []   # fileiras: 0 = em pé na frente ... 3 = deitado atrás
def pose_dente(k):
    """posição/ângulo do dente na 'esteira' em volta da gengiva: k=0 em pé no topo da frente; k cresce para trás/dentro"""
    ang = R(-25 + 38 * k); rr = 1.5 * 0.99
    return p(0, -math.sin(ang) * rr, math.cos(ang) * rr * 0.75), (ang * -1 + R(0), 0, 0)
for col in (-0.75, 0, 0.75):
    for k in range(4):
        d_ = cone(MD, 0.3, 0.0, 0.9, DENTE_M, v=3); d_.scale = (1, 0.35, 1)
        DENTES.append((d_, col, k))
def kdentes(f, desloc=0.0, cai=None):
    """desloc: quanto a esteira andou (0..1 = uma fileira); cai: (coluna, progresso da queda)"""
    for d_, col, k in DENTES:
        kk = k - (desloc if col == 0 else 0)
        loc, rot = pose_dente(kk); loc = MD + loc + p(col, 0, 0)
        h = Vector((0, -math.sin(-rot[0]) * 0.4, math.cos(rot[0]) * 0.4))
        if col == 0 and k == 0 and cai is not None:
            loc0, rot0 = pose_dente(0); loc = MD + loc0 + p(0, -0.9 * cai, 0.45 - 2.2 * cai * cai); rot = (rot0[0] - 3.0 * cai, 0, 0.8 * cai); h = Vector((0, 0, 0))
        kf(d_, f, loc + h, rot)
kdentes(0)

# ================= olho (close em cenário próprio) =================
EY = p(0, 900, 0)
plano(EY + p(0, 0.35, 0), (12, 12), mat('pele_olho', (0.5, 0.55, 0.6), 0.55), rot=(R(90), 0, 0))
bpy.ops.mesh.primitive_torus_add(major_radius=1.05, minor_radius=0.22, location=EY + p(0, 0.2, 0), rotation=(R(90), 0, 0)); bpy.context.object.data.materials.append(mat('palpebra', (0.36, 0.4, 0.45), 0.5)); bpy.ops.object.shade_smooth()
OLHO = esf(EY, 1.0, mat('olho_preto', (0.01, 0.01, 0.015), 0.05), True, 48)
bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.select_all(action='SELECT'); bpy.ops.transform.rotate(value=R(90), orient_axis='X'); bpy.ops.object.mode_set(mode='OBJECT')
OLHO.data.materials.append(mat('olho_branco', (0.93, 0.9, 0.82), 0.5))
for poly in OLHO.data.polygons:
    if poly.center.y > 0.15: poly.material_index = 1      # metade de trás = cartilagem branca
esf(EY + p(-0.3, -0.93, 0.3), 0.07, mat('reflexo', (1, 1, 1), 0.1, emis=((1, 1, 1), 2))).parent = OLHO

# ================= cadeia alimentar (blocos) =================
PIR = vazio('piramide'); PIR.location = A + p(0, 7, -3.5)
BLOCOS = []
for i, (cor, larg) in enumerate((((0.25, 0.7, 0.35), 3.6), ((0.95, 0.75, 0.2), 2.6), ((0.95, 0.45, 0.15), 1.6))):
    b_ = caixa((0, 0, 0.45 + i * 0.95), (larg, 1.2, 0.85), mat(f'bloco{i}', cor, 0.5)); b_.parent = PIR; BLOCOS.append(b_)

# ================= mordida: boca abrindo =================
TARM.animation_data.action_extrapolation = 'NOTHING'
def boca(f, k):
    """k: 0 fechada .. 1 escancarada (mandíbula desce, cabeça sobe)"""
    for nome, ang in (('Jaw_01_06', 0.75), ('Head_05', -0.35)):
        pb = TARM.pose.bones[nome]; pb.rotation_mode = 'XYZ'
        pb.rotation_euler = (ang * k, 0, 0); pb.keyframe_insert('rotation_euler', frame=f)

# ================= CENAS =================
MOVEIS = [TUB, XR, ORCA, PX, CARRO, REGUA, CARD]
def limpa(a, b, usa=()):
    for o in MOVEIS:
        if o not in usa: hold(o, a, b, LONGE)
def tub(a, b, de, ate, rot=(0, 0, 0), rot2=None, vel=1.0, nadando=True):
    kf(TUB, a, de, rot); kf(TUB, b, ate, rot2 or rot)
    nada(TARM, TACTS, a, b, vel if nadando else 60)
def s_abre(a, b):        # tubarão vindo de frente, câmera baixa
    modo(a, 'azul'); limpa(a, b, (TUB, CARD)); tub(a, b, A + p(0, 3, 0), A + p(0, 0.5, 0), (0, 0, R(180)))
    hold(CARD, a, b, A + p(3, 8, 1.5))
    mira(A + p(1.2, -5.5, -0.8), A + p(0, 1.5, 0), a, 28, 11); mira(A + p(0.8, -4.5, -0.6), A + p(0, 0.5, 0), b, 28, 11)
def s_regua(a, b):       # de lado, carro embaixo e régua em cima
    modo(a, 'azul'); limpa(a, b, (TUB, CARRO, REGUA)); tub(a, b, A, A, (0, 0, R(90)))
    hold(CARRO, a, b, A + p(0, 0, -2.6), (0, 0, R(90))); hold(REGUA, a, b, A + p(0, 0, 1.3), (0, 0, R(90)))
    mira(A + p(0, -9, -0.3), A + p(0, 0, -0.6), a, 30, 16); mira(A + p(0, -8, -0.3), A + p(0, 0, -0.6), b, 30, 16)
def s_nome(a, b):        # passa rente à câmera mostrando os dentes
    modo(a, 'azul'); limpa(a, b, (TUB,)); tub(a, b, A + p(-2.5, 1, 0), A + p(1.0, -0.3, 0), (0, 0, R(-110)))
    mira(A + p(0.5, -3.2, -0.3), A + p(-1.0, 0.5, 0), a, 30, 8); mira(A + p(0.5, -3.2, -0.3), A + p(1.5, -0.5, 0), b, 30, 8)
def s_regra(a, b):       # por trás, seguindo a cauda
    modo(a, 'azul'); limpa(a, b, (TUB, CARD)); tub(a, b, A + p(0, 0, 0), A + p(0, 5, 0), vel=0.7); hold(CARD, a, b, A + p(-2, 14, 1))
    mira(A + p(1.5, -5.5, 1.5), A + p(0, 1, 0), a, 26, 11); mira(A + p(1.2, -1.0, 1.4), A + p(0, 6, 0), b, 26, 11)
def s_bexiga(a, b):      # raio-x do peixe comum com a bolha de ar
    modo(a, 'raiox'); limpa(a, b, (PX,)); hold(PX, a, b, V, (0, 0, R(90)))
    kf(BEXIGA, a, esc=(0.1, 0.3, 0.11)); kf(BEXIGA, b, esc=(0.16, 0.48, 0.19))
    mira(V + p(0, -7.5, 0.2), V, a, 35, 16); mira(V + p(0, -6.5, 0.2), V, b, 35, 16)
def s_sem(a, b):         # raio-x do tubarão: X no lugar da bexiga
    modo(a, 'raiox'); limpa(a, b, (XR,)); hold(XR, a, b, V, (0, 0, R(90))); nada(XARM, XACTS, a, b, 1.5)
    ve(a, b, *XIS)
    mira(V + p(0, -7.5, 0.2), V, a, 35, 16); mira(V + p(0, -6.5, 0.2), V, b, 35, 16)
def s_figado(a, b):      # fígado laranja acende
    modo(a, 'raiox'); limpa(a, b, (XR,)); hold(XR, a, b, V, (0, 0, R(90))); nada(XARM, XACTS, a, b, 1.5); ve(a, b, FIGADO)
    kf(FIGADO, a, esc=(0.03, 0.1, 0.03)); kf(FIGADO, a + 12, esc=(0.22, 0.75, 0.2)); kf(FIGADO, b, esc=(0.22, 0.75, 0.2))
    mira(V + p(0, -6.5, 0.2), V, a, 35, 16); mira(V + p(0.6, -5.0, -0.2), V + p(0.2, 0, -0.2), b, 35, 16)
def s_afunda(a, b):      # para de nadar e afunda de bico
    modo(a, 'fundoA'); limpa(a, b, (TUB,)); tub(a, b, A + p(0, 0, 0.5), A + p(0, 0, -3.5), (0, 0, R(90)), (R(-35), 0, R(90)), nadando=False)
    mira(A + p(0, -8, -1.0), A + p(0, 0, -0.5), a, 28, 16); mira(A + p(0, -8, -1.5), A + p(0, 0, -2.5), b, 28, 16)
def s_pele1(a, b):       # zoom entrando no flanco do tubarão
    modo(a, 'azul'); limpa(a, b, (TUB,)); tub(a, b, A, A, (0, 0, R(90)), vel=1.5)
    mira(A + p(0, -6, 0.3), A + p(0, 0, 0.1), a, 30, 16); mira(A + p(0.2, -0.75, 0.25), A + p(0.2, 0, 0.2), b, 50, 16)
def chuva_gotas(a, b, lista, base, vel, larg=3.5, trava=False):
    ve(a, b, *lista)
    for i, g in enumerate(lista):
        x = random.uniform(-larg, larg); y0 = random.uniform(0, 7); z = 0.42 + random.uniform(0, 0.25)
        if trava: kf(g, a, base + p(x, y0, 0.1)); kf(g, b, base + p(x, y0 - 0.3, 0.1))
        else: kf(g, a, base + p(x, y0 + vel, z)); kf(g, b, base + p(x, y0 - vel, z))
def s_pele2(a, b):       # os dentículos de pertinho
    modo(a, 'lab'); limpa(a, b)
    mira(SK + p(1.5, -1.5, 1.6), SK + p(0, 2.5, 0), a, 30, 11); mira(SK + p(0.8, -0.4, 1.0), SK + p(0, 2.8, 0), b, 30, 11)
def s_pele3(a, b):       # água deslizando nos dentículos x travando na pele lisa (lado a lado)
    modo(a, 'lab'); limpa(a, b); chuva_gotas(a, b, GOTAS, SK, 5.0)
    mira(SK + p(-2.5, 0.5, 1.5), SK + p(0.5, 4, 0.2), a, 28, 11); mira(SK + p(-2.0, 1.0, 1.3), SK + p(0.5, 4.5, 0.2), b, 28, 11)
def s_mito(a, b):        # nuvem de sangue e o tubarão passando sem ligar
    modo(a, 'azul'); limpa(a, b, (TUB,)); ve(a, b, *SANGUE); tub(a, b, A + p(-5, 3.5, 0.3), A + p(2, 3.5, 0.3), (0, 0, R(-90)))
    mira(A + p(0, -3, 0), A + p(0, 5, 0), a, 28, 16); mira(A + p(0, -2.5, 0), A + p(0, 5, 0), b, 28, 16)
def s_poros(a, b):       # close no focinho com os poros
    modo(a, 'azul'); ve(a, b, *POROS); limpa(a, b, (TUB,)); tub(a, b, A, A, (0, 0, R(180)), nadando=False)
    mira(A + p(0.9, -3.6, 0.7), A + p(0, -2.0, 0.2), a, 50, 11); mira(A + p(0.6, -3.3, 0.6), A + p(0, -2.0, 0.2), b, 55, 11)
def aneis(a, b):
    ve(a, b, *ANEIS, CORACAO)
    for i, t in enumerate(ANEIS):
        k = a - i * 7
        while k < b: kf(t, k, esc=0.1); kf(t, k + 41, esc=2.6); kf(t, k + 42, esc=0.1); k += 42
    for k in range(a, b, 10): kf(CORACAO, k, esc=0.09); kf(CORACAO, k + 3, esc=0.15); kf(CORACAO, k + 6, esc=0.09)
def s_eletr(a, b):       # tubarão rondando o fundo, anéis rosa saindo da areia
    modo(a, 'fundo'); limpa(a, b, (TUB,)); aneis(a, b); tub(a, b, B + p(-3, 3.5, 0.2), B + p(0.5, 4.2, 0.0), (0, 0, R(-80)), vel=0.8)
    mira(B + p(2.5, -2.5, -0.6), B + p(0, 4.2, -0.9), a, 28, 16); mira(B + p(2.0, -1.5, -0.7), B + p(0, 4.4, -1.0), b, 28, 16)
def s_coracao(a, b):     # close no peixe enterrado com o coração batendo
    modo(a, 'fundo'); limpa(a, b, (TUB,)); aneis(a, b); tub(a, b, B + p(0, 9, 1.2), B + p(0, 7.3, 0.6), (R(-15), 0, R(180)), vel=0.8)
    mira(PRESA + p(1.2, -2.6, 0.9), PRESA + p(0, 0.3, 0.3), a, 35, 11); mira(PRESA + p(0.9, -2.2, 0.8), PRESA + p(0, 0.3, 0.3), b, 35, 11)
def s_boca(a, b):        # mandíbula em corte com as fileiras
    modo(a, 'lab'); limpa(a, b); kdentes(a); kdentes(b)
    mira(MD + p(2.0, -7.0, 3.0), MD + p(0, 0, 0.5), a, 35, 16); mira(MD + p(1.5, -6.0, 2.6), MD + p(0, 0, 0.6), b, 35, 16)
def s_quebrou(a, b):     # o dente da frente cai
    modo(a, 'lab'); limpa(a, b); kdentes(a, 0, 0.0); kdentes(b, 0, 1.0)
    mira(MD + p(2.2, -4.0, 1.9), MD + p(0, -0.4, 1.0), a, 45, 16); mira(MD + p(2.2, -4.0, 1.9), MD + p(0, -0.4, 1.0), b, 45, 16)
def s_novo(a, b):        # a fileira desliza
    modo(a, 'lab'); limpa(a, b); kdentes(a, 0.0, 1.0); kdentes(b - 6, 1.0, 1.0); kdentes(b, 1.0, 1.0)
    mira(MD + p(2.2, -4.0, 1.9), MD + p(0, -0.4, 1.0), a, 45, 16); mira(MD + p(1.6, -3.4, 1.7), MD + p(0, -0.4, 1.0), b, 45, 16)
def s_milhares(a, b):    # boca do tubarão de verdade, dentes à mostra
    modo(a, 'azul'); limpa(a, b, (TUB,)); tub(a, b, A, A, (0, 0, R(180)), nadando=False); boca(a - 1, 0); boca(a + 8, 0.9); boca(b, 0.9)
    mira(A + p(0.5, -3.6, -0.5), A + p(0, -2.0, -0.15), a, 45, 11); mira(A + p(0.3, -3.2, -0.45), A + p(0, -2.0, -0.15), b, 45, 11)
def s_lenta(a, b):       # ataque de baixo pra cima, em câmera lenta
    modo(a, 'claro'); limpa(a, b, (TUB,)); tub(a, b, A + p(0, 0, -2.5), A + p(0, 0, -1.2), (R(55), 0, R(160)), vel=3.0); boca(a, 0.1); boca(b, 0.7)
    mira(A + p(1.5, -5.5, 1.0), A + p(0, 0, -1.0), a, 28, 11); mira(A + p(1.2, -5.0, 1.2), A + p(0, 0, -0.2), b, 28, 11)
def s_olho(a, b):        # olho preto gira e vira branco
    modo(a, 'lab'); limpa(a, b)
    kf(OLHO, a, rot=(0, 0, 0)); kf(OLHO, a + int((b - a) * 0.35), rot=(0, 0, 0)); kf(OLHO, a + int((b - a) * 0.6), rot=(R(-170), 0, 0)); kf(OLHO, b, rot=(R(-170), 0, 0))
    mira(EY + p(0.8, -5.0, 0.2), EY, a, 40, 16); mira(EY + p(0.5, -4.2, 0.1), EY, b, 40, 16)
def s_mandibula(a, b):   # boca escancarando de perfil
    modo(a, 'claro'); limpa(a, b, (TUB,)); tub(a, b, A, A + p(-0.4, 0, 0), (0, 0, R(90)), nadando=False); boca(a, 0.0); boca(a + 10, 1.0); boca(b, 1.0)
    mira(A + p(-2.2, -3.2, 0.1), A + p(-1.8, 0, -0.1), a, 40, 11); mira(A + p(-2.6, -2.8, 0.0), A + p(-2.1, 0, -0.1), b, 40, 11)
ORC = C
V = A + p(0, 0, 60)
def s_fraco(a, b):       # água verde: tubarão nadando e a orca vindo por trás, bem visível
    modo(a, 'verde'); limpa(a, b, (TUB, ORCA)); tub(a, b, ORC + p(-1.5, 0, 0), ORC + p(1.0, 0, 0), (0, 0, R(-90)), vel=0.8)
    kf(ORCA, a, ORC + p(-11, 2.5, 1.2), (0, 0, R(-90))); kf(ORCA, b, ORC + p(-5.5, 1.5, 0.3), (0, 0, R(-90)))
    mira(ORC + p(4.5, -6.0, 0.8), ORC + p(-2.0, 0.8, 0.2), a, 26, 16); mira(ORC + p(4.0, -5.5, 0.8), ORC + p(-1.5, 0.8, 0.2), b, 26, 16)
def s_vira(a, b):        # a orca entra por baixo, empurra com o focinho e rola o tubarão de barriga pra cima
    modo(a, 'verde'); limpa(a, b, (TUB, ORCA)); n1 = a + int((b - a) * 0.3); n2 = a + int((b - a) * 0.75)
    kf(TUB, a, ORC + p(1.0, 0, 0), (0, 0, R(-90))); kf(TUB, n1, ORC + p(1.4, 0, 0), (0, 0, R(-90)))
    kf(TUB, n2, ORC + p(1.7, 0, 0.7), (0, R(180), R(-90))); kf(TUB, b, ORC + p(1.8, 0, 0.8), (0, R(180), R(-90))); nada(TARM, TACTS, a, n1, 0.8); nada(TARM, TACTS, n1 + 1, b, 60)
    kf(ORCA, a, ORC + p(-5.5, 1.5, 0.3), (0, 0, R(-90))); kf(ORCA, n1, ORC + p(-1.6, 0.3, -1.3), (R(15), 0, R(-80)))
    kf(ORCA, n2, ORC + p(-0.6, 0.2, -0.9), (R(30), R(25), R(-80))); kf(ORCA, b, ORC + p(-0.2, 0.2, -1.0), (R(30), R(25), R(-80)))
    mira(ORC + p(1.0, -9.5, 1.6), ORC + p(0.3, 0, -0.2), a, 28, 16); mira(ORC + p(1.2, -8.0, 1.8), ORC + p(0.8, 0, 0.1), b, 28, 16)
def s_apaga(a, b):       # de barriga branca pra cima, paralisado; a orca segura por baixo
    modo(a, 'verde'); limpa(a, b, (TUB, ORCA)); tub(a, b, ORC + p(1.8, 0, 0.8), ORC + p(1.9, 0, 0.6), (0, R(180), R(-90)), (0, R(186), R(-92)), nadando=False)
    hold(ORCA, a, b, ORC + p(-0.2, 0.2, -1.0), (R(30), R(25), R(-80)))
    mira(ORC + p(2.5, -4.5, 3.2), ORC + p(1.6, 0, 0.5), a, 32, 11); mira(ORC + p(2.3, -3.8, 2.9), ORC + p(1.7, 0, 0.5), b, 32, 11)
def s_orca(a, b):        # close na orca, com o tubarão virado ao fundo
    modo(a, 'verde'); limpa(a, b, (TUB, ORCA)); tub(a, b, ORC + p(1.9, 0, 0.6), ORC + p(2.0, 0, 0.3), (0, R(186), R(-92)), nadando=False)
    kf(ORCA, a, ORC + p(-0.2, 0.2, -1.0), (R(30), R(25), R(-80))); kf(ORCA, b, ORC + p(0.6, -1.2, -0.6), (R(10), R(10), R(-60)))
    mira(ORC + p(3.5, -6.5, -0.2), ORC + p(0.5, -0.5, -0.4), a, 32, 16); mira(ORC + p(3.2, -6.0, -0.2), ORC + p(0.8, -0.8, -0.3), b, 32, 16)
def s_mar(a, b):         # mar cheio de vida, tubarão no alto
    modo(a, 'claro'); limpa(a, b, (TUB, CARD)); tub(a, b, A + p(-3, 6, 2.5), A + p(2, 6, 2.5), (0, 0, R(-90))); hold(CARD, a, b, A + p(0, 6, -1))
    mira(A + p(0, -4, -2.5), A + p(0, 6, 0.5), a, 24, 16); mira(A + p(0, -3.5, -2.5), A + p(0, 6, 0.5), b, 24, 16)
def s_cadeia(a, b):      # a pirâmide desaba
    modo(a, 'claro'); limpa(a, b); ve(a, b, *BLOCOS); m = a + int((b - a) * 0.45)
    for i, bl in enumerate(BLOCOS):
        z = 0.45 + i * 0.95; kf(bl, a, (0, 0, z), (0, 0, 0)); kf(bl, m, (0, 0, z), (0, 0, 0))
        dx = (-1.8, 1.5, -0.6)[i]; kf(bl, m + 14, (dx, 0.2 * i, 0.45 + (0.25 if i else 0)), (0, R((35, -70, 110)[i]), R(10 * i)))
        kf(bl, b, (dx, 0.2 * i, 0.45 + (0.25 if i else 0)), (0, R((35, -70, 110)[i]), R(10 * i)))
    c = PIR.location
    mira(c + p(1.5, -7.5, 2.0), c + p(0, 0, 1.3), a, 30, 16); mira(c + p(1.2, -7.0, 1.8), c + p(0, 0, 1.0), b, 30, 16)
def s_final(a, b):       # volta ao enquadramento da abertura (loop)
    modo(a, 'azul'); limpa(a, b, (TUB, CARD)); tub(a, b, A + p(0, 5.5, 0), A + p(0, 3, 0), (0, 0, R(180))); hold(CARD, a, b, A + p(3, 8, 1.5))
    mira(A + p(1.2, -5.5, -0.8), A + p(0, 3.0, 0), a, 28, 11); mira(A + p(1.2, -5.5, -0.8), A + p(0, 1.5, 0), b, 28, 11)
# objetos que só aparecem quando a cena pede
for o in POROS + XIS + [FIGADO] + GOTAS + GOTAS2 + SANGUE + ANEIS + [CORACAO] + BLOCOS: VISIVEL.setdefault(o, set())

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
