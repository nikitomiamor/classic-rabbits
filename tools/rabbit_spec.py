"""Especificacion unica del conejo clasico.

Genera:
  - viewer/data.js  (modelo vanilla 26.3 + modelo clasico + animaciones) para el visor 3D
  - ClassicRabbitLayer.java (geometria) y ClassicRabbitAnimations.java (factores de adaptacion)

Coordenadas: las de ModelPart de Minecraft (y hacia abajo, suelo en y=24, frente en -z).
"""
import json, math, os, re, sys

R = math.radians

# ---------------------------------------------------------------- vanilla 26.3 (AdultRabbitModel)
def P(name, pivot, rot=(0, 0, 0), cubes=(), children=(), mirror=False):
    return {"name": name, "pivot": list(pivot), "rot": list(rot), "cubes": [list(c) for c in cubes],
            "mirror": mirror, "children": list(children)}

vanilla = P("root", (0, 0, 0), children=[
    P("body", (0, 23, 4), (-0.3927, 0, 0), [(0, 0, -4, -6, -9, 8, 6, 10)], children=[
        P("tail", (0, -4.9916, 0.0125), cubes=[(20, 16, -2, -3.0084, -1.0125, 4, 4, 4)]),
        P("head", (0, -5.2929, -8.1213), (0.3927, 0, 0), [(0, 16, -2.5, -3, -4, 5, 5, 5)], children=[
            P("left_ear", (1.5, -3.7071, -0.8787), cubes=[(32, 0, -1, -4.2929, -0.1213, 2, 5, 1)]),
            P("right_ear", (-1.5, -3.7071, -0.8787), cubes=[(26, 0, -1, -4.2929, -0.1213, 2, 5, 1)]),
        ]),
        P("frontlegs", (0, -1.5349, -6.3108), children=[
            P("right_front_leg", (-2, 1.9239, 0.3827), (0.3927, 0, 0), [(36, 18, -0.9, -1, -0.9, 2, 4, 2)]),
            P("left_front_leg", (2, 1.9239, 0.4827), (0.3927, 0, 0), [(44, 18, -1, -1, -1, 2, 4, 2)]),
        ]),
    ]),
    P("backlegs", (0, 23, 4), children=[
        P("right_hind_leg", (-3, 0.5, 0), children=[
            P("right_haunch", (0, -0.5, 0), (0, 0.3927, 0), [(20, 24, -1, 0, -5, 2, 1, 6)])]),
        P("left_hind_leg", (3, 0.5, 0), children=[
            P("left_haunch", (0, -0.5, 0), (0, -0.3927, 0), [(36, 24, -1, 0, -5, 2, 1, 6)])]),
    ]),
])

# ---------------------------------------------------------------- clasico (ModelRabbit 1.12.2)
# Pivotes absolutos de 1.12.2 -> relativos a los grupos que animan las animaciones de 26.3.
BODY = (0.0, 22.0, 6.0)      # pivote del grupo "body": abajo atras del cuerpo (como en 26.3)
HIP = (0.0, 17.5, 3.7)       # pivote del grupo "backlegs": cadera
SHOULDER = (0.0, 17.0, -1.0) # pivote del grupo "frontlegs": hombros
HEAD = (0.0, 16.0, -1.0)

def rel(a, b):
    return tuple(round(a[i] - b[i], 4) for i in range(3))

T20 = -0.34906584   # -20 grados
T10 = -0.17453292   # -10 grados
EAR = 0.2617994     # 15 grados

def ear(name, side, u, v):
    """Oreja con pivote en su base (las animaciones de 26.3 la giran desde ahi)."""
    th = EAR * side
    base = (1.5 * side, -4.0, -0.5)                       # centro de la base, sin rotar
    bx = base[0] * math.cos(th) + base[2] * math.sin(th)  # Ry(th) * base
    bz = -base[0] * math.sin(th) + base[2] * math.cos(th)
    return P(name, (round(bx, 4), base[1], round(bz, 4)), (0, th, 0),
             [(u, v, -1, -5, -0.5, 2, 5, 1)], mirror=True)

classic = P("root", (0, 0, 0), children=[
    P("body", BODY, children=[
        P("torso", rel((0, 19, 8), BODY), (T20, 0, 0), [(0, 0, -3, -2, -10, 6, 5, 10)], mirror=True),
        P("tail", rel((0, 20, 7), BODY), (T20, 0, 0), [(52, 6, -1.5, -1.5, 0, 3, 3, 2)], mirror=True),
        P("head", rel(HEAD, BODY), cubes=[(32, 0, -2.5, -4, -5, 5, 4, 5), (32, 9, -0.5, -2.5, -5.5, 1, 1, 1)],
          mirror=True, children=[ear("left_ear", 1, 58, 0), ear("right_ear", -1, 52, 0)]),
        P("frontlegs", rel(SHOULDER, BODY), children=[
            P("right_front_leg", rel((-3, 17, -1), SHOULDER), (T10, 0, 0), [(0, 15, -1, 0, -1, 2, 7, 2)], mirror=True),
            P("left_front_leg", rel((3, 17, -1), SHOULDER), (T10, 0, 0), [(8, 15, -1, 0, -1, 2, 7, 2)], mirror=True),
        ]),
    ]),
    P("backlegs", HIP, children=[
        # muslo en la pata (rotado -20 como en 1.12.2); pie en el "haunch" con +20 para quedar plano
        P("right_hind_leg", rel((-3, 17.5, 3.7), HIP), (T20, 0, 0), [(16, 15, -1, 0, 0, 2, 4, 5)], mirror=True, children=[
            P("right_haunch", (0, 0, 0), (-T20, 0, 0), [(8, 24, -1, 5.5, -3.7, 2, 1, 7)], mirror=True)]),
        P("left_hind_leg", rel((3, 17.5, 3.7), HIP), (T20, 0, 0), [(30, 15, -1, 0, 0, 2, 4, 5)], mirror=True, children=[
            P("left_haunch", (0, 0, 0), (-T20, 0, 0), [(26, 24, -1, 5.5, -3.7, 2, 1, 7)], mirror=True)]),
    ]),
])
CLASSIC_SCALE = 0.6  # ModelRabbit 1.12.2 dibujaba al adulto al 60 %

# ---------------------------------------------------------------- adaptacion de animaciones
# (animacion, hueso, canal) -> lista de (hueso destino, factor); lo que no figura queda igual
ADAPT = {
    # 26.3 gira el grupo de patas traseras 125 grados (pensado para pies planos). En el clasico eso
    # levanta el muslo por encima del lomo: se lo paso solo a los pies, al 25 %.
    # Resultado: muslo ~47 grados (right/left_hind_leg) y pie ~78, como el salto de 1.12.2 (50 / 80).
    ("HOP", "backlegs", "ROTATION"): [("left_haunch", 0.25), ("right_haunch", 0.25)],
    # Al pararse, 26.3 adelanta la cabeza hasta 2,5 px (pensado para su cabeza grande). Con el conejo
    # parado eso la sube y la separa del torso clasico: se anula y quedan solo sus giros.
    ("IDLE_HEAD_TILT", "head", "POSITION"): [("head", 0.0)],
    # Bebe (animaciones de bebe de 26.3): tiene los mismos dos problemas que el adulto clasico.
    ("BABY_HOP", "backlegs", "ROTATION"): [("left_haunch", 0.25), ("right_haunch", 0.25)],
    ("BABY_IDLE_HEAD_TILT", "head", "POSITION"): [("head", 0.0)],
}

def parse_anims(path):
    s = open(path, encoding="utf-8").read()
    out = {}
    # acepta los dos estilos de Vineflower: con o sin prefijos de clase (Builder, Targets, Interpolations)
    for m in re.finditer(r'public static final AnimationDefinition (\w+) = (?:AnimationDefinition\.)?Builder\.withLength\(([\d.]+)F\)(.*?)\.build\(\);', s, re.S):
        name, length, body = m.groups()
        anim = {"length": float(length), "looping": ".looping()" in body, "bones": {}}
        for a in re.finditer(r'\.addAnimation\(\s*"(\w+)",\s*new AnimationChannel\(\s*(?:AnimationChannel\.)?Targets\.(\w+),(.*?)\)\s*\)', body, re.S):
            bone, target, kfs = a.groups()
            if target == "SCALE":
                continue
            ks = []
            for t, kind, x, y, z, interp in re.findall(
                    r'new Keyframe\(\s*([-\d.]+)F,\s*KeyframeAnimations\.(\w+)\(\s*([-\d.]+)F,\s*([-\d.]+)F,\s*([-\d.]+)F\s*\),\s*(?:AnimationChannel\.)?Interpolations\.(\w+)\)', kfs):
                x, y, z = float(x), float(y), float(z)
                if kind == "degreeVec":
                    v = [R(x), R(y), R(z)]
                else:  # posVec invierte y
                    v = [x, -y, z]
                ks.append({"t": float(t), "v": v, "i": interp})
            anim["bones"].setdefault(bone, []).append({"target": target, "kf": ks})
        out[name] = anim
    return out

def f(x):
    """float de Java."""
    s = repr(float(round(x, 6)))
    return s + "F"

def java_part(lines, spec, parent_var, depth):
    var = "p_" + spec["name"]
    cb = "CubeListBuilder.create()"
    if spec["mirror"]:
        cb += ".mirror()"
    for (u, v, x, y, z, w, h, d) in spec["cubes"]:
        cb += f".texOffs({u}, {v}).addBox({f(x)}, {f(y)}, {f(z)}, {f(w)}, {f(h)}, {f(d)})"
    px, py, pz = spec["pivot"]
    rx, ry, rz = spec["rot"]
    pose = f"PartPose.offsetAndRotation({f(px)}, {f(py)}, {f(pz)}, {f(rx)}, {f(ry)}, {f(rz)})"
    ind = "        " + "    " * depth
    lines.append(f'{ind}PartDefinition {var} = {parent_var}.addOrReplaceChild("{spec["name"]}", {cb}, {pose});')
    for ch in spec["children"]:
        java_part(lines, ch, var, depth + 1)

def java_files(pkg):
    lines = []
    for ch in classic["children"]:
        java_part(lines, ch, "root", 0)
    model = f"""package {pkg};

import net.minecraft.client.model.geom.PartPose;
import net.minecraft.client.model.geom.builders.CubeListBuilder;
import net.minecraft.client.model.geom.builders.LayerDefinition;
import net.minecraft.client.model.geom.builders.MeshDefinition;
import net.minecraft.client.model.geom.builders.MeshTransformer;
import net.minecraft.client.model.geom.builders.PartDefinition;

/**
 * Conejo de 1.12.2 armado con los mismos nombres de partes que el conejo de 26.3,
 * para que las animaciones de 26.3 (salto y pararse en dos patas) se le apliquen.
 * Archivo generado por rabbit_spec.py: no editar a mano.
 */
@SuppressWarnings("unused")
public final class ClassicRabbitModel {{
    private ClassicRabbitModel() {{}}

    /** 1.12.2 dibujaba al conejo adulto al 60 %. */
    public static final float SCALE = {f(CLASSIC_SCALE)};

    public static LayerDefinition createBodyLayer() {{
        MeshDefinition mesh = new MeshDefinition();
        PartDefinition root = mesh.getRoot();
{chr(10).join(lines)}
        return LayerDefinition.create(mesh, 64, 32).apply(MeshTransformer.scaling(SCALE));
    }}
}}
"""
    rules = []
    for (anim, bone, target), lst in ADAPT.items():
        for dst, fac in lst:
            rules.append(f'        new Rule("{anim}", "{bone}", "{target}", "{dst}", {f(fac)}),')
    adapt = f"""package {pkg};

import java.util.List;

/**
 * Ajustes de las animaciones de 26.3 para el modelo clasico.
 * Archivo generado por rabbit_spec.py: no editar a mano.
 */
public final class ClassicRabbitAdaptRules {{
    private ClassicRabbitAdaptRules() {{}}

    /** Canal (animacion, hueso, tipo) que se reasigna a otro hueso con un factor. */
    public record Rule(String animation, String bone, String target, String newBone, float factor) {{}}

    public static final List<Rule> RULES = List.of(
{chr(10).join(rules).rstrip(',')}
    );
}}
"""
    return model, adapt

def main(anim_src, out_dir, baby_anim_src=None, baby_spec_json=None):
    pkg = "com.nikitomiamor.classicrabbits"
    model, adapt = java_files(pkg)
    jdir = os.path.join(out_dir, "java")
    os.makedirs(jdir, exist_ok=True)
    open(os.path.join(jdir, "ClassicRabbitModel.java"), "w", encoding="utf-8", newline="\n").write(model)
    open(os.path.join(jdir, "ClassicRabbitAdaptRules.java"), "w", encoding="utf-8", newline="\n").write(adapt)
    anims = parse_anims(anim_src)
    data = {"vanilla": vanilla, "classic": classic, "classicScale": CLASSIC_SCALE, "anims": anims,
            "adapt": [[k[0], k[1], k[2], t] for k, t in ADAPT.items()]}
    if baby_anim_src and baby_spec_json:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from to_bbmodel import baby_26  # bebe vanilla 26.3, como referencia
        for name, anim in parse_anims(baby_anim_src).items():
            anims["BABY_" + name] = anim
        data["babyVanilla"] = baby_26
        data["babyClassic"] = json.load(open(baby_spec_json, encoding="utf-8"))
    os.makedirs(os.path.join(out_dir, "viewer"), exist_ok=True)
    with open(os.path.join(out_dir, "viewer", "data.js"), "w", encoding="utf-8") as f:
        f.write("window.DATA = " + json.dumps(data) + ";\n")
    print("anims:", {k: (v["length"], v["looping"], len(v["bones"])) for k, v in anims.items()})

if __name__ == "__main__":
    main(*sys.argv[1:5])
