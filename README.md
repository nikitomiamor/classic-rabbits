# Classic Rabbits

A client-side Fabric mod for Minecraft 26.3: rabbits use the 1.12.2 model and textures with the 26.3 animations. It only changes how they look; behaviour stays vanilla.

## Download
Get the `.jar` from [Releases](../../releases). Requires Fabric Loader 0.20+.

## Building
```bash
./build.sh
```
Compiles with `javac` against the 26.3 game jar and the libraries installed by the Modrinth App (see the variables at the top of `build.sh`). The jar ends up in `build/libs/`.

`tools/` holds the scripts that generate the geometry (`rabbit_spec.py`, `from_bbmodel.py`) and a three.js viewer; `blockbench/` holds the source models.
