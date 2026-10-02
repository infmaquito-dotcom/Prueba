# Listas BiS de la PreFase (TBC en servidor 3.3.5a)

Generador de las listas de la prefase a partir de la base de datos de AzerothCore.

Necesita en `/tmp/claude-0` (o en `PREBIS_FUENTES` / `AC_DB`):
- `ac/data/sql/base/db_world/*.sql` de azerothcore-wotlk (item_template, *_locale, creature*, *_loot_template,
  gameobject*, npc_vendor, quest_template, creature_queststarter, gameobject_queststarter, trainer_spell)
- `wswotlk/` (wowsims/wotlk), `wstbc/` (wowsims/tbc), `alc/` (AtlasLootClassic, GPL-2)

```
python3 prefase.py salida                    # todas las especializaciones de specs.py
python3 prefase.py salida Paladin/Retribution
python3 validar_prefase.py salida            # comprobaciones obligatorias
```

Archivos: `ac_sql.py` (lee los volcados SQL), `ac_index.py` (fuentes de cada objeto), `fuentes.py` (reglas de la
prefase), `modelo.py` (índices de combate al 70, topes, efectos), `specs.py` (clases, pesos, talentos, gemas),
`prefase.py` (elección), `emitir.py` (los cuatro entregables), `validar_prefase.py`.
