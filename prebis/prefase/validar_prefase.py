"""Comprobaciones obligatorias de las listas de la prefase contra la base de datos de AzerothCore.

Uso: python3 validar_prefase.py <carpeta con bis_prefase.json y Bistooltip_prefase_bislists.lua>

1. Cada ID de objeto existe en item_template y su InventoryType corresponde al hueco (slot_name).
2. Cada encantamiento existe: su fórmula/pergamino/objeto está en item_template o un instructor enseña el hechizo.
3. Ningún objeto sale de Karazhan, Gruul, Magtheridon, bandas posteriores, jefes de mundo, Bancal del Magister o
   Rasganorte: debe tener al menos una fuente permitida y se listan las rechazadas.
4. Ninguna receta pide materiales de banda (reactivos de AtlasLoot Classic).
5. La armadura la puede llevar la clase al 70 y las armas las puede usar la especialización.
6. Ningún objeto pide nivel superior a 70.
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from ac_index import Index
from fuentes import Fuentes, SLOT_INV
from specs import SPECS, CLASS, GEM_LIST, METAS

# Off hand admite armas de dos manos (17) por Agarre de titán del guerrero Furia.
LUA_SLOT_INV = {"Head": {1}, "Neck": {2}, "Shoulder": {3}, "Back": {16}, "Chest": {5, 20}, "Wrist": {9},
                "Hands": {10}, "Waist": {6}, "Legs": {7}, "Feet": {8}, "Finger": {11}, "Trinket": {12},
                "Weapon": {13, 17, 21}, "Off hand": {14, 22, 23, 13, 17}, "Relic": {28}, "Ranged": {15, 25, 26}}
CLASS_EN = {"Death knight", "Druid", "Hunter", "Mage", "Paladin", "Priest", "Rogue", "Shaman", "Warlock", "Warrior"}


def main():
    out = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
    data = json.loads((out / "bis_prefase.json").read_text())["especializaciones"]
    lua = (out / "Bistooltip_prefase_bislists.lua").read_text()
    ix = Index()
    f = Fuentes(ix)
    errors, checked = [], {"objetos": 0, "encantamientos": 0, "gemas": 0, "entradas_lua": 0}

    def err(msg):
        errors.append(msg)

    # --- Lua: formato y huecos ---
    for m in re.finditer(r'Bistooltip_prefase_bislists\["([^"]+)"\]\["([^"]+)"\]\["PreFase"\]\[\d+\] = '
                         r'\{ \["slot_name"\] = "([^"]+)", \["enhs"\] = \{(.*?)\}, (\[1\].*?) \};', lua):
        cls, spec, slot, enhs, items = m.groups()
        checked["entradas_lua"] += 1
        if cls not in CLASS_EN:
            err(f"Lua: clase desconocida {cls}")
        if slot not in LUA_SLOT_INV:
            err(f"Lua: hueco desconocido {slot}")
        ids = [int(x) for x in re.findall(r"\[\d\] = (-?\d+)", items)]
        if len(ids) != 6:
            err(f"Lua {cls}/{spec}/{slot}: {len(ids)} objetos en vez de 6")
        for e in ids:
            if e < 0:
                continue
            it = ix.items.get(e)
            if not it:
                err(f"Lua {cls}/{spec}/{slot}: el objeto {e} no existe en item_template")
            elif it["InventoryType"] not in LUA_SLOT_INV[slot]:
                err(f"Lua {cls}/{spec}/{slot}: {e} tiene InventoryType {it['InventoryType']}")
        for t, v in re.findall(r'\["type"\] = "(\w+)", \["id"\] = (\d+)', enhs):
            v = int(v)
            if t == "item" and v not in ix.items:
                err(f"Lua {cls}/{spec}/{slot}: mejora {v} no existe en item_template")
            if t == "spell" and v not in ix.trainer_spells and not f.recipes_for_spell.get(v):
                err(f"Lua {cls}/{spec}/{slot}: hechizo {v} sin instructor ni fórmula en AzerothCore")
            if t == "none" and v != 0:
                err(f"Lua {cls}/{spec}/{slot}: 'none' con id {v}")

    # --- JSON: objetos, fuentes, clase, nivel ---
    for key, d in data.items():
        cls, spec = key.split("/")
        sp = SPECS[(cls, spec)]
        c = CLASS[sp["class"]]
        for group in ("huecos", "insignias"):
            for slot, lst in d[group].items():
                for x in lst:
                    checked["objetos"] += 1
                    e = x["id"]
                    it = ix.items.get(e)
                    tag = f"{key} {slot} {e}"
                    if not it:
                        err(f"{tag}: no existe en item_template")
                        continue
                    if it["InventoryType"] not in LUA_SLOT_INV[slot]:
                        err(f"{tag}: InventoryType {it['InventoryType']} no corresponde a {slot}")
                    if it["RequiredLevel"] > 70:
                        err(f"{tag}: pide nivel {it['RequiredLevel']}")
                    if it["AllowableClass"] not in (-1, 0) and not it["AllowableClass"] & c["mask"]:
                        err(f"{tag}: no lo puede usar la clase")
                    if it["class"] == 4 and it["InventoryType"] in (1, 3, 5, 20, 6, 7, 8, 9, 10) \
                            and it["subclass"] not in c["armor"]:
                        err(f"{tag}: armadura de tipo {it['subclass']} que la clase no lleva")
                    if it["class"] == 2 and it["subclass"] not in c["weapons"]:
                        err(f"{tag}: arma de tipo {it['subclass']} que la clase no usa")
                    ok, bad = f.check(e)
                    if not ok:
                        err(f"{tag}: sin fuente permitida ({', '.join(sorted(bad))})")
                    if group == "huecos" and ok and all(s[0] == "insignias" for s in ok):
                        err(f"{tag}: solo insignias pero está en la lista principal")
                    cs = f.craft_spell.get(e)
                    if cs and any(s[0] == "profesión" for s in ok) and f.reagents_bad(cs[0]):
                        err(f"{tag}: receta con materiales de banda {f.reagents_bad(cs[0])}")
        # encantamientos
        for slot, ens in d["encantamientos"].items():
            for en in ens:
                checked["encantamientos"] += 1
                sp_id = en["spell"]
                exists = sp_id in ix.trainer_spells or bool(f.recipes_for_spell.get(sp_id)) or \
                    (en["item"] in ix.items and any(ix.items[en["item"]][f"spellid_{i}"] == sp_id for i in range(1, 6)))
                if not exists and en["item"] not in ix.items:
                    err(f"{key} encantamiento {en['nombre']} ({sp_id}): no se encuentra en AzerothCore")
                pr = f.prof.get(sp_id)
                if pr and pr[2] > 375:
                    err(f"{key} encantamiento {en['nombre']}: pide {pr[2]} de habilidad")
                if pr and f.reagents_bad(sp_id):
                    err(f"{key} encantamiento {en['nombre']}: materiales de banda {f.reagents_bad(sp_id)}")
        # gemas
        for gid in {g for v in d["gemas"]["por_objeto"].values() for g in v} | {d["gemas"]["meta"]["id"]}:
            checked["gemas"] += 1
            if gid not in ix.items:
                err(f"{key}: la gema {gid} no existe en item_template")
            name = GEM_LIST.get(gid, METAS.get(gid, {})).get("name")
            designs = [e for e, it in ix.items.items() if it["name"] == f"Design: {name}"]
            if not any(f.check(dsg)[0] for dsg in designs):
                err(f"{key}: la gema {gid} ({name}) no tiene diseño conseguible en la prefase")
    print("Comprobado:", ", ".join(f"{v} {k}" for k, v in checked.items()))
    if errors:
        print(f"{len(errors)} problemas:")
        for e in errors:
            print(" -", e)
        sys.exit(1)
    print("Sin problemas: todos los ID existen, los huecos coinciden, las fuentes son de la prefase, sin materiales "
          "de banda, la clase puede usar cada objeto y nada pide nivel superior a 70.")


if __name__ == "__main__":
    main()
