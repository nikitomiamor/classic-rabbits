"""Exporta modelos (en coordenadas de ModelPart) a .bbmodel de Blockbench (formato Modded Entity).

Conversion (la misma que usa Blockbench al exportar Modded Entity):
  Blockbench x = -x_mc,  y = 24 - y_mc,  z = z_mc   (posiciones absolutas, sin aplicar rotaciones)
  rotacion Blockbench = (-rx, -ry, +rz) en grados
Uso: python to_bbmodel.py <carpeta_salida> <textura_clasica.png> <textura_bebe_26.3.png>
"""
import base64, json, math, os, sys, uuid

sys.path.insert(0, os.path.dirname(__file__))
from rabbit_spec import classic, P  # noqa: E402

D = math.degrees

# Bebe de 26.3 (BabyRabbitModel), como referencia de proporciones del "estilo nuevo".
baby_26 = P("root", (0, 0, 0), children=[
    P("body", (0, 23, 1.6), children=[
        P("body_r1", (0, -2, -1.6), (-0.5236, 0, 0), [(0, 8, -2, -2, -3, 4, 3, 6)]),
        P("tail", (0, -2.2, 2), children=[
            P("tail_r1", (-0.1, 0, 0), (-0.5236, 0, 0), [(0, 21, -1.4, -2.0268, -1.0177, 3, 3, 3)])]),
        P("head", (0, -5, -2.6), cubes=[(0, 0, -2.5, -3, -3, 5, 4, 4)], children=[
            P("right_ear", (-1.5, -3.5, -0.5), cubes=[(18, 0, -1, -3.5, -0.5, 2, 4, 1)]),
            P("left_ear", (1.5, -3.5, -0.5), cubes=[(24, 0, -1, -3.5, -0.5, 2, 4, 1)]),
        ]),
        P("frontlegs", (0, -2.5, -2.6), children=[
            P("left_front_leg", (1, 1, -0.5), (0.3927, 0, 0), children=[
                P("left_front_leg_r1", (0, 1, 0), (-0.3927, 0, 0), [(18, 8, -0.5, -1.5, -0.5, 1, 3, 1)])]),
            P("right_front_leg", (-1, 1, -0.5), (0.3927, 0, 0), children=[
                P("right_front_leg_r1", (0, 1, 0), (-0.3927, 0, 0), [(14, 8, -0.5, -1.5, -0.5, 1, 3, 1)])]),
        ]),
    ]),
    P("backlegs", (0, 23, 2), children=[
        P("left_hind_leg", (1.5, 0.5, 0.5), (0, 3.1416, 0), children=[
            P("left_haunch", (1, 0, 0.5), (0, -0.7854, 0), [(10, 17, -2, -0.5, 0, 2, 1, 3)])]),
        P("right_hind_leg", (-1.5, 0.5, 0.5), (0, 3.1416, 0), children=[
            P("right_haunch", (0.5, 0, -0.9), (0, 0.7854, 0), [(0, 17, -2, -0.5, 0, 2, 1, 3)])]),
    ]),
])


# Bebe de 1.12.2: el mismo modelo, pero ModelRabbit.render() escalaba al dibujar:
#   cabeza, orejas y nariz: scale(0.56666666) + translate(0, 22, 2)
#   todo lo demas:          scale(0.4)        + translate(0, 36, 0)
BABY_HEAD = (0.56666666, (0.0, 22.0, 2.0))
BABY_BODY = (0.4, (0.0, 36.0, 0.0))
HEAD_PARTS = {"head", "left_ear", "right_ear"}


def make_baby_1122(spec):
    """Devuelve el bebe de 1.12.2 con la escala ya aplicada a la geometria.
    Los cubos guardan las medidas originales para el UV (u, v, x, y, z, w, h, d, uw, uh, ud)."""
    def walk(part, parent_abs, parent_new_abs):
        ax = [parent_abs[i] + part["pivot"][i] for i in range(3)]
        s, t = BABY_HEAD if part["name"] in HEAD_PARTS else BABY_BODY
        new_abs = [s * (ax[i] + t[i]) for i in range(3)]
        cubes = [(u, v, x * s, y * s, z * s, w * s, h * s, d * s, w, h, d)
                 for (u, v, x, y, z, w, h, d) in part["cubes"]]
        node = P(part["name"], [new_abs[i] - parent_new_abs[i] for i in range(3)], part["rot"], cubes,
                 mirror=part["mirror"])
        node["children"] = [walk(ch, ax, new_abs) for ch in part["children"]]
        return node
    root = P("root", (0, 0, 0))
    root["children"] = [walk(ch, [0, 0, 0], [0, 0, 0]) for ch in spec["children"]]
    return root


def mirrored_faces(u, v, w, h, d):
    """UV por cara equivalente al UV de caja espejado (tal como lo calcula Blockbench)."""
    return {
        "north": {"uv": [u + d + w, v + d, u + d, v + d + h], "texture": 0},
        "east": {"uv": [u + 2 * d + w, v + d, u + d + w, v + d + h], "texture": 0},
        "south": {"uv": [u + 2 * d + 2 * w, v + d, u + 2 * d + w, v + d + h], "texture": 0},
        "west": {"uv": [u + d, v + d, u, v + d + h], "texture": 0},
        "up": {"uv": [u + d, v + d, u + d + w, v], "texture": 0},
        "down": {"uv": [u + d + w, v, u + d + 2 * w, v + d], "texture": 0},
    }


def r(x):
    return round(x, 4) + 0.0


def box_faces(u, v, w, h, d):
    """Caras con el UV de caja de Blockbench."""
    return {
        "north": {"uv": [u + d, v + d, u + d + w, v + d + h], "texture": 0},
        "east": {"uv": [u, v + d, u + d, v + d + h], "texture": 0},
        "south": {"uv": [u + 2 * d + w, v + d, u + 2 * d + 2 * w, v + d + h], "texture": 0},
        "west": {"uv": [u + d + w, v + d, u + 2 * d + w, v + d + h], "texture": 0},
        "up": {"uv": [u + d + w, v + d, u + d, v], "texture": 0},
        "down": {"uv": [u + d + 2 * w, v, u + d + w, v + d], "texture": 0},
    }


def convert(spec, elements, abs_mc=(0.0, 0.0, 0.0), is_root=True):
    """Devuelve la lista de hijos del outliner para esta parte."""
    out = []
    for part in spec["children"]:
        px = abs_mc[0] + part["pivot"][0]
        py = abs_mc[1] + part["pivot"][1]
        pz = abs_mc[2] + part["pivot"][2]
        origin = [r(-px), r(24 - py), r(pz)]
        children = []
        for i, cube in enumerate(part["cubes"]):
            u, v, x, y, z, w, h, d = cube[:8]
            per_face = len(cube) == 11          # cubo escalado: UV por cara con las medidas originales
            if per_face:
                assert part["mirror"], "solo se usa con cubos espejados"
                faces = mirrored_faces(u, v, *cube[8:])
            else:
                faces = box_faces(u, v, w, h, d)
            cid = str(uuid.uuid4())
            elements.append({
                "name": part["name"] + ("" if i == 0 else f"_{i + 1}"),
                "box_uv": not per_face, "rescale": False, "locked": False, "render_order": "default",
                "allow_mirror_modeling": True,
                "from": [r(-(px + x + w)), r(24 - (py + y + h)), r(pz + z)],
                "to": [r(-(px + x)), r(24 - (py + y)), r(pz + z + d)],
                "autouv": 0, "color": i % 8, "origin": origin,
                "uv_offset": [u, v], "mirror_uv": bool(part["mirror"]),
                "faces": faces,
                "type": "cube", "uuid": cid,
            })
            children.append(cid)
        children += convert(part, elements, (px, py, pz), False)
        rx, ry, rz = part["rot"]
        out.append({
            "name": part["name"], "origin": origin,
            "rotation": [r(-D(rx)), r(-D(ry)), r(D(rz))],
            "color": 0, "uuid": str(uuid.uuid4()), "export": True, "mirror_uv": bool(part["mirror"]),
            "isOpen": True, "locked": False, "visibility": True, "autouv": 0,
            "children": children,
        })
    return out


def bbmodel(name, spec, tex_path, tex_w, tex_h):
    elements = []
    outliner = convert(spec, elements)
    src = "data:image/png;base64," + base64.b64encode(open(tex_path, "rb").read()).decode()
    box_uv = all(e["box_uv"] for e in elements)
    return {
        # Modded Entity obliga UV de caja; con UV por cara se usa Generic Model ("free").
        "meta": {"format_version": "4.10", "model_format": "modded_entity" if box_uv else "free", "box_uv": box_uv},
        "name": name, "model_identifier": name, "modded_entity_entity_class": "", "modded_entity_version": "1.17",
        "modded_entity_flip_y": True,
        "visible_box": [1, 1, 0], "variable_placeholders": "", "variable_placeholder_buttons": [],
        "timeline_setups": [], "unhandled_root_fields": {},
        "resolution": {"width": tex_w, "height": tex_h},
        "elements": elements, "outliner": outliner,
        "textures": [{
            "path": "", "name": os.path.basename(tex_path), "folder": "", "namespace": "", "id": "0",
            "width": tex_w, "height": tex_h, "uv_width": tex_w, "uv_height": tex_h,
            "particle": False, "use_as_default": False, "layers_enabled": False, "sync_to_project": "",
            "render_mode": "default", "render_sides": "auto", "frame_time": 1, "frame_order_type": "loop",
            "frame_order": "", "frame_interpolate": False, "visible": True, "internal": True, "saved": False,
            "uuid": str(uuid.uuid4()), "source": src,
        }],
    }


if __name__ == "__main__":
    out_dir, tex_classic, tex_baby = sys.argv[1:4]
    os.makedirs(out_dir, exist_ok=True)
    for fname, spec, tex, tw, th in (
        ("conejo_clasico.bbmodel", classic, tex_classic, 64, 32),
        ("conejo_bebe_26.3_referencia.bbmodel", baby_26, tex_baby, 32, 32),
        ("conejo_bebe_1.12.2.bbmodel", make_baby_1122(classic), tex_classic, 64, 32),
    ):
        data = bbmodel(fname.split(".bbmodel")[0], spec, tex, tw, th)
        with open(os.path.join(out_dir, fname), "w", encoding="utf-8") as f:
            json.dump(data, f, indent=1)
        print(fname, "cubos:", len(data["elements"]))
