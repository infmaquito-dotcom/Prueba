"""Qué objetos se pueden conseguir en la prefase y cómo se describe su fuente (en español).

Reglas de la prefase (especificación del oficial, 2 de octubre de 2026):
  - Sí: mazmorras de TBC de fase 1 en normal y heroico (sin Bancal del Magister), reputaciones y misiones de
    Terrallende, artesanía con patrones de esas fuentes, botín de mundo BoE y todo el contenido clásico,
    bandas incluidas (se marcan).
  - No: bandas de TBC, Kazzak y Caminante del Destino, Bancal del Magister, Rasganorte, nada que pida
    materiales de banda, contenido de fases 2 a 5 (Ogri'la, Guardia del cielo, Ala Abisal, Sol Devastado).
  - JcJ: la especificación no lo menciona entre lo conseguible; se deja fuera.
  - Insignias de justicia: lista aparte con la fase en que se vendían en el TBC original.
"""
import collections
import json
import os
import re
from pathlib import Path

from ac_index import MAPS, FACTIONS, RANKS, ALLIANCE_RACES, HORDE_RACES

FUENTES = Path(os.environ.get("PREBIS_FUENTES", "/tmp/claude-0"))

BADGE_VENDORS = {18525: "G'eras", 25046: "Smith Hauthaa", 25950: "Shaani"}  # Shattrath, Quel'Danas
WORLD_BOSSES = {17711, 18728}  # Caminante del Destino, Señor Supremo Kazzak
RAID_QUEST_ZONES = {2562, 3457, 3923, 3836, 3607, 3845, 3606, 3959, 3805, 4075, 4131, 4080, 3842, 3618}
LATER_ZONES = {4080, 4131}  # Isla de Quel'Danas, Bancal del Magister
PVP_PREFIX = ("Gladiator's", "Merciless Gladiator's", "Vengeful Gladiator's", "Brutal Gladiator's", "Veteran's",
              "Vindicator's", "Guardian's", "General's", "Marshal's", "Warlord's", "High Warlord's",
              "Grand Marshal's", "Lieutenant Commander's", "Champion's", "Sergeant's", "Legionnaire's",
              "Knight-Lieutenant's", "Blood Guard's", "Stone Guard's", "Savage Gladiator's", "Hateful Gladiator's",
              "Deadly Gladiator's", "Furious Gladiator's", "Relentless Gladiator's", "Wrathful Gladiator's")
QUEST_ZONES = {
    3483: "Península del Fuego Infernal", 3521: "Marisma de Zangar", 3519: "Bosque de Terokkar", 3518: "Nagrand",
    3522: "Montañas Filospada", 3523: "Tormenta Abisal", 3520: "Valle Sombraluna", 3703: "Ciudad de Shattrath",
    3562: "Murallas del Fuego Infernal", 3713: "El Horno de Sangre", 3714: "Las Salas Arrasadas",
    3717: "Recinto de los Esclavos", 3716: "La Sotiénaga", 3715: "La Cámara de Vapor", 3792: "Tumbas de Maná",
    3790: "Criptas Auchenai", 3791: "Salas Sethekk", 3789: "Laberinto de las Sombras",
    2367: "Antiguas Laderas de Trabalomas", 2366: "La Ciénaga Negra", 3849: "El Mechanar", 3847: "El Invernáculo",
    3848: "El Arcatraz", 3430: "Bosque Canción Eterna", 3433: "Tierras Fantasma", 3524: "Isla Bruma Azur",
    3525: "Isla Bruma de Sangre", 3557: "El Exodar", 3487: "Ciudad de Lunargenta", 3688: "Auchindoun",
}
# Jefes que el núcleo invoca por guion (no tienen aparición en la tabla creature): mapa escrito a mano.
SCRIPTED_BOSSES = {
    17848: 560, 17862: 560, 18096: 560,            # Antiguas Laderas de Trabalomas
    17879: 269, 17880: 269, 17881: 269,            # La Ciénaga Negra
    20912: 552,                                    # El Arcatraz: Presagista Skyriss
    18478: 558,                                    # Criptas Auchenai (heroico): Avatar de los Martirizados
    20992: 540,                                    # Las Salas Arrasadas (heroico): Guardia de sangre Porung
    # Karazhan, Monte Hyjal, Caverna Santuario Serpiente, Templo Oscuro, Meseta de La Fuente del Sol
    16152: 532, 17521: 532, 17533: 532, 17534: 532, 18168: 532, 16179: 532, 16180: 532, 16181: 532,
    17767: 534, 17808: 534, 17842: 534, 17888: 534, 21217: 548, 23420: 564,
    24892: 580, 25038: 580, 25315: 580, 25840: 580,
}
# Invocaciones de contenido posterior a la fase 1 (Anzu 2.1, Yor 2.1, Skettis/Guardia del cielo, Ogri'la, Fuerza Vil)
LATER_NPCS = {23035, 22930, 21838, 23161, 23162, 23163, 23165, 23230, 22825, 22826, 22827, 22828, 20888}
NORTHREND_ZONES = {3537, 495, 65, 394, 3711, 66, 67, 210, 2817, 4197, 4395, 206, 1196, 3477, 4494, 4196, 4228,
                   4264, 4272, 4415, 4100, 4723, 4809, 4813, 4820, 4265, 3456, 4493, 4500, 4603, 4273, 4722, 4812,
                   4987, 2159, 4742, 3979}
EVENT_SORTS = {-22, -284, -366, -369, -370, -41, -1002, -1003, -1005, -376, -374, -1001}  # fiestas de temporada
CLASSIC_DUNGEONS = {33: "Castillo de Colmillo Oscuro", 34: "Las Mazmorras", 36: "Las Minas de la Muerte",
                    43: "Cuevas de los Lamentos", 47: "Horado Rajacieno", 48: "Cavernas de Brazanegra",
                    70: "Uldaman", 90: "Gnomeregan", 109: "El Templo Sumergido", 129: "Zahúrda Rajacieno",
                    189: "Monasterio Escarlata", 209: "Zul'Farrak", 229: "Cumbre de Roca Negra",
                    230: "Profundidades de Roca Negra", 289: "Scholomance", 329: "Stratholme", 349: "Maraudon",
                    389: "Sima Ígnea", 429: "La Masacre"}
SLOT_INV = {  # InventoryType de item_template -> hueco
    1: "Head", 2: "Neck", 3: "Shoulder", 16: "Back", 5: "Chest", 20: "Chest", 9: "Wrist", 10: "Hands", 6: "Waist",
    7: "Legs", 8: "Feet", 11: "Finger", 12: "Trinket", 13: "Weapon", 17: "Weapon", 21: "Weapon", 22: "Off hand",
    14: "Off hand", 23: "Off hand", 15: "Ranged", 25: "Ranged", 26: "Ranged", 28: "Relic",
}


# Materiales que solo dan las bandas (o Rasganorte, que no está abierto): una receta que los pida no vale.
RAID_MATS = {30183: "Vórtice abisal", 32428: "Corazón de oscuridad", 34664: "Mota solar", 32897: "Marca de los Illidari",
             30311: "Pieza de armadura de Kael", 23571: "Primal Might? (no)", }
RAID_MATS.pop(23571)


def load_professions():
    """Recetas de AtlasLootClassic (GPL-2): hechizo -> (objeto creado, profesión, habilidad, [(reactivo, cantidad)])."""
    out, by_item = {}, {}
    text = (FUENTES / "alc/AtlasLootClassic/Data/Profession.lua").read_text(encoding="utf-8", errors="replace")
    for m in re.finditer(r"\[(\d+)\] = \{(nil|\d+),(\d+),(\d+),\d+,\d+,\{([\d,]*)\},\{([\d,]*)\}\}", text):
        spell, item, prof, skill = int(m.group(1)), m.group(2), int(m.group(3)), int(m.group(4))
        item = None if item == "nil" else int(item)
        regs = list(zip(map(int, filter(None, m.group(5).split(","))), map(int, filter(None, m.group(6).split(",")))))
        if spell not in out or (item and not out[spell][0]):
            out[spell] = (item, prof, skill, regs)
        if item and item not in by_item:
            by_item[item] = spell
    return out, by_item


def load_tbc_phase():
    """Fase de cada objeto en el TBC original (wowsims/tbc, solo como orientación para el control de fases)."""
    ph = {}
    for line in (FUENTES / "wstbc/sim/core/items/all_items.go").read_text().splitlines():
        m = re.search(r'ID: (\d+),.*?Phase: (\d+)', line)
        if m:
            ph[int(m.group(1))] = int(m.group(2))
    return ph


def load_wowsims_wotlk():
    """Bonificación de ranura y datos de artesanía de wowsims/wotlk (datos de Wowhead WotLK)."""
    items = {}
    for f in ("leftover_db.json", "db.json"):
        for it in json.loads((FUENTES / "wswotlk/assets/database" / f).read_text())["items"]:
            items[it["id"]] = it
    return items


def load_tooltips(ids):
    """Texto de los tooltips WotLK de Wowhead (volcado de wowsims/wotlk) para los objetos pedidos."""
    out = {}
    with open(FUENTES / "wswotlk/assets/db_inputs/wowhead_item_tooltips.csv", encoding="utf-8") as f:
        for line in f:
            a, _, b = line.partition(",")
            if a.isdigit() and int(a) in ids:
                t = json.loads(b).get("tooltip", "")
                out[int(a)] = " ".join(re.sub(r"<[^>]+>", " ", t).replace("&nbsp;", " ").split())
    return out


class Fuentes:
    def __init__(self, ix):
        self.ix = ix
        self.phase = load_tbc_phase()
        self.ws = load_wowsims_wotlk()
        # receta: hechizo que enseña -> objetos receta; y el hechizo de fabricación de cada objeto (wowsims)
        self.recipes_for_spell = collections.defaultdict(list)
        for e, it in ix.items.items():
            if it["class"] == 9 and it["spellid_2"]:
                self.recipes_for_spell[it["spellid_2"]].append(e)
        self.prof, self.prof_by_item = load_professions()
        self.craft_spell = {}
        for iid, it in self.ws.items():
            for s in it.get("sources") or []:
                if "crafted" in s:
                    self.craft_spell[iid] = (s["crafted"].get("spellId"), s["crafted"].get("profession"))
        for item, spell in self.prof_by_item.items():
            if item not in self.craft_spell:
                self.craft_spell[item] = (spell, {2: 2, 3: 8, 4: 1, 8: 11, 9: 4, 10: 3, 14: 7, 15: 6}.get(self.prof[spell][1]))
        self._cache = {}
        self._rcache = {}
        # objetos "propios" de cada tabla de botín (directos o por referencias poco compartidas): sirven para
        # distinguir el botín de un jefe sin aparición del botín de mundo que comparten cientos de criaturas
        refuse = collections.Counter(r["Reference"] for rows in ix.closs.values() for r in rows if r["Reference"])
        def own(rows, d=0):
            out = set()
            for r in rows:
                if r["Reference"]:
                    if refuse[r["Reference"]] <= 4 and d < 4:
                        out |= own(ix.ref.get(r["Reference"], []), d + 1)
                elif r["Item"]:
                    out.add(r["Item"])
            return out
        self.own = {}
        for e, t in ix.ctpl.items():
            if t["lootid"] and ix.heroic_of.get(e, e) not in ix.cmap:
                self.own[e] = own(ix.closs.get(t["lootid"], []))

    # ---------- descripción de una fuente ----------
    def _boss(self, npc):
        n = self.ix.creature_name(self.ix.heroic_of.get(npc, npc))
        return re.sub(r"\s*\(\d\)$", "", n)

    def describe(self, s, item=None):
        """(permitida, categoría, instancia_es, jefe_es, faccion, nota)"""
        ix = self.ix
        t = s["type"]
        m = s.get("map")
        if t == "drop" and m is None:
            npc = ix.heroic_of.get(s["npc"], s["npc"])
            if npc in LATER_NPCS:
                return (False, "invocación de fase posterior", "", "", "", "")
            if npc in SCRIPTED_BOSSES:
                m = SCRIPTED_BOSSES[npc]
            elif item in self.own.get(s["npc"], ()):
                return (False, "criatura sin ubicación conocida", "", "", "", "")
            else:
                return (True, "mundo", "Botín de mundo", "BoE / subasta", "", "")
        cat = MAPS.get(m, (None, None, "world"))[2] if m is not None else "world"
        if t == "drop" and ix.heroic_of.get(s["npc"], s["npc"]) in LATER_NPCS:
            return (False, "invocación de fase posterior", "", "", "", "")
        if t in ("drop", "object"):
            if t == "drop" and s["npc"] in WORLD_BOSSES:
                return (False, "jefe de mundo", "", "", "", "")
            if cat == "no":
                return (False, "prohibido", MAPS[m][0], "", "", "")
            if cat == "world" and (s.get("chance") or 0) < 0.5:
                # botín de mundo aleatorio (muy baja probabilidad en muchas criaturas)
                return (True, "mundo", "Botín de mundo", "BoE / subasta", "", "")
            if t == "drop":
                boss = self._boss(s["npc"])
            else:
                boss = ix.gotpl.get(s["go"], {}).get("name", "Cofre")
            inst = MAPS.get(m, ("Mundo", "World", "world"))[0]
            if cat == "tbc5":
                inst += " (Heroico)" if s.get("heroic") else ""
                return (True, "mazmorra", inst, boss, "", "")
            if cat == "classic_raid":
                return (True, "banda clásica", inst, boss, "", "Banda clásica")
            if m in CLASSIC_DUNGEONS:
                return (True, "mazmorra clásica", CLASSIC_DUNGEONS[m], boss, "", "")
            zone = QUEST_ZONES.get(s.get("zone"))
            return (True, "mundo", f"Mundo: {zone}" if zone else inst, boss, "", "")
        if t == "vendor":
            npc = s["npc"]
            if npc in BADGE_VENDORS:
                return (True, "insignias", "Insignias de justicia", BADGE_VENDORS[npc], "", "")
            if m is not None and MAPS.get(m, (0, 0, "world"))[2] == "no":
                return (False, "prohibido", "", "", "", "")
            if s.get("zone") in LATER_ZONES:
                return (False, "fase posterior", "", "", "", "")
            if s.get("extcost"):
                # ItemExtendedCost.dbc no está en AzerothCore: solo se aceptan objetos de reputación de Terrallende
                # (inscripciones, Esporaggar...) sin temple; JcJ y fichas de banda quedan fuera.
                it = ix.items.get(item, {})
                fac = FACTIONS.get(it.get("RequiredReputationFaction"))
                pvp = any(it.get(f"stat_type{i}") == 35 for i in range(1, 11))
                if fac and fac[2] in ("", "A", "H") and not pvp:
                    return (True, "vendedor", "Vendedor", self._boss(npc), "", "coste extra además del oro (ItemExtendedCost)")
                return (False, "coste especial (JcJ u otras fichas)", "", "", "", "")
            return (True, "vendedor", "Vendedor", self._boss(npc), "", "")
        if t == "quest":
            q = ix.quests.get(s["quest"], {})
            zone = q.get("QuestSortID", 0)
            facs = [q.get(f"RewardFactionID{i}") for i in range(1, 6)]
            starts = ix.qstart.get(s["quest"], set())
            if starts and all(MAPS.get(m, ("", "", ""))[2] == "no" for m, z in starts):
                return (False, "misión de Rasganorte o de banda", "", "", "", "")
            if any(z in NORTHREND_ZONES for m, z in starts):
                return (False, "misión de Rasganorte", "", "", "", "")
            if zone in NORTHREND_ZONES:
                return (False, "misión de Rasganorte", "", "", "", "")
            if zone in EVENT_SORTS:
                return (False, "evento de temporada", "", "", "", "")
            if zone in RAID_QUEST_ZONES:
                return (False, "misión de banda o de Quel'Danas", "", "", "", "")
            if any(FACTIONS.get(f, ("", "", ""))[2] in ("later", "raid") for f in facs if f):
                return (False, "misión de fase posterior", "", "", "", "")
            title = ix.qtitle_es.get(q.get("ID")) or q.get("LogTitle", "")
            races = q.get("AllowableRaces") or 0
            side = "A" if races and not races & HORDE_RACES else "H" if races and not races & ALLIANCE_RACES else ""
            where = QUEST_ZONES.get(zone) or ("Feria de la Luna Negra" if zone == -364 else
                                               "Azeroth" if zone > 0 else "clase o profesión")
            return (True, "misión", "Misión: " + where,
                    title, side, "")
        if t == "container":
            return (None, "contenedor", "", "", "", "")
        return (False, t, "", "", "", "")

    def sources(self, iid, depth=0):
        """Lista de fuentes permitidas [(categoría, instancia, jefe, facción, nota)] y motivos de rechazo."""
        if iid in self._cache:
            return self._cache[iid]
        ix = self.ix
        ok, bad = [], set()
        for s in ix.src.get(iid, []):
            if s["type"] == "container":
                if depth < 2:
                    sub, _ = self.sources(s["item"], depth + 1)
                    ok += sub
                continue
            allowed, cat, inst, boss, side, note = self.describe(s, iid)
            if allowed:
                ok.append((cat, inst, boss, side, note))
            else:
                bad.add(cat)
        # artesanía: hechizo de fabricación (wowsims) -> receta en AzerothCore o instructor
        cs = self.craft_spell.get(iid)
        if cs and self.reagents_bad(cs[0]):
            bad.add("receta con materiales de banda o de Rasganorte: " + "; ".join(self.reagents_bad(cs[0])))
            cs = None
        if cs:
            spell, prof = cs
            prof_es = {1: "Alquimia", 2: "Herrería", 3: "Encantamiento", 4: "Ingeniería", 7: "Joyería",
                       8: "Peletería", 11: "Sastrería", 6: "Inscripción"}.get(prof, "Profesión")
            recs = self.recipes_for_spell.get(spell, [])
            rec_ok = []
            for r in recs:
                sub, _ = self.sources(r, depth + 1) if depth < 2 else ([], set())
                if sub:
                    rank = ix.items[r]["RequiredSkillRank"]
                    rec_ok.append((r, sub, rank))
            rec_ok = [x for x in rec_ok if x[2] <= 375]
            if rec_ok:
                r, sub, rank = rec_ok[0]
                where = f"{sub[0][1]}: {sub[0][2]}".strip(": ")
                ok.append(("profesión", prof_es, f"{ix.items[r]['name']} ({rank}) — {where}", sub[0][3], ""))
            elif spell in ix.trainer_spells:
                rank = ix.trainer_spells[spell]["ReqSkillRank"]
                if rank > 375:
                    bad.add("profesión por encima de 375")
                elif iid >= 34000 and iid not in self.phase:
                    bad.add("receta de instructor de WotLK (materiales de Rasganorte)")
                else:
                    ok.append(("profesión", prof_es, f"Instructor ({rank})", "", ""))
            elif recs:
                bad.add("receta de banda o de fase posterior")
        self._cache[iid] = (ok, bad)
        return ok, bad

    def check(self, iid):
        """Fuentes permitidas en la prefase y motivos de rechazo, con los filtros de reputación y fase."""
        it = self.ix.items[iid]
        if iid >= 36000 and iid not in self.phase:
            # objetos añadidos en WotLK (misiones de Rasganorte que AzerothCore no sitúa por zona, etc.)
            return [], {"objeto de WotLK"}
        ok, bad = self.sources(iid)
        bad = set(bad)
        f = FACTIONS.get(it["RequiredReputationFaction"])
        if f and f[2] in ("later", "raid"):
            return [], bad | {f"reputación {f[0]}"}
        ph = self.phase.get(iid)
        if ph and ph > 1:
            badge = [s for s in ok if s[0] == "insignias"]
            if not badge:
                return [], bad | {f"fase {ph} del TBC original"}
        return ok, bad

    def reagents_bad(self, spell):
        """Reactivos de la receta que no se pueden conseguir en la prefase (materiales de banda o de Rasganorte)."""
        if spell in self._rcache:
            return self._rcache[spell]
        bad = []
        for rid, n in self.prof.get(spell, (None, 0, 0, []))[3]:
            if rid in RAID_MATS:
                bad.append(f"{n}x {RAID_MATS[rid]} ({rid})")
                continue
            srcs = self.ix.src.get(rid, [])
            if srcs and rid not in self._rcache.get("_stack", set()):
                allowed = [x for x in srcs if self.describe(x, rid)[0] is not False]
                if not allowed and not self.craft_spell.get(rid):
                    bad.append(f"{n}x {self.ix.items.get(rid, {}).get('name', rid)} ({rid}) solo en contenido cerrado")
        self._rcache[spell] = bad
        return bad

    def faction_of(self, it, srcs):
        races = it["AllowableRace"]
        if races not in (-1, 0) and races & ALLIANCE_RACES and not races & HORDE_RACES:
            return "Alianza"
        if races not in (-1, 0) and races & HORDE_RACES and not races & ALLIANCE_RACES:
            return "Horda"
        f = FACTIONS.get(it["RequiredReputationFaction"])
        if f and f[2] in ("A", "H"):
            return {"A": "Alianza", "H": "Horda"}[f[2]]
        sides = {s[3] for s in srcs if s[3]}
        if sides == {"A"}:
            return "Alianza"
        if sides == {"H"}:
            return "Horda"
        return "Ambas"

    def reputation(self, it):
        f = it["RequiredReputationFaction"]
        if f:
            name = FACTIONS.get(f, (f"facción {f}", "", ""))
            return name, RANKS.get(it["RequiredReputationRank"], str(it["RequiredReputationRank"]))
        return None
