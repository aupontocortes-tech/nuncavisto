"""Piolho (modelo Sketchfab) com chapéu de Napoleão e soldados franceses (Quaternius) — helpers para a cena."""
import bpy, math, os
from mathutils import Vector, Matrix
R = math.radians
AQ = os.path.dirname(os.path.abspath(__file__))
def mat(n, c, r=0.5, metal=0.0, emis=None):
    m = bpy.data.materials.new(n); m.use_nodes = True; b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*c, 1); b.inputs['Roughness'].default_value = r; b.inputs['Metallic'].default_value = metal
    if emis: b.inputs['Emission Color'].default_value = (*emis[0], 1); b.inputs['Emission Strength'].default_value = emis[1]
    return m
def importa(arq):
    antes = set(bpy.data.objects); a0 = set(bpy.data.actions)
    bpy.ops.import_scene.gltf(filepath=os.path.join(AQ, arq))
    novos = [o for o in bpy.data.objects if o not in antes]
    g = bpy.data.objects.new(arq + '_g', None); bpy.context.scene.collection.objects.link(g)
    for o in novos:
        if o.parent is None: o.parent = g
    return g, novos, [a for a in bpy.data.actions if a not in a0]
def prende(o, alvo):
    """prende o objeto no alvo mantendo a posição no mundo"""
    bpy.context.view_layer.update(); mw = o.matrix_world.copy(); o.parent = alvo; o.matrix_parent_inverse = alvo.matrix_world.inverted(); o.matrix_world = mw
def prende_osso(o, arm, osso):
    bpy.context.view_layer.update(); mw = o.matrix_world.copy()
    o.parent = arm; o.parent_type = 'BONE'; o.parent_bone = osso; bpy.context.view_layer.update(); o.matrix_world = mw
PRETO = None
def _mats():
    global PRETO, OURO, AZUL, BRANCO, VERM
    if PRETO: return
    PRETO = mat('preto', (0.03, 0.03, 0.035), 0.55); OURO = mat('ouro', (1.0, 0.72, 0.25), 0.25, 1.0)
    AZUL = mat('azul_farda', (0.06, 0.11, 0.38), 0.6); BRANCO = mat('branco', (0.92, 0.92, 0.9), 0.6); VERM = mat('verm', (0.75, 0.05, 0.05), 0.5)
def cil(loc, r, h, m, rot=(0, 0, 0), v=32):
    bpy.ops.mesh.primitive_cylinder_add(vertices=v, radius=r, depth=h, location=loc, rotation=rot); o = bpy.context.object; o.data.materials.append(m); bpy.ops.object.shade_smooth(); return o
def esf(loc, esc, m):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=12, location=loc); o = bpy.context.object; o.scale = esc; o.data.materials.append(m); bpy.ops.object.shade_smooth(); return o

def piolho(tam=0.5, chapeu=False):
    """piolho com cabeça para +Y, de pé no chão (z=0). tam = comprimento total em metros."""
    _mats()
    g, objs, _ = importa('piolho.glb')
    raiz = bpy.data.objects.new('Piolho', None); bpy.context.scene.collection.objects.link(raiz)
    s = tam / 8.6
    g.parent = raiz; g.scale = (s, s, s); g.rotation_euler = (0, 0, math.pi); g.location = (0, 0, 1.07 * s)
    bpy.context.view_layer.update()
    if chapeu:
        # chapéu bicorne (meia-lua atravessada na cabeça) com debrum dourado e cocarda
        cab = Vector((0, 3.85 * s, 0.62 * s + 1.07 * s))
        topo = cab + Vector((0, 0, 0.15 * s))
        h = cil(topo, 1.0 * s, 0.28 * s, PRETO, rot=(R(90), 0, 0), v=64)
        import bmesh
        bpy.context.view_layer.update(); bm = bmesh.new(); bm.from_mesh(h.data)
        bmesh.ops.bisect_plane(bm, geom=bm.verts[:] + bm.edges[:] + bm.faces[:], plane_co=(0, 0, 0), plane_no=(0, 1, 0), clear_inner=True)
        bmesh.ops.triangle_fill(bm, use_beauty=True, use_dissolve=True, edges=[e for e in bm.edges if e.is_boundary]); bm.to_mesh(h.data); bm.free()
        h.scale = (1, 1, 1); bv = h.modifiers.new('bv', 'BEVEL'); bv.width = 0.1 * s; bv.segments = 3
        d = esf(topo + Vector((0, 0.05 * s, 0.1 * s)), (1.02 * s, 0.16 * s, 0.06 * s), OURO)      # debrum dourado na base
        for i, (m, r) in enumerate(((AZUL, 0.32), (BRANCO, 0.21), (VERM, 0.1))):
            c = cil(topo + Vector((0.55 * s, 0.15 * s + i * 0.02 * s, 0.6 * s)), r * s, 0.04 * s, m, rot=(R(90), 0, 0))
            prende(c, raiz)
        for o in (h, d): prende(o, raiz)
    return raiz

def soldado(cor_casaco=None, napoleao=False):
    """soldado francês de 1812: casaco azul, calça branca, botas pretas, barretina (shako) com pluma vermelha e mosquete."""
    _mats()
    g, objs, acts = importa('humano.gltf')
    arm = [o for o in objs if o.type == 'ARMATURE'][0]
    raiz = bpy.data.objects.new('Soldado', None); bpy.context.scene.collection.objects.link(raiz); g.parent = raiz
    for o in objs:
        if o.type != 'MESH': continue
        for ms in o.material_slots:
            n = ms.material.name.split('.')[0]
            if o.name.startswith('Casual_Feet'): ms.material = PRETO
            elif o.name.startswith('Casual_Legs'): ms.material = BRANCO
            elif n in ('Purple', 'LightBlue'): ms.material = cor_casaco or AZUL
    bpy.context.view_layer.update()
    hc = arm.matrix_world @ arm.pose.bones['Head'].head
    if napoleao:      # bicorne atravessado, sem mosquete
        import bmesh
        h = cil(hc + Vector((0, 0, 0.3)), 0.26, 0.07, PRETO, rot=(R(90), 0, 0), v=48)
        bm = bmesh.new(); bm.from_mesh(h.data)
        bmesh.ops.bisect_plane(bm, geom=bm.verts[:] + bm.edges[:] + bm.faces[:], plane_co=(0, 0, 0), plane_no=(0, 1, 0), clear_inner=True)
        bmesh.ops.triangle_fill(bm, use_beauty=True, use_dissolve=True, edges=[e for e in bm.edges if e.is_boundary]); bm.to_mesh(h.data); bm.free()
        c = cil(hc + Vector((0.13, -0.045, 0.43)), 0.035, 0.01, VERM, rot=(R(90), 0, 0))
        for o in (h, c): prende_osso(o, arm, 'Head')
        arm.animation_data_create()
        for t in list(arm.animation_data.nla_tracks): arm.animation_data.nla_tracks.remove(t)
        arm.animation_data.action = None; return raiz, arm, acts
    sh = cil(hc + Vector((0, 0, 0.36)), 0.12, 0.24, PRETO); pl = cil(hc + Vector((0, -0.12, 0.33)), 0.05, 0.06, OURO, rot=(R(90), 0, 0))
    pena = esf(hc + Vector((0, -0.02, 0.55)), (0.035, 0.035, 0.09), VERM); aba = cil(hc + Vector((0, -0.08, 0.25)), 0.1, 0.02, PRETO); aba.scale = (1, 0.8, 1)
    for o in (sh, pl, pena, aba): prende_osso(o, arm, 'Head')
    wr = arm.matrix_world @ arm.pose.bones['Wrist.R'].head
    mos = cil(wr + Vector((0, 0, 0.35)), 0.018, 1.3, mat('madeira', (0.3, 0.18, 0.08), 0.6)); prende_osso(mos, arm, 'Wrist.R')
    arm.animation_data_create()
    for t in list(arm.animation_data.nla_tracks): arm.animation_data.nla_tracks.remove(t)
    arm.animation_data.action = None
    return raiz, arm, acts
