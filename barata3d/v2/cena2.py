"""Cena 3D da barata (banheiro à noite) no Blender, por código. Versão LEVE (render rápido).
uso: python3 cena.py shots.json <ini> <fim> <saida> [preview f1,f2,...]
"""
import bpy, math, sys, json, os, random
from mathutils import Vector

AQUI = os.path.dirname(os.path.abspath(__file__))
args = sys.argv[1:]
SHOTS = json.load(open(args[0])); F0, F1 = int(args[1]), int(args[2]); OUT = args[3]
PREVIEW = len(args) > 4 and args[4] == 'preview'
FPS = SHOTS['fps']
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene; sc.render.fps = FPS
def p(x, y, z): return Vector((x, y, z))

# ---------------- materiais ----------------
def mat(nome, cor, rough=0.5, metal=0.0, emis=None):
    m = bpy.data.materials.new(nome); m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*cor, 1); b.inputs['Roughness'].default_value = rough; b.inputs['Metallic'].default_value = metal
    if emis: b.inputs['Emission Color'].default_value = (*emis[0], 1); b.inputs['Emission Strength'].default_value = emis[1]
    return m
def mat_azulejo(escala, c1, c2, rejunte, rough=0.12):
    m = bpy.data.materials.new('az'); m.use_nodes = True; nt = m.node_tree; b = nt.nodes['Principled BSDF']
    b.inputs['Roughness'].default_value = rough
    br = nt.nodes.new('ShaderNodeTexBrick'); br.inputs['Scale'].default_value = escala; br.offset = 0.0
    br.inputs['Color1'].default_value = (*c1, 1); br.inputs['Color2'].default_value = (*c2, 1); br.inputs['Mortar'].default_value = (*rejunte, 1)
    br.inputs['Mortar Size'].default_value = 0.012; br.inputs['Brick Width'].default_value = 0.5; br.inputs['Row Height'].default_value = 0.5
    tc = nt.nodes.new('ShaderNodeTexCoord'); nt.links.new(tc.outputs['Object'], br.inputs['Vector'])
    nt.links.new(br.outputs['Color'], b.inputs['Base Color'])
    bp = nt.nodes.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = 0.4; bp.invert = True
    nt.links.new(br.outputs['Fac'], bp.inputs['Height']); nt.links.new(bp.outputs['Normal'], b.inputs['Normal'])
    return m
def om(o, m): o.data.materials.clear(); o.data.materials.append(m)

# ---------------- banheiro ----------------
PISO = mat_azulejo(6, (0.82, 0.82, 0.8), (0.76, 0.77, 0.75), (0.35, 0.33, 0.3))
bpy.ops.mesh.primitive_plane_add(size=4, location=(0, 0, 0)); om(bpy.context.object, PISO)
PAREDE = mat_azulejo(4, (0.55, 0.68, 0.72), (0.5, 0.63, 0.68), (0.85, 0.85, 0.82), 0.08)
for loc, rot in (((0, 0.9, 1.2), (math.radians(90), 0, 0)), ((-1.0, 0, 1.2), (math.radians(90), 0, math.radians(90))), ((1.4, 0, 1.2), (math.radians(90), 0, math.radians(90))), ((0, -1.5, 1.2), (math.radians(90), 0, 0))):
    bpy.ops.mesh.primitive_plane_add(size=4, location=loc, rotation=rot); om(bpy.context.object, PAREDE)
bpy.ops.mesh.primitive_plane_add(size=4, location=(0, 0, 2.5), rotation=(math.pi, 0, 0)); om(bpy.context.object, mat('teto', (0.8, 0.8, 0.78), 0.9))
# ralo (grelha) no piso
RALO = p(-0.25, -0.15, 0)
bpy.ops.mesh.primitive_cylinder_add(radius=0.06, depth=0.004, location=RALO + p(0, 0, 0.0005), vertices=64); ral = bpy.context.object; om(ral, mat('ralo', (0.75, 0.75, 0.75), 0.25, 1.0))
bpy.ops.mesh.primitive_cylinder_add(radius=0.05, depth=0.006, location=RALO + p(0, 0, 0.0004), vertices=64); om(bpy.context.object, mat('buraco', (0.01, 0.01, 0.01), 0.9))
for k in (-4, -3, -2, 2, 3, 4):
    bpy.ops.mesh.primitive_cube_add(size=1, location=RALO + p(k * 0.011, 0, 0.0028)); g = bpy.context.object; g.scale = (0.0035, 0.1, 0.002); om(g, ral.data.materials[0])
# gabinete da pia (a "quina" da fuga)
GX, GY, GH = 0.35, 0.6, 0.82
bpy.ops.mesh.primitive_cube_add(size=1, location=(GX, GY, GH / 2)); gab = bpy.context.object; gab.scale = (0.8, 0.5, GH); om(gab, mat('gabinete', (0.92, 0.9, 0.86), 0.35))
bpy.ops.mesh.primitive_cube_add(size=1, location=(GX, GY - 0.03, GH + 0.015)); tampo = bpy.context.object; tampo.scale = (0.86, 0.58, 0.03); om(tampo, mat('marmore', (0.92, 0.92, 0.93), 0.15))
QUINA = p(GX, GY - 0.03 - 0.29, GH + 0.03)          # borda da frente do tampo (y menor)
bpy.ops.mesh.primitive_cylinder_add(radius=0.2, depth=0.12, location=(GX, GY, GH + 0.09), vertices=64); om(bpy.context.object, mat('cuba', (0.97, 0.97, 0.97), 0.1)); bpy.ops.object.shade_smooth()
bpy.ops.mesh.primitive_cylinder_add(radius=0.012, depth=0.18, location=(GX, GY + 0.2, GH + 0.12)); om(bpy.context.object, mat('torneira', (0.8, 0.8, 0.82), 0.1, 1.0))
# vaso e tapete (fundo)
bpy.ops.mesh.primitive_cylinder_add(radius=0.2, depth=0.4, location=(-0.6, 0.5, 0.2), vertices=48); om(bpy.context.object, mat('vaso', (0.95, 0.95, 0.95), 0.1)); bpy.ops.object.shade_smooth()
bpy.ops.mesh.primitive_plane_add(size=1, location=(0.0, -0.3, 0.002)); tp = bpy.context.object; tp.scale = (0.5, 0.3, 1); om(tp, mat('tapete', (0.2, 0.35, 0.6), 0.95))
# sabonete no chão perto da pia
bpy.ops.mesh.primitive_cube_add(size=1, location=(0.05, 0.2, 0.01)); sb = bpy.context.object; sb.scale = (0.07, 0.045, 0.02)
bv = sb.modifiers.new('b', 'BEVEL'); bv.width = 0.008; bv.segments = 4; om(sb, mat('sabonete', (0.95, 0.55, 0.7), 0.35))

# chinelo (sola azul)
def chinelo():
    bpy.ops.mesh.primitive_cylinder_add(radius=0.5, depth=0.025, vertices=64); o = bpy.context.object
    o.scale = (0.1, 0.27, 1); bpy.ops.object.transform_apply(scale=True)
    bv = o.modifiers.new('b', 'BEVEL'); bv.width = 0.008; bv.segments = 3
    o.data.materials.append(mat('chinelo', (0.08, 0.28, 0.85), 0.55)); bpy.ops.object.shade_smooth()
    bpy.ops.mesh.primitive_torus_add(major_radius=0.05, minor_radius=0.009, location=(0, 0.04, 0.02)); t = bpy.context.object
    t.scale = (1, 1.4, 1); t.rotation_euler = (math.radians(90), 0, 0); t.data.materials.append(mat('tira', (0.95, 0.95, 0.95), 0.4)); t.parent = o
    return o
CHI = chinelo(); CHI.location = (0, -5, 3)
CHI_MAO = chinelo(); CHI_MAO.scale = (0.9, 0.9, 0.9)

# ---------------- baratas ----------------
def importa(arq):
    antes = set(bpy.data.objects); bpy.ops.import_scene.gltf(filepath=os.path.join(AQUI, '..', arq))
    novos = [o for o in bpy.data.objects if o not in antes]
    raizes = [o for o in novos if o.parent is None]
    if len(raizes) == 1: return raizes[0], novos
    grupo = bpy.data.objects.new(arq + '_grupo', None); sc.collection.objects.link(grupo)
    for r in raizes: r.parent = grupo
    return grupo, novos
# realista (closes): normaliza ~8 cm de antena a antena, cabeça para -Y
R_raiz, R_objs = importa('barata.glb')
for o in R_objs:
    if o.name.startswith('Object_4') or o.name.startswith('Cube_0'): o.hide_render = True; o.hide_viewport = True
REAL = bpy.data.objects.new('Real', None); sc.collection.objects.link(REAL)
REALROT = bpy.data.objects.new('RealRot', None); sc.collection.objects.link(REALROT); REALROT.parent = REAL; REALROT.rotation_euler = (0, 0, math.radians(90))
R_raiz.parent = REALROT; R_raiz.scale = (0.0135,) * 3
bpy.context.view_layer.update()
def bbox(objs):
    dg = bpy.context.evaluated_depsgraph_get(); pts = []
    for o in objs:
        if o.type == 'MESH' and not o.hide_render:
            oe = o.evaluated_get(dg); me = oe.to_mesh(); vs = list(me.vertices); pts += [oe.matrix_world @ v.co for v in vs[::25]]
    return Vector([min(q[i] for q in pts) for i in range(3)]), Vector([max(q[i] for q in pts) for i in range(3)])
mn, mx = bbox(R_objs); REALROT.location = (-(mn.x + mx.x) / 2, -(mn.y + mx.y) / 2, -mn.z)
print('real bbox', [round(v, 4) for v in (mx - mn)])
# andando (corrida/pêndulo): já ~6 cm, cabeça -Y; animação em loop
A_raiz, A_objs = importa('barata_andando.glb')
for o in A_objs:
    if o.name.startswith('Icosphere'): o.hide_render = True; o.hide_viewport = True
ANDA = bpy.data.objects.new('Anda', None); sc.collection.objects.link(ANDA); A_raiz.parent = ANDA
VEL = {'v': 1.0}
ANIM = [(o, o.animation_data.action) for o in A_objs if o.animation_data and o.animation_data.action]
for o, a in ANIM:
    o.animation_data.action = None
    tr = o.animation_data.nla_tracks.new(); st = tr.strips.new(a.name, 4, a); st.repeat = 900; st.scale = 0.14   # passo rápido
bpy.context.view_layer.update()
mn, mx = bbox(A_objs); A_raiz.location = (-(mn.x + mx.x) / 2, -(mn.y + mx.y) / 2, -mn.z)
print('anda bbox', [round(v, 4) for v in (mx - mn)])
ESCONDE = {}   # frame -> {'real': bool, 'anda': bool}
CHI_MAO.parent = None
# humano (mascote cabeça de cavalo, de pijama)
H_raiz, H_objs = importa('humano.gltf')
HARM = bpy.data.objects['CharacterArmature']
for o in H_objs:
    if o.name.startswith('Icosphere') or o.name.startswith('Casual_Head'): o.hide_render = True; o.hide_viewport = True
antes = set(bpy.data.objects); bpy.ops.import_scene.fbx(filepath=os.path.join(AQUI, '..', 'horse_head.fbx'))
hh = [o for o in bpy.data.objects if o not in antes]; CAV = [o for o in hh if o.type == 'MESH'][0]; a2 = [o for o in hh if o.type == 'ARMATURE'][0]
a2.data.pose_position = 'REST'; HARM.data.pose_position = 'REST'; bpy.context.view_layer.update()
bpy.context.view_layer.objects.active = CAV; CAV.select_set(True)
for m in list(CAV.modifiers):
    if m.type == 'ARMATURE': bpy.ops.object.modifier_apply(modifier=m.name)
mw = CAV.matrix_world.copy(); CAV.parent = None; bpy.data.objects.remove(a2); bpy.context.view_layer.update()
CAV.parent = HARM; CAV.parent_type = 'BONE'; CAV.parent_bone = 'Head'; bpy.context.view_layer.update(); CAV.matrix_world = mw
HARM.data.pose_position = 'POSE'
for mm in CAV.data.materials:
    b = mm.node_tree.nodes.get('Principled BSDF')
    for l in list(mm.node_tree.links):
        if l.to_socket.name == 'Alpha': mm.node_tree.links.remove(l)
    if b: b.inputs['Alpha'].default_value = 1.0
for nome in ('Purple', 'LightBlue'):
    mm = bpy.data.materials.get(nome)
    if not mm: continue
    nt = mm.node_tree; b = nt.nodes['Principled BSDF']
    wv = nt.nodes.new('ShaderNodeTexWave'); wv.wave_type = 'BANDS'; wv.bands_direction = 'Z'; wv.inputs['Scale'].default_value = 7; wv.inputs['Distortion'].default_value = 0
    cr = nt.nodes.new('ShaderNodeValToRGB'); cr.color_ramp.interpolation = 'CONSTANT'; cr.color_ramp.elements[0].color = (0.35, 0.55, 0.9, 1); cr.color_ramp.elements[1].position = 0.5; cr.color_ramp.elements[1].color = (0.92, 0.94, 0.98, 1)
    tc = nt.nodes.new('ShaderNodeTexCoord'); nt.links.new(tc.outputs['Object'], wv.inputs['Vector']); nt.links.new(wv.outputs['Fac'], cr.inputs['Fac']); nt.links.new(cr.outputs['Color'], b.inputs['Base Color'])
HUM = bpy.data.objects.new('Humano', None); sc.collection.objects.link(HUM); H_raiz.parent = HUM
HARM.animation_data_create(); HARM.animation_data.action = None
HTRACK = HARM.animation_data.nla_tracks.new()
def acao(nome, a, b, vel=1.0):
    act = bpy.data.actions[nome]; ln = act.frame_range[1] - act.frame_range[0]
    tr = HARM.animation_data.nla_tracks.new()
    st = tr.strips.new(f'{nome}_{a}', a, act); st.scale = vel; st.repeat = max(1.0, (b - a) / (ln * vel)); st.extrapolation = 'NOTHING'
HUM_VIS = set()
CHI_MAO.parent = HARM; CHI_MAO.parent_type = 'BONE'; CHI_MAO.parent_bone = 'Wrist.R'
CHI_MAO.location = (0, 0.12, 0); CHI_MAO.rotation_euler = (math.radians(90), 0, 0)
def humano(a, b, loc, rotz, nome, vel=1.0):
    hold(HUM, a, b, loc, (0, 0, rotz)); acao(nome, a, b, vel)
    for f in range(a, b + 1): HUM_VIS.add(f)


# ---------------- luz ----------------
w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True
BG = w.node_tree.nodes['Background']; BG.inputs[0].default_value = (0.25, 0.32, 0.45, 1)
def luz(nome, tipo, e, loc, rot, tam=0.3, cor=(1, 1, 1)):
    L = bpy.data.lights.new(nome, tipo); L.energy = e; L.color = cor
    if tipo == 'AREA': L.size = tam
    o = bpy.data.objects.new(nome, L); sc.collection.objects.link(o); o.location = loc; o.rotation_euler = rot; return L
LAMP = luz('lampada', 'AREA', 60, (0.1, 0.0, 2.45), (0, 0, 0), 0.5, (1, 0.95, 0.85))
LUA = luz('lua', 'AREA', 8, (-0.9, -1.2, 1.6), (math.radians(60), 0, math.radians(-40)), 1.0, (0.55, 0.65, 1.0))
def kluz(f, ligada):
    LAMP.energy = 60 if ligada else 3; LAMP.keyframe_insert('energy', frame=f)
    BG.inputs[1].default_value = 0.35 if ligada else 0.12; BG.inputs[1].keyframe_insert('default_value', frame=f)

# ---------------- câmera ----------------
camd = bpy.data.cameras.new('cam'); CAM = bpy.data.objects.new('cam', camd); sc.collection.objects.link(CAM); sc.camera = CAM
camd.clip_start = 0.001; camd.dof.use_dof = True; camd.sensor_width = 36
FOCO = bpy.data.objects.new('foco', None); sc.collection.objects.link(FOCO); camd.dof.focus_object = FOCO
def mira(cl, alvo, f, lens=50, fstop=8):
    CAM.location = cl; CAM.rotation_euler = (Vector(alvo) - Vector(cl)).to_track_quat('-Z', 'Y').to_euler(); FOCO.location = alvo
    CAM.keyframe_insert('location', frame=f); CAM.keyframe_insert('rotation_euler', frame=f); FOCO.keyframe_insert('location', frame=f)
    camd.lens = lens; camd.keyframe_insert('lens', frame=f); camd.dof.aperture_fstop = fstop; camd.dof.keyframe_insert('aperture_fstop', frame=f)
def kf(o, f, loc=None, rot=None):
    if loc is not None: o.location = loc; o.keyframe_insert('location', frame=f)
    if rot is not None: o.rotation_euler = rot; o.keyframe_insert('rotation_euler', frame=f)
def hold(o, a, b, loc, rot): kf(o, a, loc, rot); kf(o, b, loc, rot)
def usa(a, b, real=True, anda=False):
    for f in range(a, b + 1): ESCONDE[f] = {'real': real, 'anda': anda}
LONGE = p(0, -5, -1)


# ---------------- shots v2 (um plano por frase, ângulos sempre diferentes) ----------------
def olhar(loc, alvo):
    d = Vector(alvo) - Vector(loc); return math.atan2(d.x, -d.y)
def fora(a, b):
    hold(CHI, a, b, p(0, -5, 3), (0, 0, 0))
def moverH(a, b, l0, l1, rotz, nome, vel=1.0):
    kf(HUM, a, l0, (0, 0, rotz)); kf(HUM, b, l1, (0, 0, rotz)); acao(nome, a, b, vel)
    for f in range(a, b + 1): HUM_VIS.add(f)

# corredor (fora do banheiro) para o humano correndo
CY = 6.0
bpy.ops.mesh.primitive_plane_add(size=1, location=(25, CY, 0)); cp = bpy.context.object; cp.scale = (60, 3, 1); om(cp, PISO)
bpy.ops.mesh.primitive_plane_add(size=1, location=(25, CY + 1.2, 1.3), rotation=(math.radians(90), 0, 0)); cw = bpy.context.object; cw.scale = (60, 2.6, 1); om(cw, PAREDE)
for k in range(0, 60, 4):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(k, CY + 1.15, 1.0)); q = bpy.context.object; q.scale = (0.9, 0.05, 2.0); om(q, mat('porta', (0.45, 0.3, 0.18), 0.5))
    luz(f'cor{k}', 'POINT', 120, (k + 2, CY, 2.3), (0, 0, 0))

CH = p(0.0, 0.05, 0)
H0 = p(-0.25, -0.75, 0)            # onde o humano fica no banheiro
ROSTO = H0 + p(0, 0, 1.72)
FACE_CH = olhar(H0, CH)
P_PIA = p(0.68, 0.28, 0.835)       # quina (meio da espessura do tampo, borda da frente)
TOPO_PIA = 0.85

def s_voo1(a, b):
    usa(a, b); kluz(a, False); fora(a, b)
    kf(REAL, a, p(0.15, 0.3, 1.25), (math.radians(-25), math.radians(25), math.radians(160)))
    kf(REAL, b, p(0.03, 0.1, 1.2), (math.radians(-35), math.radians(-20), math.radians(175)))
    mira(p(0.0, -0.08, 1.2), p(0.15, 0.3, 1.25), a, 55, 14); mira(p(0.0, -0.06, 1.2), p(0.03, 0.1, 1.2), b, 55, 14)
def s_voo2(a, b):   # humano inteiro, barata vindo na cara dele
    usa(a, b); kluz(a, True); fora(a, b)
    humano(a, b, H0, olhar(H0, p(0.3, 0.5, 0)), 'Idle')
    kf(REAL, a, p(0.4, 0.5, 1.5), (math.radians(-30), 0, math.radians(200))); kf(REAL, b, ROSTO + p(0.08, 0.25, -0.02), (math.radians(-20), math.radians(30), math.radians(210)))
    mira(H0 + p(1.25, -0.2, 1.1), H0 + p(0.25, 0.3, 1.05), a, 22, 11); mira(H0 + p(1.15, -0.25, 1.15), H0 + p(0.2, 0.25, 1.1), b, 22, 11)
def s_voo3(a, b):   # close da barata no ar, patas abertas, humano desfocado atrás
    usa(a, b); kluz(a, True); fora(a, b)
    humano(a, b, H0, olhar(H0, p(0.3, 0.5, 0)), 'Idle')
    c0 = ROSTO + p(0.1, 0.35, -0.05); c1 = ROSTO + p(0.07, 0.22, -0.03)
    kf(REAL, a, c0, (math.radians(-20), math.radians(40), math.radians(200))); kf(REAL, b, c1, (math.radians(10), math.radians(-35), math.radians(225)))
    mira(c0 + p(0.08, 0.12, 0.04), c0, a, 60, 6); mira(c1 + p(0.07, 0.11, 0.03), c1, b, 60, 6)
def s_voo4(a, b):   # humano leva susto
    usa(a, b); kluz(a, True); fora(a, b)
    humano(a, b, H0, olhar(H0, p(0.3, 0.5, 0)), 'HitRecieve', 1.6)
    kf(REAL, a, ROSTO + p(0.06, 0.15, 0), (0, math.radians(60), math.radians(230))); kf(REAL, b, ROSTO + p(0.0, -0.05, -0.6), (math.radians(90), math.radians(180), math.radians(300)))
    mira(H0 + p(0.35, 1.0, 1.55), ROSTO + p(0, 0, -0.1), a, 30, 11); mira(H0 + p(0.3, 0.95, 1.5), ROSTO + p(0, 0, -0.15), b, 30, 11)
def s_voce(a, b):   # barata no chão, câmera na altura dela
    usa(a, b); kluz(a, False); fora(a, b); hold(REAL, a, b, CH, (0, 0, 0))
    mira(CH + p(0.0, -0.16, 0.012), CH + p(0, 0, 0.008), a, 40, 14); mira(CH + p(0.0, -0.1, 0.01), CH + p(0, 0, 0.008), b, 45, 14)
def s_hora(a, b):   # banheiro escuro, de cima, do canto
    usa(a, b); kluz(a, False); fora(a, b); hold(REAL, a, b, RALO + p(0, 0, -0.05), (0, 0, 0))
    mira(p(1.25, -1.35, 2.2), p(-0.1, 0.0, 0.2), a, 16, 8); mira(p(1.2, -1.3, 2.15), p(-0.15, 0.0, 0.15), b, 16, 8)
def s_ralo1(a, b):  # antenas e cabeça saindo pela grade
    usa(a, b); kluz(a, False); fora(a, b)
    kf(REAL, a, RALO + p(0, 0.02, -0.035), (math.radians(-55), 0, 0)); kf(REAL, b, RALO + p(0, -0.005, -0.006), (math.radians(-28), 0, 0))
    mira(RALO + p(0.012, -0.075, 0.012), RALO + p(0, -0.005, 0.002), a, 42, 30); mira(RALO + p(0.01, -0.065, 0.01), RALO + p(0, -0.01, 0.004), b, 45, 30)
def s_ralo2(a, b):  # sai inteira
    usa(a, b); kluz(a, False); fora(a, b)
    kf(REAL, a, RALO + p(0, 0.0, -0.012), (math.radians(-35), 0, 0)); kf(REAL, b, RALO + p(0, -0.06, 0.0), (0, 0, 0))
    mira(RALO + p(0.09, -0.12, 0.05), RALO + p(0, -0.02, 0.0), a, 40, 14); mira(RALO + p(0.07, -0.16, 0.04), RALO + p(0, -0.05, 0.005), b, 40, 14)
def s_escuro(a, b):  # barata pequena no chão escuro, plano aberto baixo
    usa(a, b); kluz(a, False); fora(a, b); hold(REAL, a, b, RALO + p(0.05, -0.12, 0), (0, 0, math.radians(-30)))
    mira(RALO + p(0.2, -0.3, 0.05), RALO + p(0.05, -0.12, 0.01), a, 35, 10); mira(RALO + p(0.17, -0.27, 0.045), RALO + p(0.05, -0.12, 0.01), b, 35, 10)
def s_olho(a, b):
    usa(a, b); kluz(a, False); fora(a, b); hold(REAL, a, b, CH, (0, 0, 0))
    cab = CH + p(0, -0.024, 0.007)
    mira(cab + p(0.045, -0.06, 0.018), cab, a, 70, 32); mira(cab + p(0.025, -0.04, 0.01), cab, b, 85, 32)
def s_antenas(a, b):
    usa(a, b); kluz(a, False); fora(a, b); hold(REAL, a, b, CH, (0, 0, math.radians(15)))
    cab = CH + p(0, -0.03, 0.006)
    mira(cab + p(-0.11, -0.14, 0.06), cab, a, 50, 32); mira(cab + p(0.11, -0.14, 0.05), cab, b, 50, 32)
SAB = p(0.05, 0.2, 0.01)
def s_cheiro(a, b):  # antenas viradas pro sabonete, câmera de trás/cima
    usa(a, b); kluz(a, False); fora(a, b)
    kf(REAL, a, CH, (0, 0, math.radians(15))); kf(REAL, b, CH + p(0.01, 0.03, 0), (0, 0, olhar(CH, SAB)))
    mira(CH + p(-0.06, -0.12, 0.09), CH + p(0.02, 0.06, 0.0), a, 35, 14); mira(CH + p(-0.05, -0.1, 0.08), CH + p(0.03, 0.08, 0.0), b, 35, 14)
def s_luz(a, b):   # humano na porta acendendo a luz, visto do chão
    usa(a, b); kluz(a, False); kluz(a + 8, True); fora(a, b); hold(REAL, a, b, CH, (0, 0, math.radians(15)))
    humano(a, b, H0, FACE_CH, 'Interact')
    mira(CH + p(0.025, 0.075, 0.018), H0 + p(0, 0, 0.9), a, 18, 6); mira(CH + p(0.025, 0.07, 0.018), H0 + p(0, 0, 0.95), b, 18, 6)
def s_humano(a, b):  # contra-plongée: humano gigante, ponto de vista da barata
    usa(a, b); kluz(a, True); fora(a, b); hold(REAL, a, b, CH, (0, 0, math.radians(15)))
    humano(a, b, H0, FACE_CH, 'Idle')
    mira(CH + p(0.0, -0.03, 0.01), H0 + p(0, 0, 1.3), a, 14, 5); mira(CH + p(0.0, -0.035, 0.01), H0 + p(0, 0, 1.4), b, 14, 5)
def s_chinelo(a, b):  # humano inteiro de lado levantando o chinelo
    usa(a, b); kluz(a, True); fora(a, b); hold(REAL, a, b, CH, (0, 0, math.radians(15)))
    humano(a, b, H0, FACE_CH, 'Sword_Slash', 2.5)
    mira(H0 + p(1.3, 0.25, 1.0), H0 + p(0.15, 0.2, 1.0), a, 20, 11); mira(H0 + p(1.25, 0.2, 1.05), H0 + p(0.15, 0.2, 1.05), b, 20, 11)
def s_costas(a, b):  # barata de costas, humano desfocado ao fundo
    usa(a, b); kluz(a, True); fora(a, b); hold(REAL, a, b, CH, (0, 0, math.radians(15)))
    humano(a, b, H0, FACE_CH, 'Idle_Sword')
    mira(CH + p(0.04, 0.16, 0.035), CH + p(-0.03, -0.12, 0.04), a, 35, 9); mira(CH + p(0.035, 0.14, 0.03), CH + p(-0.03, -0.12, 0.04), b, 35, 9)
def s_cercos1(a, b):
    usa(a, b); kluz(a, True); fora(a, b); hold(REAL, a, b, CH, (0, 0, math.radians(15)))
    tr = CH + p(-0.009, 0.032, 0.006)
    mira(tr + p(0.1, 0.14, 0.06), tr, a, 50, 32); mira(tr + p(0.05, 0.08, 0.025), tr, b, 65, 32)
def s_cercos2(a, b):  # macro
    usa(a, b); kluz(a, True); fora(a, b); hold(REAL, a, b, CH, (0, 0, math.radians(15)))
    tr = CH + p(-0.009, 0.034, 0.005)
    mira(tr + p(-0.07, 0.1, 0.035), tr, a, 70, 36); mira(tr + p(-0.05, 0.08, 0.025), tr, b, 80, 36)
def s_vento(a, b):   # chinelo descendo por cima da barata
    usa(a, b); kluz(a, True); hold(REAL, a, b, CH, (0, 0, math.radians(15)))
    kf(CHI, a, CH + p(0.0, 0.0, 0.55), (math.radians(-15), 0, 0)); kf(CHI, b, CH + p(0.0, 0.0, 0.18), (math.radians(-8), 0, 0))
    mira(CH + p(0.2, -0.22, 0.05), CH + p(0, 0, 0.12), a, 24, 9); mira(CH + p(0.19, -0.21, 0.05), CH + p(0, 0, 0.1), b, 24, 9)
def s_sente(a, b):   # pelos do cerco, de trás
    usa(a, b); kluz(a, True); hold(REAL, a, b, CH, (0, 0, math.radians(15)))
    kf(CHI, a, CH + p(0.0, 0.0, 0.18), (math.radians(-8), 0, 0)); kf(CHI, b, CH + p(0.0, 0.0, 0.12), (math.radians(-6), 0, 0))
    tr = CH + p(-0.009, 0.034, 0.005)
    mira(tr + p(0.08, 0.1, 0.06), tr + p(0, -0.01, 0.01), a, 45, 22); mira(tr + p(0.07, 0.09, 0.055), tr + p(0, -0.01, 0.01), b, 45, 22)
def s_vira(a, b):    # gira e dispara (modelo andando)
    usa(a, b, real=False, anda=True); kluz(a, True)
    m = a + 8
    kf(ANDA, a, CH, (0, 0, math.radians(15))); kf(ANDA, m, CH + p(0.005, 0, 0), (0, 0, math.radians(110)))
    kf(ANDA, b, CH + p(0.32, -0.04, 0), (0, 0, math.radians(100)))
    kf(CHI, a, CH + p(0.0, 0.0, 0.12), (math.radians(-6), 0, 0)); kf(CHI, b, CH + p(0.0, 0.0, 0.03), (math.radians(-2), 0, 0))
    mira(CH + p(0.0, -0.25, 0.06), CH + p(0.03, 0, 0.01), a, 30, 9); mira(CH + p(0.15, -0.28, 0.06), CH + p(0.25, -0.03, 0.01), b, 30, 9)
def s_alarme(a, b):  # correndo, câmera acompanhando
    usa(a, b, real=False, anda=True); kluz(a, True); fora(a, b)
    s0 = CH + p(0.32, -0.04, 0); s1 = s0 + p(0.35, 0.05, 0)
    kf(ANDA, a, s0, (0, 0, math.radians(100))); kf(ANDA, b, s1, (0, 0, math.radians(95)))
    mira(s0 + p(0.06, -0.1, 0.03), s0 + p(0.02, 0, 0.01), a, 35, 12); mira(s1 + p(0.06, -0.1, 0.03), s1 + p(0.02, 0, 0.01), b, 35, 12)
def s_pa(a, b):      # chinelo bate onde ela estava
    usa(a, b, real=False, anda=True); kluz(a, True)
    kf(CHI, a, CH + p(0, 0, 0.12), (math.radians(-6), 0, 0)); kf(CHI, a + 3, CH + p(0, 0, 0.013), (0, 0, 0)); kf(CHI, b, CH + p(0, 0, 0.013), (0, 0, 0))
    hold(ANDA, a, b, CH + p(0.75, 0.05, 0), (0, 0, math.radians(95)))
    mira(CH + p(-0.2, -0.28, 0.08), CH + p(0.05, 0, 0.01), a, 26, 9); mira(CH + p(-0.19, -0.27, 0.08), CH + p(0.05, 0, 0.01), b, 26, 9)
def s_vazio(a, b):   # close no chinelo no chão, nada embaixo
    usa(a, b, real=False, anda=True); kluz(a, True); hold(CHI, a, b, CH + p(0, 0, 0.013), (0, 0, 0))
    hold(ANDA, a, b, CH + p(0.8, 0.05, 0), (0, 0, math.radians(95)))
    mira(CH + p(0.12, -0.18, 0.03), CH + p(0, 0, 0.01), a, 40, 12); mira(CH + p(0.1, -0.16, 0.025), CH + p(0, 0, 0.01), b, 40, 12)
def s_corre(a, b):   # corrida no chão, câmera baixa acompanhando (piso passa)
    usa(a, b, real=False, anda=True); kluz(a, True); fora(a, b)
    s0 = p(-0.7, -0.3, 0); s1 = p(0.6, -0.25, 0)
    kf(ANDA, a, s0, (0, 0, math.radians(92))); kf(ANDA, b, s1, (0, 0, math.radians(92)))
    mira(s0 + p(0.0, -0.12, 0.02), s0 + p(0.03, 0, 0.01), a, 30, 12); mira(s1 + p(0.0, -0.12, 0.02), s1 + p(0.03, 0, 0.01), b, 30, 12)
def s_cavalo_corre(a, b):  # humano correndo no corredor, câmera de lado
    usa(a, b, real=False, anda=False); kluz(a, False); fora(a, b)
    h0 = p(2, CY, 0); h1 = p(2 + 5.5 * (b - a) / FPS, CY, 0)
    moverH(a, b, h0, h1, math.radians(90), 'Run')
    mira(h0 + p(0.4, -2.2, 1.1), h0 + p(0.4, 0, 1.0), a, 24, 11); mira(h1 + p(0.4, -2.2, 1.1), h1 + p(0.4, 0, 1.0), b, 24, 11)
def s_velocidade(a, b):  # mais rápido, câmera de frente-lado
    usa(a, b, real=False, anda=False); kluz(a, False); fora(a, b)
    x0 = 2 + 5.5 * 2.0
    h0 = p(x0, CY, 0); h1 = p(x0 + 8 * (b - a) / FPS, CY, 0)
    moverH(a, b, h0, h1, math.radians(90), 'Run', 0.7)
    mira(h0 + p(2.4, -1.3, 0.6), h0 + p(0.3, 0, 1.1), a, 22, 9); mira(h1 + p(2.4, -1.3, 0.6), h1 + p(0.3, 0, 1.1), b, 22, 9)
PIA0 = p(0.68, 0.66, TOPO_PIA)
def s_pia(a, b):     # correndo no tampo em direção à borda
    usa(a, b, real=False, anda=True); kluz(a, True); fora(a, b)
    s1 = p(0.68, 0.36, TOPO_PIA)
    kf(ANDA, a, PIA0, (0, 0, math.radians(8))); kf(ANDA, b, s1, (0, 0, 0))
    mira(PIA0 + p(0.12, 0.12, 0.06), PIA0 + p(0, -0.08, 0.0), a, 30, 12); mira(s1 + p(0.12, 0.1, 0.05), P_PIA + p(0, -0.05, 0.0), b, 30, 12)
def s_nao_freia(a, b):  # de frente, na borda, câmera baixa no vazio
    usa(a, b, real=False, anda=True); kluz(a, True); fora(a, b)
    s0 = p(0.68, 0.36, TOPO_PIA); s1 = p(0.68, 0.30, TOPO_PIA)
    kf(ANDA, a, s0, (0, 0, 0)); kf(ANDA, b, s1, (0, 0, 0))
    mira(P_PIA + p(0.0, -0.12, -0.005), s0 + p(0, 0, 0.01), a, 45, 14); mira(P_PIA + p(0.0, -0.1, -0.003), s1 + p(0, 0, 0.01), b, 50, 14)
def giro(f0, f1, t0, t1, passo=2):
    """barata pendurada pelas patas de trás na quina, girando de t0 a t1 graus em volta do eixo X"""
    n = max(2, (f1 - f0) // passo)
    for k in range(n + 1):
        u = k / n; u = u * u * (3 - 2 * u); th = math.radians(t0 + (t1 - t0) * u)
        off = Vector((0, -0.035, 0.015)); r = mathutils.Matrix.Rotation(th, 3, 'X') @ off
        kf(ANDA, f0 + int(round((f1 - f0) * k / n)), P_PIA + r, (th, 0, 0))
import mathutils
def s_pula(a, b):    # o giro rápido (~1 s), plano aberto de lado
    usa(a, b, real=False, anda=True); kluz(a, True); fora(a, b)
    kf(ANDA, a, p(0.68, 0.30, TOPO_PIA), (0, 0, 0)); kf(ANDA, a + 3, P_PIA + Vector((0, -0.035, 0.015)), (0, 0, 0))
    giro(a + 3, min(b, a + 27), 0, 180, 1)
    if b > a + 27: kf(ANDA, b, P_PIA + mathutils.Matrix.Rotation(math.pi, 3, 'X') @ Vector((0, -0.035, 0.015)), (math.pi, 0, 0))
    mira(P_PIA + p(0.35, -0.12, -0.02), P_PIA + p(0, 0, -0.01), a, 40, 9); mira(P_PIA + p(0.34, -0.12, -0.02), P_PIA + p(0, 0, -0.01), b, 40, 9)
def s_garras(a, b):  # replay lento: close nas patas de trás agarrando a quina
    usa(a, b, real=False, anda=True); kluz(a, True); fora(a, b)
    giro(a, b, 0, 70, 3)
    mira(P_PIA + p(0.13, -0.11, 0.03), P_PIA + p(0, -0.01, 0.0), a, 50, 22); mira(P_PIA + p(0.12, -0.11, 0.01), P_PIA + p(0, -0.01, -0.005), b, 50, 22)
def s_pendulo(a, b):  # replay lento: o arco inteiro, de lado
    usa(a, b, real=False, anda=True); kluz(a, True); fora(a, b)
    giro(a, b, 40, 180, 3)
    mira(P_PIA + p(0.22, -0.02, -0.01), P_PIA + p(0, 0, -0.012), a, 55, 16); mira(P_PIA + p(0.21, 0.0, -0.03), P_PIA + p(0, 0.02, -0.02), b, 55, 16)
EMB = P_PIA + mathutils.Matrix.Rotation(math.pi, 3, 'X') @ Vector((0, -0.035, 0.015))
def s_ninja(a, b):   # de cabeça pra baixo embaixo do tampo
    usa(a, b, real=False, anda=True); kluz(a, True); fora(a, b)
    hold(ANDA, a, b, EMB, (math.pi, 0, 0))
    mira(EMB + p(0.06, -0.09, -0.06), EMB + p(0, 0, -0.008), a, 50, 18); mira(EMB + p(0.04, -0.07, -0.05), EMB + p(0, 0, -0.008), b, 55, 18)
def s_gravidade(a, b):  # o giro de novo, visto de frente/baixo
    usa(a, b, real=False, anda=True); kluz(a, True); fora(a, b)
    giro(a, a + int((b - a) * 0.7), 0, 180, 2); kf(ANDA, b, EMB, (math.pi, 0, 0))
    mira(P_PIA + p(0.02, -0.2, -0.08), P_PIA + p(0, 0, -0.01), a, 45, 14); mira(P_PIA + p(0.03, -0.19, -0.09), P_PIA + p(0, 0.01, -0.015), b, 45, 14)
def s_bungee(a, b):  # balançando pendurada
    usa(a, b, real=False, anda=True); kluz(a, True); fora(a, b)
    n = 6
    for k in range(n + 1):
        th = math.radians(180 - 18 * math.cos(k * math.pi / 2) * (1 - k / n))
        r = mathutils.Matrix.Rotation(th, 3, 'X') @ Vector((0, -0.035, 0.015)); kf(ANDA, a + (b - a) * k // n, P_PIA + r, (th, 0, 0))
    mira(P_PIA + p(0.16, 0.0, -0.04), P_PIA + p(0, 0.02, -0.02), a, 50, 16); mira(P_PIA + p(0.15, 0.01, -0.05), P_PIA + p(0, 0.02, -0.02), b, 50, 16)
HP = p(0.62, -0.25, 0)
def s_olha(a, b):    # humano olhando a pia, câmera embaixo do tampo (barata em primeiro plano)
    usa(a, b, real=False, anda=True); kluz(a, True); fora(a, b); hold(ANDA, a, b, EMB, (math.pi, 0, 0))
    humano(a, b, HP, olhar(HP, P_PIA), 'Idle_Sword')
    mira(EMB + p(0.05, -0.02, -0.03), HP + p(0, 0, 1.2), a, 22, 6); mira(EMB + p(0.05, -0.025, -0.03), HP + p(0, 0, 1.25), b, 22, 6)
def s_nada(a, b):    # close no cavalo procurando
    usa(a, b, real=False, anda=True); kluz(a, True); fora(a, b); hold(ANDA, a, b, EMB, (math.pi, 0, 0))
    humano(a, b, HP, olhar(HP, P_PIA) + math.radians(25), 'Interact')
    mira(HP + p(-0.3, 0.75, 1.75), HP + p(0, 0, 1.65), a, 30, 9); mira(HP + p(-0.28, 0.72, 1.74), HP + p(0, 0, 1.65), b, 30, 9)
def s_sumiu(a, b):   # escuro embaixo da pia, close
    usa(a, b, real=False, anda=True); kluz(a, True); fora(a, b); hold(ANDA, a, b, EMB, (math.pi, 0, 0))
    mira(EMB + p(-0.07, -0.06, -0.04), EMB + p(0, 0, -0.008), a, 55, 18); mira(EMB + p(-0.05, -0.05, -0.035), EMB + p(0, 0, -0.008), b, 60, 18)
def s_odeiam(a, b):  # humano indo embora
    usa(a, b, real=False, anda=True); kluz(a, True); fora(a, b); hold(ANDA, a, b, EMB, (math.pi, 0, 0))
    moverH(a, b, HP, HP + p(-0.6, -0.5, 0), olhar(HP, HP + p(-0.6, -0.5, 0)), 'Walk')
    mira(EMB + p(0.0, -0.03, -0.03), HP + p(-0.3, -0.3, 0.9), a, 20, 5); mira(EMB + p(0.0, -0.035, -0.03), HP + p(-0.5, -0.45, 0.9), b, 20, 5)
def s_antes(a, b):
    usa(a, b, real=False, anda=True); kluz(a, True); fora(a, b); hold(ANDA, a, b, EMB, (math.pi, 0, 0))
    mira(EMB + p(0.08, -0.12, -0.06), EMB + p(0, 0, -0.005), a, 60, 12); mira(EMB + p(0.05, -0.08, -0.03), EMB + p(0, 0, -0.005), b, 65, 14)
def s_final(a, b):
    usa(a, b, real=False, anda=True); kluz(a, True); kluz(b - 14, False); fora(a, b); hold(ANDA, a, b, EMB, (math.pi, 0, 0))
    mira(EMB + p(0.04, -0.06, -0.03), EMB + p(0, 0, -0.005), a, 70, 14); mira(EMB + p(0.03, -0.045, -0.02), EMB + p(0, 0, -0.005), b, 75, 14)

FUN = {k[2:]: v for k, v in globals().items() if k.startswith('s_')}
for s in SHOTS['shots']:
    # objetos fora de uso ficam longe
    FUN[s['id']](s['ini'], s['fim'])

def fcurves(ad):
    try: return ad.action.fcurves
    except AttributeError:
        from bpy_extras import anim_utils
        cb = anim_utils.action_get_channelbag_for_slot(ad.action, ad.action_slot); return cb.fcurves if cb else []
FIMS = {s['fim'] for s in SHOTS['shots']}
for o in (CAM, FOCO, REAL, ANDA, CHI, HUM, camd, camd.dof, LAMP, w.node_tree):
    ad = getattr(o, 'animation_data', None)
    if ad and ad.action:
        for fc in fcurves(ad):
            for k in fc.keyframe_points:
                k.interpolation = 'CONSTANT' if int(round(k.co.x)) in FIMS or fc.data_path in ('energy',) or 'default_value' in fc.data_path else 'LINEAR'

def visibilidade(f):
    e = ESCONDE.get(f, {'real': True, 'anda': False})
    for o in R_objs:
        if o.type == 'MESH' and not (o.name.startswith('Object_4') or o.name.startswith('Cube_0')): o.hide_render = not e['real']
    for o in A_objs:
        if o.type == 'MESH' and not o.name.startswith('Icosphere'): o.hide_render = not e['anda']
    v = f in HUM_VIS
    for o in H_objs + [CAV, CHI_MAO] + list(CHI_MAO.children):
        if o.type == 'MESH' and not (o.name.startswith('Icosphere') or o.name.startswith('Casual_Head')): o.hide_render = not v

# ---------------- render (leve) ----------------
sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'
sc.cycles.samples = 6 if PREVIEW else 16; sc.cycles.use_denoising = True
sc.cycles.max_bounces = 3; sc.cycles.diffuse_bounces = 2; sc.cycles.glossy_bounces = 2; sc.cycles.transmission_bounces = 2
sc.cycles.use_adaptive_sampling = True; sc.cycles.adaptive_threshold = 0.05
sc.render.resolution_x = 360 if PREVIEW else 720; sc.render.resolution_y = 640 if PREVIEW else 1280
sc.render.image_settings.file_format = 'JPEG'; sc.render.image_settings.quality = 92
sc.view_settings.view_transform = 'AgX'; sc.view_settings.look = 'AgX - Punchy'
os.makedirs(OUT, exist_ok=True)
fr = list(range(F0, F1 + 1)) if not PREVIEW else [int(x) for x in args[5].split(',')]
for f in fr:
    sc.frame_set(f); visibilidade(f)
    pass
    sc.render.filepath = os.path.join(OUT, f'{f:05d}.jpg'); bpy.ops.render.render(write_still=True)
print('ok', len(fr))
