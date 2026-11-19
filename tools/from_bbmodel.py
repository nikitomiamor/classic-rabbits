"""Convierte el .bbmodel del bebe (Blockbench, Generic Model, UV por cara) al modelo del mod.

- Grupos -> partes (mismos nombres; las animaciones de 26.3 los buscan por nombre).
- Cubos con rotacion propia -> sub-parte "<grupo>_r<n>" con ese pivote y giro.
- Cada cubo guarda las medidas originales de su UV (el UV de caja espejado del conejo adulto),
  porque los cubos del bebe son mas chicos que el area de textura que usan.
Coordenadas: Minecraft x = -x_bb, y = 24 - y_bb, z = z_bb; rotacion mc = (-rx, -ry, +rz).
Uso: python from_bbmodel.py <bebe.bbmodel> <carpeta_java> [<salida_json_para_visor>]
"""
import json, math, os, sys

PKG = "com.nikitomiamor.classicrabbits"
TEX_W, TEX_H = 64, 32


def mirrored_faces(u, v, w, h, d):
    return {
        "north": [u + d + w, v + d, u + d, v + d + h],
        "east": [u + 2 * d + w, v + d, u + d + w, v + d + h],
        "south": [u + 2 * d + 2 * w, v + d, u + 2 * d + w, v + d + h],
        "west": [u + d, v + d, u, v + d + h],
        "up": [u + d, v + d, u + d + w, v],
        "down": [u + d + w, v, u + d + 2 * w, v + d],
    }


def uv_box_from_faces(name, faces):
    """Recupera (u, v, w, h, d) del UV de caja espejado y comprueba que todas las caras coincidan."""
    f = {k: faces[k]["uv"] for k in faces}
    w = abs(f["north"][0] - f["north"][2])
    h = abs(f["north"][3] - f["north"][1])
    d = abs(f["east"][0] - f["east"][2])
    u = min(f["west"][0], f["west"][2])
    v = min(f["up"][1], f["up"][3])
    expect = mirrored_faces(u, v, w, h, d)
    for k, uv in expect.items():
        if any(abs(a - b) > 1e-3 for a, b in zip(uv, f[k])):
            raise SystemExit(f"El cubo '{name}' tiene un UV distinto al de caja espejado en la cara {k}: {f[k]} (esperado {uv})")
    return int(u), int(v), int(w), int(h), int(d)


def to_mc(p):
    return [-p[0], 24.0 - p[1], p[2]]


def load(path):
    bb = json.load(open(path, encoding="utf-8"))
    elements = {e["uuid"]: e for e in bb["elements"]}
    groups = {g["uuid"]: g for g in bb.get("groups", [])}

    def group_node(entry, parent_abs):
        g = groups[entry["uuid"]] if "name" not in entry else entry  # 5.0 guarda los datos aparte
        abs_p = to_mc(g["origin"])
        rx, ry, rz = g.get("rotation", [0, 0, 0])
        node = {"name": g["name"], "pivot": [abs_p[i] - parent_abs[i] for i in range(3)],
                "rot": [-math.radians(rx), -math.radians(ry), math.radians(rz)],
                "cubes": [], "children": []}
        extra = 0
        for ch in entry["children"]:
            if isinstance(ch, str):
                e = elements[ch]
                u, v, uw, uh, ud = uv_box_from_faces(e["name"], e["faces"])
                frm, to = e["from"], e["to"]
                erot = e.get("rotation", [0, 0, 0])
                if any(abs(a) > 1e-6 for a in erot):
                    extra += 1
                    piv = to_mc(e["origin"])
                    sub = {"name": f'{g["name"]}_r{extra}', "pivot": [piv[i] - abs_p[i] for i in range(3)],
                           "rot": [-math.radians(erot[0]), -math.radians(erot[1]), math.radians(erot[2])],
                           "cubes": [], "children": []}
                    ref = piv
                    target = sub
                    node["children"].append(sub)
                else:
                    ref = abs_p
                    target = node
                x = -to[0] - ref[0]
                y = 24.0 - to[1] - ref[1]
                z = frm[2] - ref[2]
                target["cubes"].append([u, v, x, y, z, to[0] - frm[0], to[1] - frm[1], to[2] - frm[2],
                                        uw, uh, ud, bool(e.get("mirror_uv", False))])
            else:
                node["children"].append(group_node(ch, abs_p))
        return node

    return {"name": "root", "pivot": [0, 0, 0], "rot": [0, 0, 0], "cubes": [],
            "children": [group_node(o, [0, 0, 0]) for o in bb["outliner"]]}


def jf(x):
    return repr(float(round(x, 5))) + "F"


def java(root):
    """Cada cubo va a tamano completo (el del adulto, asi el UV de caja calza solo) dentro de una
    mini-parte "<parte>_c<n>" que lo escala en cada eje hasta el tamano del bebe.
    Es lo mismo que hacia 1.12.2 al dibujar, y funciona con Sodium (que copia el UV al crear el cubo)."""
    lines = []

    def walk(part, parent_var, depth):
        var = "p_" + part["name"]
        px, py, pz = part["pivot"]
        rx, ry, rz = part["rot"]
        ind = "        " + "    " * depth
        lines.append(f'{ind}PartDefinition {var} = {parent_var}.addOrReplaceChild("{part["name"]}", CubeListBuilder.create(), '
                     f'PartPose.offsetAndRotation({jf(px)}, {jf(py)}, {jf(pz)}, {jf(rx)}, {jf(ry)}, {jf(rz)}));')
        for i, (u, v, x, y, z, w, h, d, uw, uh, ud, mir) in enumerate(part["cubes"]):
            cb = "CubeListBuilder.create()" + (".mirror()" if mir else "")
            cb += f".texOffs({u}, {v}).addBox(0.0F, 0.0F, 0.0F, {jf(uw)}, {jf(uh)}, {jf(ud)})"
            pose = (f"new PartPose({jf(x)}, {jf(y)}, {jf(z)}, 0.0F, 0.0F, 0.0F, "
                    f"{jf(w / uw)}, {jf(h / uh)}, {jf(d / ud)})")
            lines.append(f'{ind}    {var}.addOrReplaceChild("{part["name"]}_c{i + 1}", {cb}, {pose});')
        for ch in part["children"]:
            walk(ch, var, depth + 1)

    for ch in root["children"]:
        walk(ch, "root", 0)
    return f"""package {PKG};

import net.minecraft.client.model.geom.PartPose;
import net.minecraft.client.model.geom.builders.CubeListBuilder;
import net.minecraft.client.model.geom.builders.LayerDefinition;
import net.minecraft.client.model.geom.builders.MeshDefinition;
import net.minecraft.client.model.geom.builders.PartDefinition;

/**
 * Conejo bebe (hecho en Blockbench a partir del bebe de 1.12.2), con los nombres de partes
 * que animan las animaciones de bebe de 26.3. Usa la misma textura que el adulto clasico.
 * Cada cubo esta a tamano de adulto (para que el UV calce) y una mini-parte lo escala.
 * Archivo generado por from_bbmodel.py: no editar a mano.
 */
@SuppressWarnings("unused")
public final class ClassicBabyRabbitModel {{
    private ClassicBabyRabbitModel() {{}}

    public static LayerDefinition createBodyLayer() {{
        MeshDefinition mesh = new MeshDefinition();
        PartDefinition root = mesh.getRoot();
{chr(10).join(lines)}
        return LayerDefinition.create(mesh, {TEX_W}, {TEX_H});
    }}
}}
"""


if __name__ == "__main__":
    spec = load(sys.argv[1])
    out_java = sys.argv[2]
    os.makedirs(out_java, exist_ok=True)
    open(os.path.join(out_java, "ClassicBabyRabbitModel.java"), "w", encoding="utf-8", newline="\n").write(java(spec))
    if len(sys.argv) > 3:
        json.dump(spec, open(sys.argv[3], "w", encoding="utf-8"))
    def count(p):
        return len(p["cubes"]) + sum(count(c) for c in p["children"])
    print("cubos:", count(spec))
