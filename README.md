# Classic Rabbits

Mod de Fabric (solo cliente) para Minecraft 26.3: los conejos usan el modelo y las texturas de la 1.12.2 con las animaciones de 26.3. Solo cambia cómo se ven; el comportamiento es el de vanilla.

## Descarga
El `.jar` está en [Releases](../../releases). Requiere Fabric Loader 0.20+.

## Compilar
```bash
./build.sh
```
Compila con `javac` contra el jar de 26.3 y las librerías que instala Modrinth (ver variables al principio de `build.sh`). El jar sale en `build/libs/`.

`tools/` tiene los scripts que generan la geometría (`rabbit_spec.py`, `from_bbmodel.py`) y un visor three.js; `blockbench/` los modelos fuente.
