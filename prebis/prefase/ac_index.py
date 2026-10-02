"""Índice de fuentes de objetos a partir de la base de datos de AzerothCore 3.3.5.

Para cada objeto devuelve dónde se consigue: botín de criatura (con mapa y si es heroico), cofre, vendedor,
misión, otro objeto (bolsas) y receta. Todo sale de las tablas SQL de AzerothCore; los nombres de mapas y zonas,
que en el servidor viven en los DBC del cliente, están escritos a mano abajo.
"""
import collections
import os
from pathlib import Path

import ac_sql

AC = Path(os.environ.get("AC_DB", "/tmp/claude-0/ac/data/sql/base/db_world"))
CACHE = Path(os.environ.get("AC_CACHE", "/tmp/claude-0/acdb"))


def T(name, **kw):
    return ac_sql.cached(CACHE, name, AC / f"{name}.sql", **kw)


# ---------- Mapas (Map.dbc) ----------
MAPS = {
    # Mazmorras de TBC (fase 1)
    543: ("Murallas del Fuego Infernal", "Hellfire Ramparts", "tbc5"), 542: ("El Horno de Sangre", "The Blood Furnace", "tbc5"),
    540: ("Las Salas Arrasadas", "The Shattered Halls", "tbc5"), 547: ("Recinto de los Esclavos", "The Slave Pens", "tbc5"),
    546: ("La Sotiénaga", "The Underbog", "tbc5"), 545: ("La Cámara de Vapor", "The Steamvault", "tbc5"),
    557: ("Tumbas de Maná", "Mana-Tombs", "tbc5"), 558: ("Criptas Auchenai", "Auchenai Crypts", "tbc5"),
    556: ("Salas Sethekk", "Sethekk Halls", "tbc5"), 555: ("Laberinto de las Sombras", "Shadow Labyrinth", "tbc5"),
    560: ("Antiguas Laderas de Trabalomas", "Old Hillsbrad Foothills", "tbc5"),
    269: ("La Ciénaga Negra", "The Black Morass", "tbc5"), 554: ("El Mechanar", "The Mechanar", "tbc5"),
    553: ("El Invernáculo", "The Botanica", "tbc5"), 552: ("El Arcatraz", "The Arcatraz", "tbc5"),
    # Prohibido
    585: ("Bancal del Magister", "Magisters' Terrace", "no"),
    532: ("Karazhan", "Karazhan", "no"), 565: ("Guarida de Gruul", "Gruul's Lair", "no"),
    544: ("Guarida de Magtheridon", "Magtheridon's Lair", "no"), 548: ("Caverna Santuario Serpiente", "Serpentshrine Cavern", "no"),
    550: ("El Ojo", "Tempest Keep", "no"), 534: ("Cima Hyjal", "Hyjal Summit", "no"), 564: ("Templo Oscuro", "Black Temple", "no"),
    568: ("Zul'Aman", "Zul'Aman", "no"), 580: ("Meseta de La Fuente del Sol", "Sunwell Plateau", "no"),
    # Bandas clásicas (permitidas, se marcan)
    409: ("Núcleo de Magma", "Molten Core", "classic_raid"), 469: ("Guarida Alanegra", "Blackwing Lair", "classic_raid"),
    531: ("Templo de Ahn'Qiraj", "Temple of Ahn'Qiraj", "classic_raid"), 509: ("Ruinas de Ahn'Qiraj", "Ruins of Ahn'Qiraj", "classic_raid"),
    309: ("Zul'Gurub", "Zul'Gurub", "classic_raid"),
    # Mundo
    530: ("Terrallende", "Outland", "world"), 0: ("Reinos del Este", "Eastern Kingdoms", "world"),
    1: ("Kalimdor", "Kalimdor", "world"), 571: ("Rasganorte", "Northrend", "no"),
}
# Mapas de Rasganorte y bandas de WotLK (incluida Naxxramas 80 y Onyxia 80): prohibidos.
for m in (533, 249, 574, 575, 576, 578, 595, 599, 600, 601, 602, 603, 604, 608, 615, 616, 619, 624, 631, 632, 649, 650, 658, 668, 724):
    MAPS.setdefault(m, ("Rasganorte / banda de WotLK", "Northrend / WotLK raid", "no"))

FACTIONS = {
    946: ("Bastión del Honor", "Honor Hold", "A"), 947: ("Thrallmar", "Thrallmar", "H"),
    942: ("Expedición Cenarion", "Cenarion Expedition", ""), 1011: ("Bajo Arrabal", "Lower City", ""),
    935: ("Los Sha'tar", "The Sha'tar", ""), 989: ("Vigilantes del Tiempo", "Keepers of Time", ""),
    932: ("Los Aldor", "The Aldor", ""), 934: ("Los Arúspices", "The Scryers", ""),
    933: ("El Consorcio", "The Consortium", ""), 978: ("Kurenai", "Kurenai", "A"), 941: ("Los Mag'har", "The Mag'har", "H"),
    970: ("Esporaggar", "Sporeggar", ""),
    # Fases posteriores o de banda: no entran en la prefase
    1015: ("Ala Abisal", "Netherwing", "later"), 1031: ("Guardia del cielo Sha'tari", "Sha'tari Skyguard", "later"),
    1038: ("Ogri'la", "Ogri'la", "later"), 1077: ("Ofensiva Sol Devastado", "Shattered Sun Offensive", "later"),
    967: ("El Ojo Violeta", "The Violet Eye", "raid"), 1012: ("Juramorte Lengua de Ceniza", "Ashtongue Deathsworn", "raid"),
    990: ("La Escama de las Arenas", "The Scale of the Sands", "raid"),
}
RANKS = {3: "Neutral", 4: "Amistoso", 5: "Honorable", 6: "Venerado", 7: "Exaltado"}

ALLIANCE_RACES = 1 | 4 | 8 | 64 | 1024
HORDE_RACES = 2 | 16 | 32 | 128 | 512


class Index:
    def __init__(self):
        self.items = {r["entry"]: r for r in T("item_template")}
        self.name_es = {
            r["ID"]: r["Name"] for r in ac_sql.cached(CACHE, "item_locale", AC / "item_template_locale.sql",
                                                       where=lambda d: d["locale"] == "esES", keep=["ID", "Name"])}
        ct = T("creature_template", keep=["entry", "difficulty_entry_1", "name", "lootid", "rank", "npcflag", "faction"])
        self.ctpl = {r["entry"]: r for r in ct}
        self.cname_es = {r["entry"]: r["Name"] for r in ac_sql.cached(
            CACHE, "creature_locale", AC / "creature_template_locale.sql", where=lambda d: d["locale"] == "esES",
            keep=["entry", "Name"])}
        # mapa de cada criatura (por sus apariciones); las versiones heroicas heredan el de la normal
        self.cmap = collections.defaultdict(set)
        for r in T("creature", keep=["id1", "map", "zoneId"]):
            self.cmap[r["id1"]].add((r["map"], r["zoneId"]))
        self.heroic_of = {}
        for r in ct:
            if r["difficulty_entry_1"]:
                self.heroic_of[r["difficulty_entry_1"]] = r["entry"]
        # botín
        self.ref = collections.defaultdict(list)
        for r in T("reference_loot_template"):
            self.ref[r["Entry"]].append(r)
        self.closs = collections.defaultdict(list)
        for r in T("creature_loot_template"):
            self.closs[r["Entry"]].append(r)
        self.goloot = collections.defaultdict(list)
        for r in T("gameobject_loot_template"):
            self.goloot[r["Entry"]].append(r)
        self.itemloot = collections.defaultdict(list)
        for r in T("item_loot_template"):
            self.itemloot[r["Entry"]].append(r)
        gt = T("gameobject_template", keep=["entry", "type", "name", "Data1"])
        self.gotpl = {r["entry"]: r for r in gt}
        self.gomap = collections.defaultdict(set)
        for r in T("gameobject", keep=["id", "map", "zoneId"]):
            self.gomap[r["id"]].add((r["map"], r["zoneId"]))
        self.vendor = collections.defaultdict(list)
        for r in T("npc_vendor"):
            self.vendor[r["item"]].append(r)
        self.quests = {r["ID"]: r for r in T("quest_template")}
        self.qtitle_es = {r["ID"]: r["Title"] for r in ac_sql.cached(
            CACHE, "quest_locale", AC / "quest_template_locale.sql", where=lambda d: d["locale"] == "esES",
            keep=["ID", "Title"])}
        self.trainer_spells = {r["SpellId"]: r for r in T("trainer_spell")}
        # dónde empieza cada misión (mapa del PNJ u objeto que la da)
        self.qstart = collections.defaultdict(set)
        for r in T("creature_queststarter"):
            for m, z in self.cmap.get(r["id"], ()):
                self.qstart[r["quest"]].add((m, z))
        for r in T("gameobject_queststarter"):
            for m, z in self.gomap.get(r["id"], ()):
                self.qstart[r["quest"]].add((m, z))
        self._build()

    # ----- botín: objeto -> [(tipo, id_fuente, probabilidad)]
    def _expand(self, rows, depth=0, seen=None):
        out = []
        for r in rows:
            if r["Reference"]:
                if depth < 6:
                    for item, ch in self._expand(self.ref.get(r["Reference"], []), depth + 1):
                        out.append((item, ch * (r["Chance"] or 100) / 100))
            elif r["Item"]:
                out.append((r["Item"], r["Chance"]))
        return out

    def _build(self):
        self.src = collections.defaultdict(list)
        lootid_to_creatures = collections.defaultdict(list)
        for e, r in self.ctpl.items():
            if r["lootid"]:
                lootid_to_creatures[r["lootid"]].append(e)
        for lootid, rows in self.closs.items():
            creatures = lootid_to_creatures.get(lootid, [])
            items = self._expand(rows)
            for c in creatures:
                normal = self.heroic_of.get(c, c)
                maps = self.cmap.get(normal) or {(None, None)}
                for item, ch in items:
                    for m, z in maps:
                        self.src[item].append({"type": "drop", "npc": c, "heroic": c in self.heroic_of,
                                               "map": m, "zone": z, "chance": ch})
        for e, g in self.gotpl.items():
            if g["type"] == 3 and g["Data1"] in self.goloot:
                maps = self.gomap.get(e) or {(None, None)}
                for item, ch in self._expand(self.goloot[g["Data1"]]):
                    for m, z in maps:
                        self.src[item].append({"type": "object", "go": e, "map": m, "zone": z, "chance": ch,
                                               "heroic": "Heroic" in (g["name"] or "")})
        for item, rows in self.vendor.items():
            for r in rows:
                maps = self.cmap.get(r["entry"]) or {(None, None)}
                for m, z in list(maps)[:1]:
                    self.src[item].append({"type": "vendor", "npc": r["entry"], "map": m, "zone": z,
                                           "extcost": r["ExtendedCost"]})
        for q in self.quests.values():
            ids = [q.get(f"RewardItem{i}") for i in range(1, 5)] + [q.get(f"RewardChoiceItemID{i}") for i in range(1, 7)]
            for item in ids:
                if item:
                    self.src[item].append({"type": "quest", "quest": q["ID"], "zone": q["QuestSortID"]})
        for bag, rows in self.itemloot.items():
            for item, ch in self._expand(rows):
                self.src[item].append({"type": "container", "item": bag, "chance": ch})

    def creature_name(self, e):
        return self.cname_es.get(e) or self.ctpl.get(e, {}).get("name", f"#{e}")

    def creature_name_en(self, e):
        return self.ctpl.get(e, {}).get("name", f"#{e}")

    def item_name_es(self, i):
        return self.name_es.get(i) or self.items.get(i, {}).get("name", f"#{i}")
