#!/usr/bin/env python3
"""Compila el pre-BiS (fase PreRaid) de TBC por clase/spec y le añade la fuente de cada objeto.

Uso: PREBIS_FUENTES=<carpeta con los repos de origen> python3 compilar_prebis.py <carpeta de salida>
Ver README.md en esta carpeta."""
import csv, json, os, re, sys, collections
from pathlib import Path

ROOT = Path(os.environ.get("PREBIS_FUENTES", "fuentes"))
BIS = ROOT / "BiS-Tooltip_335a_backport_TBC/Bistooltip_wowtbc_bislists.lua"
ALC = ROOT / "alc"
OUT = Path(sys.argv[1])

# ---------- Nombres y fase de objetos ----------
names, phase = {}, {}
for line in (ROOT / "wstbc/sim/core/items/all_items.go").read_text().splitlines():
    m = re.search(r'Name: "((?:[^"\\]|\\.)*)", ID: (\d+),.*?Phase: (\d+)', line)
    if m:
        names[int(m.group(2))] = m.group(1).replace('\\"', '"')
        phase[int(m.group(2))] = int(m.group(3))
for f in [ROOT / "bistracker/allitemsdata.json", *sorted((ROOT / "bistracker/AllItems").glob("*.json"))]:
    try:
        d = json.loads(f.read_text())
    except Exception:
        continue
    for k, v in d.items():
        if isinstance(v, dict) and "name_enus" in v:
            names.setdefault(int(k), v["name_enus"])

# ---------- Mazmorras y jefes (AtlasLoot) ----------
INST_ES = {
    "HellfireRamparts": "Murallas del Fuego Infernal", "TheBloodFurnace": "El Horno de Sangre",
    "TheShatteredHalls": "Las Salas Arrasadas", "Mana-Tombs": "Tumbas de Maná",
    "AuchenaiCrypts": "Criptas Auchenai", "SethekkHalls": "Salas Sethekk",
    "ShadowLabyrinth": "Laberinto de las Sombras", "TheSlavePens": "Recinto de los Esclavos",
    "TheUnderbog": "La Sotiénaga", "TheSteamvault": "La Cámara de Vapor",
    "OldHillsbradFoothills": "Antiguas Laderas de Trabalomas", "TheBlackMorass": "La Ciénaga Negra",
    "TheArcatraz": "El Arcatraz", "TheBotanica": "El Invernáculo", "TheMechanar": "El Mechanar",
    "MagistersTerrace": "Bancal del Magister", "Karazhan": "Karazhan", "ZulAman": "Zul'Aman",
    "WorldBossesBC": "Jefe de mundo", "MagtheridonsLair": "Guarida de Magtheridon",
    "GruulsLair": "Guarida de Gruul", "SerpentshrineCavern": "Caverna Santuario Serpiente",
    "TempestKeep": "El Castillo de la Tempestad", "HyjalSummit": "Cima Hyjal",
    "BlackTemple": "Templo Oscuro", "SunwellPlateau": "Meseta de La Fuente del Sol",
}
RAIDS = {"Karazhan", "ZulAman", "WorldBossesBC", "MagtheridonsLair", "GruulsLair", "SerpentshrineCavern",
         "TempestKeep", "HyjalSummit", "BlackTemple", "SunwellPlateau"}
PROF_ES = {4: "Primeros auxilios", 5: "Herrería", 6: "Peletería", 7: "Alquimia", 9: "Cocina",
           10: "Minería", 11: "Sastrería", 12: "Ingeniería", 13: "Encantamiento", 17: "Joyería",
           18: "Inscripción"}


def lua_blocks(text, key_re):
    """Devuelve {clave: texto del bloque data["clave"] = { ... }}."""
    out = {}
    starts = [(m.group(1), m.start()) for m in re.finditer(r'^data\["([^"]+)"\] = \{', text, re.M)]
    for i, (k, s) in enumerate(starts):
        e = starts[i + 1][1] if i + 1 < len(starts) else len(text)
        out[k] = text[s:e]
    return out


# ---------- Reputaciones, insignias, JcJ ----------
FAC_ES = {
    "TheAldor": "Los Aldor", "TheScryers": "Los Arúspices", "TheShatar": "Los Sha'tar",
    "LowerCity": "Bajo Arrabal", "KeepersOfTime": "Vigilantes del Tiempo", "TheVioletEye": "El Ojo Violeta",
    "TheScaleOfTheSands": "La Escama de las Arenas", "CenarionExpedition": "Expedición Cenarion",
    "TheConsortium": "El Consorcio", "AshtongueDeathsworn": "Juramorte Lengua de Ceniza",
    "ShatteredSunOffensive": "Ofensiva Sol Devastado", "ShatariSkyguard": "Guardia del cielo Sha'tari",
    "Netherwing": "Ala Abisal", "Sporeggar": "Esporaggar", "Ogrila": "Ogri'la", "Tranquillien": "Tranquillien",
    "Thrallmar": "Thrallmar", "TheMaghar": "Los Mag'har", "HonorHold": "Bastión del Honor", "Kurenai": "Kurenai",
}
REP_ES = {"Exalted": "Exaltado", "Revered": "Reverenciado", "Honored": "Honorable", "Friendly": "Amistoso"}
fac_src = {}
fac = (ALC / "AtlasLootClassic_Factions/data-tbc.lua").read_text()
for k, block in lua_blocks(fac, None).items():
    if k == "DUMMY":
        continue
    level = None
    for line in block.splitlines():
        m = re.search(r'name = ALIL\["(Exalted|Revered|Honored|Friendly)"\]', line)
        if m:
            level = m.group(1)
        for it in re.findall(r'\{\s*\d+,\s*(\d+)', line):
            fac_src.setdefault(int(it), f"Reputación: {FAC_ES.get(k, k)} ({REP_ES.get(level, level or '?')})")

col = (ALC / "AtlasLootClassic_Collections/data-tbc.lua").read_text()
COL_ES = {"BadgeofJustice": "Insignias de Justicia (G'eras, Shattrath)",
          "BadgeofJustice4": "Insignias de Justicia (vendedor de fase 4)",
          "BadgeofJusticeP5": "Insignias de Justicia (vendedor de fase 5)",
          "BCCSunmote": "Motas de sol (fase 5)", "WorldEpicsBC": "Botín de mundo (épico aleatorio)"}
col_src = {}
for k, block in lua_blocks(col, None).items():
    if k in COL_ES:
        for it in re.findall(r'\{\s*\d+,\s*(\d+)', block):
            col_src.setdefault(int(it), COL_ES[k])

pvp = (ALC / "AtlasLootClassic_PvP/data-tbc.lua").read_text()
PVP_ES = {"HonorSetBCC": "Honor", "ReputationSetBCC": "Honor (conjunto de reputación)",
          "ArenaS1PvP": "Arena temporada 1", "ArenaS2PvP": "Arena temporada 2",
          "ArenaS3PvP": "Arena temporada 3", "ArenaS4PvP": "Arena temporada 4",
          "HellfirePeninsulaPvP": "JcJ de mundo: Península del Fuego Infernal (Marcas de Fuego Infernal)",
          "NagrandPvP": "JcJ de mundo: Nagrand (Halaa)", "TerokkarPvP": "JcJ de mundo: Terokkar (Fichas de Espíritu)",
          "ZangarmarshPvP": "JcJ de mundo: Marisma de Zangar"}
pvp_src = {}
for k, block in lua_blocks(pvp, None).items():
    if k in PVP_ES:
        for it in re.findall(r'\{\s*\d+,\s*(\d+)', block):
            pvp_src.setdefault(int(it), PVP_ES[k])

# ---------- Questie (misiones, vendedores, botín de PNJ) ----------
def lua_value(s, i=0):
    """Parser mínimo de literales de tabla Lua. Devuelve (valor, índice)."""
    while s[i] in " \t\n":
        i += 1
    c = s[i]
    if c == "{":
        i += 1; arr, dic, n = [], {}, 1
        while True:
            while s[i] in " \t\n,":
                i += 1
            if s[i] == "}":
                return (dic if dic else arr), i + 1
            if s[i] == "[":
                k, i = lua_value(s, i + 1)
                i = s.index("]", i) + 1
                i = s.index("=", i) + 1
                v, i = lua_value(s, i)
                dic[k] = v
            else:
                v, i = lua_value(s, i)
                arr.append(v); dic_n = n; n += 1
    if c in "'\"":
        j, out = i + 1, []
        while s[j] != c:
            if s[j] == "\\":
                j += 1
            out.append(s[j]); j += 1
        return "".join(out), j + 1
    m = re.match(r"-?[0-9.]+(?:e-?\d+)?|nil|true|false", s[i:])
    tok = m.group(0)
    val = None if tok == "nil" else tok == "true" if tok in ("true", "false") else (float(tok) if "." in tok or "e" in tok else int(tok))
    return val, i + len(tok)


def load_questie(name, wanted=None):
    out = {}
    for line in (ROOT / "qdb" / f"{name}.lua").read_text(encoding="utf-8", errors="replace").splitlines():
        m = re.match(r"^\[(\d+)\] = (\{.*\}),$", line)
        if m and (wanted is None or int(m.group(1)) in wanted):
            out[int(m.group(1))] = lua_value(m.group(2))[0]
    return out


AREA = {}
with open(ROOT / "questie/ExternalScripts(DONOTINCLUDEINRELEASE)/DBC - WoW.tools/areatable_tbc.csv", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        AREA[int(r["ID"])] = r["AreaName_lang"]
QDB = {}


def qget(lst, i):
    return lst[i - 1] if isinstance(lst, list) and len(lst) >= i else None


def questie_source(item):
    it = QDB["items"].get(item)
    if not it:
        return None
    quests = qget(it, 6) or []
    if quests:
        names_q = []
        for q in quests[:2]:
            qd = QDB["quests"].get(q)
            if qd:
                zone = qget(qd, 17)
                z = AREA.get(zone, "") if isinstance(zone, int) and zone > 0 else ""
                names_q.append(qget(qd, 1) + (f" ({z})" if z else ""))
        return "Misión", " / ".join(dict.fromkeys(names_q)) or f"misión #{quests[0]}"
    vendors = qget(it, 14) or []
    if vendors:
        vs = []
        for v in vendors[:3]:
            nd = QDB["npcs"].get(v)
            if nd:
                z = AREA.get(qget(nd, 9) or 0, "")
                vs.append(f"{qget(nd, 1)}" + (f" ({z})" if z else ""))
        return "Vendedor", ", ".join(dict.fromkeys(vs))
    drops = qget(it, 2) or []
    if drops:
        if len(drops) > 8:
            return "Botín de mundo", f"Botín aleatorio de mundo ({len(drops)} criaturas)"
        ds = []
        for d in drops[:3]:
            nd = QDB["npcs"].get(d)
            if nd:
                z = AREA.get(qget(nd, 9) or 0, "")
                ds.append(f"{qget(nd, 1)}" + (f" ({z})" if z else ""))
        return "Botín", ", ".join(dict.fromkeys(ds))
    if qget(it, 3):
        return "Botín", "Cofre (objeto del mundo)"
    return None


EVENTOS = {
    35497: "Festival de Fuego del Solsticio: Ahune (Recinto de los Esclavos)",
    35511: "Festival de Fuego del Solsticio: Ahune (Recinto de los Esclavos)",
    35514: "Festival de Fuego del Solsticio: Ahune (Recinto de los Esclavos)",
    38287: "Fiesta de la Cerveza: Coren Cerveza Temible (Profundidades de Roca Negra)",
    38288: "Fiesta de la Cerveza: Coren Cerveza Temible (Profundidades de Roca Negra)",
    38290: "Fiesta de la Cerveza: Coren Cerveza Temible (Profundidades de Roca Negra)",
}


def special(item):
    if item in EVENTOS:
        return "Evento", EVENTOS[item], "Solo durante el evento de temporada"
    n = names.get(item, "")
    if n.startswith("Darkmoon Card"):
        return "Mazo de la Luna Negra", "Se crea al completar un mazo (cartas de inscripción/botín); se entrega en la Feria de la Luna Negra", ""
    for pre, temp, aviso in (("Merciless Gladiator's", "temporada 2 (Gladiador despiadado)", "Arena temporada 2: fase 2 en adelante"),
                             ("Vengeful Gladiator's", "temporada 3 (Gladiador vengativo)", "Arena temporada 3: fase 3 en adelante"),
                             ("Brutal Gladiator's", "temporada 4 (Gladiador brutal)", "Arena temporada 4: fase 5"),
                             ("Gladiator's", "temporada 1 (Gladiador)", "")):
        if n.startswith(pre):
            return "JcJ", f"Arena {temp}: puntos de arena y honor", aviso
    if n.startswith(("High Warlord's", "Grand Marshal's", "General's", "Marshal's", "Warlord's", "Lieutenant Commander's", "Champion's")):
        return "JcJ", "Honor (vendedor de JcJ)", ""
    return None


CLASSIC_ES = {
    "MoltenCore": "Núcleo de Magma", "Onyxia": "Guarida de Onyxia", "BlackwingLair": "Guarida de Alanegra",
    "TheRuinsofAhnQiraj": "Ruinas de Ahn'Qiraj", "TheTempleofAhnQiraj": "Templo de Ahn'Qiraj",
    "Naxxramas": "Naxxramas (nivel 60)", "WorldBosses": "Jefe de mundo (nivel 60)",
}
ATLAS = []  # (inst_ids, bosses, item_data, es_clasico)
for src_file, dr_file, classic in (("source-tbc.lua", "data-tbc.lua", False), ("source.lua", "data.lua", True)):
    dr = (ALC / "AtlasLootClassic_DungeonsAndRaids" / dr_file).read_text()
    bosses = {}
    for k, block in lua_blocks(dr, None).items():
        items_part = block.split("items = {", 1)[-1]
        bosses[k] = [m.group(1) for m in re.finditer(r'^\s*name = (?:AL|ALIL)\["([^"]+)"\]', items_part, re.M)]
    src_txt = (ALC / "AtlasLootClassic_Data" / src_file).read_text()
    inst_ids = re.findall(r'"([^"]+)"', src_txt.split('["AtlasLootIDs"] = {', 1)[1].split("},", 1)[0])
    data = {}
    for m in re.finditer(r'^\[(\d+)\] = (.+),$', src_txt, re.M):
        data[int(m.group(1))] = lua_value(m.group(2))[0]
    ATLAS.append((inst_ids, bosses, data, classic))


def norm(v):
    """Normaliza una entrada de AtlasLoot a una lista de {1: inst, 2: jefe, 3: tipo, 5: dificultad}."""
    if isinstance(v, dict):
        return [v]
    if isinstance(v, list) and v and all(isinstance(x, (list, dict)) for x in v):
        return [y for x in v for y in norm(x)]
    if isinstance(v, list):
        return [{i + 1: x for i, x in enumerate(v)}]
    return []


def atlas_source(item):
    for inst_ids, bosses, data, classic in ATLAS:
        v = data.get(item)
        if isinstance(v, int):
            v = data.get(v)
        srcs = norm(v) if v is not None else []
        if not srcs:
            continue
        s = srcs[0]
        t = s.get(3)
        if isinstance(t, int) and t > 3:
            return "Profesión", PROF_ES.get(t, str(t)), ""
        if s.get(1):
            out = []
            for s in srcs[:3]:
                key = inst_ids[s[1] - 1]
                bl = bosses.get(key, [])
                b = s.get(2) or 0
                boss = bl[b - 1] if isinstance(b, int) and 0 < b <= len(bl) else "?"
                out.append((key, boss, s.get(5) == 0))
            key, boss, heroic = out[0]
            if classic:
                tipo = "Banda clásica" if key in CLASSIC_ES else "Mazmorra clásica"
                return tipo, f"{CLASSIC_ES.get(key, key)}: {boss}", "Contenido de nivel 60 (antes de TBC)"
            detalle = " / ".join(dict.fromkeys(f"{INST_ES.get(k, k)}{' (heroica)' if h else ''}: {bo}" for k, bo, h in out))
            if key in RAIDS:
                return "Banda", detalle, "Es de banda, no es pre-raid"
            aviso = "Contenido de fase 5 (Bancal del Magister)" if key == "MagistersTerrace" else ""
            return ("Mazmorra heroica" if heroic else "Mazmorra"), detalle, aviso
        if t == 2:
            return None
    return None


# Pistas de los tooltips de Wowhead ("Dropped by"), extraídas del volcado de wowsims/wotlk.
TT_EXTRA = json.loads((Path(__file__).parent / "tooltips_wowhead.json").read_text())

# Fuentes que ninguna base cubre bien, revisadas a mano.
MANUAL = json.loads((Path(__file__).parent / "fuentes_manual.json").read_text()) \
    if (Path(__file__).parent / "fuentes_manual.json").exists() else {}


def source(item):
    """(tipo, detalle, aviso)"""
    if str(item) in MANUAL:
        return tuple(MANUAL[str(item)] + [""] * (3 - len(MANUAL[str(item)])))
    sp = special(item)
    if sp:
        return sp
    a = atlas_source(item)
    if a:
        return a
    if item in fac_src:
        return "Reputación", fac_src[item].split(": ", 1)[1], ""
    if item in col_src:
        d = col_src[item]
        aviso = "Disponible solo en fases posteriores" if ("fase 4" in d or "fase 5" in d) else ""
        return ("Insignias" if "Insignias" in d else "Otro"), d, aviso
    if item in pvp_src:
        return "JcJ", pvp_src[item], ""
    q = questie_source(item)
    if q:
        return q[0], q[1], ""
    for e in TT_EXTRA.get(str(item), []):
        if e.startswith("Dropped by: "):
            return "Botín", f"{e[12:]} (criatura rara o jefe de mundo de Terrallende)", ""
    if 31100 <= item <= 31300:
        return "Botín de mundo", "Botín de mundo ligado al equipar (se puede comprar en la subasta)", ""
    return "Sin confirmar", "Fuente sin confirmar; revisar en Wowhead", ""


# ---------- Listas PreRaid ----------
SLOT_ES = {
    "Head": "Cabeza", "Neck": "Cuello", "Shoulder": "Hombros", "Shoulders": "Hombros", "Back": "Espalda",
    "Cloak": "Espalda", "Chest": "Pecho", "Wrist": "Muñecas", "Wrists": "Muñecas", "Bracer": "Muñecas",
    "Hands": "Manos", "Gloves": "Manos", "Waist": "Cintura", "Belt": "Cintura", "Legs": "Piernas",
    "Feet": "Pies", "Boots": "Pies", "Rings": "Anillos", "Ring": "Anillos", "Trinkets": "Abalorios",
    "Trinket": "Abalorios", "MitigationTrinkets": "Abalorios (mitigación)", "StaminaTrinkets": "Abalorios (aguante)",
    "ThreatTrinkets": "Abalorios (amenaza)", "1Handed": "Arma de una mano", "1HandedWeapons": "Arma de una mano",
    "Weapons": "Arma", "MainHand": "Mano principal", "MainHandWeapons": "Mano principal",
    "OffHand": "Mano izquierda", "OffHandWeapons": "Mano izquierda", "Offhand": "Mano izquierda",
    "OffHands": "Mano izquierda", "Offhands": "Mano izquierda", "OffhandsAndShields": "Mano izquierda / escudo",
    "Shields": "Escudo", "ShieldsOffHands": "Escudo / mano izquierda", "2HandedWeapon": "Arma de dos manos",
    "2HandedWeapons": "Arma de dos manos", "TwoHanded": "Arma de dos manos",
    "MainAndTwohanded": "Mano principal / dos manos", "MainAndTwohandedWeapons": "Mano principal / dos manos",
    "RangedWeapon": "A distancia", "GunsAndBows": "A distancia", "Wands": "Varita", "Idols": "Ídolo",
    "Librams": "Tratado", "Totems": "Tótem",
}
CLASS_ES = {"Druid": "Druida", "Hunter": "Cazador", "Mage": "Mago", "Paladin": "Paladín", "Priest": "Sacerdote",
            "Rogue": "Pícaro", "Shaman": "Chamán", "Warrior": "Guerrero", "Warlock": "Brujo"}
SPEC_ES = {
    ("Druid", "Balance"): "Equilibrio", ("Druid", "FeralTank"): "Feral (tanque)",
    ("Druid", "FeralDps"): "Feral (DPS)", ("Druid", "Restoration"): "Restauración",
    ("Hunter", "BeastMastery"): "Bestias", ("Hunter", "Marksmanship"): "Puntería",
    ("Hunter", "Survival"): "Supervivencia", ("Mage", "Arcane"): "Arcano", ("Mage", "Fire"): "Fuego",
    ("Mage", "Frost"): "Escarcha", ("Paladin", "Holy"): "Sagrado", ("Paladin", "Protection"): "Protección",
    ("Paladin", "Retribution"): "Reprensión", ("Priest", "Holy"): "Sagrado (sanación)",
    ("Priest", "Shadow"): "Sombra", ("Rogue", "DPS"): "DPS (Combate/Asesinato)",
    ("Shaman", "Elemental"): "Elemental", ("Shaman", "Enhancement"): "Mejora",
    ("Shaman", "Restoration"): "Restauración", ("Warrior", "Arms"): "Armas", ("Warrior", "Fury"): "Furia",
    ("Warrior", "Protection"): "Protección", ("Warrior", "DPS"): "DPS (Armas/Furia)",
    ("Warlock", "Affliction"): "Aflicción", ("Warlock", "Demonology"): "Demonología",
    ("Warlock", "Destruction"): "Destrucción",
}

text = BIS.read_text()
cls_order = [c for c in re.findall(r'\["name"\] = "(\w+)"', text)]
spec_order = {}
for m in re.finditer(r'\["name"\] = "(\w+)", \["specs"\] = \{(.*?)\}\};', text, re.S):
    spec_order[m.group(1)] = re.findall(r'"(\w+)"', m.group(2))

entries = collections.defaultdict(list)
for m in re.finditer(r'^Bistooltip_wowtbc_bislists\["(\w+)"\]\["(\w+)"\]\["PreRaid"\]\[(\d+)\] = \{ \["slot_name"\] = "(\w+)", \["enhs"\] = \{(.*?)\}, (.*?) \};$', text, re.M):
    c, sp, idx, slot, enhs, rest = m.groups()
    items = [int(v) for _, v in sorted((int(a), b) for a, b in re.findall(r'\[(\d+)\] = (-?\d+)', rest))]
    entries[(c, sp)].append((int(idx), slot, items))

QDB["items"] = load_questie("tbcItemDB")
QDB["quests"] = load_questie("tbcQuestDB")
QDB["npcs"] = load_questie("tbcNpcDB")

rows, missing = [], set()
for c in cls_order:
    for sp in spec_order[c]:
        for idx, slot, items in sorted(entries[(c, sp)]):
            for rank, it in enumerate(items, 1):
                if it <= 0:
                    continue
                t, d, aviso = source(it)
                if not aviso and phase.get(it, 1) > 1 and t not in ("Profesión",):
                    aviso = f"Disponible desde la fase {phase[it]}"
                elif not aviso and phase.get(it, 1) > 1:
                    aviso = f"Receta disponible desde la fase {phase[it]}"
                if t == "Sin confirmar":
                    missing.add(it)
                rows.append({
                    "clase": CLASS_ES[c], "especializacion": SPEC_ES[(c, sp)],
                    "ranura": SLOT_ES.get(slot, slot), "opcion": rank, "item_id": it,
                    "objeto": names.get(it, f"#{it}"), "tipo_fuente": t, "fuente": d, "aviso": aviso,
                    "wowhead": f"https://www.wowhead.com/tbc/es/item={it}",
                })

# "Obtenible": se puede conseguir con un personaje recién llegado a 70, antes de Karazhan/Gruul/Magtheridon.
BLOQUEA = ("desde la fase", "Es de banda", "Contenido de nivel 60", "fase 2", "fase 3", "fase 4", "fase 5", "fases posteriores",
           "Solo durante el evento")
for r in rows:
    r["obtenible_prerraid"] = "no" if any(b in r["aviso"] for b in BLOQUEA) else "sí"
    if r["tipo_fuente"] == "JcJ" and "temporada 2" in r["fuente"]:
        r["obtenible_prerraid"] = "no"
        r["aviso"] = r["aviso"] or "Arena temporada 2: fase 2 en adelante"
    if r["tipo_fuente"] == "Sin confirmar":
        r["obtenible_prerraid"] = "?"

DOBLES = ("Anillos", "Abalorios")


def fmt(r):
    if not r["fuente"]:
        return r["tipo_fuente"]
    if r["tipo_fuente"] in ("Mazmorra", "Mazmorra heroica", "Insignias", "Banda", "Banda clásica", "Mazmorra clásica",
                            "Botín de mundo", "Evento"):
        return r["fuente"]
    return f"{r['tipo_fuente']}: {r['fuente']}"
groups = collections.OrderedDict()
for r in rows:
    groups.setdefault((r["clase"], r["especializacion"], r["ranura"]), []).append(r)
rec = []
for (c, sp, slot), opts in groups.items():
    good = [o for o in opts if o["obtenible_prerraid"] == "sí"]
    n = 2 if slot.startswith(DOBLES) else 1
    picks = good[:n] or opts[:1]  # sin opción obtenible: se muestra la de la lista con su aviso
    alts = [o for o in good[n:n + 2]]
    for i, pk in enumerate(picks):
        rec.append({
            "clase": c, "especializacion": sp, "ranura": slot + (f" {i + 1}" if n == 2 else ""),
            "objeto": pk["objeto"], "item_id": pk["item_id"], "tipo_fuente": pk["tipo_fuente"], "fuente": pk["fuente"],
            "alternativas": " · ".join(f"{a['objeto']} ({fmt(a)})" for a in alts) if i == 0 else "",
            "aviso": pk["aviso"] if pk["obtenible_prerraid"] != "sí" else "",
            "mejor_de_la_lista_si_no_es_obtenible": "" if i or (good and opts[0] is good[0]) else f"{opts[0]['objeto']} ({opts[0]['aviso']})",
            "wowhead": pk["wowhead"],
        })

OUT.mkdir(parents=True, exist_ok=True)
with open(OUT / "prebis_tbc_nivel70.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader(); w.writerows(rows)
with open(OUT / "prebis_recomendado.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=list(rec[0].keys()))
    w.writeheader(); w.writerows(rec)

md = ["# Pre-BiS de nivel 70 (TBC) por clase y especialización", "",
      "Equipo recomendado al llegar a 70, antes de Karazhan, Gruul y Magtheridon. Para cada ranura se muestra la mejor "
      "opción que se puede conseguir sin bandas, y dos alternativas. Los enlaces abren el objeto en Wowhead en español.", "",
      "Fuentes: listas pre-raid de Wowhead/wowtbc.gg incluidas en el addon BiS-Tooltip (backport TBC 3.3.5a); "
      "origen de cada objeto según AtlasLoot Classic, Questie y los tooltips de Wowhead. "
      "La tabla completa con las 6 opciones por ranura está en `prebis_tbc_nivel70.csv`.", "",
      "Se considera obtenible lo que existe en la fase 1 de TBC (mazmorras normales y heroicas, reputaciones, "
      "profesiones, misiones, Insignias de Justicia y arena temporada 1). Si tu servidor abre las fases de otra forma, "
      "revisa la columna `aviso` del CSV completo. ⚠ marca una ranura donde la lista de origen no trae ninguna opción "
      "de fase 1.", ""]
cur = None
for r in rec:
    key = (r["clase"], r["especializacion"])
    if key != cur:
        if cur and cur[0] != key[0] or cur is None:
            md += [f"## {r['clase']}", ""]
        md += [f"### {r['clase']} · {r['especializacion']}", "",
               "| Ranura | Objeto | Fuente | Alternativas |", "|---|---|---|---|"]
        cur = key
    fuente = fmt(r) + (f" ⚠ {r['aviso']}" if r["aviso"] else "")
    md.append(f"| {r['ranura']} | [{r['objeto']}]({r['wowhead']}) | {fuente} | {r['alternativas'] or ''} |")
    if r is rec[-1] or (rec[rec.index(r) + 1]["clase"], rec[rec.index(r) + 1]["especializacion"]) != key:
        md.append("")
(OUT / "prebis_tbc_nivel70.md").write_text("\n".join(md), encoding="utf-8")

print("filas", len(rows), "specs", len(entries), "objetos únicos", len({r['item_id'] for r in rows}))
print("sin nombre", sorted({r['item_id'] for r in rows if r['objeto'].startswith('#')}))
print("sin fuente", len(missing))
for it in sorted(missing):
    print(it, names.get(it))
