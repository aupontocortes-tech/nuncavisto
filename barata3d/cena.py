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
for k in range(-4, 5):
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
    antes = set(bpy.data.objects); bpy.ops.import_scene.gltf(filepath=os.path.join(AQUI, arq))
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
    tr = o.animation_data.nla_tracks.new(); st = tr.strips.new(a.name, 4, a); st.repeat = 400; st.scale = 0.35   # passo rápido
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
antes = set(bpy.data.objects); bpy.ops.import_scene.fbx(filepath=os.path.join(AQUI, 'horse_head.fbx'))
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

# ---------------- shots ----------------
CH = p(0.0, 0.05, 0)   # ponto da barata no chão
def s_intro(a, b):   # barata planando pelo ar, de frente pra câmera, no escuro
    usa(a, b); kluz(a, False)
    kf(REAL, a, p(0.1, 0.4, 1.2), (math.radians(-25), math.radians(20), math.radians(160)))
    kf(REAL, b, p(0.015, 0.06, 1.155), (math.radians(-30), math.radians(-15), math.radians(175)))
    hold(ANDA, a, b, LONGE, (0, 0, 0)); hold(CHI, a, b, p(0, -5, 3), (0, 0, 0))
    mira(p(0.02, -0.06, 1.17), p(0.1, 0.4, 1.2), a, 60, 12); mira(p(0.01, -0.05, 1.16), p(0.02, 0.1, 1.15), b, 60, 12)
def s_ralo(a, b):    # sobe pelo ralo
    usa(a, b); kluz(a, False)
    kf(REAL, a, RALO + p(0, 0, -0.03), (math.radians(-60), 0, math.radians(200)))
    kf(REAL, b, RALO + p(0.0, -0.02, 0.003), (0, 0, math.radians(200)))
    mira(RALO + p(0.06, -0.18, 0.06), RALO + p(0, 0, 0.005), a, 50, 10); mira(RALO + p(0.04, -0.14, 0.04), RALO + p(0, -0.02, 0.006), b, 50, 10)
def s_olho(a, b):
    usa(a, b); kluz(a, False); hold(REAL, a, b, CH, (0, 0, 0))
    cab = CH + p(0, -0.024, 0.007)
    mira(cab + p(0.07, -0.12, 0.05), cab, a, 60, 32); mira(cab + p(0.04, -0.08, 0.025), cab, b, 70, 32)
def s_antenas(a, b):
    usa(a, b); kluz(a, False); hold(REAL, a, b, CH, (0, 0, math.radians(15)))
    cab = CH + p(0, -0.03, 0.006)
    mira(cab + p(-0.11, -0.14, 0.06), cab, a, 50, 32); mira(cab + p(0.11, -0.14, 0.05), cab, b, 50, 32)
def s_luz(a, b):
    usa(a, b); kluz(a, False); kluz(a + 6, True); hold(REAL, a, b, CH, (0, 0, math.radians(15)))
    humano(a, b, p(-0.35, -0.75, 0), math.radians(-20), 'Interact')
    mira(CH + p(0.05, 0.25, 0.04), CH + p(-0.25, -0.6, 0.6), a, 22, 6); mira(CH + p(0.05, 0.24, 0.04), CH + p(-0.25, -0.6, 0.6), b, 22, 6)
def s_chinelo(a, b):  # câmera de baixo, chinelo gigante no alto
    usa(a, b); kluz(a, True); hold(REAL, a, b, CH, (0, 0, math.radians(15)))
    hold(CHI, a, b, p(0, -5, 3), (0, 0, 0))
    humano(a, b, CH + p(0.05, -0.38, 0), 0, 'Sword_Slash', 2.2)
    mira(CH + p(0.0, 0.1, 0.008), CH + p(0.03, -0.3, 0.75), a, 16, 6); mira(CH + p(0.0, 0.09, 0.008), CH + p(0.03, -0.3, 0.8), b, 16, 6)
def s_cercos(a, b):  # zoom na traseira
    usa(a, b); kluz(a, True); hold(REAL, a, b, CH, (0, 0, math.radians(15)))
    tr = CH + p(-0.009, 0.032, 0.006)
    mira(tr + p(0.1, 0.14, 0.06), tr, a, 50, 32); mira(tr + p(0.04, 0.07, 0.02), tr, b, 70, 32)
def s_fuga(a, b):     # chinelo descendo, ela vira e corre (modelo andando)
    usa(a, b, real=False, anda=True); kluz(a, True)
    m = a + int((b - a) * 0.35)
    hold(ANDA, a, m, CH, (0, 0, math.radians(15)))
    kf(ANDA, m + 6, CH + p(0.005, 0.0, 0), (0, 0, math.radians(120)))
    kf(ANDA, b, CH + p(0.25, -0.05, 0), (0, 0, math.radians(100)))
    kf(CHI, a, CH + p(0.0, -0.05, 0.35), (math.radians(-20), 0, 0)); kf(CHI, b, CH + p(0.0, 0.0, 0.06), (math.radians(-5), 0, 0))
    mira(CH + p(-0.12, -0.25, 0.1), CH + p(0.02, 0, 0.01), a, 40, 9); mira(CH + p(0.0, -0.3, 0.12), CH + p(0.15, -0.03, 0.01), b, 40, 9)
def s_erra(a, b):
    usa(a, b, real=False, anda=True); kluz(a, True)
    kf(CHI, a, CH + p(0.0, 0.0, 0.06), (math.radians(-5), 0, 0)); kf(CHI, a + 4, CH + p(0, 0, 0.013), (0, 0, 0)); kf(CHI, b, CH + p(0, 0, 0.013), (0, 0, 0))
    kf(ANDA, a, CH + p(0.3, -0.05, 0), (0, 0, math.radians(100))); kf(ANDA, b, CH + p(0.45, 0.1, 0), (0, 0, math.radians(130)))
    mira(CH + p(-0.2, -0.3, 0.08), CH + p(0.05, 0, 0.01), a, 30, 9); mira(CH + p(-0.19, -0.29, 0.08), CH + p(0.05, 0, 0.01), b, 30, 9)
INI_PIA = QUINA + p(-0.25, 0.15, 0)   # a corrida acontece em cima do tampo da pia
def s_corrida(a, b):
    usa(a, b, real=False, anda=True); kluz(a, True); hold(CHI, a, b, p(0, -5, 3), (0, 0, 0))
    kf(ANDA, a, INI_PIA, (0, 0, math.radians(90))); kf(ANDA, b, QUINA + p(-0.04, 0.03, 0), (0, 0, math.radians(90)))
    mira(INI_PIA + p(0.06, -0.12, 0.03), INI_PIA + p(0.02, 0, 0.01), a, 40, 9); mira(QUINA + p(0.02, -0.14, 0.035), QUINA + p(-0.04, 0.03, 0.01), b, 40, 9)
PIVO = bpy.data.objects.new('pivo', None); sc.collection.objects.link(PIVO); PIVO.location = QUINA
def s_pulo(a, b):
    usa(a, b, real=False, anda=True); kluz(a, True)
    m = a + int((b - a) * 0.75)
    kf(ANDA, a, QUINA + p(-0.04, 0.05, 0), (0, 0, math.radians(180))); kf(ANDA, m, QUINA + p(0, 0.0, 0), (0, 0, math.radians(180)))
    kf(ANDA, b, QUINA + p(0, -0.025, -0.01), (math.radians(-40), 0, math.radians(180)))
    mira(QUINA + p(0.15, -0.1, 0.02), QUINA + p(0, 0.02, 0.0), a, 45, 9); mira(QUINA + p(0.12, -0.08, -0.01), QUINA + p(0, -0.01, -0.005), b, 45, 9)
def pendulo(a, b, lento):
    usa(a, b, real=False, anda=True); kluz(a, True)
    # a barata gira 180° em volta da quina (eixo X), terminando de cabeça pra baixo embaixo do tampo
    for k in range(9):
        t = k / 8; f = a + int((b - a) * (0.15 + 0.7 * t)) if True else a
        ang = math.radians(-40 - 140 * (t * t * (3 - 2 * t)))
        r = 0.03
        pos = QUINA + p(0, -r * math.cos(ang + math.pi / 2) * 0 + -r * math.sin(-ang) * 0, 0)
        y = QUINA.y - r * math.sin(-ang); z = QUINA.z - 0.03 + r * math.cos(-ang) * 0.0 - r * (1 - math.cos(-ang)) * 0.5
        kf(ANDA, f, p(QUINA.x, y, z), (ang, 0, math.radians(180)))
    kf(ANDA, b, p(QUINA.x, QUINA.y + 0.04, QUINA.z - 0.03 - 0.008), (math.radians(-180), 0, math.radians(180)))
    if lento:
        mira(QUINA + p(0.25, -0.1, -0.03), QUINA + p(0, 0, -0.015), a, 55, 11); mira(QUINA + p(0.23, -0.1, -0.07), QUINA + p(0, 0.02, -0.03), b, 55, 11)
    else:
        mira(QUINA + p(0.22, -0.2, 0.02), QUINA + p(0, 0, -0.01), a, 45, 11); mira(QUINA + p(0.2, -0.2, -0.06), QUINA + p(0, 0.02, -0.03), b, 45, 11)
def s_pendulo(a, b): pendulo(a, b, False)
def s_pendulo2(a, b): pendulo(a, b, True)
EMBAIXO = p(QUINA.x, QUINA.y + 0.04, QUINA.z - 0.038)
def s_procura(a, b):  # chinelo/humano procurando em cima da pia; barata escondida embaixo
    usa(a, b, real=False, anda=True); kluz(a, True)
    hold(ANDA, a, b, EMBAIXO, (math.radians(-180), 0, math.radians(180)))
    hold(CHI, a, b, p(0, -5, 3), (0, 0, 0))
    humano(a, b, QUINA + p(0.05, -0.42, -GH - 0.03), 0, 'Idle_Sword')
    mira(EMBAIXO + p(0.08, -0.13, -0.07), EMBAIXO, a, 30, 9); mira(EMBAIXO + p(0.07, -0.12, -0.065), EMBAIXO, b, 30, 9)
def s_final(a, b):
    usa(a, b, real=False, anda=True); kluz(a, True); kluz(a + 30, False)
    hold(ANDA, a, b, EMBAIXO, (math.radians(-180), 0, math.radians(180))); hold(CHI, a, b, p(0, -5, 3), (0, 0, 0))
    mira(EMBAIXO + p(0.08, -0.12, -0.06), EMBAIXO + p(0, 0, -0.005), a, 60, 12); mira(EMBAIXO + p(0.03, -0.05, -0.02), EMBAIXO + p(0, 0, -0.005), b, 70, 14)

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
                k.interpolation = 'CONSTANT' if int(round(k.co.x)) in FIMS or fc.data_path in ('energy',) or 'default_value' in fc.data_path else 'BEZIER'

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
    if PREVIEW: print('DBG', f, 'anda', [round(v,3) for v in ANDA.matrix_world.translation], 'cam', [round(v,3) for v in CAM.matrix_world.translation], 'vis', [o.name for o in A_objs if o.type=='MESH' and not o.hide_render][:3])
    sc.render.filepath = os.path.join(OUT, f'{f:05d}.jpg'); bpy.ops.render.render(write_still=True)
print('ok', len(fr))
