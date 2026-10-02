# Cómo se generan las tablas de pre-BiS

`compilar_prebis.py` junta tres cosas:

1. **Qué objetos van en cada ranura.** La fase `PreRaid` de `Bistooltip_wowtbc_bislists.lua` del addon
   [BiS-Tooltip backport TBC 3.3.5a](https://github.com/boegi1/BiS-Tooltip_335a_backport_TBC), armada con las listas
   de Wowhead/wowtbc.gg. Hasta 6 opciones por ranura, de la mejor a la alternativa.
2. **De dónde sale cada objeto.** En este orden:
   [AtlasLoot Classic](https://github.com/Hoizame/AtlasLootClassic) (mazmorras, jefes, heroicas, profesiones,
   reputaciones, insignias, JcJ), [Questie v9.0.0](https://github.com/Questie/Questie/tree/v9.0.0/Database/TBC)
   (misiones, vendedores, botín de PNJ), `tooltips_wowhead.json` (el «Dropped by» de los tooltips de Wowhead que
   publica [wowsims/wotlk](https://github.com/wowsims/wotlk)) y `fuentes_manual.json` (casos revisados a mano).
3. **Nombre y fase de cada objeto.** `sim/core/items/all_items.go` de [wowsims/tbc](https://github.com/wowsims/tbc).
   Un objeto o receta de fase 2 o posterior se marca como no obtenible antes de las bandas.

Para regenerar, clona esos repos en una carpeta con estos nombres y ejecuta:

```
fuentes/
  BiS-Tooltip_335a_backport_TBC/   alc/ (AtlasLootClassic)   wstbc/ (wowsims/tbc)
  qdb/ (tbcItemDB.lua, tbcQuestDB.lua, tbcNpcDB.lua de Questie v9.0.0)
  questie/ExternalScripts(DONOTINCLUDEINRELEASE)/DBC - WoW.tools/areatable_tbc.csv
  bistracker/ (Zentarg/bistracker, solo para nombres de respaldo)

PREBIS_FUENTES=fuentes python3 compilar_prebis.py ..
```

## Versión con la base de datos WotLK

`compilar_prebis_wotlk.py` genera `prebis_wotlk_nivel70.md/.csv` para un servidor WotLK con tope en 70 y bandas cerradas: puntúa todos
los objetos de TBC que no salen de bandas (incluidos Bancal del Magister y Quel'Danas, marcados) con sus estadísticas de WotLK 3.3.5
(`assets/database/*.json` de [wowsims/wotlk](https://github.com/wowsims/wotlk), sacadas de Wowhead WotLK) y los pesos
de estadísticas de cada especialización de wowsims WotLK, con el golpe valorado antes del tope y el maná por 5 para
sanadores. Necesita además `wswotlk/` (wowsims/wotlk) en la carpeta de fuentes y reutiliza `compilar_prebis.py`.
