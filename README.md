# Classic Rabbits

A client-side Fabric mod for Minecraft 26.3: rabbits use the classic model and textures with the 26.3 animations, and baby rabbits use a custom model made in Blockbench that blends the classic baby with the new one. It only changes how they look; behaviour stays vanilla.

## Download
Get the `.jar` from [Releases](../../releases). Requires Fabric Loader 0.20+.

## Building
```bash
./build.sh
```
Compiles with `javac` against the 26.3 game jar and the libraries installed by the Modrinth App (see the variables at the top of `build.sh`). The jar ends up in `build/libs/`.

`tools/` holds the scripts that generate the geometry (`rabbit_spec.py`, `from_bbmodel.py`) and a three.js viewer (`tools/viewer`, serve it over http; drop the 26.3 and classic rabbit textures in `tools/viewer/tex/` to see them textured); `blockbench/` holds the source models.

## License
[LGPL-3.0](COPYING.LESSER) (it builds on the [GPL-3.0](COPYING)).
