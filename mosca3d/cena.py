"""Monta a cena 3D da mosca no Blender (por código) e renderiza um trecho.
uso: python3 cena.py <shots.json> <frame_ini> <frame_fim> <pasta_saida> [preview]
shots.json: {"fps":24,"shots":[{"id":"intro","ini":0,"fim":120}, ...]}
"""
import bpy, math, sys, json, os, random
from mathutils import Vector, Euler

AQUI = os.path.dirname(os.path.abspath(__file__))
args = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:]
SHOTS = json.load(open(args[0])); F0, F1 = int(args[1]), int(args[2]); OUT = args[3]
PREVIEW = len(args) > 4 and args[4] == 'preview'
FPS = SHOTS['fps']
S = 0.09            # escala da mosca (fica com ~7 mm, tamanho real)

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.fps = FPS

# ---------------- materiais ----------------
def mat(nome, cor, rough=0.5, metal=0.0, sss=0.0, transm=0.0, emis=None, alpha=1.0):
    m = bpy.data.materials.new(nome); m.use_nodes = True
    p = m.node_tree.nodes['Principled BSDF']
    p.inputs['Base Color'].default_value = (*cor, 1); p.inputs['Roughness'].default_value = rough
    p.inputs['Metallic'].default_value = metal
    if transm: p.inputs['Transmission Weight'].default_value = transm
    if sss: p.inputs['Subsurface Weight'].default_value = sss
    if emis: p.inputs['Emission Color'].default_value = (*emis[0], 1); p.inputs['Emission Strength'].default_value = emis[1]
    if alpha < 1: p.inputs['Alpha'].default_value = alpha
    return m

def mat_madeira():
    m = bpy.data.materials.new('madeira'); m.use_nodes = True; nt = m.node_tree
    p = nt.nodes['Principled BSDF']; p.inputs['Roughness'].default_value = 0.5
    tc = nt.nodes.new('ShaderNodeTexCoord'); mp = nt.nodes.new('ShaderNodeMapping'); mp.inputs['Scale'].default_value = (60, 3, 3)
    nz = nt.nodes.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 6; nz.inputs['Detail'].default_value = 10; nz.inputs['Distortion'].default_value = 0.4
    cr = nt.nodes.new('ShaderNodeValToRGB'); cr.color_ramp.elements[0].color = (0.30, 0.15, 0.07, 1); cr.color_ramp.elements[1].color = (0.55, 0.32, 0.16, 1)
    bp = nt.nodes.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = 0.15
    nt.links.new(tc.outputs['Object'], mp.inputs['Vector']); nt.links.new(mp.outputs['Vector'], nz.inputs['Vector'])
    nt.links.new(nz.outputs['Fac'], cr.inputs['Fac']); nt.links.new(cr.outputs['Color'], p.inputs['Base Color'])
    nt.links.new(nz.outputs['Fac'], bp.inputs['Height']); nt.links.new(bp.outputs['Normal'], p.inputs['Normal'])
    return m

def mat_bolo():
    m = bpy.data.materials.new('massa'); m.use_nodes = True; nt = m.node_tree
    p = nt.nodes['Principled BSDF']; p.inputs['Roughness'].default_value = 0.9
    nz = nt.nodes.new('ShaderNodeTexVoronoi'); nz.inputs['Scale'].default_value = 900
    cr = nt.nodes.new('ShaderNodeValToRGB'); cr.color_ramp.elements[0].color = (0.62, 0.36, 0.1, 1); cr.color_ramp.elements[1].color = (0.95, 0.72, 0.35, 1)
    bp = nt.nodes.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = 0.6
    nt.links.new(nz.outputs['Distance'], cr.inputs['Fac']); nt.links.new(cr.outputs['Color'], p.inputs['Base Color'])
    nt.links.new(nz.outputs['Distance'], bp.inputs['Height']); nt.links.new(bp.outputs['Normal'], p.inputs['Normal'])
    return m

def mat_azulejo():
    m = bpy.data.materials.new('azulejo'); m.use_nodes = True; nt = m.node_tree
    p = nt.nodes['Principled BSDF']; p.inputs['Roughness'].default_value = 0.15
    br = nt.nodes.new('ShaderNodeTexBrick'); br.inputs['Scale'].default_value = 7
    br.inputs['Color1'].default_value = (0.86, 0.88, 0.9, 1); br.inputs['Color2'].default_value = (0.8, 0.83, 0.86, 1)
    br.inputs['Mortar'].default_value = (0.55, 0.55, 0.55, 1); br.offset = 0.0; br.inputs['Mortar Size'].default_value = 0.01
    tc = nt.nodes.new('ShaderNodeTexCoord'); nt.links.new(tc.outputs['Object'], br.inputs['Vector'])
    nt.links.new(br.outputs['Color'], p.inputs['Base Color'])
    return m

def mat_teto():
    m = bpy.data.materials.new('teto'); m.use_nodes = True; nt = m.node_tree
    p = nt.nodes['Principled BSDF']; p.inputs['Base Color'].default_value = (0.72, 0.71, 0.68, 1); p.inputs['Roughness'].default_value = 0.95
    nz = nt.nodes.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 4000; nz.inputs['Detail'].default_value = 8
    bp = nt.nodes.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = 0.4
    nt.links.new(nz.outputs['Fac'], bp.inputs['Height']); nt.links.new(bp.outputs['Normal'], p.inputs['Normal'])
    return m

def obj_mat(o, m):
    o.data.materials.clear(); o.data.materials.append(m)

# ---------------- mosca ----------------
bpy.ops.import_scene.gltf(filepath=os.path.join(AQUI, 'fly.glb'))
bpy.data.objects['Icosphere'].hide_render = True; bpy.data.objects['Icosphere'].hide_viewport = True
RAIZ = bpy.data.objects['Sketchfab_model']
ARM = bpy.data.objects['Object_4']
RAIZ.scale = (S, S, S)
mosca = bpy.data.objects.new('Mosca', None); sc.collection.objects.link(mosca)
RAIZ.parent = mosca
bpy.context.view_layer.update()
# centraliza: pés no chão (z=0), centro em x/y
pts = [o.matrix_world @ Vector(c) for o in bpy.data.objects if o.name in ('Object_59', 'Object_60') for c in o.bound_box]
mn = Vector([min(p[i] for p in pts) for i in range(3)]); mx = Vector([max(p[i] for p in pts) for i in range(3)])
RAIZ.location = (-(mn.x + mx.x) / 2, -(mn.y + mx.y) / 2, -mn.z)
TAM = (mx - mn)
print('mosca tamanho (m):', [round(v, 4) for v in TAM])
for o in ('Object_59', 'Object_60'):
    bpy.data.objects[o].data.materials[0].node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value = 0.35

PB = ARM.pose.bones
ASAS = ['Bone.006_08', 'Bone.010_012']
PERNAS = ['Bone.014_016', 'Bone.018_020', 'Bone.022_032', 'Bone.026_036', 'Bone.030_026', 'Bone.034_029']
for b in PB: b.rotation_mode = 'XYZ'

# ---------------- cenário: cozinha ----------------
MESA_Z = 0.0
bpy.ops.mesh.primitive_plane_add(size=3, location=(0, 0, MESA_Z)); mesa = bpy.context.object; obj_mat(mesa, mat_madeira())
# prato e bolo (atrás da mosca)
PX, PY = 0.07, 0.13
bpy.ops.mesh.primitive_cylinder_add(radius=0.11, depth=0.012, location=(PX, PY, 0.006), vertices=96); prato = bpy.context.object
obj_mat(prato, mat('loucaprato', (0.95, 0.95, 0.94), 0.12)); bpy.ops.object.shade_smooth()
import bmesh
def cunha(nome, r, h, ang, loc, rotz):
    me = bpy.data.meshes.new(nome); bm = bmesh.new()
    a0, a1 = -ang / 2, ang / 2; n = 32
    pts = [(0, 0)] + [(r * math.cos(a0 + (a1 - a0) * i / n), r * math.sin(a0 + (a1 - a0) * i / n)) for i in range(n + 1)]
    vb = [bm.verts.new((x, y, 0)) for x, y in pts]; vt = [bm.verts.new((x, y, h)) for x, y in pts]
    bm.faces.new(vb[::-1]); bm.faces.new(vt)
    for i in range(len(pts)):
        j = (i + 1) % len(pts); bm.faces.new((vb[i], vb[j], vt[j], vt[i]))
    bm.to_mesh(me); bm.free(); o = bpy.data.objects.new(nome, me); sc.collection.objects.link(o)
    o.location = loc; o.rotation_euler = (0, 0, rotz)
    bv = o.modifiers.new('b', 'BEVEL'); bv.width = 0.0012; bv.segments = 3
    return o
BX, BY, ROTB = PX - 0.03, PY - 0.07, math.radians(90)     # ponta do bolo apontando pra frente (-Y)
camadas = [(0.012, 0.018, mat_bolo()), (0.030, 0.004, mat('creme', (0.97, 0.94, 0.86), 0.5, sss=0.2)),
           (0.034, 0.018, mat_bolo()), (0.052, 0.007, mat('choco', (0.14, 0.06, 0.025), 0.22))]
for k, (z0, h, mm) in enumerate(camadas):
    o = cunha(f'bolo{k}', 0.09 + (0.001 if k == 3 else 0), h, math.radians(40 if k < 3 else 41), (BX, BY, z0), ROTB); obj_mat(o, mm)
TOPO = 0.059
# parede de azulejo e janela
bpy.ops.mesh.primitive_plane_add(size=4, location=(0, 0.6, 1.0), rotation=(math.radians(90), 0, 0)); parede = bpy.context.object; obj_mat(parede, mat_azulejo())
bpy.ops.mesh.primitive_plane_add(size=0.7, location=(-0.4, 0.59, 0.55), rotation=(math.radians(90), 0, 0)); jan = bpy.context.object
obj_mat(jan, mat('janela', (1, 1, 1), emis=((1.0, 0.92, 0.78), 6)))
# sala (paredes em volta, pra nunca aparecer fundo cinza)
AZ = parede.data.materials[0]
for loc, rot in (((0, -1.2, 1.0), (math.radians(90), 0, 0)), ((1.4, 0, 1.0), (math.radians(90), 0, math.radians(90))), ((-1.4, 0, 1.0), (math.radians(90), 0, math.radians(90)))):
    bpy.ops.mesh.primitive_plane_add(size=4, location=loc, rotation=rot); obj_mat(bpy.context.object, AZ)
# armário alto no fundo e farelos
bpy.ops.mesh.primitive_cube_add(size=1, location=(0.55, 0.45, 0.6)); ar = bpy.context.object; ar.scale = (0.5, 0.25, 1.2); obj_mat(ar, mat('armario', (0.75, 0.55, 0.32), 0.4))
random.seed(3)
FAR = mat_bolo()
for i in range(40):
    r = random.uniform(0.0008, 0.0025); a = random.uniform(0, 6.28); d = random.uniform(0.02, 0.09)
    bpy.ops.mesh.primitive_ico_sphere_add(radius=r, subdivisions=1, location=(PX + d * math.cos(a), PY + d * math.sin(a), 0.012 + r * 0.6))
    obj_mat(bpy.context.object, FAR)
# xícara e garrafa (fundo desfocado)
bpy.ops.mesh.primitive_cylinder_add(radius=0.04, depth=0.09, location=(-0.22, 0.3, 0.045), vertices=64); obj_mat(bpy.context.object, mat('xic', (0.75, 0.15, 0.12), 0.2)); bpy.ops.object.shade_smooth()
bpy.ops.mesh.primitive_cylinder_add(radius=0.035, depth=0.28, location=(0.3, 0.42, 0.14), vertices=64); obj_mat(bpy.context.object, mat('garrafa', (0.2, 0.45, 0.25), 0.05, transm=0.8)); bpy.ops.object.shade_smooth()
# teto (bem acima, 1,4 m)
TETO_Z = 1.4
bpy.ops.mesh.primitive_plane_add(size=6, location=(0, 0, TETO_Z)); teto = bpy.context.object; obj_mat(teto, mat_teto())
teto.rotation_euler = (math.radians(180), 0, 0)
bpy.ops.mesh.primitive_cylinder_add(radius=0.12, depth=0.05, location=(0.5, 0.3, TETO_Z - 0.03)); obj_mat(bpy.context.object, mat('lamp', (1, 1, 1), emis=((1, 0.95, 0.85), 15)))

# chinelo (sola azul arredondada)
def chinelo():
    bpy.ops.mesh.primitive_cylinder_add(radius=0.5, depth=0.025, vertices=64); o = bpy.context.object
    o.scale = (0.1, 0.26, 1); bpy.ops.object.transform_apply(scale=True)
    bev = o.modifiers.new('b', 'BEVEL'); bev.width = 0.008; bev.segments = 4
    o.data.materials.append(mat('chinelo', (0.1, 0.3, 0.85), 0.55)); bpy.ops.object.shade_smooth()
    bpy.ops.mesh.primitive_torus_add(major_radius=0.05, minor_radius=0.008, location=(0, 0.04, 0.02)); t = bpy.context.object
    t.scale = (1, 1.4, 1); t.rotation_euler = (math.radians(90), 0, 0); t.data.materials.append(mat('tira', (0.95, 0.95, 0.95), 0.4)); t.parent = o
    return o
CHI = chinelo(); CHI.location = (0, -2, 3)

# gota de suco digestivo
bpy.ops.mesh.primitive_uv_sphere_add(radius=1, segments=48, ring_count=24); GOTA = bpy.context.object
obj_mat(GOTA, mat('gota', (0.9, 0.8, 0.45), 0.02, transm=0.85)); bpy.ops.object.shade_smooth(); GOTA.scale = (0, 0, 0)

# ---------------- luz e mundo ----------------
w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True
w.node_tree.nodes['Background'].inputs[0].default_value = (0.55, 0.62, 0.75, 1); w.node_tree.nodes['Background'].inputs[1].default_value = 0.35
def luz(nome, tipo, energia, loc, rot, tam=0.3, cor=(1, 1, 1)):
    L = bpy.data.lights.new(nome, tipo); L.energy = energia; L.color = cor
    if tipo == 'AREA': L.size = tam
    o = bpy.data.objects.new(nome, L); sc.collection.objects.link(o); o.location = loc; o.rotation_euler = rot; return o
SOL = luz('chave', 'AREA', 40, (-0.5, 0.5, 0.9), (math.radians(-35), math.radians(-30), 0), 0.8, (1, 0.94, 0.85))
luz('preench', 'AREA', 15, (0.6, -0.6, 0.5), (math.radians(50), math.radians(40), 0), 1.0, (0.8, 0.88, 1))
luz('teto_l', 'AREA', 20, (0.5, 0.3, TETO_Z - 0.06), (0, 0, 0), 0.25, (1, 0.95, 0.85))

# ---------------- câmera ----------------
camd = bpy.data.cameras.new('cam'); CAM = bpy.data.objects.new('cam', camd); sc.collection.objects.link(CAM); sc.camera = CAM
camd.lens = 60; camd.clip_start = 0.0005; camd.dof.use_dof = True; camd.dof.aperture_fstop = 4.0; camd.sensor_width = 36
FOCO = bpy.data.objects.new('foco', None); sc.collection.objects.link(FOCO); camd.dof.focus_object = FOCO

def mira(cam_loc, alvo, f, lens=None, fstop=None):
    CAM.location = cam_loc; d = Vector(alvo) - Vector(cam_loc)
    CAM.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
    FOCO.location = alvo
    CAM.keyframe_insert('location', frame=f); CAM.keyframe_insert('rotation_euler', frame=f); FOCO.keyframe_insert('location', frame=f)
    if lens: camd.lens = lens; camd.keyframe_insert('lens', frame=f)
    if fstop: camd.dof.aperture_fstop = fstop; camd.dof.keyframe_insert('aperture_fstop', frame=f)

def hold(o, a, b, loc, rot):
    kf(o, a, loc=loc, rot=rot); kf(o, b, loc=loc, rot=rot)
def kf(o, f, loc=None, rot=None, esc=None):
    if loc is not None: o.location = loc; o.keyframe_insert('location', frame=f)
    if rot is not None: o.rotation_euler = rot; o.keyframe_insert('rotation_euler', frame=f)
    if esc is not None: o.scale = esc; o.keyframe_insert('scale', frame=f)

# ---------------- animação por shot ----------------
H = TAM.z  # altura da mosca
CABECA = Vector((0, -TAM.y * 0.42, H * 0.55))  # frente da mosca = -Y
def p(x, y, z): return Vector((x, y, z))
ESTADO = {}   # frame -> dict(asas=bool, andar=bool)

def shot_intro(a, b):
    hold(mosca, a, b, (0, 0, 0), (0, 0, 0))
    for f, ang in ((a, -40), (b, 10)):
        r = 0.026; t = math.radians(ang - 90)
        mira(p(r * math.cos(t), r * math.sin(t), 0.007), p(0, 0, H * 0.5), f, 60, 32)
def shot_olho(a, b):
    hold(mosca, a, b, (0, 0, 0), (0, 0, 0))
    mira(CABECA + p(0.004, -0.03, 0.006), CABECA, a, 90, 16)
    mira(CABECA + p(0.002, -0.017, 0.003), CABECA, b, 90, 16)
def shot_cozinha(a, b):
    m = a + int((b - a) * 0.45)
    kf(mosca, a, loc=(0.03, 0.0, 0.09), rot=(0, 0, math.radians(30)))
    kf(mosca, m, loc=(0.0, 0.0, 0.0), rot=(0, 0, 0))
    kf(mosca, b, loc=(0.0, 0.0, 0.0), rot=(0, 0, 0))
    for f in range(a, m): ESTADO.setdefault(f, {})['asas'] = True
    mira(p(-0.04, -0.13, 0.05), p(0.02, 0.03, 0.012), a, 40, 32)
    mira(p(-0.03, -0.1, 0.035), p(0.01, 0.01, 0.006), b, 45, 32)
# a mosca anda em cima do bolo (topo da cobertura z=0.063)
NOBOLO = p(BX, BY + 0.035, TOPO)
def shot_pes(a, b):
    rz = math.radians(25); fr = p(math.sin(rz), -math.cos(rz), 0); ld = p(math.cos(rz), math.sin(rz), 0)
    kf(mosca, a, loc=NOBOLO + fr * 0.012, rot=(0, 0, math.radians(25) + math.pi)); kf(mosca, b, loc=NOBOLO, rot=(0, 0, math.radians(25) + math.pi))
    for f in range(a, b): ESTADO.setdefault(f, {})['andar'] = True
    mira(NOBOLO + fr * 0.012 + ld * 0.03 + p(0, 0, 0.004), NOBOLO + fr * 0.010 + p(0, 0, 0.0018), a, 80, 28)
    mira(NOBOLO + fr * 0.002 + ld * 0.026 + p(0, 0, 0.0035), NOBOLO + p(0, 0, 0.0018), b, 80, 28)
def shot_boca(a, b):
    kf(mosca, a, loc=NOBOLO, rot=(math.radians(-6), 0, math.radians(25)))
    kf(mosca, b, loc=NOBOLO, rot=(math.radians(-6), 0, math.radians(25)))
    rz = math.radians(25); frente = p(math.sin(rz) * TAM.y * 0.5, -math.cos(rz) * TAM.y * 0.5, 0)
    g = NOBOLO + frente + p(0, 0, 0.0004); m = a + int((b - a) * 0.5)
    kf(GOTA, a, loc=g, esc=(0, 0, 0)); kf(GOTA, a + int((b - a) * 0.3), loc=g, esc=(0.0014, 0.0014, 0.0009))
    kf(GOTA, m, loc=g, esc=(0.0014, 0.0014, 0.0009)); kf(GOTA, b - 10, loc=g, esc=(0, 0, 0))
    kf(GOTA, a - 1, esc=(0, 0, 0)); kf(GOTA, b + 1, esc=(0, 0, 0))
    fr = p(math.sin(rz), -math.cos(rz), 0)
    mira(g + fr * 0.022 + p(0.004, 0, 0.004), g - fr * 0.002 + p(0, 0, 0.0018), a, 100, 28)
    mira(g + fr * 0.016 + p(0.003, 0, 0.003), g - fr * 0.002 + p(0, 0, 0.0018), b, 100, 28)
def shot_chinelo(a, b):
    hold(mosca, a, b, NOBOLO, (0, 0, math.radians(25)))
    rz = math.radians(25); fr = p(math.sin(rz), -math.cos(rz), 0); tr = -fr
    kf(CHI, a - 1, loc=(0, -2, 3)); kf(CHI, a, loc=NOBOLO + tr * 0.09 + p(0, 0, 0.32), rot=(math.radians(-35), 0, rz))
    kf(CHI, b, loc=NOBOLO + tr * 0.06 + p(0, 0, 0.16), rot=(math.radians(-25), 0, rz))
    mira(NOBOLO + fr * 0.03 + p(0, 0, 0.002), NOBOLO + tr * 0.01 + p(0, 0, 0.012), a, 28, 20)
    mira(NOBOLO + fr * 0.026 + p(0, 0, 0.002), NOBOLO + tr * 0.01 + p(0, 0, 0.012), b, 28, 20)
def shot_radar(a, b):
    hold(mosca, a, b, NOBOLO, (0, 0, math.radians(25)))
    rz = math.radians(25); tr = p(-math.sin(rz), math.cos(rz), 0)
    kf(CHI, a, loc=NOBOLO + tr * 0.06 + p(0, 0, 0.16), rot=(math.radians(-25), 0, rz))
    kf(CHI, b, loc=NOBOLO + tr * 0.045 + p(0, 0, 0.11), rot=(math.radians(-20), 0, rz))
    for f, ang in ((a, 0), (b, 70)):
        t = math.radians(ang)
        mira(NOBOLO + p(0.012 * math.cos(t), 0.012 * math.sin(t), 0.045), NOBOLO, f, 50, 24)
def shot_salto(a, b):
    m = a + int((b - a) * 0.6)
    kf(mosca, a, loc=NOBOLO, rot=(0, 0, math.radians(25)))
    kf(mosca, m, loc=NOBOLO + p(0, 0, -0.0006), rot=(math.radians(8), 0, math.radians(25)))   # agacha, inclina pra trás
    kf(mosca, b, loc=NOBOLO + p(-0.004, 0.012, 0.018), rot=(math.radians(-15), 0, math.radians(25)))
    for f in range(m, b + 1): ESTADO.setdefault(f, {})['asas'] = True
    rz = math.radians(25); tr = p(-math.sin(rz), math.cos(rz), 0)
    kf(CHI, a, loc=NOBOLO + tr * 0.045 + p(0, 0, 0.11), rot=(math.radians(-20), 0, rz))
    kf(CHI, b, loc=NOBOLO + tr * 0.02 + p(0, 0, 0.03), rot=(math.radians(-8), 0, rz))
    mira(NOBOLO + p(0.035, -0.02, 0.006), NOBOLO + p(0, 0, 0.003), a, 70, 20)
    mira(NOBOLO + p(0.04, -0.02, 0.014), NOBOLO + p(-0.002, 0.006, 0.01), b, 70, 20)
def shot_voo(a, b):
    o = p(-0.05, 0.1, 0.4)
    kf(mosca, a, loc=o, rot=(math.radians(-10), 0, math.radians(100)))
    kf(mosca, b, loc=o + p(-0.05, 0.02, 0.09), rot=(math.radians(-10), 0, math.radians(100)))
    for f in range(a, b + 1): ESTADO.setdefault(f, {})['asas'] = True
    mira(o + p(0.01, -0.035, 0.006), o + p(0, 0, 0.003), a, 85, 16)
    mira(o + p(-0.04, -0.035, 0.095), o + p(-0.05, 0.02, 0.093), b, 85, 16)
TETOP = p(-0.1, 0.15, TETO_Z)
def shot_teto(a, b):
    kf(mosca, a, loc=TETOP, rot=(math.radians(180), 0, math.radians(40)))
    kf(mosca, b, loc=TETOP, rot=(math.radians(180), 0, math.radians(40)))
    hold(CHI, a, b, (0.0, 0.04, 0.02), (math.radians(-3), 0, math.radians(20)))   # chinelo já bateu na mesa
    for f, d in ((a, 0.05), (b, 0.03)):
        mira(TETOP + p(0.02, -d, -0.025), TETOP + p(0, 0, -0.003), f, 70, 16)
def shot_final(a, b):
    hold(mosca, a, b, TETOP, (math.radians(180), 0, math.radians(40)))
    hold(CHI, a, b, (0.0, 0.04, 0.02), (math.radians(-3), 0, math.radians(20)))
    mira(TETOP + p(0.015, -0.03, -0.02), TETOP + p(0, 0, -0.003), a, 70, 16)
    mira(TETOP + p(0.25, -0.6, -0.6), TETOP + p(0, 0, -0.003), b, 40, 32)

def fcurves(ad):
    try: return ad.action.fcurves
    except AttributeError:
        from bpy_extras import anim_utils
        cb = anim_utils.action_get_channelbag_for_slot(ad.action, ad.action_slot)
        return cb.fcurves if cb else []
FUN = {k[5:]: v for k, v in globals().items() if k.startswith('shot_')}
for s in SHOTS['shots']:
    FUN[s['id']](s['ini'], s['fim'])
# interpolação: câmera suave (BEZIER), cortes secos entre shots via CONSTANT no último key de cada shot
for o in (CAM, FOCO, mosca, CHI, GOTA, camd, camd.dof):
    ad = getattr(o, 'animation_data', None)
    if ad and ad.action:
        for fc in fcurves(ad):
            for k in fc.keyframe_points: k.interpolation = 'BEZIER'; k.easing = 'AUTO'
FIMS = {s['fim'] for s in SHOTS['shots']}
for o in (CAM, FOCO, mosca, CHI, camd, camd.dof):
    ad = getattr(o, 'animation_data', None)
    if ad and ad.action:
        for fc in fcurves(ad):
            for k in fc.keyframe_points:
                if int(round(k.co.x)) in FIMS: k.interpolation = 'CONSTANT'

# pernas e asas por frame (handler)
def pose(f):
    e = ESTADO.get(f, {})
    t = f / FPS
    for i, n in enumerate(PERNAS):
        b = PB.get(n)
        if not b: continue
        amp = 0.18 if e.get('andar') else 0.0
        vel = 9 if e.get('andar') else 1.3
        b.rotation_euler = (amp * math.sin(t * vel + i * (math.pi if i % 2 else 0) + i), 0, 0)
    for j, n in enumerate(ASAS):
        b = PB.get(n)
        if not b: continue
        if e.get('asas'):
            ang = 0.9 if f % 2 == 0 else -0.5
            b.rotation_euler = (0, 0, ang if j == 0 else -ang)
        else:
            b.rotation_euler = (0, 0, 0)
def handler(scene, depsgraph=None):
    pose(scene.frame_current)
bpy.app.handlers.frame_change_pre.append(handler)

# ---------------- render ----------------
sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'; sc.render.threads_mode = 'AUTO'
RAPIDO = os.environ.get('RAPIDO') == '1'
sc.cycles.samples = 8 if PREVIEW else (12 if RAPIDO else 32); sc.cycles.use_denoising = True
sc.cycles.max_bounces = 3 if RAPIDO else 6; sc.cycles.transmission_bounces = 4 if RAPIDO else 6
sc.render.resolution_x = 360 if PREVIEW else 900; sc.render.resolution_y = 640 if PREVIEW else 1600
sc.render.resolution_percentage = 100
sc.render.image_settings.file_format = 'JPEG'; sc.render.image_settings.quality = 92
sc.view_settings.view_transform = 'AgX'; sc.view_settings.look = 'AgX - Punchy'; sc.view_settings.exposure = -0.4
sc.render.use_motion_blur = False
os.makedirs(OUT, exist_ok=True)
fr = list(range(F0, F1 + 1)) if not PREVIEW else [int(x) for x in args[5].split(',')]
for f in fr:
    sc.frame_set(f); pose(f)
    print('CAM', f, [round(v,4) for v in CAM.matrix_world.translation], 'FOCO', [round(v,4) for v in FOCO.matrix_world.translation], 'MOSCA', [round(v,4) for v in mosca.matrix_world.translation], 'GOTA', [round(v,4) for v in GOTA.scale])
    sc.render.filepath = os.path.join(OUT, f'{f:05d}.jpg')
    bpy.ops.render.render(write_still=True)
print('ok', len(fr), 'frames')
