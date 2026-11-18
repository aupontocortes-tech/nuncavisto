"""Cena 3D: orca, cada fato com a sua demonstração."""

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
# ================= orca =================
OG, ONOV, _ = importa('orca.glb')
ORCA = normaliza(OG, ONOV, 6.5, p(0, 99, 0))
VISIVEL = {}
mar(p(0, 0, 0), (0.05, 0.3, 0.55), fundo=-3.2, raios=6, raio_=14, livre=2.5)
def kfo(a, b, loc=(0, 0, 0), rot=(0, 0, 0), rot2=None):
    kf(ORCA, a, p(*loc), rot); kf(ORCA, b, p(*loc), rot2 or rot)
def ca(a, b, cam, alvo, lens=35, fstop=8):
    mira(cam, alvo, a, lens, fstop); mira(cam, alvo, b, lens, fstop)
def s_abre(a, b):
    modo(a, 'azul'); kfo(a, b, (0, 6, 0.4), (0, 0, 0), (0, -2, 0.4)); ca(a, b, p(2.5, -9, 1.2), p(0, 0, 0.3))
def s_boca(a, b):
    modo(a, 'azul'); kfo(a, b, (0, 0, 0), (0, 0, 0), (0, 0, 0)); ca(a, b, p(2.8, 3.5, 2.2), p(0, 2.8, 1.4), 50, 4)
def s_respira(a, b):
    modo(a, 'claro'); kfo(a, b, (0, 0, 0)); ca(a, b, p(-4, -2, 3.2), p(0, 1.2, 1.4), 40, 6)
def s_mergulho(a, b):
    modo(a, 'fundoA'); kfo(a, b, (0, 0, -3.0), (0, 0, 0), (0, 0, -0.5)); ca(a, b, p(6, -5, -1), p(0, 0, -2.6))
def s_peixe(a, b):
    modo(a, 'azul'); kfo(a, b, (0, 0, 0)); ca(a, b, p(3.5, -6, 0.5), p(0, 0, 0))
def s_cauda(a, b):
    modo(a, 'azul'); kfo(a, b, (0, 0, 0), (R(0), 0, 0), (R(18), 0, 0)); ca(a, b, p(-4, -5, 1.8), p(0, -3.1, 0.2), 50, 4)
def s_motor(a, b):
    modo(a, 'escuro'); kfo(a, b, (0, 0, 0)); ca(a, b, p(0, -4, 0), p(0, -3, 0), 60, 3)
def s_barbatana(a, b):
    modo(a, 'claro'); kfo(a, b, (0, 0, 0)); ca(a, b, p(3, -3, 3.8), p(0, 0, 1.6), 40, 6)
def s_tecido(a, b):
    modo(a, 'raiox'); kfo(a, b, (0, 0, 0)); ca(a, b, p(0.8, -3, 2.0), p(0, 0, 1.6), 55, 3)
def s_estabiliza(a, b):
    modo(a, 'azul'); kfo(a, b, (0, 0, 0), (0, 0, 0), (0, 0, R(12))); ca(a, b, p(-6, 3, 1.5), p(0, 0, 0))
def s_casaco(a, b):
    modo(a, 'lab'); kfo(a, b, (0, 0, 0)); ca(a, b, p(4, -6, 1.5), p(0, 0, 0))
def s_dentes(a, b):
    modo(a, 'lab'); kfo(a, b, (0, 0, 0)); ca(a, b, p(2, 3.5, 1.0), p(0, 2.8, 0.5), 55, 4)
def s_agarrar(a, b):
    modo(a, 'azul'); kfo(a, b, (0, 0, 0)); ca(a, b, p(-3, 4, 1.0), p(0, 2.5, 0.2), 45, 5)
def s_sobe(a, b):
    modo(a, 'claro'); kfo(a, b, (0, 0, 4.0), (0, 0, 0)); ca(a, b, p(4, -6, 2.5), p(0, 0, 4.0))
def s_final(a, b):
    modo(a, 'azul'); kfo(a, b, (0, 0, -0.5)); ca(a, b, p(7, -16, 0.8), p(0, -2, 0))

# ---------- cortes internos (aproximados; ajustar pela prévia) ----------
def osso_bola(loc, esc, m):
    return esf(p(*loc), esc, m, True, 32)
PULMAO_M = mat('pulmao', (0.9, 0.35, 0.45), 0.5, emis=((1.0, 0.4, 0.5), 2.2))
CORACAO_M = mat('coracao_o', (1.0, 0.15, 0.2), 0.4, emis=((1.0, 0.1, 0.15), 3.5))
MUSC_M = mat('mioglob', (1.0, 0.45, 0.1), 0.4, emis=((1.0, 0.4, 0.05), 3.0), alpha=0.85)
GORD_M = mat('gordura_c', (1.0, 0.92, 0.6), 0.6, emis=((1.0, 0.9, 0.5), 1.2), alpha=0.35)
ESPI_M = mat('espiraculo_o', (1.0, 0.85, 0.2), 0.4, emis=((1.0, 0.8, 0.1), 4))
TAMPA_M = mat('tampa_o', (1.0, 0.25, 0.2), 0.4, emis=((1.0, 0.2, 0.1), 3))
PULM = [esf(p(sx*0.45, 0.8, 0.25), (0.42, 1.3, 0.55), PULMAO_M, True, 24) for sx in (-1, 1)]
for o in PULM: o.parent = ORCA
CORA = esf(p(0, 0.2, -0.05), (0.32, 0.36, 0.3), CORACAO_M, True, 20); CORA.parent = ORCA
ESPI = cone(p(0, 2.7, 1.0), 0.16, 0.12, 0.25, ESPI_M, v=12); ESPI.parent = ORCA
TAMPA = caixa(p(0, 2.7, 1.2), (0.32, 0.05, 0.32), TAMPA_M); TAMPA.parent = ORCA
MUSC = esf(p(0, 0, 0), (1.05, 2.8, 0.85), MUSC_M, True, 32); MUSC.parent = ORCA
GORD = esf(p(0, 0, 0), (1.35, 3.1, 1.1), GORD_M, True, 32); GORD.parent = ORCA

ORGAOS = PULM + [CORA, ESPI, TAMPA, MUSC, GORD]
for o in ORGAOS: VISIVEL[o] = set()
CORPO = [o for o in ONOV if o.type == 'MESH']
INTERNO = []
def interno(a, b, *objs):
    INTERNO.append((a, b))
    for o in objs: mostra(o, a, b)
def kfinterna(a, b, *objs, mostra_=True):
    for o in objs: o.hide_render = False
def s_espiraculo(a, b):
    interno(a, b, ESPI, TAMPA); modo(a, 'claro'); kfo(a, b, (0, 0, 0)); ca(a, b, p(1.8, 1.5, 3.4), p(0, 2.5, 1.0), 60, 3)
    kf(TAMPA, a, p(0, 2.7, 1.2), (0, 0, 0)); kf(TAMPA, b, p(0, 2.7, 1.2), (0, 0, 0))
def s_pulmoes(a, b):
    interno(a, b, *PULM); modo(a, 'raiox'); kfo(a, b, (0, 0, 0), (0, 0, 0)); ca(a, b, p(0, -9, 1.0), p(0, 0.5, 0.3), 35, 8)
def s_tampa(a, b):
    interno(a, b, TAMPA, ESPI); modo(a, 'azul'); kfo(a, b, (0, 0, 0)); ca(a, b, p(2.5, 2.2, 3.0), p(0, 2.6, 1.0), 60, 3)
    kf(TAMPA, a, p(0, 2.7, 1.2), (R(-70), 0, 0)); kf(TAMPA, b, p(0, 2.7, 1.2), (0, 0, 0))
def s_coracao(a, b):
    interno(a, b, CORA, *PULM); modo(a, 'raiox'); kfo(a, b, (0, 0, 0)); ca(a, b, p(0, -8, 0.6), p(0, 0.2, 0.0), 35, 8)
    kf(CORA, a, p(0, 0.2, -0.05), (0, 0, 0), esc=(1, 1, 1)); kf(CORA, b, p(0, 0.2, -0.05), (0, 0, 0), esc=(1, 1, 1))
def s_mioglobina(a, b):
    modo(a, 'escuro'); kfo(a, b, (0, 0, 0)); ca(a, b, p(-3, -6, 1.2), p(0, 0, 0.1), 60, 3)
def s_gordura(a, b):
    modo(a, 'raiox'); kfo(a, b, (0, 0, 0)); ca(a, b, p(0, -9, 0.5), p(0, 0, 0), 35, 8)

# corpo some só nos cortes internos
_fora = set(range(0, 1800)) - {f for a, b in INTERNO for f in range(a, b + 1)}
for o in CORPO: VISIVEL[o] = _fora

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
