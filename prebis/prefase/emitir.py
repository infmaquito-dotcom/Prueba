"""Escribe los cuatro entregables a partir de los datos de cada especialización."""
import json
import re
from pathlib import Path

from specs import SPECS, CLASS, GEM_LIST, METAS

SLOTS_LUA = ["Head", "Neck", "Shoulder", "Back", "Chest", "Wrist", "Hands", "Waist", "Legs", "Feet", "Finger",
             "Trinket", "Weapon", "Off hand", "Relic", "Ranged"]
CLASS_ORDER = ["Death knight", "Druid", "Hunter", "Mage", "Paladin", "Priest", "Rogue", "Shaman", "Warlock", "Warrior"]
SLOT_ES = {"Head": "Cabeza", "Neck": "Cuello", "Shoulder": "Hombros", "Back": "Espalda", "Chest": "Pecho",
           "Wrist": "Muñecas", "Hands": "Manos", "Waist": "Cintura", "Legs": "Piernas", "Feet": "Pies",
           "Finger": "Anillos", "Trinket": "Abalorios", "Weapon": "Arma", "Off hand": "Mano izquierda",
           "Relic": "Reliquia", "Ranged": "A distancia"}
# nombres de la lista original (Bistooltip wowtbc) -> huecos de esta lista
TBC_SLOT = {"Head": "Head", "Neck": "Neck", "Shoulders": "Shoulder", "Back": "Back", "Chest": "Chest",
            "Wrist": "Wrist", "Hands": "Hands", "Waist": "Waist", "Legs": "Legs", "Feet": "Feet", "Rings": "Finger",
            "Trinkets": "Trinket", "2HandedWeapons": "Weapon", "MainHand": "Weapon", "1HandedWeapons": "Weapon",
            "Weapons": "Weapon", "OffHand": "Off hand", "Shields": "Off hand", "Librams": "Relic", "Idols": "Relic",
            "Totems": "Relic", "Ranged": "Ranged", "Wands": "Ranged"}

ALC = Path("/tmp/claude-0/alc/AtlasLootClassic/Data/VendorPrice.lua")
PRICES = {}
if ALC.exists():
    for m in re.finditer(r'\[(\d+)\] = "BoJ:(\d+)"', ALC.read_text()):
        PRICES[int(m.group(1))] = int(m.group(2))


def lua_str(s):
    return '"' + str(s).replace("\\", "\\\\").replace('"', '\\"') + '"'


def enhs_for(d, slot):
    """Gemas (item), encantamiento (spell o item) y ranuras vacías (none) del primer objeto del hueco."""
    out = []
    lst = d["huecos"].get(slot) or []
    if not lst:
        return out
    top = lst[0]
    gems = d["gemas"]["por_objeto"].get(str(top["id"]), [])
    gi = iter(gems)
    for color in top["ranuras"]:
        if color == "meta":
            out.append(("item", d["gemas"]["meta"]["id"]))
        else:
            g = next(gi, None)
            out.append(("item", g) if g else ("none", 0))
    ens = d["encantamientos"].get(slot) or []
    if ens:
        en = ens[0]
        if en["item"] and not en["comprobacion"].startswith(("Instructor", "Fórmula")):
            out.append(("item", en["item"]))
        else:
            out.append(("spell", en["spell"]))
    return out


def write_lua_lists(all_data, path):
    L = ["-- Listas BiS de la PreFase de TBC para servidores 3.3.5a (AzerothCore). Generado por prefase.py.",
         "Bistooltip_prefase_bislists = {};"]
    present = [c for c in CLASS_ORDER if any(k[0] == c for k in all_data)]
    for c in present:
        L.append(f'Bistooltip_prefase_bislists[{lua_str(c)}] = {{}};')
    L.append("Bistooltip_prefase_classes = {};")
    for n, c in enumerate(present, 1):
        specs = [k[1] for k in all_data if k[0] == c]
        inner = ",\n".join(f"    [{i}] = {lua_str(s)}" for i, s in enumerate(specs, 1))
        L.append(f'Bistooltip_prefase_classes[{n}] = {{ ["name"] = {lua_str(c)}, ["specs"] = {{ \n{inner}\n}}}};')
    L.append('Bistooltip_prefase_phases = { "PreFase" };')
    for (c, s), d in all_data.items():
        base = f'Bistooltip_prefase_bislists[{lua_str(c)}][{lua_str(s)}]'
        L.append(f"{base} = {{}};")
        L.append(f'{base}["PreFase"] = {{}};')
        i = 0
        for slot in SLOTS_LUA:
            if slot not in d["huecos"]:
                continue
            i += 1
            ids = [x["id"] for x in d["huecos"][slot][:6]]
            ids += [-1] * (6 - len(ids))
            enh = ", ".join(f'[{j}] = {{ ["type"] = "{t}", ["id"] = {v} }}'
                            for j, (t, v) in enumerate(enhs_for(d, slot), 1))
            items = ", ".join(f"[{j}] = {v}" for j, v in enumerate(ids, 1))
            L.append(f'{base}["PreFase"][{i}] = {{ ["slot_name"] = {lua_str(slot)}, ["enhs"] = {{ {enh} }}, {items} }};')
    Path(path).write_text("\n".join(L) + "\n", encoding="utf-8")


def source_pairs(x, badge=False):
    """Pares (instance, boss) en el formato del archivo de fuentes."""
    out = []
    if badge:
        price = PRICES.get(x["id"])
        out.append(("Insignias de justicia", f"G'eras ({price} insignias)" if price else "G'eras"))
        return out
    if x.get("reputacion"):
        out.append((f"Reputación: {x['reputacion']['faccion_en']}", x["reputacion"]["nivel"]))
    for f in x["fuentes"]:
        cat, inst, boss = f["categoria"], f["instancia"], f["jefe"]
        if cat == "profesión":
            recipe = boss.split(" — ")[0]
            out.append((inst, recipe.replace("Pattern:", "Patrón:").replace("Plans:", "Diseño:")
                        .replace("Design:", "Boceto:").replace("Formula:", "Fórmula:").replace("Schematic:", "Esquema:")))
        elif cat == "vendedor" and x.get("reputacion"):
            continue
        else:
            out.append((inst, boss))
    return out[:4]


def write_lua_sources(all_data, path):
    L = ["-- Fuentes de cada objeto de las listas de la PreFase (AzerothCore 3.3.5a). Generado por prefase.py.",
         "ResolvedSources = ResolvedSources or {}"]
    done = set()
    for d in all_data.values():
        for badge, group in ((False, d["huecos"]), (True, d["insignias"])):
            for slot, lst in group.items():
                for x in lst:
                    if x["id"] in done:
                        continue
                    done.add(x["id"])
                    pairs = ", ".join(f"{{ instance={lua_str(i)}, boss={lua_str(b)} }}" for i, b in source_pairs(x, badge))
                    L.append(f"if not ResolvedSources[{x['id']}] then ResolvedSources[{x['id']}] = {{ {pairs} }} end")
    Path(path).write_text("\n".join(L) + "\n", encoding="utf-8")


def write_json(all_data, path):
    out = {"descripcion": "Listas BiS de la PreFase de TBC (servidor 3.3.5a, nivel 70). Generado por prefase.py.",
           "fuentes_de_datos": {
               "azerothcore": "azerothcore-wotlk, data/sql/base/db_world: item_template, item_template_locale, "
                              "creature_template(+locale), creature, creature_loot_template, reference_loot_template, "
                              "gameobject(+template, loot), item_loot_template, npc_vendor, quest_template(+locale), "
                              "creature_queststarter, gameobject_queststarter, trainer_spell",
               "wowsims_wotlk": "pesos de nivel 80 (ui/<spec>/sim.ts), bonificaciones de ranura y estadísticas de "
                                "encantamientos (assets/database/db.json), tooltips WotLK (db_inputs)",
               "wowsims_tbc": "fase original de cada objeto (sim/core/items/all_items.go), solo orientación",
               "atlasloot_classic": "reactivos y habilidad de recetas (Data/Profession.lua) y precio en insignias "
                                    "(Data/VendorPrice.lua); licencia GPL-2",
               "questie": "no se usa"},
           "especializaciones": {f"{c}/{s}": d for (c, s), d in all_data.items()}}
    Path(path).write_text(json.dumps(out, ensure_ascii=False, indent=1, default=str), encoding="utf-8")


def _src_txt(x):
    f = x["fuentes"][0] if x["fuentes"] else {"instancia": "", "jefe": ""}
    t = f"{f['instancia']}: {f['jefe']}".strip(": ")
    if x.get("reputacion"):
        t = f"{x['reputacion']['faccion']} ({x['reputacion']['nivel']}) · " + t
    if x.get("banda_clasica"):
        t += " **[banda clásica]**"
    if x["fuentes"] and x["fuentes"][0]["categoria"] == "profesión" and x.get("ligado_al_recoger"):
        t += " (se liga al recogerlo: lo tiene que fabricar el propio jugador)"
    return t


def write_revision(all_data, path, validacion=None):
    L = ["# Revisión de las listas BiS de la PreFase (TBC en servidor 3.3.5a)", "",
         "Estas listas son para la prefase que abre el 3 de octubre de 2026: mazmorras de TBC de fase 1 en normal y "
         "heroico (sin Bancal del Magister), reputaciones y misiones de Terrallende, profesiones con recetas de esas "
         "fuentes, botín de mundo y todo el contenido clásico. No entran bandas de TBC, Kazzak, Caminante del Destino, "
         "Rasganorte ni recetas con materiales de banda.", "",
         "Cómo leerlas: en cada hueco el objeto 1 es el mejor. **EP** es una puntuación en «puntos de poder de ataque» "
         "(o de poder con hechizos para lanzadores): cuanto más alto, mejor para esa especialización. Los objetos de "
         "insignias de justicia van en una lista aparte porque en el TBC original se vendían por fases.", "",
         "Datos: AzerothCore (azerothcore-wotlk) para objetos, botín, vendedores y misiones; pesos de wowsims WotLK "
         "adaptados al nivel 70; fases originales de wowsims TBC; recetas y precios en insignias de AtlasLoot Classic "
         "(GPL-2). No se ha usado Questie.", ""]
    for (c, s), d in all_data.items():
        L += [f"## {d['clase_es']} {d['spec_es']}", ""]
        # tabla de cambios
        L += ["### Qué cambia respecto a la lista PreRaid original del TBC", "",
              "| Hueco | Lista original del TBC | Prefase 3.3.5 (esta lista) | Por qué |", "|---|---|---|---|"]
        for slot in SLOTS_LUA:
            cmp = d["comparacion"].get(slot)
            if not cmp:
                continue
            o = cmp["original"][0] if cmp["original"] else None
            n = cmp["prefase"][0] if cmp["prefase"] else None
            if not o or not n:
                continue
            if o["id"] == n["id"]:
                why = "Se mantiene."
            elif o["estado"] == "fuera":
                why = f"El original no vale en la prefase: {o.get('motivo', '')}."
            elif o["estado"] == "insignias":
                why = "El original se compra con insignias: está en la lista de insignias."
            elif o["estado"] in ("sigue", "baja"):
                pos = f"queda en el puesto {o['puesto']}" if o.get("puesto") else "queda fuera de los 6 primeros"
                why = (f"Con las estadísticas de 3.3.5a el nuevo puntúa más ({n['ep']} frente a {o.get('ep')} EP); "
                       f"el original {pos}.")
            else:
                why = o["estado"]
            L.append(f"| {SLOT_ES[slot]} | {o.get('nombre', o['id'])} ({o['id']}) | {n['nombre']} ({n['id']}) | {why} |")
        L.append("")
        # lista completa
        L += ["### Lista por hueco", "", "| Hueco | # | Objeto | ID | Dónde | Bando | EP |", "|---|---|---|---|---|---|---|"]
        for slot in SLOTS_LUA:
            for i, x in enumerate(d["huecos"].get(slot, []), 1):
                L.append(f"| {SLOT_ES[slot] if i == 1 else ''} | {i} | {x['nombre_es']} ({x['nombre_en']}) | {x['id']} | "
                         f"{_src_txt(x)} | {x['faccion']} | {x['ep']} |")
        L.append("")
        L += ["### Objetos de insignias de justicia (lista aparte)", "",
              "| Hueco | Objeto | ID | Precio en el TBC original | Fase en que se vendía | EP |", "|---|---|---|---|---|---|"]
        for slot in SLOTS_LUA:
            for x in d["insignias"].get(slot, [])[:3]:
                ph = x["fase_tbc_original"]
                L.append(f"| {SLOT_ES[slot]} | {x['nombre_es']} | {x['id']} | {PRICES.get(x['id'], '?')} | "
                         f"{'fase ' + str(ph) if ph else 'sin dato'} | {x['ep']} |")
        L.append("")
        # gemas
        g = d["gemas"]
        req = g["meta"]["requisito"]
        req_txt = ", ".join(f"{n} {dict(R='rojas', Y='amarillas', B='azules')[c]}" for c, n in req.get("min", {}).items())
        if "more" in req:
            req_txt = f"más {req['more'][0]} que {req['more'][1]}"
        L += ["### Gemas, meta y encantamientos", "",
              f"- **Meta:** {g['meta']['nombre']} ({g['meta']['id']}). Requisito en 3.3.5a: al menos {req_txt}. "
              f"Con las gemas propuestas se tienen {g['meta']['colores_conseguidos']['R']} rojas, "
              f"{g['meta']['colores_conseguidos']['Y']} amarillas y {g['meta']['colores_conseguidos']['B']} azules "
              f"(las naranjas y moradas cuentan para dos colores). Diseño: {g['meta']['fuente']}."]
        if g["meta"].get("valor_extra"):
            L.append(f"  - Valor de su efecto: {g['meta']['valor_extra'][1]}.")
        if g["alternativas_meta"]:
            L.append("  - Alternativas: " + ", ".join(f"{a['nombre']} ({a['id']})" for a in g["alternativas_meta"]) + ".")
        used = sorted({x for v in g["por_objeto"].values() for x in v})
        L.append("- **Gemas usadas:** " + ", ".join(f"{GEM_LIST[x]['name']} ({x})" for x in used) + ".")
        L.append("- **Gemas sin diseño en la prefase:** " + ", ".join(
            f"{v['nombre']} ({k})" for k, v in g["gemas_excluidas"].items()) + " (diseños de la Ofensiva Sol Devastado, fase 5).")
        L.append("- **Encantamientos:**")
        for slot, ens in d["encantamientos"].items():
            if ens:
                e = ens[0]
                L.append(f"  - {SLOT_ES[slot]}: {e['nombre']} (hechizo {e['spell']}"
                         + (f", objeto {e['item']}" if e["item"] else "") + f"). {e['comprobacion']}.")
        L.append("")
        # topes y pesos
        L += ["### Topes al nivel 70 contra un jefe de nivel 73 (reglas de WotLK)", ""]
        for k, v in d["topes"].items():
            L.append(f"- {k}: {v['cálculo']}.")
        tot = d["totales_equipo"]
        L.append(f"- Con el equipo 1 de cada hueco, gemas y encantamientos: {round(tot.get('HIT', 0))} de golpe y "
                 f"{round(tot.get('EXP', 0))} de pericia.")
        L += ["", "### Pesos (EP) al nivel 70", "",
              f"Pesos de wowsims WotLK (nivel 80) adaptados: factor de los índices = 2,079 x "
              f"({d['pesos']['referencia']['stat']} al 70 / al 80) = 2,079 x {d['pesos']['referencia']['70']} / "
              f"{d['pesos']['referencia']['80']} = {d['pesos']['factor_indices']}. Las estadísticas primarias, el poder "
              f"de ataque y el DPS del arma no cambian.", ""]
        L += ["| Estadística | Nivel 80 (wowsims) | Nivel 70 | Usado para ordenar |", "|---|---|---|---|"]
        for k, v in d["pesos"]["nivel_80_wowsims"].items():
            L.append(f"| {k} | {v:.2f} | {d['pesos']['nivel_70'][k]:.2f} | {d['pesos']['nivel_70_para_ordenar'][k]:.2f} |")
        L += ["", "El peso del golpe «usado para ordenar» sale de probar varios pesos y quedarse con el que da el mejor "
                  "equipo real teniendo en cuenta el tope (el golpe sobrante apenas vale).",
              "", "**Confianza:** media. Los pesos de wowsims están calculados al 80 con equipo de banda; al 70 el "
                  "reparto entre estadísticas es parecido, pero los efectos de abalorios y encantamientos con "
                  "probabilidad son estimaciones con las suposiciones que se indican en bis_prefase.json.", ""]
        t = d["talentos"]
        L += ["### Talentos (61 puntos) y glifos", "", f"Reparto {t['reparto']}.", ""] + [f"- {x}" for x in t["texto"]]
        L += ["", t["razon"], "", t.get("golpe_pericia", ""), ""]
        for gl in d["glifos"]:
            L.append(f"- {gl['tipo']}: {gl['nombre_es'] or gl['nombre_en']} ({gl['id']}): {gl['efecto']}.")
        L += ["", "Glifos: " + d["glifos"][0]["nota"] if d["glifos"] else "", ""]
    L += ["## Lo que no se pudo comprobar", "",
          "- **Especializaciones de profesión:** «Instructor (375)» significa que la receta la enseña un instructor. "
          "Algunas (Coraza/Baluarte de reyes, Campeón corazón de león, piezas de escamas abisales) exigen además una "
          "especialización (forjador de armaduras, maestro espadero, peletero de escamas de dragón...). Sin Spell.dbc "
          "no se puede leer qué especialización pide cada una.",
          "- **Hechizos (Spell.dbc):** AzerothCore no incluye los DBC del cliente. Que un encantamiento existe se "
          "comprueba porque su fórmula, pergamino u objeto está en item_template o su hechizo lo enseña un instructor "
          "(trainer_spell); sus estadísticas vienen de wowsims WotLK. Los reactivos de las recetas salen de AtlasLoot "
          "Classic, no de AzerothCore.",
          "- **Costes de vendedor (ItemExtendedCost.dbc):** tampoco está en AzerothCore. Los precios en insignias son "
          "los del TBC original (AtlasLoot) y pueden ser distintos en el servidor.",
          "- **Naxxramas de nivel 60:** en 3.3.5a el mapa 533 es la Naxxramas de nivel 80 y AzerothCore no tiene botín "
          "de la versión clásica, así que sus objetos no aparecen aunque el gremio los tenga.",
          "- **Jefes invocados por guion** (Ciénaga Negra, Antiguas Laderas, Arcatraz, Avatar de los Martirizados, "
          "Porung): no tienen aparición en la tabla creature; su mazmorra se ha puesto a mano.",
          "- **Glifos:** se comprueba que el objeto existe, no qué tinta necesita.",
          "- **Fases:** la fase original de cada objeto viene de wowsims TBC (solo orientación); los diseños de gemas "
          "de la Ofensiva Sol Devastado (Quel'Danas, fase 5) se excluyen.", ""]
    if validacion:
        L += ["## Resultado del script de comprobación", "", "```", validacion.strip(), "```", ""]
    Path(path).write_text("\n".join(L), encoding="utf-8")
