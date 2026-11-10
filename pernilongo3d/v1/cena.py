"""Cena 3D do pernilongo (quarto à noite) no Blender, por código.
uso: python3 cena.py shots.json <ini> <fim> <saida> [preview f1,f2,...]
"""
import bpy, math, sys, json, os, random
from mathutils import Vector, Matrix

AQUI = os.path.dirname(os.path.abspath(__file__))
ASSET = os.path.join(AQUI, '..')
args = sys.argv[1:]
SHOTS = json.load(open(args[0])); F0, F1 = int(args[1]), int(args[2]); OUT = args[3]
PREVIEW = len(args) > 4 and args[4] == 'preview'
FPS = SHOTS['fps']
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene; sc.render.fps = FPS
def p(x, y, z): return Vector((x, y, z))
R = math.radians

# ---------------- materiais ----------------
def mat(nome, cor, rough=0.5, metal=0.0, emis=None, alpha=1.0):
    m = bpy.data.materials.new(nome); m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*cor, 1); b.inputs['Roughness'].default_value = rough; b.inputs['Metallic'].default_value = metal
    if emis: b.inputs['Emission Color'].default_value = (*emis[0], 1); b.inputs['Emission Strength'].default_value = emis[1]
    if alpha < 1: b.inputs['Alpha'].default_value = alpha
    return m
def mat_madeira(c1, c2, escala=3.0):
    m = bpy.data.materials.new('madeira'); m.use_nodes = True; nt = m.node_tree; b = nt.nodes['Principled BSDF']
    b.inputs['Roughness'].default_value = 0.45
    br = nt.nodes.new('ShaderNodeTexBrick'); br.inputs['Scale'].default_value = escala; br.offset = 0.5
    br.inputs['Color1'].default_value = (*c1, 1); br.inputs['Color2'].default_value = (*c2, 1); br.inputs['Mortar'].default_value = (c2[0] * 0.5, c2[1] * 0.5, c2[2] * 0.5, 1)
    br.inputs['Mortar Size'].default_value = 0.004; br.inputs['Brick Width'].default_value = 1.6; br.inputs['Row Height'].default_value = 0.14
    tc = nt.nodes.new('ShaderNodeTexCoord'); nt.links.new(tc.outputs['Object'], br.inputs['Vector'])
    nt.links.new(br.outputs['Color'], b.inputs['Base Color'])
    return m
def mat_brilho(nome, cor, forca, alpha=0.6):
    """material que brilha e é meio transparente (rastro de gás, cheiro)"""
    m = bpy.data.materials.new(nome); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    o = nt.nodes.new('ShaderNodeOutputMaterial'); e = nt.nodes.new('ShaderNodeEmission'); t = nt.nodes.new('ShaderNodeBsdfTransparent'); mx = nt.nodes.new('ShaderNodeMixShader')
    e.inputs['Color'].default_value = (*cor, 1); e.inputs['Strength'].default_value = forca
    mx.inputs['Fac'].default_value = alpha
    nt.links.new(t.outputs[0], mx.inputs[1]); nt.links.new(e.outputs[0], mx.inputs[2]); nt.links.new(mx.outputs[0], o.inputs['Surface'])
    m.blend_method = 'BLEND' if hasattr(m, 'blend_method') else None
    return m
def om(o, m): o.data.materials.clear(); o.data.materials.append(m)
def caixa(loc, tam, m, bev=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc); o = bpy.context.object; o.scale = tam
    if bev: bpy.ops.object.transform_apply(scale=True); b = o.modifiers.new('b', 'BEVEL'); b.width = bev; b.segments = 4
    om(o, m); return o

# ---------------- quarto ----------------
PISO = mat_madeira((0.42, 0.27, 0.16), (0.36, 0.22, 0.13))
bpy.ops.mesh.primitive_plane_add(size=5, location=(0, 0, 0)); om(bpy.context.object, PISO)
PAREDE = mat('parede', (0.62, 0.66, 0.72), 0.85)
for loc, rot in (((0, 1.6, 1.3), (R(90), 0, 0)), ((-1.8, 0, 1.3), (R(90), 0, R(90))), ((1.9, 0, 1.3), (R(90), 0, R(90))), ((0, -2.3, 1.3), (R(90), 0, 0))):
    bpy.ops.mesh.primitive_plane_add(size=5, location=loc, rotation=rot); om(bpy.context.object, PAREDE)
bpy.ops.mesh.primitive_plane_add(size=5, location=(0, 0, 2.6), rotation=(math.pi, 0, 0)); om(bpy.context.object, mat('teto', (0.85, 0.85, 0.83), 0.9))
# cama de casal (cabeceira na parede y=1.6)
MADEIRA = mat('cama', (0.3, 0.18, 0.1), 0.5)
caixa((0, 0.55, 0.18), (1.7, 2.1, 0.36), MADEIRA, 0.02)
caixa((0, 1.55, 0.6), (1.8, 0.08, 1.2), MADEIRA, 0.02)                      # cabeceira
caixa((0, 0.55, 0.45), (1.6, 2.0, 0.2), mat('colchao', (0.93, 0.93, 0.9), 0.8), 0.04)
TOPO = 0.55
for x in (-0.42, 0.42):
    o = caixa((x, 1.3, TOPO + 0.07), (0.6, 0.32, 0.14), mat('trav', (0.95, 0.95, 0.97), 0.85), 0.05)
# cobertor cobrindo até a cintura
COB = caixa((0, -0.05, TOPO + 0.2), (1.66, 1.0, 0.3), mat('cobertor', (0.2, 0.32, 0.55), 0.9), 0.06)
# criado-mudo + abajur
caixa((-1.15, 1.35, 0.28), (0.45, 0.4, 0.56), MADEIRA, 0.01)
bpy.ops.mesh.primitive_cylinder_add(radius=0.04, depth=0.3, location=(-1.15, 1.35, 0.71)); om(bpy.context.object, mat('pe', (0.2, 0.2, 0.2), 0.3, 1))
bpy.ops.mesh.primitive_cone_add(radius1=0.15, radius2=0.09, depth=0.18, location=(-1.15, 1.35, 0.92)); om(bpy.context.object, mat('cupula', (0.95, 0.9, 0.8), 0.7))
# guarda-roupa (parede x=1.9)
GR = caixa((1.6, 0.0, 1.0), (0.6, 1.3, 2.0), mat('guarda', (0.85, 0.82, 0.76), 0.5), 0.01)
caixa((1.29, -0.3, 1.0), (0.02, 0.03, 0.4), mat('puxador', (0.7, 0.7, 0.7), 0.2, 1))
caixa((1.29, 0.3, 1.0), (0.02, 0.03, 0.4), mat('puxador2', (0.7, 0.7, 0.7), 0.2, 1))
# janela (parede x=-1.8) com luar
caixa((-1.79, -0.6, 1.4), (0.02, 1.0, 1.0), mat('vidro_noite', (0.05, 0.08, 0.15), 0.1, emis=((0.3, 0.4, 0.8), 0.6)))
caixa((-1.77, -0.6, 1.4), (0.03, 0.04, 1.0), MADEIRA); caixa((-1.77, -0.6, 1.4), (0.03, 1.0, 0.04), MADEIRA)
# tapete
bpy.ops.mesh.primitive_plane_add(size=1, location=(0.2, -1.1, 0.003)); tp = bpy.context.object; tp.scale = (1.2, 0.7, 1); om(tp, mat('tapete', (0.55, 0.2, 0.2), 0.95))

# ---------------- importação ----------------
def importa(arq):
    antes = set(bpy.data.objects); ac0 = set(bpy.data.actions)
    if arq.endswith('.fbx'): bpy.ops.import_scene.fbx(filepath=os.path.join(ASSET, arq))
    else: bpy.ops.import_scene.gltf(filepath=os.path.join(ASSET, arq))
    novos = [o for o in bpy.data.objects if o not in antes]
    raizes = [o for o in novos if o.parent is None]
    grupo = bpy.data.objects.new(arq + '_grupo', None); sc.collection.objects.link(grupo)
    for r in raizes: r.parent = grupo
    return grupo, novos, [a for a in bpy.data.actions if a not in ac0]

def kf(o, f, loc=None, rot=None, esc=None):
    if loc is not None: o.location = loc; o.keyframe_insert('location', frame=f)
    if rot is not None: o.rotation_euler = rot; o.keyframe_insert('rotation_euler', frame=f)
    if esc is not None: o.scale = esc; o.keyframe_insert('scale', frame=f)
def hold(o, a, b, loc, rot): kf(o, a, loc, rot); kf(o, b, loc, rot)

# ---------------- humano: cara de cavalo de pijama listrado ----------------
H_raiz, H_objs, H_acts = importa('humano.gltf')
HARM = [o for o in H_objs if o.type == 'ARMATURE'][0]
for o in H_objs:
    if o.name.startswith('Icosphere') or o.name.startswith('Casual_Head'): o.hide_render = True; o.hide_viewport = True
antes = set(bpy.data.objects); bpy.ops.import_scene.fbx(filepath=os.path.join(ASSET, 'horse_head.fbx'))
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
def listras(mm, c1, c2, escala=7):
    nt = mm.node_tree; b = nt.nodes['Principled BSDF']
    wv = nt.nodes.new('ShaderNodeTexWave'); wv.wave_type = 'BANDS'; wv.bands_direction = 'Z'; wv.inputs['Scale'].default_value = escala; wv.inputs['Distortion'].default_value = 0
    cr = nt.nodes.new('ShaderNodeValToRGB'); cr.color_ramp.interpolation = 'CONSTANT'; cr.color_ramp.elements[0].color = (*c1, 1); cr.color_ramp.elements[1].position = 0.5; cr.color_ramp.elements[1].color = (*c2, 1)
    tc = nt.nodes.new('ShaderNodeTexCoord'); nt.links.new(tc.outputs['Object'], wv.inputs['Vector']); nt.links.new(wv.outputs['Fac'], cr.inputs['Fac']); nt.links.new(cr.outputs['Color'], b.inputs['Base Color'])
H_MATS = set(CAV.data.materials)
for o in H_objs:
    if o.type == 'MESH' and not o.hide_render: H_MATS |= set(o.data.materials)
for nome in ('Purple', 'LightBlue'):
    mm = bpy.data.materials.get(nome)
    if mm: listras(mm, (0.35, 0.55, 0.9), (0.92, 0.94, 0.98))
HUM = bpy.data.objects.new('Humano', None); sc.collection.objects.link(HUM); H_raiz.parent = HUM
HARM.animation_data_create(); HARM.animation_data.action = None
def acao(arm, acts, nome, a, b, vel=1.0):
    act = [x for x in acts if x.name.split('.')[0] == nome][0]; ln = act.frame_range[1] - act.frame_range[0]
    tr = arm.animation_data.nla_tracks.new()
    st = tr.strips.new(f'{nome}_{a}', a, act); st.scale = vel; st.repeat = max(1.0, (b - a) / (ln * vel)); st.extrapolation = 'NOTHING'
# picadas (bolinhas vermelhas) — aparecem de manhã
PICADAS = []
for osso, off in (('Head', (0.06, -0.12, 0.25)), ('LowerArm.R', (0.03, 0.12, 0.04)), ('LowerArm.L', (-0.03, 0.15, 0.04)), ('UpperArm.R', (0.05, 0.1, 0.02)), ('Head', (-0.08, -0.1, 0.18))):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.022, location=(0, 0, 0)); b_ = bpy.context.object; b_.scale = (1, 1, 0.45); om(b_, mat('picada', (0.85, 0.12, 0.1), 0.5))
    b_.parent = HARM; b_.parent_type = 'BONE'; b_.parent_bone = osso; b_.location = off; PICADAS.append(b_)

# ---------------- mulher: pijama rosa, máscara de dormir e bobes ----------------
M_raiz, M_objs, M_acts = importa('mulher.gltf')
MARM = [o for o in M_objs if o.type == 'ARMATURE'][0]
for o in M_objs:
    if o.name.startswith('Icosphere'): o.hide_render = True; o.hide_viewport = True
for o in M_objs:
    if o.type != 'MESH': continue
    for mm in o.data.materials:
        b = mm.node_tree.nodes.get('Principled BSDF')
        if not b: continue
        n = mm.name.split('.')[0]
        if n == 'Skin': b.inputs['Base Color'].default_value = (0.8, 0.55, 0.42, 1)
        elif n in ('Shirt', 'Pants'): listras(mm, (0.95, 0.45, 0.65), (0.99, 0.85, 0.9), 9)
        elif n == 'Belt': b.inputs['Base Color'].default_value = (0.95, 0.45, 0.65, 1)
bpy.context.view_layer.update()
dg = bpy.context.evaluated_depsgraph_get()
pts = []
for o in M_objs:
    if o.type == 'MESH' and not o.hide_render:
        me = o.evaluated_get(dg).to_mesh(); pts += [o.matrix_world @ v.co for v in list(me.vertices)[::10]]
mh = max(q.z for q in pts) - min(q.z for q in pts)
M_raiz.scale = (1.62 / mh,) * 3
MUL = bpy.data.objects.new('Mulher', None); sc.collection.objects.link(MUL); M_raiz.parent = MUL
MARM.animation_data_create(); MARM.animation_data.action = None
# máscara de dormir + bobes no osso da cabeça (posição ajustada pelo tamanho do modelo)
bpy.context.view_layer.update()
hb = MARM.pose.bones['Head']; hl = hb.bone.length
S_ = M_raiz.scale[0] * MARM.scale[0]
def no_osso(o, loc):
    o.parent = MARM; o.parent_type = 'BONE'; o.parent_bone = 'Head'; o.location = Vector(loc) / S_ - Vector((0, hl, 0)); o.scale = tuple(v / S_ for v in o.scale)
mk = caixa((0, 0, 0), (0.24, 0.07, 0.03), mat('mascara', (0.9, 0.35, 0.6), 0.6), 0.01); no_osso(mk, (0, 0.2, 0.3))
for i, x in enumerate((-0.09, 0, 0.09)):
    bpy.ops.mesh.primitive_cylinder_add(radius=0.035, depth=0.08, location=(0, 0, 0)); bo = bpy.context.object
    om(bo, mat('bobe', (0.4, 0.75, 0.95) if i != 1 else (0.98, 0.85, 0.3), 0.5)); bo.rotation_euler = (0, R(90), 0); no_osso(bo, (x, 0.53, -0.04))
MASCARA = [mk]
# cabeça menor (fica mais proporcional) e detalhes femininos: laço, batom e brincos
cs = MARM.pose.bones['Head'].constraints.new('LIMIT_SCALE'); cs.owner_space = 'LOCAL'
for ax in ('x', 'y', 'z'):
    setattr(cs, f'use_min_{ax}', True); setattr(cs, f'use_max_{ax}', True); setattr(cs, f'min_{ax}', 0.7); setattr(cs, f'max_{ax}', 0.7)
ROSA = mat('laco', (0.95, 0.2, 0.5), 0.4)
for sx in (-1, 1):
    bpy.ops.mesh.primitive_cone_add(radius1=0.05, depth=0.08, location=(0, 0, 0)); lc = bpy.context.object; om(lc, ROSA)
    lc.rotation_euler = (0, R(-90 * sx), 0); no_osso(lc, (0.05 * sx, 0.45, -0.22))
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.03, location=(0, 0, 0)); lc = bpy.context.object; om(lc, ROSA); no_osso(lc, (0, 0.45, -0.22))
bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=(0, 0, 0)); lb = bpy.context.object; lb.scale = (0.05, 0.018, 0.015)
om(lb, mat('batom', (0.85, 0.05, 0.2), 0.3)); no_osso(lb, (0, 0.12, 0.27))
for sx in (-1, 1):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.018, location=(0, 0, 0)); br = bpy.context.object; om(br, mat('brinco', (1.0, 0.8, 0.2), 0.2, 1.0)); no_osso(br, (0.2 * sx, 0.12, 0.02))

# ---------------- pernilongo ----------------
Q_raiz, Q_objs, _ = importa('pernilongo.glb')
QS = 0.12
MQ = bpy.data.objects.new('Pernilongo', None); sc.collection.objects.link(MQ)       # posição/direção (cabeça para +Y)
TREME = bpy.data.objects.new('Treme', None); sc.collection.objects.link(TREME); TREME.parent = MQ
Q_raiz.parent = TREME; Q_raiz.scale = (QS,) * 3
MQ['voa'] = 1.0
CORPO = [o for o in Q_objs if o.type == 'MESH' and o.name.startswith('Default')][0]
ASA = [o for o in Q_objs if o.type == 'MESH' and o.name.startswith('Plane')][0]
# separa as duas asas, cada uma girando na raiz
import bmesh
def separa_asa(lado):
    o = ASA.copy(); o.data = ASA.data.copy(); sc.collection.objects.link(o); o.parent = ASA.parent; o.matrix_parent_inverse = ASA.matrix_parent_inverse.copy()
    bm = bmesh.new(); bm.from_mesh(o.data)
    fora = [v for v in bm.verts if (v.co.x < 0) == (lado > 0)]
    bmesh.ops.delete(bm, geom=fora, context='VERTS'); bm.to_mesh(o.data); bm.free()
    return o
bpy.context.view_layer.update()
ASAS = []
for lado in (1, -1):
    o = separa_asa(lado)
    piv = bpy.data.objects.new(f'piv{lado}', None); sc.collection.objects.link(piv); piv.parent = TREME
    raiz_w = ASA.matrix_world @ Vector((0, 0, 0))
    # raiz da asa no modelo: x≈±0.012, y≈-0.02, z≈0.006 (unidades do modelo)
    piv.location = Vector((0.012 * lado, -0.02, 0.006)) * QS
    bpy.context.view_layer.update()
    mwo = o.matrix_world.copy(); o.parent = piv; o.matrix_parent_inverse = piv.matrix_world.inverted(); o.matrix_world = mwo
    d = piv.driver_add('rotation_euler', 1).driver; d.type = 'SCRIPTED'
    v = d.variables.new(); v.name = 'voa'; v.type = 'SINGLE_PROP'; v.targets[0].id = MQ; v.targets[0].data_path = '["voa"]'
    d.expression = f'{lado} * voa * (0.15 + 0.75 * sin(frame * 2.7))'
    dz = piv.driver_add('rotation_euler', 2).driver; dz.type = 'SCRIPTED'
    v = dz.variables.new(); v.name = 'voa'; v.type = 'SINGLE_PROP'; v.targets[0].id = MQ; v.targets[0].data_path = '["voa"]'
    dz.expression = f'{lado} * (1 - voa) * -1.1'          # pousado: asas dobradas para trás
    ASAS.append(piv)
ASA.hide_render = True; ASA.hide_viewport = True
for ax, fr, amp in ((0, 0.35, 0.0025), (1, 0.27, 0.002), (2, 0.42, 0.003)):
    d = TREME.driver_add('location', ax).driver; d.type = 'SCRIPTED'
    v = d.variables.new(); v.name = 'voa'; v.type = 'SINGLE_PROP'; v.targets[0].id = MQ; v.targets[0].data_path = '["voa"]'
    d.expression = f'voa * {amp} * (sin(frame * {fr}) + 0.5 * sin(frame * {fr * 2.3} + 1))'
def kvoa(f, voando):
    MQ['voa'] = 1.0 if voando else 0.0; MQ.keyframe_insert('["voa"]', frame=f)
# ponta da tromba (vértice mais à frente) e barriga (sangue)
me = CORPO.data; ponta = max(me.vertices, key=lambda v: v.co.y).co
bpy.context.view_layer.update()
PONTA_LOCAL = TREME.matrix_world.inverted() @ (CORPO.matrix_world @ ponta)
bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=(0, 0, 0)); BARRIGA = bpy.context.object
om(BARRIGA, mat('sangue', (0.55, 0.02, 0.02), 0.2, emis=((0.4, 0.0, 0.0), 0.3))); bpy.ops.object.shade_smooth()
BARRIGA.parent = TREME; BARRIGA.location = Vector((0, -0.075, 0.0)) * QS
def kbarriga(f, k):
    s = 0.0001 + k * QS
    kf(BARRIGA, f, esc=(0.022 * s, 0.05 * s, 0.022 * s))
kbarriga(0, 0)

# ---------------- rastro de gás carbônico e cheiro ----------------
def curva(nome, pts, raio, m):
    cu = bpy.data.curves.new(nome, 'CURVE'); cu.dimensions = '3D'; cu.bevel_depth = raio; cu.bevel_resolution = 4
    sp = cu.splines.new('NURBS'); sp.points.add(len(pts) - 1)
    for i, q in enumerate(pts): sp.points[i].co = (*q, 1)
    sp.use_endpoint_u = True; sp.order_u = 4
    o = bpy.data.objects.new(nome, cu); sc.collection.objects.link(o); cu.materials.append(m); return o
CO2_MAT = mat_brilho('co2', (0.3, 0.85, 1.0), 2.5, 0.35)
CHEIRO_MAT = mat_brilho('cheiro', (0.55, 1.0, 0.25), 2.5, 0.6)
VISIVEL = {}      # objeto -> set de frames onde aparece (o resto: escondido)
def mostra(o, a, b):
    VISIVEL.setdefault(o, set()).update(range(a, b + 1))

# ---------------- set do ferrão (corte da pele, longe do quarto) ----------------
SF = p(20, 0, 0)
PELE = mat('pele', (0.86, 0.6, 0.5), 0.6)
caixa(SF + p(0, 0.08, -0.02), (0.5, 0.15, 0.04), PELE)                                      # epiderme (corte na frente, y=0)
caixa(SF + p(0, 0.08, -0.1), (0.5, 0.15, 0.12), mat('derme', (0.95, 0.72, 0.65), 0.7))     # derme
bpy.ops.mesh.primitive_cylinder_add(radius=0.022, depth=0.5, location=SF + p(0, 0.01, -0.1), rotation=(0, R(90), 0)); VASO = bpy.context.object
om(VASO, mat('vaso', (0.6, 0.02, 0.03), 0.3, emis=((0.5, 0.0, 0.0), 0.4)))
ESTILETES = []
for i, (cor, dx, ang) in enumerate((((1.0, 0.55, 0.1), -0.012, -12), ((1.0, 0.55, 0.1), 0.012, 12),      # serram
                                    ((0.2, 0.5, 1.0), -0.03, -35), ((0.2, 0.5, 1.0), 0.03, 35),           # seguram
                                    ((0.3, 0.95, 0.3), -0.004, -4), ((0.95, 0.15, 0.1), 0.004, 3))):      # saliva, canudo
    bpy.ops.mesh.primitive_cone_add(radius1=0.0035, radius2=0.0012, depth=1, location=(0, 0, 0)); e = bpy.context.object
    om(e, mat(f'est{i}', cor, 0.35, emis=(cor, 0.6))); ESTILETES.append((e, dx, ang))
def kestiletes(f, k, ks=None):
    """k: quanto entraram (0..1); ks: estiletes que abrem (seguram)"""
    for i, (e, dx, ang) in enumerate(ESTILETES):
        prof = 0.03 + 0.06 * k if i < 4 else 0.03 + 0.072 * k
        a = R(ang) * (k if i in (2, 3) else 1)
        top = SF + p(0, 0, 0.015)
        e.rotation_euler = (0, math.pi + a, 0); e.scale = (1, 1, prof)
        e.location = top + p(dx * 0.3 + math.sin(a) * prof / 2, 0, -math.cos(a) * prof / 2)
        e.keyframe_insert('location', frame=f); e.keyframe_insert('rotation_euler', frame=f); e.keyframe_insert('scale', frame=f)
kestiletes(0, 0)
# gotinhas de saliva (verde) e de sangue subindo (vermelho)
GOTAS = []
for i in range(6):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.004, location=SF + p(-0.004, 0, -0.06 - i * 0.01)); g = bpy.context.object
    om(g, mat('saliva', (0.4, 1.0, 0.4), 0.2, emis=((0.3, 1.0, 0.3), 2))); GOTAS.append(g)
SANGUE = []
for i in range(6):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.004, location=SF + p(0.004, 0, -0.06 - i * 0.01)); g = bpy.context.object
    om(g, mat('sangue_g', (0.9, 0.05, 0.05), 0.2, emis=((0.9, 0.0, 0.0), 1.5))); SANGUE.append(g)

# ---------------- set da banheira ----------------
SB = p(-20, 0, 0)
bpy.ops.mesh.primitive_plane_add(size=6, location=SB); om(bpy.context.object, mat('piso_b', (0.8, 0.82, 0.85), 0.2))
bpy.ops.mesh.primitive_plane_add(size=6, location=SB + p(0, 1.2, 1.5), rotation=(R(90), 0, 0)); om(bpy.context.object, mat('az_b', (0.55, 0.75, 0.8), 0.2))
caixa(SB + p(0.3, 0.6, 0.28), (1.6, 0.75, 0.56), mat('banheira', (0.97, 0.97, 0.97), 0.1), 0.08)
caixa(SB + p(0.3, 0.6, 0.5), (1.45, 0.6, 0.04), mat('agua_sangue', (0.6, 0.02, 0.03), 0.05, emis=((0.4, 0, 0), 0.3)))
bpy.ops.mesh.primitive_cylinder_add(radius=0.025, depth=1.3, location=(0, 0, 0)); CANUDO = bpy.context.object
om(CANUDO, mat('canudo', (0.95, 0.95, 0.95), 0.3)); listras(CANUDO.data.materials[0], (0.95, 0.2, 0.2), (0.97, 0.97, 0.97), 20)

# ---------------- set da chuva (lá fora) ----------------
SC_ = p(0, 20, 0)
bpy.ops.mesh.primitive_plane_add(size=40, location=SC_ + p(0, 6, 0), rotation=(R(90), 0, 0)); om(bpy.context.object, mat('ceu', (0.02, 0.03, 0.06), 0.9, emis=((0.05, 0.08, 0.16), 1.0)))
VIDRO = mat('gota', (0.85, 0.92, 1.0), 0.0)
VIDRO.node_tree.nodes['Principled BSDF'].inputs['Transmission Weight'].default_value = 1.0
VIDRO.node_tree.nodes['Principled BSDF'].inputs['IOR'].default_value = 1.33
CHUVA = []
random.seed(4)
for i in range(70):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.012, location=(0, 0, 0)); g = bpy.context.object; g.scale = (1, 1, 1.25); om(g, VIDRO); bpy.ops.object.shade_smooth()
    CHUVA.append((g, random.uniform(-0.5, 0.5), random.uniform(-0.3, 0.6), random.uniform(0, 1)))
GOTA = CHUVA[0][0]

# ---------------- luz ----------------
w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True
BG = w.node_tree.nodes['Background']; BG.inputs[0].default_value = (0.2, 0.26, 0.42, 1)
def luz(nome, tipo, e, loc, rot, tam=0.3, cor=(1, 1, 1)):
    L = bpy.data.lights.new(nome, tipo); L.energy = e; L.color = cor
    if tipo == 'AREA': L.size = tam
    o = bpy.data.objects.new(nome, L); sc.collection.objects.link(o); o.location = loc; o.rotation_euler = rot; return L
LUA = luz('lua', 'AREA', 60, (-1.6, -0.6, 1.5), (0, R(-75), 0), 1.0, (0.55, 0.65, 1.0))
TETO = luz('teto', 'AREA', 25, (0, 0.2, 2.5), (0, 0, 0), 1.2, (0.7, 0.75, 1.0))
SOL = luz('sol', 'SUN', 0, (0, 0, 5), (R(55), 0, R(-60)), cor=(1.0, 0.85, 0.65))
FORA = luz('fora', 'AREA', 0, SC_ + p(0.3, 1.5, 1.4), (R(-60), 0, R(10)), 2.0, (0.7, 0.8, 1.0))
FORA2 = luz('fora2', 'AREA', 0, SC_ + p(-0.8, -1.2, 1.2), (R(55), 0, R(-35)), 1.5, (1.0, 0.9, 0.8))
SETS = luz('sets', 'SUN', 0, (0, 0, 5), (R(40), 0, R(30)), cor=(1, 0.97, 0.92))
EMIS_H = []     # materiais dos humanos (para a visão de calor)
for mm in set(list(H_MATS) + [m for o in M_objs if o.type == 'MESH' for m in o.data.materials] + [mk.data.materials[0]]):
    b = mm.node_tree.nodes.get('Principled BSDF') if mm and mm.node_tree else None
    if b: EMIS_H.append(b)
def modo(f, m):
    """noite | termica | dia | fora | set"""
    LUA.energy = {'noite': 60, 'termica': 0, 'dia': 10, 'fora': 0, 'set': 0}[m]
    TETO.energy = {'noite': 25, 'termica': 0, 'dia': 40, 'fora': 0, 'set': 0}[m]
    SOL.energy = {'dia': 4.0}.get(m, 0)
    FORA.energy = {'fora': 400}.get(m, 0); FORA2.energy = {'fora': 60}.get(m, 0)
    SETS.energy = {'set': 4.0}.get(m, 0)
    BG.inputs[1].default_value = {'noite': 0.18, 'termica': 0.0, 'dia': 0.8, 'fora': 0.05, 'set': 0.6}[m]
    for L in (LUA, TETO, SOL, FORA, FORA2, SETS): L.keyframe_insert('energy', frame=f)
    BG.inputs[1].keyframe_insert('default_value', frame=f)
    for b in EMIS_H:
        b.inputs['Emission Color'].default_value = (1.0, 0.42, 0.08, 1); b.inputs['Emission Strength'].default_value = 3.0 if m == 'termica' else 0.0
        b.inputs['Emission Strength'].keyframe_insert('default_value', frame=f)

# ---------------- câmera ----------------
camd = bpy.data.cameras.new('cam'); CAM = bpy.data.objects.new('cam', camd); sc.collection.objects.link(CAM); sc.camera = CAM
camd.clip_start = 0.001; camd.dof.use_dof = True; camd.sensor_width = 36
FOCO = bpy.data.objects.new('foco', None); sc.collection.objects.link(FOCO); camd.dof.focus_object = FOCO
def mira(cl, alvo, f, lens=50, fstop=8):
    CAM.location = cl; CAM.rotation_euler = (Vector(alvo) - Vector(cl)).to_track_quat('-Z', 'Y').to_euler(); FOCO.location = alvo
    CAM.keyframe_insert('location', frame=f); CAM.keyframe_insert('rotation_euler', frame=f); FOCO.keyframe_insert('location', frame=f)
    camd.lens = lens; camd.keyframe_insert('lens', frame=f); camd.dof.aperture_fstop = fstop; camd.dof.keyframe_insert('aperture_fstop', frame=f)

# ================= posições fixas =================
HX, MX_ = -0.42, 0.42
def deitado(obj, x, y_pe, a, b):
    hold(obj, a, b, p(x, y_pe, TOPO + 0.13), (R(-90), 0, 0))
def sentado(obj, x, y_pe, a, b, ang=-25):
    # tronco pra fora do cobertor; pernas escondidas dentro da cama
    t = R(-ang); hold(obj, a, b, p(x, 0.5 - 0.9 * math.sin(t), TOPO + 0.12 - 0.9 * math.cos(t)), (R(ang), 0, 0))
H_PE, M_PE = -0.27, -0.1
H_SENT = p(-0.42, 0.5 + 0.65 * math.sin(R(25)), TOPO + 0.12 + 0.65 * math.cos(R(25)))   # cabeça sentado
LONGE = p(0, -50, -5)

def osso(arm, nome, f):
    sc.frame_set(f); bpy.context.view_layer.update()
    return arm.matrix_world @ arm.pose.bones[nome].head

def casal(a, b, h='Idle', m='Idle'):
    deitado(HUM, HX, H_PE, a, b); deitado(MUL, MX_, M_PE, a, b)
    acao(HARM, H_acts, h, a, b, 1.6); acao(MARM, M_acts, m, a, b, 1.6)

# calcula onde ficam as cabeças/braço com o casal deitado (frame de teste 0)
casal(-200, -100)
sc.frame_set(-150); bpy.context.view_layer.update()
H_CAB = HARM.matrix_world @ HARM.pose.bones['Head'].head
M_CAB = MARM.matrix_world @ MARM.pose.bones['Head'].head
H_BRACO = HARM.matrix_world @ HARM.pose.bones['LowerArm.L'].head
H_BOCA = H_CAB + p(0, 0.12, 0.2)
print('cabecas', [round(v, 2) for v in H_CAB], [round(v, 2) for v in M_CAB], 'braco', [round(v, 2) for v in H_BRACO])
ORELHA = H_CAB + p(-0.12, 0.05, 0.12)
POUSO = p(H_BRACO.x - 0.02, H_BRACO.y - 0.12, max(H_BRACO.z, TOPO + 0.2) + 0.04)
ESCONDE = p(1.28, 0.7, 1.6)      # parede atrás do guarda-roupa (lateral)

def voo(a, b, de, ate, rotz=None, voando=True):
    kvoa(a, voando); kvoa(b, voando)
    d = Vector(ate) - Vector(de)
    rz = rotz if rotz is not None else math.atan2(-d.x, d.y)
    kf(MQ, a, de, (0, 0, rz)); kf(MQ, b, ate, (0, 0, rz))
def parado(a, b, loc, rot, voando=False):
    kvoa(a, voando); kvoa(b, voando); hold(MQ, a, b, loc, rot)
def ve(a, b, *objs):
    for o in objs: mostra(o, a, b)

ROTA = [p(1.2, -1.6, 1.4), p(0.7, -0.9, 1.25), p(0.0, -0.1, 1.1), p(-0.3, 0.7, 0.95), H_BOCA + p(0, -0.15, 0.1)]
TRILHA = curva('trilha', [H_BOCA] + [q for q in reversed(ROTA[:-1])], 0.035, CO2_MAT)
TRILHA.data.bevel_factor_mapping_end = 'SPLINE'
def ktrilha(f, k): TRILHA.data.bevel_factor_end = k; TRILHA.data.keyframe_insert('bevel_factor_end', frame=f)
ktrilha(0, 0)
FUMOS = []
for i in range(4):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.05, location=H_BOCA + p(0, -0.05 * i, 0.05 * i)); s = bpy.context.object; om(s, CO2_MAT); FUMOS.append(s)
CHEIROS = []
for i in range(5):
    x = H_BRACO.x + random.uniform(-0.15, 0.15); y = H_BRACO.y + random.uniform(-0.3, 0.3); z0 = TOPO + 0.22
    CHEIROS.append(curva(f'ch{i}', [p(x, y, z0), p(x + 0.05, y, z0 + 0.1), p(x - 0.05, y, z0 + 0.2), p(x + 0.05, y, z0 + 0.3), p(x - 0.03, y, z0 + 0.4)], 0.007, CHEIRO_MAT))

bpy.ops.mesh.primitive_uv_sphere_add(radius=0.012, location=POUSO + p(0, 0.004, -0.012)); BOLINHA = bpy.context.object; BOLINHA.scale = (1, 1, 0.45)
om(BOLINHA, mat('picada2', (0.9, 0.15, 0.12), 0.5))
def perto(alvo, off, f, lens=50, fs=8): mira(Vector(alvo) + Vector(off), alvo, f, lens, fs)

# ================= cenas =================
def s_abre(a, b):       # close do pernilongo voando no escuro, de frente
    modo(a, 'noite'); casal(a, b); c = p(0.3, -0.6, 1.2); voo(a, b, c, c + p(-0.03, 0.04, 0.0), 0)
    mira(c + p(0.03, 0.07, 0.02), c + p(0, 0.005, 0), a, 55, 5); mira(c + p(0.02, 0.1, 0.02), c + p(-0.03, 0.045, 0), b, 55, 5)
def s_zumbe(a, b):      # pernilongo passando na orelha do cavalo
    modo(a, 'noite'); casal(a, b); voo(a, b, ORELHA + p(0.25, -0.1, 0.05), ORELHA + p(-0.05, 0.02, 0))
    mira(H_CAB + p(0.35, -0.35, 0.3), H_CAB + p(0.05, 0, 0.1), a, 35, 6); mira(H_CAB + p(0.3, -0.3, 0.28), ORELHA, b, 35, 6)
def s_voce(a, b):       # gira em volta do pernilongo
    modo(a, 'noite'); casal(a, b); c = p(0.6, -1.0, 1.3); voo(a, b, c, c + p(0.0, 0.05, 0))
    mira(c + p(0.08, -0.07, 0.03), c, a, 35, 11); mira(c + p(-0.06, -0.06, 0.03), c + p(0, 0.05, 0), b, 35, 11)
def s_hora(a, b):       # quarto inteiro, escuro
    modo(a, 'noite'); casal(a, b); voo(a, b, ROTA[0], ROTA[0] + p(-0.1, 0.1, 0))
    mira(p(1.4, -2.15, 1.9), p(-0.1, 0.4, 0.6), a, 20, 16); mira(p(1.3, -2.1, 1.85), p(-0.1, 0.45, 0.6), b, 20, 16)
def s_cama_longe(a, b): # por trás do pernilongo, a cama lá longe
    modo(a, 'noite'); casal(a, b); c = ROTA[0]; voo(a, b, c, c + p(-0.03, 0.05, 0))
    mira(c + p(0.06, -0.14, 0.04), p(-0.1, 1.0, 0.7), a, 30, 3); mira(c + p(0.05, -0.12, 0.035), p(-0.1, 1.0, 0.7), b, 30, 3)
def s_bafo(a, b):       # boca soltando nuvem azul
    modo(a, 'noite'); casal(a, b); parado(a, b, LONGE, (0, 0, 0)); ve(a, b, *FUMOS)
    for i, s in enumerate(FUMOS):
        kf(s, a, H_BOCA + p(0, -0.02, 0.02), esc=(0.2, 0.2, 0.2)); kf(s, b, H_BOCA + p(0.05 * (i - 1.5), -0.25 - 0.1 * i, 0.15 + 0.08 * i), esc=(1.3, 1.3, 1.3))
    mira(H_CAB + p(0.45, -0.25, 0.45), H_BOCA + p(0, -0.1, 0.05), a, 40, 8); mira(H_CAB + p(0.42, -0.3, 0.45), H_BOCA + p(0, -0.15, 0.1), b, 40, 8)
def s_dez(a, b):        # a trilha atravessa o quarto até o pernilongo
    modo(a, 'noite'); casal(a, b); voo(a, b, ROTA[0], ROTA[0] + p(0, 0.03, 0)); ve(a, b, TRILHA); ktrilha(a, 0.05); ktrilha(b, 1.0)
    mira(p(1.5, -2.1, 2.2), p(0.2, -0.2, 0.9), a, 18, 16); mira(p(1.45, -2.05, 2.15), p(0.2, -0.2, 0.9), b, 18, 16)
def s_rastro(a, b):     # voa seguindo a trilha
    modo(a, 'noite'); casal(a, b); ve(a, b, TRILHA); ktrilha(a, 1.0); voo(a, b, ROTA[1], ROTA[2])
    mira(ROTA[1] + p(0.2, -0.25, 0.1), ROTA[1], a, 30, 6); mira(ROTA[2] + p(0.2, -0.25, 0.1), ROTA[2], b, 30, 6)
def s_termica(a, b):    # visão de calor
    modo(a, 'termica'); casal(a, b); voo(a, b, ROTA[3], ROTA[3] + p(-0.05, 0.1, -0.05))
    mira(p(0.35, -1.0, 1.45), p(0.0, 0.6, 0.65), a, 24, 22); mira(p(0.3, -0.85, 1.4), p(0.0, 0.65, 0.65), b, 24, 22)
def s_duas(a, b):       # vista de cima: os dois na cama
    modo(a, 'noite'); casal(a, b); parado(a, b, LONGE, (0, 0, 0))
    mira(p(0, 0.75, 2.45), p(0, 0.76, 0.6), a, 22, 16); mira(p(0, 0.6, 2.3), p(0, 0.61, 0.6), b, 22, 16)
def s_sangue(a, b):     # pernilongo pairando entre os dois
    modo(a, 'noite'); casal(a, b); c = p(0.0, 0.6, 1.05); voo(a, b, c, c + p(0.03, 0, 0), R(180))
    mira(c + p(0.08, -0.12, 0.05), c + p(-0.01, 0.02, 0), a, 30, 14); mira(c + p(0.07, -0.11, 0.05), c + p(0.02, 0.02, 0), b, 30, 14)
def s_cheiro(a, b):     # close no braço dele com fumaça verde
    modo(a, 'noite'); casal(a, b); parado(a, b, LONGE, (0, 0, 0)); ve(a, b, *CHEIROS)
    mira(H_BRACO + p(-0.5, -0.45, 0.35), H_BRACO + p(0, 0, 0.2), a, 35, 10); mira(H_BRACO + p(-0.45, -0.4, 0.33), H_BRACO + p(0, 0, 0.22), b, 35, 10)
def s_queijo(a, b):     # mais cheiro, câmera mais perto
    modo(a, 'noite'); casal(a, b); parado(a, b, LONGE, (0, 0, 0)); ve(a, b, *CHEIROS)
    mira(H_BRACO + p(-0.3, -0.2, 0.25), H_BRACO + p(0, 0, 0.25), a, 40, 10); mira(H_BRACO + p(-0.25, -0.15, 0.3), H_BRACO + p(0, 0, 0.3), b, 40, 10)
def s_ima(a, b):        # pernilongo vira e vai direto nele
    modo(a, 'noite'); casal(a, b); ve(a, b, *CHEIROS); c = p(0.1, 0.4, 1.0); voo(a, b, c, c + p(-0.3, -0.05, -0.1))
    mira(c + p(0.25, -0.3, 0.1), c, a, 35, 6); mira(c + p(0.0, -0.35, 0.05), c + p(-0.25, -0.05, -0.08), b, 35, 6)
def s_banho(a, b):      # ela dormindo de máscara e bobes, roncando
    modo(a, 'noite'); casal(a, b); parado(a, b, LONGE, (0, 0, 0))
    mira(M_CAB + p(0.35, -0.3, 0.35), M_CAB + p(0, 0, 0.08), a, 40, 6); mira(M_CAB + p(0.3, -0.25, 0.3), M_CAB + p(0, 0, 0.08), b, 40, 6)
def s_escolhe(a, b):    # pernilongo descendo para ele
    modo(a, 'noite'); casal(a, b); voo(a, b, H_CAB + p(0.2, -0.4, 0.45), H_CAB + p(0.05, -0.25, 0.28))
    mira(H_CAB + p(0.5, -0.8, 0.6), H_CAB + p(0.0, -0.2, 0.15), a, 30, 8); mira(H_CAB + p(0.45, -0.75, 0.55), H_CAB + p(0.0, -0.2, 0.15), b, 30, 8)
def s_femea(a, b):      # close lateral, girando
    modo(a, 'noite'); casal(a, b); c = p(-0.1, 0.0, 1.0); voo(a, b, c, c + p(0, 0.06, 0))
    mira(c + p(0.09, -0.01, 0.02), c, a, 45, 16); mira(c + p(0.08, 0.07, 0.02), c + p(0, 0.06, 0), b, 45, 16)
def s_asas(a, b):       # bem de perto nas asas batendo
    modo(a, 'noite'); casal(a, b); c = p(-0.1, 0.05, 1.0); voo(a, b, c, c + p(0, 0.03, 0))
    mira(c + p(0.0, -0.07, 0.07), c + p(0, 0.0, 0.005), a, 60, 18); mira(c + p(0.02, -0.06, 0.06), c + p(0, 0.03, 0.005), b, 60, 18)
def s_zumbido(a, b):    # perto da orelha dele
    modo(a, 'noite'); casal(a, b); voo(a, b, ORELHA + p(-0.08, -0.03, 0.02), ORELHA + p(-0.02, 0.0, 0.0))
    mira(ORELHA + p(-0.15, -0.3, 0.12), ORELHA, a, 45, 6); mira(ORELHA + p(-0.13, -0.27, 0.11), ORELHA, b, 45, 6)
def s_mao(a, b):        # ele senta e prepara o tapa
    modo(a, 'noite'); sentado(HUM, HX, H_PE, a, b); deitado(MUL, MX_, M_PE, a, b)
    acao(HARM, H_acts, 'Sword_Slash', a, b, 1.0); acao(MARM, M_acts, 'Idle', a, b, 1.6)
    c = H_SENT + p(0.12, -0.35, 0.05); voo(a, b, c, c + p(0.02, 0, 0))
    mira(c + p(0.06, -0.13, 0.01), c + p(-0.02, 0.15, 0.0), a, 32, 16); mira(c + p(0.06, -0.12, 0.01), c + p(-0.02, 0.15, 0.0), b, 32, 16)
def s_tapa(a, b):
    modo(a, 'noite'); sentado(HUM, HX, H_PE, a, b); deitado(MUL, MX_, M_PE, a, b)
    acao(HARM, H_acts, 'Sword_Slash', a - 14, b, 1.0); acao(MARM, M_acts, 'Idle', a, b, 1.6)
    c = H_SENT + p(0.12, -0.35, 0.05); voo(a, b, c, c + p(-0.1, 0, 0.05))
    mira(c + p(0.06, -0.13, 0.01), c + p(-0.02, 0.15, 0.0), a, 32, 16); mira(c + p(0.06, -0.13, 0.01), c + p(-0.04, 0.15, 0.02), b, 32, 16)
def s_errou(a, b):      # pernilongo jogado de lado, girando
    modo(a, 'noite'); sentado(HUM, HX, H_PE, a, b); deitado(MUL, MX_, M_PE, a, b)
    acao(HARM, H_acts, 'Idle', a, b, 1.0); acao(MARM, M_acts, 'Idle', a, b, 1.6)
    c = H_SENT + p(0.0, -0.35, 0.1); kvoa(a, True); kvoa(b, True)
    kf(MQ, a, c, (R(40), R(-60), 0)); kf(MQ, a + 12, c + p(-0.25, -0.1, 0.1), (R(-30), R(200), R(40))); kf(MQ, b, c + p(-0.35, -0.15, 0.15), (0, 0, R(20)))
    mira(c + p(0.06, -0.18, 0.03), c, a, 35, 16); mira(c + p(-0.2, -0.28, 0.13), c + p(-0.25, -0.1, 0.1), a + 12, 35, 16); mira(c + p(-0.3, -0.33, 0.18), c + p(-0.35, -0.15, 0.15), b, 35, 16)
def s_pousa(a, b):      # pousa no braço dele
    modo(a, 'noite'); casal(a, b); kvoa(a, True); kvoa(a + 30, True); kvoa(a + 34, False); kvoa(b, False)
    kf(MQ, a, POUSO + p(0.1, -0.15, 0.15), (0, 0, R(30))); kf(MQ, a + 32, POUSO, (R(-15), 0, R(30))); kf(MQ, b, POUSO, (R(-15), 0, R(30)))
    mira(POUSO + p(-0.1, -0.22, 0.08), POUSO, a, 50, 6); mira(POUSO + p(-0.06, -0.15, 0.04), POUSO, b, 60, 6)
def s_seis(a, b):       # close no ferrão encostando na pele
    modo(a, 'noite'); casal(a, b); parado(a, b, POUSO, (R(-15), 0, R(30))); kbarriga(a, 0); kbarriga(b, 0)
    mira(POUSO + p(-0.07, -0.06, 0.02), POUSO + p(0.0, 0.005, -0.003), a, 45, 16); mira(POUSO + p(-0.06, -0.05, 0.015), POUSO + p(0.0, 0.008, -0.004), b, 50, 16)
SET_CAM = SF + p(0, -0.3, -0.03)
def s_serra(a, b):      # corte da pele: 6 estiletes entrando, dois abrindo
    modo(a, 'set'); parado(a, b, LONGE, (0, 0, 0)); kestiletes(a, 0.1); kestiletes(b, 1.0)
    mira(SET_CAM, SF + p(0, 0, -0.04), a, 40, 22); mira(SET_CAM + p(0, 0.08, 0), SF + p(0, 0, -0.05), b, 40, 22)
def s_suga(a, b):       # saliva desce (verde), sangue sobe (vermelho)
    modo(a, 'set'); parado(a, b, LONGE, (0, 0, 0)); kestiletes(a, 1.0); kestiletes(b, 1.0); ve(a, b + 60, *(GOTAS + SANGUE))
    for i, g in enumerate(GOTAS):
        kf(g, a, SF + p(-0.004, 0, 0.0 - i * 0.005)); kf(g, b, SF + p(-0.004, 0, -0.06 - i * 0.008))
    for i, g in enumerate(SANGUE):
        kf(g, a, SF + p(0.004, 0, -0.1 + i * 0.008)); kf(g, b, SF + p(0.004, 0, -0.03 + i * 0.006))
    mira(SET_CAM + p(0, 0.15, 0), SF + p(0, 0, -0.05), a, 40, 22); mira(SET_CAM + p(0, 0.2, -0.01), SF + p(0, 0, -0.05), b, 40, 22)
def s_saliva(a, b):     # close na gotinha verde
    modo(a, 'set'); parado(a, b, LONGE, (0, 0, 0)); kestiletes(a, 1.0); kestiletes(b, 1.0)
    for i, g in enumerate(GOTAS): kf(g, a, SF + p(-0.004, 0, -0.06 - i * 0.008)); kf(g, b, SF + p(-0.004 - 0.01 * (i % 3), 0, -0.09 - i * 0.004))
    mira(SF + p(-0.01, -0.12, -0.06), SF + p(-0.004, 0, -0.08), a, 60, 16); mira(SF + p(-0.01, -0.1, -0.07), SF + p(-0.004, 0, -0.085), b, 60, 16)
def s_peso(a, b):       # barriga enchendo de sangue
    modo(a, 'noite'); casal(a, b); parado(a, b, POUSO, (R(-15), 0, R(30))); kbarriga(a, 0.3); kbarriga(b, 1.0)
    mira(POUSO + p(0.07, -0.05, 0.03), POUSO + p(0, -0.005, 0.0), a, 70, 16); mira(POUSO + p(0.06, -0.06, 0.025), POUSO + p(0, -0.005, 0.0), b, 70, 16)
def s_banheira(a, b):   # cavalo bebendo a banheira de canudo
    modo(a, 'set'); parado(a, b, LONGE, (0, 0, 0)); kbarriga(a, 1.0)
    hold(HUM, a, b, SB + p(-0.75, 0.5, 0), (0, 0, R(-90))); acao(HARM, H_acts, 'Idle', a, b, 1.0)
    hold(MUL, a, b, LONGE, (0, 0, 0)); ve(a, b, CANUDO)
    kf(CANUDO, a, SB + p(-0.25, 0.52, 1.0), (0, R(-55), 0))
    kf(CANUDO, b, SB + p(-0.25, 0.52, 1.0), (0, R(-55), 0))
    mira(SB + p(0.2, -2.6, 1.3), SB + p(-0.1, 0.5, 0.9), a, 28, 16); mira(SB + p(0.1, -2.4, 1.25), SB + p(-0.1, 0.5, 0.9), b, 28, 16)
def s_coceira(a, b):    # braço com a picada vermelha aparecendo, pernilongo indo embora
    modo(a, 'noite'); casal(a, b); kbarriga(a, 1.0); ve(a, b, BOLINHA)
    voo(a, b, POUSO + p(0, 0, 0.02), POUSO + p(0.25, -0.2, 0.3))
    kf(BOLINHA, a, esc=(0.3, 0.3, 0.15)); kf(BOLINHA, b, esc=(1.6, 1.6, 0.7))
    mira(POUSO + p(-0.12, -0.15, 0.25), POUSO + p(0.0, 0.0, -0.03), a, 45, 14); mira(POUSO + p(-0.1, -0.13, 0.22), POUSO + p(0.0, 0.0, -0.03), b, 45, 14)
def s_esconde(a, b):    # pousado na parede, gordinho, atrás do guarda-roupa
    modo(a, 'noite'); casal(a, b); kbarriga(a, 1.0); parado(a, b, ESCONDE, (R(90), 0, R(90)))
    mira(ESCONDE + p(-0.12, -0.16, 0.03), ESCONDE, a, 50, 6); mira(ESCONDE + p(-0.08, -0.11, 0.02), ESCONDE, b, 55, 6)
def chuva(a, b, lenta=1.0):
    for g, x, y, fase in CHUVA[1:]:
        dur = 10 / lenta; t0 = a - int(fase * dur)
        k = t0
        while k < b:
            kf(g, k, SC_ + p(x, y, 1.6)); kf(g, k + dur, SC_ + p(x, y, -0.4)); k += dur
        mostra(g, a, b)
def s_chuva(a, b):
    modo(a, 'fora'); kbarriga(a, 1.0); c = SC_ + p(0, 0, 0.6); voo(a, b, c, c + p(0.02, 0, 0)); chuva(a, b, 1.0)
    hold(HUM, a, b, LONGE, (0, 0, 0)); hold(MUL, a, b, LONGE, (0, 0, 0))
    mira(c + p(0.0, -0.3, 0.05), c, a, 45, 10); mira(c + p(0.0, -0.25, 0.05), c, b, 45, 10)
def s_gota(a, b):       # câmera lenta: a gota gigante cai em cima
    modo(a, 'fora'); kbarriga(a, 1.0); c = SC_ + p(0, 0, 0.6); voo(a, b, c, c + p(0.01, 0, 0)); chuva(a, b, 0.15)
    hold(HUM, a, b, LONGE, (0, 0, 0)); hold(MUL, a, b, LONGE, (0, 0, 0)); mostra(GOTA, a, b)
    kf(GOTA, a, c + p(0, 0.005, 0.35)); kf(GOTA, b, c + p(0, 0.005, 0.03))
    mira(c + p(0.12, -0.18, 0.12), c + p(0, 0, 0.08), a, 50, 6); mira(c + p(0.1, -0.15, 0.1), c + p(0, 0, 0.05), b, 50, 6)
def s_carona(a, b):     # desce grudado na gota e se solta
    modo(a, 'fora'); kbarriga(a, 1.0); c = SC_ + p(0, 0, 0.6); chuva(a, b, 0.15); mostra(GOTA, a, b)
    hold(HUM, a, b, LONGE, (0, 0, 0)); hold(MUL, a, b, LONGE, (0, 0, 0))
    m = a + int((b - a) * 0.55); kvoa(a, False); kvoa(m, False); kvoa(m + 3, True); kvoa(b, True)
    kf(GOTA, a, c + p(0, 0.005, 0.03)); kf(GOTA, b, c + p(0, 0.005, -0.5))
    kf(MQ, a, c, (R(-20), 0, 0)); kf(MQ, m, c + p(0, 0, -0.25), (R(-20), 0, 0)); kf(MQ, b, c + p(0.15, 0, -0.18), (0, 0, R(-60)))
    mira(c + p(0.15, -0.35, 0.0), c + p(0, 0, -0.12), a, 40, 8); mira(c + p(0.2, -0.38, -0.1), c + p(0.08, 0, -0.2), b, 40, 8)
def s_manha(a, b):      # de manhã: sentado, se coçando, cheio de picadas
    modo(a, 'dia'); sentado(HUM, HX, H_PE, a, b, -20); deitado(MUL, MX_, M_PE, a, b)
    acao(HARM, H_acts, 'Interact', a, b, 0.8); acao(MARM, M_acts, 'Idle', a, b, 1.6); ve(a, b + 200, *PICADAS)
    parado(a, b, LONGE, (0, 0, 0))
    mira(p(HX + 0.35, -1.0, 1.4), H_SENT + p(0, 0, -0.25), a, 30, 10); mira(p(HX + 0.3, -0.85, 1.38), H_SENT + p(0, 0, -0.2), b, 30, 10)
def s_anjo(a, b):       # ela dormindo tranquila
    modo(a, 'dia'); sentado(HUM, HX, H_PE, a, b, -20); deitado(MUL, MX_, M_PE, a, b)
    acao(HARM, H_acts, 'Interact', a, b, 0.8); acao(MARM, M_acts, 'Idle', a, b, 1.6); parado(a, b, LONGE, (0, 0, 0))
    mira(p(0.9, -0.7, 1.5), p(0.0, 0.8, 0.75), a, 26, 14); mira(p(0.85, -0.6, 1.45), p(0.0, 0.8, 0.75), b, 26, 14)
def s_final(a, b):      # pernilongo atrás do guarda-roupa, satisfeito
    modo(a, 'dia'); sentado(HUM, HX, H_PE, a, b, -20); deitado(MUL, MX_, M_PE, a, b)
    acao(HARM, H_acts, 'Interact', a, b, 0.8); acao(MARM, M_acts, 'Idle', a, b, 1.6)
    kbarriga(a, 1.0); parado(a, b, ESCONDE, (R(90), 0, R(90)))
    mira(ESCONDE + p(-0.12, -0.16, 0.02), ESCONDE, a, 55, 4); mira(ESCONDE + p(-0.08, -0.1, 0.015), ESCONDE, b, 60, 4)

FUN = {k[2:]: v for k, v in globals().items() if k.startswith('s_')}
for s in SHOTS['shots']:
    FUN[s['id']](s['ini'], s['fim'])

def fcurves(ad):
    try: return ad.action.fcurves
    except AttributeError:
        from bpy_extras import anim_utils
        cb = anim_utils.action_get_channelbag_for_slot(ad.action, ad.action_slot); return cb.fcurves if cb else []
FIMS = {s['fim'] for s in SHOTS['shots']}
ANIMADOS = [CAM, FOCO, MQ, HUM, MUL, BARRIGA, TRILHA.data, GOTA, CANUDO, camd, camd.dof, w.node_tree] + FUMOS + PICADAS + [BOLINHA] + GOTAS + SANGUE + [e for e, _, _ in ESTILETES] + [g for g, *_ in CHUVA]
ANIMADOS += [L for L in (LUA, TETO, SOL, FORA, SETS)] + [m.node_tree for m in bpy.data.materials if m.node_tree and m.node_tree.animation_data]
for o in ANIMADOS:
    ad = getattr(o, 'animation_data', None)
    if ad and ad.action:
        for fc in fcurves(ad):
            for k in fc.keyframe_points:
                k.interpolation = 'CONSTANT' if int(round(k.co.x)) in FIMS or fc.data_path in ('energy', '["voa"]') or 'default_value' in fc.data_path else 'LINEAR'

def visibilidade(f):
    for o, fs in VISIVEL.items():
        o.hide_render = f not in fs

# ---------------- render (leve) ----------------
sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'
sc.cycles.samples = 6 if PREVIEW else 16; sc.cycles.use_denoising = True
sc.cycles.max_bounces = 4; sc.cycles.diffuse_bounces = 2; sc.cycles.glossy_bounces = 2; sc.cycles.transmission_bounces = 4; sc.cycles.transparent_max_bounces = 8
sc.cycles.use_adaptive_sampling = True; sc.cycles.adaptive_threshold = 0.05
sc.render.use_motion_blur = True; sc.render.motion_blur_shutter = 0.5
sc.render.resolution_x = 360 if PREVIEW else 720; sc.render.resolution_y = 640 if PREVIEW else 1280
sc.render.image_settings.file_format = 'JPEG'; sc.render.image_settings.quality = 92
sc.view_settings.view_transform = 'AgX'; sc.view_settings.look = 'AgX - Punchy'
os.makedirs(OUT, exist_ok=True)
fr = list(range(F0, F1 + 1)) if not PREVIEW else [int(x) for x in args[5].split(',')]
for f in fr:
    sc.frame_set(f); visibilidade(f)
    sc.render.filepath = os.path.join(OUT, f'{f:05d}.jpg'); bpy.ops.render.render(write_still=True)
print('ok', len(fr))
