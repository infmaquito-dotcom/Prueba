#!/usr/bin/env python3
"""Pre-BiS de nivel 70 (antes de Karazhan, Gruul y Magtheridon) con las estadísticas de la base de datos WotLK 3.3.5.

Toma todos los objetos de TBC con sus estadísticas WotLK (base de wowsims/wotlk, extraída de Wowhead WotLK),
filtra los que se pueden conseguir en la fase 1 sin bandas y los puntúa por especialización con pesos de
estadísticas. Los abalorios siguen el orden de las listas de Wowhead/wowtbc porque su valor está en efectos de
uso o de probabilidad que una suma de estadísticas no mide.

Uso: PREBIS_FUENTES=<carpeta con los repos de origen> python3 compilar_prebis_wotlk.py <carpeta de salida>
"""
import collections, csv, io, json, os, runpy, sys, contextlib
from pathlib import Path

ROOT = Path(os.environ.get("PREBIS_FUENTES", "fuentes"))
OUT = Path(sys.argv[1])
HERE = Path(__file__).parent

# Reutiliza el compilador de la versión TBC: listas originales, fuentes en español y fases.
with contextlib.redirect_stdout(io.StringIO()):
    sys.argv = [str(HERE / "compilar_prebis.py"), str(OUT / ".tmp_tbc")]
    TBC = runpy.run_path(str(HERE / "compilar_prebis.py"))
for f in (OUT / ".tmp_tbc").glob("*"):
    f.unlink()
(OUT / ".tmp_tbc").rmdir()
source, phase_tbc, tbc_rows = TBC["source"], TBC["phase"], TBC["rows"]
fac_src, col_src = TBC["fac_src"], TBC["col_src"]

DB = json.loads((ROOT / "wswotlk/assets/database/db.json").read_text())
LEFT = json.loads((ROOT / "wswotlk/assets/database/leftover_db.json").read_text())
ITEMS = {i["id"]: i for i in LEFT["items"] + DB["items"]}
ZONES = {z["id"]: z["name"] for z in DB["zones"]}
NPCS = {n["id"]: n["name"] for n in DB["npcs"]}

S = dict(STR=0, AGI=1, STA=2, INT=3, SPI=4, SP=5, MP5=6, SHIT=7, SCRIT=8, SHASTE=9, AP=11, MHIT=12, MCRIT=13,
         MHASTE=14, ARP=15, EXP=16, ARMOR=20, RAP=21, DEF=22, BLOCK=23, BLOCKV=24, DODGE=25, PARRY=26, RES=27,
         HEALTH=28, BARMOR=34)

# ---------- Pesos (wowsims/wotlk, ui/<spec>/sim.ts) ----------
# Ajustes para nivel 70 sin bandas: el golpe no está al tope, así que se le da su valor antes del tope, y los
# sanadores valoran el maná por 5 (wowsims lo deja en 0 porque asume buffs de banda).
W = {
    "balance_druid": dict(INT=0.43, SPI=0.34, SP=1, SCRIT=0.82, SHASTE=0.80, SHIT=1.2),
    "feral_druid": dict(STR=2.40, AGI=2.39, AP=1, MHIT=2.51, MCRIT=2.23, MHASTE=1.83, ARP=2.08, EXP=2.44, MH=16.5),
    "feral_tank_druid": dict(ARMOR=3.5665, BARMOR=0.5187, STA=7.3021, STR=2.3786, AGI=4.4974, AP=1, EXP=2.6597,
                             MHIT=2.9282, MCRIT=1.5143, MHASTE=2.0983, ARP=1.584, DEF=1.8171, DODGE=2.0196,
                             HEALTH=0.4465),
    "restoration_druid": dict(INT=0.38, SPI=0.34, SP=1, SCRIT=0.69, SHASTE=0.77, MP5=1.0),
    "hunter": dict(STA=0.5, AGI=2.65, INT=1.1, RAP=1.0, AP=1.0, MHIT=2, MCRIT=1.5, MHASTE=1.39, ARP=1.32, RANGED=6.32),
    "mage": dict(INT=0.48, SPI=0.42, SP=1, SHIT=1.2, SCRIT=0.58, SHASTE=0.94),
    "holy_paladin": dict(INT=0.38, SPI=0.34, SP=1, SCRIT=0.69, SHASTE=0.77, MP5=1.0),
    "protection_paladin": dict(ARMOR=0.07, BARMOR=0.06, STA=1.14, STR=1.00, AGI=0.62, AP=0.26, EXP=0.69, MHIT=0.79,
                               MCRIT=0.30, MHASTE=0.17, ARP=0.04, SP=0.13, BLOCK=0.52, BLOCKV=0.28, DODGE=0.46,
                               PARRY=0.61, DEF=0.54, MH=3.33),
    "retribution_paladin": dict(STR=2.53, AGI=1.13, INT=0.15, SP=0.32, AP=1, MHIT=1.96, MCRIT=1.16, MHASTE=1.44,
                                ARP=0.76, EXP=1.80, MH=7.33),
    # wowsims da a Intelecto 2.73 al sacerdote sanador, un valor de nivel 80 que aquí distorsiona; se usa el perfil
    # de los demás sanadores con más peso al Espíritu.
    "healing_priest": dict(INT=0.5, SPI=0.6, SP=1, SCRIT=0.6, SHASTE=0.5, MP5=1.0),
    "shadow_priest": dict(INT=0.11, SPI=0.47, SP=1, SHIT=1.2, SCRIT=0.74, SHASTE=1.65),
    "rogue": dict(AGI=1.86, STR=1.14, AP=1, MHIT=2.0, MCRIT=1.32, MHASTE=1.48, ARP=0.84, EXP=1.5, MH=2.94, OH=2.45),
    "elemental_shaman": dict(INT=0.22, SP=1, SHIT=1.2, SCRIT=0.67, SHASTE=1.29),
    "enhancement_shaman": dict(INT=1.48, AGI=1.59, STR=1.1, SP=1.13, AP=1.0, MHIT=2.0, MCRIT=0.81, MHASTE=1.61,
                               ARP=0.48, EXP=1.5, MH=5.21, OH=2.21),
    "restoration_shaman": dict(INT=0.22, SPI=0.05, SP=1, SCRIT=0.67, SHASTE=1.29, MP5=1.0),
    "warrior": dict(STR=2.72, AGI=1.82, AP=1, EXP=2.55, MHIT=2.5, MCRIT=2.12, MHASTE=1.72, ARP=2.17, ARMOR=0.03,
                    MH=6.29, OH=3.58),
    "protection_warrior": dict(ARMOR=0.174, BARMOR=0.155, STA=2.336, STR=1.555, AGI=2.771, AP=0.32, EXP=1.44,
                               MHIT=1.432, MCRIT=0.925, MHASTE=0.431, ARP=1.055, BLOCK=1.320, BLOCKV=1.373,
                               DODGE=2.606, PARRY=2.649, DEF=3.305, MH=6.081),
    "warlock": dict(INT=0.18, SPI=0.54, SP=1, SHIT=1.2, SCRIT=0.53, SHASTE=0.81, STA=0.01),
}

# ---------- Clases: armaduras, armas y configuración de armas por especialización ----------
CLOTH, LEATHER, MAIL, PLATE = 1, 2, 3, 4
AXE, DAGGER, FIST, MACE, OFFHAND, POLEARM, SHIELD, STAFF, SWORD = 1, 2, 3, 4, 5, 6, 7, 8, 9
BOW, XBOW, GUN, IDOL, LIBRAM, THROWN, TOTEM, WAND = 1, 2, 3, 4, 5, 6, 7, 8
MAINHAND, ONEHAND, OFFHAND_H, TWOHAND = 1, 2, 3, 4
CLASS = {  # id de clase wowsims, armaduras, armas (tipo -> manos permitidas), a distancia
    "Druida": (1, {CLOTH, LEATHER}, {DAGGER: "1", FIST: "1", MACE: "12", POLEARM: "2", STAFF: "2", OFFHAND: "1"}, {IDOL}),
    "Cazador": (2, {CLOTH, LEATHER, MAIL}, {AXE: "12", DAGGER: "1", FIST: "1", POLEARM: "2", STAFF: "2", SWORD: "12"},
                {BOW, XBOW, GUN}),
    "Mago": (3, {CLOTH}, {DAGGER: "1", SWORD: "1", STAFF: "2", OFFHAND: "1"}, {WAND}),
    "Paladín": (4, {CLOTH, LEATHER, MAIL, PLATE}, {AXE: "12", MACE: "12", POLEARM: "2", SWORD: "12", SHIELD: "1",
                                                  OFFHAND: "1"}, {LIBRAM}),
    "Sacerdote": (5, {CLOTH}, {DAGGER: "1", MACE: "1", STAFF: "2", OFFHAND: "1"}, {WAND}),
    "Pícaro": (6, {CLOTH, LEATHER}, {AXE: "1", DAGGER: "1", FIST: "1", MACE: "1", SWORD: "1"}, {BOW, XBOW, GUN, THROWN}),
    "Chamán": (7, {CLOTH, LEATHER, MAIL}, {AXE: "12", DAGGER: "1", FIST: "1", MACE: "12", STAFF: "2", SHIELD: "1",
                                         OFFHAND: "1"}, {TOTEM}),
    "Brujo": (8, {CLOTH}, {DAGGER: "1", SWORD: "1", STAFF: "2", OFFHAND: "1"}, {WAND}),
    "Guerrero": (9, {CLOTH, LEATHER, MAIL, PLATE}, {AXE: "12", DAGGER: "1", FIST: "1", MACE: "12", POLEARM: "2",
                                                   STAFF: "2", SWORD: "12", SHIELD: "1"}, {BOW, XBOW, GUN, THROWN}),
}
# Especialización -> (pesos, configuraciones de arma a comparar)
#   "2h": arma de dos manos; "caster": mano principal + objeto de mano izquierda (o escudo si se permite);
#   "dw": dos armas de una mano; "tank": una mano + escudo.
SPECS = [
    ("Druida", "Equilibrio", "balance_druid", ["2h", "caster"]),
    ("Druida", "Feral (tanque)", "feral_tank_druid", ["2h"]),
    ("Druida", "Feral (DPS)", "feral_druid", ["2h"]),
    ("Druida", "Restauración", "restoration_druid", ["2h", "caster"]),
    ("Cazador", "Bestias", "hunter", ["2h", "dw"]),
    ("Cazador", "Puntería", "hunter", ["2h", "dw"]),
    ("Cazador", "Supervivencia", "hunter", ["2h", "dw"]),
    ("Mago", "Arcano", "mage", ["2h", "caster"]),
    ("Mago", "Fuego", "mage", ["2h", "caster"]),
    ("Mago", "Escarcha", "mage", ["2h", "caster"]),
    ("Paladín", "Sagrado", "holy_paladin", ["caster"]),
    ("Paladín", "Protección", "protection_paladin", ["tank"]),
    ("Paladín", "Reprensión", "retribution_paladin", ["2h"]),
    ("Sacerdote", "Sagrado (sanación)", "healing_priest", ["2h", "caster"]),
    ("Sacerdote", "Sombra", "shadow_priest", ["2h", "caster"]),
    ("Pícaro", "DPS (Combate/Asesinato)", "rogue", ["dw"]),
    ("Chamán", "Elemental", "elemental_shaman", ["2h", "caster"]),
    ("Chamán", "Mejora", "enhancement_shaman", ["dw"]),
    ("Chamán", "Restauración", "restoration_shaman", ["2h", "caster"]),
    ("Guerrero", "Protección", "protection_warrior", ["tank"]),
    ("Guerrero", "DPS (Armas/Furia)", "warrior", ["2h"]),
    ("Brujo", "Aflicción", "warlock", ["2h", "caster"]),
    ("Brujo", "Demonología", "warlock", ["2h", "caster"]),
    ("Brujo", "Destrucción", "warlock", ["2h", "caster"]),
]

# ---------- Qué se puede conseguir antes de las bandas ----------
RAID_ZONES = {3457, 3923, 3836, 3607, 3845, 3606, 3959, 3805, 4075}   # Kara, Gruul, Mag, SSC, TK, Hyjal, BT, ZA, SWP
LATER_ZONES = {4131, 4080}                                             # Bancal del Magister, Isla de Quel'Danas
WORLD_BOSSES = {17711, 18728}                                          # Kazzard y Kazzak
LATER_FACTIONS = ("Ogri'la", "Guardia del cielo", "Ofensiva Sol Devastado", "Ala Abisal", "Juramorte",
                  "El Ojo Violeta")  # El Ojo Violeta se sube en Karazhan
EVENT_SOURCES = ("Headless Horseman", "Coren Direbrew", "Ahune", "Cofre (objeto del mundo)",
                 "Shartuul", "Terokk")  # eventos de temporada y jefes invocados de la 2.1 (fase 2)
SKIP_NAMES = ("Merciless Gladiator's", "Vengeful Gladiator's", "Brutal Gladiator's", "Veteran's", "Vindicator's",
              "Guardian's")


def obtainable(it):
    iid = it["id"]
    if it.get("quality", 0) < 3 or it.get("ilvl", 0) < 85 or it.get("expansion") not in (2, None):
        return False
    if it.get("expansion") is None and iid < 23000:
        return False
    if iid in phase_tbc:
        if phase_tbc[iid] > 1:
            return False
    elif iid >= 32000:
        return False  # objetos de 2.1 en adelante sin dato de fase: se descartan por prudencia
    if any(it["name"].startswith(p) for p in SKIP_NAMES):
        return False
    if iid in fac_src and any(f in fac_src[iid] for f in LATER_FACTIONS):
        return False
    if iid in col_src and ("fase" in col_src[iid] or "Motas" in col_src[iid]):
        return False
    t, d, aviso = source(iid)
    if aviso or t in ("Banda", "Banda clásica", "Mazmorra clásica", "Evento"):
        return False
    if any(e in d for e in EVENT_SOURCES) or "Horseman's" in it["name"]:
        return False  # botín de eventos de temporada
    srcs = it.get("sources") or []
    if not srcs:
        return t != "Sin confirmar"
    ok = False
    for s in srcs:
        k, v = next(iter(s.items()))
        if k == "drop":
            if v.get("zoneId") in RAID_ZONES | LATER_ZONES or v.get("npcId") in WORLD_BOSSES:
                continue
            ok = True
        elif k in ("crafted", "quest", "soldBy"):
            if k == "soldBy" and v.get("zoneId") in LATER_ZONES:
                continue
            ok = True
    return ok


POOL = [it for it in ITEMS.values() if obtainable(it)]

# ---------- Gemas (raras de TBC con estadísticas WotLK) ----------
GEMS = [g for g in DB["gems"] if g.get("quality") == 3 and g["id"] < 40000 and 2 <= g["color"] <= 7]
METAS = [g for g in DB["gems"] if g["color"] == 1 and g["id"] < 40000]
FITS = {2: {2, 6, 7}, 3: {3, 5, 7}, 4: {4, 5, 6}}  # color de ranura -> colores de gema que la cumplen


def vec_score(vec, w):
    return sum(vec[S[k]] * v for k, v in w.items() if k in S and S[k] < len(vec))


def socket_score(it, w):
    socks = it.get("gemSockets") or []
    if not socks:
        return 0.0
    best_any = max((vec_score(g["stats"], w) for g in GEMS), default=0)
    meta = max((vec_score(g["stats"], w) for g in METAS), default=0)
    free = sum(meta if c == 1 else best_any for c in socks)
    matched = sum(meta if c == 1 else max((vec_score(g["stats"], w) for g in GEMS if g["color"] in FITS.get(c, ())),
                                          default=0) for c in socks)
    return max(free, matched + vec_score(it["socketBonus"], w))


def item_score(it, w, slot_kind):
    sc = vec_score(it["stats"], w) + socket_score(it, w)
    if it.get("weaponSpeed"):
        dps = (it["weaponDamageMin"] + it["weaponDamageMax"]) / 2 / it["weaponSpeed"]
        sc += dps * w.get({"mh": "MH", "oh": "OH", "ranged": "RANGED"}.get(slot_kind, "MH"), 0)
    return sc


# ---------- Ranuras ----------
ARMOR_SLOTS = [(1, "Cabeza"), (2, "Cuello"), (3, "Hombros"), (4, "Espalda"), (5, "Pecho"), (6, "Muñecas"),
               (7, "Manos"), (8, "Cintura"), (9, "Piernas"), (10, "Pies"), (11, "Anillos")]
ARMORED = {1, 3, 5, 6, 7, 8, 9, 10}


def wearable(it, cls):
    cid, armors, weapons, ranged = CLASS[cls]
    if it.get("classAllowlist") and cid not in it["classAllowlist"]:
        return False
    if it["type"] in ARMORED and it.get("armorType", 0) not in armors:
        return False
    return True


def weapon_ok(it, cls, hands):
    _, _, weapons, _ = CLASS[cls]
    wt, ht = it.get("weaponType", 0), it.get("handType", 0)
    allowed = weapons.get(wt, "")
    if hands == "2h":
        return ht == TWOHAND and "2" in allowed
    if hands == "mh":
        return ht in (MAINHAND, ONEHAND) and "1" in allowed and wt not in (SHIELD, OFFHAND)
    if hands == "oh_dw":
        return ht in (ONEHAND, OFFHAND_H) and "1" in allowed and wt not in (SHIELD, OFFHAND)
    if hands == "oh_caster":
        return wt in (OFFHAND, SHIELD) and "1" in allowed
    if hands == "shield":
        return wt == SHIELD and "1" in allowed
    return False


def ranked(cands, w, kind="armor", n=3):
    seen, out = set(), []
    for sc, it in sorted(((item_score(it, w, kind), it) for it in cands), key=lambda x: -x[0]):
        key = it["name"]
        if key in seen or sc <= 0:
            continue
        seen.add(key)
        out.append((sc, it))
        if len(out) == n:
            break
    return out


def fmt_src(iid):
    t, d, aviso = source(iid)
    if t == "Sin confirmar":
        it = ITEMS.get(iid, {})
        for s in it.get("sources") or []:
            k, v = next(iter(s.items()))
            if k == "drop":
                z = ZONES.get(v.get("zoneId"), "")
                npc = NPCS.get(v.get("npcId"), "")
                hero = " (heroica)" if v.get("difficulty") == 2 else ""
                return "Botín", f"{z}{hero}: {npc}".strip(": ")
            if k == "quest":
                return "Misión", v.get("name", "")
            if k == "soldBy":
                return "Vendedor", f"{v.get('npcName', '')} ({ZONES.get(v.get('zoneId'), '')})"
            if k == "crafted":
                return "Profesión", ""
    return t, d


def fmt(t, d):
    if t == "Profesión":
        return f"Fabricado ({d})" if d else "Fabricado"
    if not d:
        return t
    if t in ("Mazmorra", "Mazmorra heroica", "Insignias", "Botín de mundo", "Evento"):
        return d
    return f"{t}: {d}"


rows, full = [], []
tbc_first = {}
for r in tbc_rows:
    if r["obtenible_prerraid"] == "sí":
        tbc_first.setdefault((r["clase"], r["especializacion"], r["ranura"]), []).append(r["objeto"])


HORDA = ("General's", "Warlord's", "High Warlord's", "Thrallmar", "Mag'har")
ALIANZA = ("Marshal's", "Grand Marshal's", "Lieutenant Commander's", "Bastión del Honor", "Kurenai")


def faction(it, d):
    text = it["name"] + " " + d
    if any(text.startswith(h) or h in d for h in HORDA):
        return "Horda"
    if any(text.startswith(a) or a in d for a in ALIANZA):
        return "Alianza"
    return ""


def emit(cls, spec, slot, picks, alts, tbc_slot, note=""):
    for i, (sc, it) in enumerate(picks):
        t, d = fmt_src(it["id"])
        tbc_list = tbc_first.get((cls, spec, tbc_slot), [])
        rows.append({
            "clase": cls, "especializacion": spec, "ranura": slot + (f" {i + 1}" if len(picks) > 1 else ""),
            "objeto": it["name"], "item_id": it["id"], "puntos": round(sc, 1), "tipo_fuente": t, "fuente": d,
            "faccion": faction(it, d),
            "alternativas": " · ".join(f"{a['name']} ({fmt(*fmt_src(a['id']))})" for _, a in alts) if i == 0 else "",
            "en_lista_tbc": "sí" if it["name"] in tbc_list else ("—" if not tbc_list else "no"),
            "nota": note if i == 0 else "",
            "wowhead": f"https://www.wowhead.com/wotlk/es/item={it['id']}",
        })


for cls, spec, wkey, configs in SPECS:
    w = W[wkey]
    pool = [it for it in POOL if wearable(it, cls)]
    for typ, slot in ARMOR_SLOTS:
        cands = [it for it in pool if it["type"] == typ]
        if typ == 11:
            top = ranked(cands, w, n=4)
            emit(cls, spec, slot, top[:2], top[2:4], "Anillos")
        else:
            top = ranked(cands, w)
            emit(cls, spec, slot, top[:1], top[1:3], slot)
    # Abalorios: orden de la lista Wowhead/wowtbc, solo los obtenibles.
    trink = []
    for r in tbc_rows:
        if (r["clase"], r["especializacion"]) == (cls, spec) and r["ranura"].startswith("Abalorios") \
                and r["obtenible_prerraid"] == "sí" and r["item_id"] in ITEMS and obtainable(ITEMS[r["item_id"]]) \
                and r["objeto"] not in [t["name"] for _, t in trink]:
            trink.append((0.0, ITEMS[r["item_id"]]))
    emit(cls, spec, "Abalorios", trink[:2], trink[2:4], "Abalorios",
         "Orden de la lista Wowhead/wowtbc (efectos de uso y probabilidad)")
    # Armas: se compara cada configuración y se elige la de más puntos.
    best = None
    for cfg in configs:
        if cfg == "2h":
            t = ranked([it for it in pool if it["type"] == 13 and weapon_ok(it, cls, "2h")], w, "mh")
            parts = [("Arma de dos manos", t)]
        elif cfg == "caster":
            mh = ranked([it for it in pool if it["type"] == 13 and weapon_ok(it, cls, "mh")], w, "mh")
            oh = ranked([it for it in pool if it["type"] == 13 and weapon_ok(it, cls, "oh_caster")], w, "oh")
            parts = [("Mano principal", mh), ("Mano izquierda", oh)]
        elif cfg == "dw":
            mh = ranked([it for it in pool if it["type"] == 13 and weapon_ok(it, cls, "mh")], w, "mh", n=4)
            oh = ranked([it for it in pool if it["type"] == 13 and weapon_ok(it, cls, "oh_dw")], w, "oh", n=4)
            oh = [x for x in oh if not mh or x[1]["name"] != mh[0][1]["name"] or not x[1].get("unique")][:3]
            parts = [("Mano principal", mh[:3]), ("Mano izquierda", oh)]
        else:  # tank
            mh = ranked([it for it in pool if it["type"] == 13 and weapon_ok(it, cls, "mh")], w, "mh")
            sh = ranked([it for it in pool if it["type"] == 13 and weapon_ok(it, cls, "shield")], w, "oh")
            parts = [("Mano principal", mh), ("Escudo", sh)]
        total = sum(p[1][0][0] for p in parts if p[1])
        if best is None or total > best[0]:
            best = (total, cfg, parts)
    for slot, lst in best[2]:
        tbc_slot = {"Arma de dos manos": "Arma de dos manos", "Mano principal": "Arma de una mano",
                    "Mano izquierda": "Mano izquierda", "Escudo": "Escudo"}[slot]
        emit(cls, spec, slot, lst[:1], lst[1:3], tbc_slot)
    # A distancia / reliquia
    _, _, _, rng = CLASS[cls]
    cands = [it for it in pool if it["type"] == 14 and it.get("rangedWeaponType") in rng]
    label = {IDOL: "Ídolo", LIBRAM: "Tratado", TOTEM: "Tótem", WAND: "Varita"}.get(next(iter(rng)), "A distancia")
    top = ranked(cands, w, "ranged")
    if label in ("Ídolo", "Tratado", "Tótem"):
        # Las reliquias valen por su efecto sobre un hechizo concreto: se sigue la lista Wowhead/wowtbc.
        rel = []
        for r in tbc_rows:
            if (r["clase"], r["especializacion"]) == (cls, spec) and r["ranura"] == label \
                    and r["obtenible_prerraid"] == "sí" and r["item_id"] in ITEMS and obtainable(ITEMS[r["item_id"]]):
                rel.append((0.0, ITEMS[r["item_id"]]))
        emit(cls, spec, label, rel[:1], rel[1:3], label, "Orden de la lista Wowhead/wowtbc (efecto sobre un hechizo)")
    else:
        emit(cls, spec, label, top[:1], top[1:3], label)

# ---------- Salida ----------
OUT.mkdir(parents=True, exist_ok=True)
with open(OUT / "prebis_wotlk_nivel70.csv", "w", newline="", encoding="utf-8-sig") as f:
    wr = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    wr.writeheader(); wr.writerows(rows)

md = ["# Pre-BiS de nivel 70 con la base de datos WotLK (3.3.5)", "",
      "Equipo para un personaje recién llegado a 70, antes de Karazhan, Gruul y Magtheridon, elegido con las "
      "estadísticas que tienen los objetos de TBC en la base de datos de WotLK 3.3.5 (poder con hechizos en vez de "
      "daño y sanación por separado, índice de golpe/crítico/celeridad unificado, penetración de armadura como "
      "índice, sin poder de ataque feral en las armas, etc.).", "",
      "**Cómo se eligió:** cada objeto se puntúa con los pesos de estadísticas de wowsims WotLK para la "
      "especialización, contando gemas raras de TBC y bonificación de ranura. Solo entran objetos de la fase 1 que "
      "no salen de bandas: mazmorras normales y heroicas, reputaciones, profesiones, misiones, Insignias de Justicia "
      "y JcJ (honor y arena temporada 1). Quedan fuera las reputaciones que se suben en bandas (El Ojo Violeta) o en "
      "fases posteriores. Los abalorios y las reliquias siguen la lista de Wowhead/wowtbc porque su valor está en "
      "efectos de uso o sobre un hechizo que la suma de estadísticas no mide. Los bonus de conjunto no se cuentan.", "",
      "**Columna «¿En lista TBC?»:** «no» quiere decir que con las estadísticas WotLK sale un objeto distinto al de "
      "las listas originales de TBC.", ""]
cur = None
for i, r in enumerate(rows):
    key = (r["clase"], r["especializacion"])
    if key != cur:
        if cur is None or cur[0] != key[0]:
            md += [f"## {r['clase']}", ""]
        md += [f"### {r['clase']} · {r['especializacion']}", "",
               "| Ranura | Objeto | Fuente | ¿En lista TBC? | Alternativas |", "|---|---|---|---|---|"]
        cur = key
    nota = f" ({r['nota']})" if r["nota"] else ""
    nota += f" · solo {r['faccion']}" if r["faccion"] else ""
    md.append(f"| {r['ranura']} | [{r['objeto']}]({r['wowhead']}) | {fmt(r['tipo_fuente'], r['fuente'])}{nota} | "
              f"{r['en_lista_tbc']} | {r['alternativas']} |")
    if i + 1 == len(rows) or (rows[i + 1]["clase"], rows[i + 1]["especializacion"]) != key:
        md.append("")
(OUT / "prebis_wotlk_nivel70.md").write_text("\n".join(md), encoding="utf-8")

ch = collections.Counter(r["en_lista_tbc"] for r in rows)
print("filas", len(rows), "pool", len(POOL), "cambios", dict(ch))
