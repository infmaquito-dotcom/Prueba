"""Listas BiS de la prefase de TBC en un servidor 3.3.5a (AzerothCore), por especialización.

Uso: python3 prefase.py <carpeta_salida> [Clase/Spec ...]

Genera bis_prefase.json, Bistooltip_prefase_bislists.lua, Bistooltip_prefase_sources.lua y revision.md.
Fuentes: AzerothCore (azerothcore-wotlk, data/sql/base/db_world) para objetos, botín, vendedores, misiones y
nombres esES; wowsims/wotlk solo para pesos de nivel 80 (que se adaptan al 70), bonificaciones de ranura y
estadísticas de encantamientos; wowsims/tbc solo para la fase original de cada objeto. No se usa Questie.
"""
import collections
import itertools
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import modelo
from modelo import item_stats, ws_vec, score, effects, equip_stats, ES
from ac_index import Index, MAPS
from fuentes import Fuentes, SLOT_INV, load_tooltips
from specs import SPECS, CLASS, GEM_LIST, METAS, GLYPHS, ENCHANT_EXTRA, MANUAL_VALUES, RELICS

SLOT_ORDER = ["Head", "Neck", "Shoulder", "Back", "Chest", "Wrist", "Hands", "Waist", "Legs", "Feet", "Finger",
              "Trinket", "Weapon", "Off hand", "Relic", "Ranged"]
SLOT_ES = {"Head": "Cabeza", "Neck": "Cuello", "Shoulder": "Hombros", "Back": "Espalda", "Chest": "Pecho",
           "Wrist": "Muñecas", "Hands": "Manos", "Waist": "Cintura", "Legs": "Piernas", "Feet": "Pies",
           "Finger": "Anillos", "Trinket": "Abalorios", "Weapon": "Arma", "Off hand": "Mano izquierda",
           "Relic": "Reliquia", "Ranged": "A distancia"}
# tipo de ranura de wowsims (enchant.type) -> hueco
WS_SLOT = {1: "Head", 2: "Neck", 3: "Shoulder", 4: "Back", 5: "Chest", 6: "Wrist", 7: "Hands", 8: "Waist", 9: "Legs",
           10: "Feet", 11: "Finger", 13: "Weapon", 14: "Ranged"}
FITS = {2: {"R"}, 4: {"Y"}, 8: {"B"}}  # color de ranura de item_template -> color que la cumple
COLORS = {"R": {"R"}, "Y": {"Y"}, "B": {"B"}, "O": {"R", "Y"}, "P": {"R", "B"}, "G": {"Y", "B"}}


BONUS_ARMOR_INV = {2, 11, 12, 13, 14, 15, 17, 21, 22, 23, 25, 26, 28}
WS_ENCHANTS = json.loads(Path("/tmp/claude-0/wswotlk/assets/database/db.json").read_text())["enchants"]


class Builder:
    def __init__(self):
        self.ix = Index()
        self.f = Fuentes(self.ix)
        self.tbc_lists = self._tbc_lists()
        # bonificación de ranura: id de encantamiento (item_template.socketBonus) -> estadísticas (vía wowsims)
        self.bonus = {}
        for iid, w in self.f.ws.items():
            it = self.ix.items.get(iid)
            if it and it["socketBonus"] and w.get("socketBonus"):
                self.bonus.setdefault(it["socketBonus"], ws_vec(w["socketBonus"]))
        self.by_name = collections.defaultdict(list)
        for e, it in self.ix.items.items():
            self.by_name[it["name"]].append(e)
        self.pool = self._pool()
        self._cands = {}
        self.tt = load_tooltips({e for e, *_ in self.pool} | set(METAS))

    # ---------- listas originales del TBC (Bistooltip wowtbc, solo para comparar en revision.md) ----------
    def _tbc_lists(self):
        out = collections.defaultdict(dict)
        p = Path("/tmp/claude-0/BiS-Tooltip_335a_backport_TBC/Bistooltip_wowtbc_bislists.lua")
        if not p.exists():
            return out
        for m in re.finditer(r'\["(\w+)"\]\["(\w+)"\]\["PreRaid"\]\[\d+\] = \{ \["slot_name"\] = "(\w+)".*?\}, (.*?) \};',
                             p.read_text()):
            ids = [int(x) for x in re.findall(r"\] = (-?\d+)", m.group(4)) if int(x) > 0]
            out[(m.group(1), m.group(2))][m.group(3)] = ids
        return out

    # ---------- catálogo de la prefase ----------
    def _pool(self):
        """(id, hueco, fuentes permitidas, motivos, solo_insignias) de todo lo equipable que se puede conseguir."""
        pool = []
        for e, it in self.ix.items.items():
            slot = SLOT_INV.get(it["InventoryType"])
            if not slot or it["class"] not in (2, 4) or it["Quality"] < 2 or it["RequiredLevel"] > 70:
                continue
            if it["RandomProperty"] or it["RandomSuffix"] or it["ItemLevel"] > 200:
                continue
            ok, bad = self.f.check(e)
            if not ok:
                continue
            badge_only = all(s[0] == "insignias" for s in ok)
            pool.append((e, slot, ok, bad, badge_only))
        return pool

    # ---------- uso por clase ----------
    def usable(self, it, cls, kind):
        c = CLASS[cls]
        if it["AllowableClass"] not in (-1, 0) and not it["AllowableClass"] & c["mask"]:
            return False
        sub = it["subclass"]
        if it["class"] == 4:
            inv = it["InventoryType"]
            if inv in (1, 3, 5, 20, 6, 7, 8, 9, 10) and sub not in c["armor"]:
                return False
            if inv == 14 and sub == 6 and "shield" not in (kind.get("off") or ()):  # escudo
                return False
            if inv == 28 and sub != c.get("relic"):
                return False
        if it["class"] == 2:
            if sub not in c["weapons"]:
                return False
        return True

    def weapon_kind(self, it):
        inv, sub = it["InventoryType"], it["subclass"]
        if it["class"] == 4:
            return "shield" if sub == 6 else "relic" if inv == 28 else "held" if inv == 23 else None
        if inv == 17:
            return "2h"
        if inv in (13, 21):
            return "mh" if inv == 21 else "1h"
        if inv == 22:
            return "oh"
        if inv in (15, 25, 26):
            return "wand" if sub == 19 else "ranged"
        return None

    # ---------- valoración ----------
    def gem_value(self, gid, w):
        return score(GEM_LIST[gid]["stats"], w)

    def best_gems(self, w, allowed):
        """Mejor gema de cada color (R, Y, B, O, P, G) entre las permitidas."""
        best = {}
        for gid in allowed:
            g = GEM_LIST[gid]
            v = score(g["stats"], w)
            if v > best.get(g["color"], (0, None))[0]:
                best[g["color"]] = (v, gid)
        return best

    def socket_value(self, it, w, best, meta_val):
        socks = [it[f"socketColor_{i}"] for i in (1, 2, 3) if it[f"socketColor_{i}"]]
        if not socks:
            return 0.0, []
        any_best = max(best.values())
        free = sum(meta_val if c == 1 else any_best[0] for c in socks)
        matched = 0.0
        for c in socks:
            if c == 1:
                matched += meta_val
            else:
                need = next(iter(FITS[c]))
                matched += max(v for col, (v, _) in best.items() if need in COLORS[col])
        bonus = score(self.bonus.get(it["socketBonus"], {}), w)
        return max(free, matched + bonus), socks

    def evaluate(self, e, sp, w, best, meta_val, slot=None):
        it = self.ix.items[e]
        st = item_stats(it)
        if "ARMOR" in st and it["InventoryType"] in BONUS_ARMOR_INV:  # armadura adicional (anillos, armas, abalorios...)
            st["BARMOR"] = st.pop("ARMOR")
        for k, v in equip_stats(self.tt.get(e, "")).items():  # hechizos de equipar que AzerothCore no guarda como estadística
            if v > st.get(k, 0):
                st[k] = v
        dps = st.pop("DPS", 0)
        st.pop("SPEED", None)
        v = score(st, w)
        notes = []
        kind = self.weapon_kind(it)
        if dps:
            wkey = {"Off hand": "OH", "Ranged": "RANGED"}.get(slot, "MH")
            v += dps * w.get(wkey, 0)
        sv, socks = self.socket_value(it, w, best, meta_val)
        v += sv
        if e in MANUAL_VALUES.get(sp["key"], {}):
            mv, why = MANUAL_VALUES[sp["key"]][e]
            v += mv
            notes.append(why)
        elif it["InventoryType"] in (12, 28):
            ef, en = effects(self.tt.get(e, ""))
            v += score(ef, w)
            notes += en
        return v, st, dps, socks, notes

    # ---------- elección por hueco ----------
    def candidates(self, sp, slot, badge):
        key = (sp["key"], slot, badge, tuple(sp["weapons"].get("main", ())), tuple(sp["weapons"].get("off") or ()))
        if key not in self._cands:
            self._cands[key] = [x for x in self._cands_raw(sp, slot, badge)]
        return self._cands[key]

    def rank_slot(self, sp, slot, w, best, meta_val, badge, n=6):
        out, seen = [], set()
        for e, s, ok, bad, badge_only in self.candidates(sp, slot, badge):
            it = self.ix.items[e]
            v, st, dps, socks, notes = self.evaluate(e, sp, w, best, meta_val, slot)
            if slot == "Relic" and v <= 0 and sp["key"] in RELICS:
                continue
            if slot == "Relic" and v <= 0:
                notes = notes + ["efecto de reliquia no valorado: se ordena por nivel de objeto"]
                v = it["ItemLevel"] / 1000
            if v <= 0 or it["name"] in seen:
                continue
            seen.add(it["name"])
            out.append((v, e, ok, st, dps, socks, notes))
        out.sort(key=lambda x: -x[0])
        return out[:n]

    def _cands_raw(self, sp, slot, badge):
        cls = sp["class"]
        for e, s, ok, bad, badge_only in self.pool:
            if badge_only != badge:
                continue
            it = self.ix.items[e]
            if not self.usable(it, cls, sp["weapons"]):
                continue
            kind = self.weapon_kind(it)
            if slot == "Weapon":
                if s not in ("Weapon",) or kind not in sp["weapons"]["main"]:
                    continue
                if sp["weapons"].get("main_sub") and it["subclass"] not in sp["weapons"]["main_sub"]:
                    continue
            elif slot == "Off hand":
                if kind not in (sp["weapons"].get("off") or ()):
                    continue
                if kind in ("1h", "oh", "2h") and sp["weapons"].get("off_sub") and \
                        it["subclass"] not in sp["weapons"]["off_sub"]:
                    continue
            elif slot == "Relic":
                if kind != "relic":
                    continue
            elif slot == "Ranged":
                if kind not in sp["weapons"].get("ranged", ()):
                    continue
            elif s != slot:
                continue
            yield (e, s, ok, bad, badge_only)

    # ---------- plan de gemas con la meta ----------
    def gem_plan(self, chosen, w, allowed, meta):
        """Gemas para las ranuras del equipo elegido que maximizan EP cumpliendo el requisito de la meta."""
        req = METAS[meta]["req"] if meta else {}
        CAP = 8
        options = []  # por objeto: lista de (r, y, b, valor, gemas)
        cand = {}
        for gid in allowed:
            g = GEM_LIST[gid]
            v = score(g["stats"], w)
            if v > cand.get(g["color"], (0, None))[0]:
                cand[g["color"]] = (v, gid)
        for e in chosen:
            it = self.ix.items[e]
            socks = [it[f"socketColor_{i}"] for i in (1, 2, 3) if it[f"socketColor_{i}"] and it[f"socketColor_{i}"] != 1]
            if not socks:
                continue
            bonus = score(self.bonus.get(it["socketBonus"], {}), w)
            opts = {}
            for combo in itertools.product(cand.items(), repeat=len(socks)):
                val = sum(c[1][0] for c in combo)
                if all(next(iter(FITS[s])) in COLORS[c[0]] for s, c in zip(socks, combo)):
                    val += bonus
                r = sum("R" in COLORS[c[0]] for c in combo)
                y = sum("Y" in COLORS[c[0]] for c in combo)
                b = sum("B" in COLORS[c[0]] for c in combo)
                key = (r, y, b)
                if val > opts.get(key, (-1,))[0]:
                    opts[key] = (val, e, [c[1][1] for c in combo])
            options.append(list(opts.items()))
        # programación dinámica sobre recuentos de colores (topados en 8)
        dp = {(0, 0, 0): (0.0, [])}
        for opts in options:
            nd = {}
            for (r, y, b), (val, plan) in dp.items():
                for (dr, dy, db), (v2, e, gems) in opts:
                    k = (min(r + dr, CAP), min(y + dy, CAP), min(b + db, CAP))
                    nv = val + v2
                    if nv > nd.get(k, (-1,))[0]:
                        nd[k] = (nv, plan + [(e, gems)])
            dp = nd
        best = None
        for (r, y, b), (val, plan) in dp.items():
            if meets(req, r, y, b):
                if not best or val > best[0]:
                    best = (val, plan, (r, y, b))
        return best

    def allowed_gems(self):
        out, why = [], {}
        for gid, g in GEM_LIST.items():
            ok, src = self.design_ok(g["name"])
            why[gid] = src
            if ok:
                out.append(gid)
        return out, why

    def design_ok(self, gem_name):
        designs = self.by_name.get("Design: " + gem_name, [])
        for d in designs:
            ok, bad = self.f.check(d)
            if ok:
                return True, f"Diseño {d} ({self.ix.items[d]['RequiredSkillRank']}): {ok[0][1]} — {ok[0][2]}"
        if designs:
            return False, f"Diseño {designs} no conseguible en la prefase"
        return False, "Sin diseño en AzerothCore"

    # ---------- encantamientos ----------
    def enchants_for(self, sp, slot, w, it=None):
        """Encantamientos permitidos para el hueco, con su comprobación en AzerothCore."""
        out = []
        ench = WS_ENCHANTS
        for en in ench + ENCHANT_EXTRA:
            es = WS_SLOT.get(en["type"])
            if es == "Weapon" and slot == "Off hand" and en.get("enchantType") != 2 and \
                    set(sp["weapons"].get("off") or ()) & {"1h", "oh", "2h"}:
                es = "Off hand"   # arma de la mano izquierda
            if en.get("enchantType") == 2:
                es = "Off hand"
            if es != slot:
                continue
            if en.get("classAllowlist") and CLASS[sp["class"]]["ws"] not in en["classAllowlist"]:
                continue
            if en.get("enchantType") == 1 and "2h" not in sp["weapons"]["main"]:
                continue
            if en.get("enchantType") == 4:  # solo bastones
                continue
            if en.get("enchantType") == 2 and slot != "Off hand":  # escudo
                continue
            if slot == "Off hand" and en.get("enchantType") != 2 and "shield" in (sp["weapons"].get("off") or ()) \
                    and not set(sp["weapons"]["off"]) & {"1h", "oh", "2h"}:
                continue
            if en.get("requiredProfession"):
                continue  # los de profesión (anillos de encantador, etc.) se tratan aparte
            ok, how = self.enchant_ok(en)
            if not ok:
                continue
            st = ws_vec(en["stats"])
            v = score(st, w)
            mv = MANUAL_VALUES.get(sp["key"], {}).get(("spell", en["spellId"]))
            if mv:
                v += mv[0]
                how += "; " + mv[1]
            if v > 0:
                out.append((v, en, how))
        out.sort(key=lambda x: -x[0])
        return out

    def enchant_ok(self, en):
        ix, f = self.ix, self.f
        if en.get("spellId", 0) >= 44000:
            return False, "encantamiento de WotLK"
        pr = f.prof.get(en.get("spellId"))
        if pr and pr[2] > 375:
            return False, f"necesita {pr[2]} de habilidad"
        if pr and f.reagents_bad(en["spellId"]):
            return False, "materiales de banda: " + "; ".join(f.reagents_bad(en["spellId"]))
        if en.get("itemId") and en["itemId"] in ix.items:
            item = en["itemId"]
            ok, bad = f.check(item)
            if ok:
                return True, f"Objeto {item}: {ok[0][1]} — {ok[0][2]}"
            # kits de piernas y pergaminos de encantamiento: receta
            for rid in self.by_name.get("Pattern: " + ix.items[item]["name"], []) + \
                    self.by_name.get("Formula: " + ix.items[item]["name"], []):
                ok, bad = f.check(rid)
                if ok and ix.items[rid]["RequiredSkillRank"] <= 375:
                    return True, f"Receta {rid} ({ix.items[rid]['RequiredSkillRank']}): {ok[0][1]} — {ok[0][2]}"
        sp = en.get("spellId")
        for rid in f.recipes_for_spell.get(sp, []):
            ok, bad = f.check(rid)
            if ok and ix.items[rid]["RequiredSkillRank"] <= 375:
                return True, f"Fórmula {rid} ({ix.items[rid]['RequiredSkillRank']}): {ok[0][1]} — {ok[0][2]}"
        if sp in ix.trainer_spells and ix.trainer_spells[sp]["ReqSkillRank"] <= 375:
            return True, f"Instructor de encantamiento (habilidad {ix.trainer_spells[sp]['ReqSkillRank']})"
        return False, ""


def fmt_src(srcs, n=3):
    seen, out = set(), []
    for cat, inst, boss, side, note in srcs:
        key = (inst, re.sub(r"[^a-z]", "", boss.lower())[:12])
        if key in seen:
            continue
        seen.add(key)
        out.append({"categoria": cat, "instancia": inst, "jefe": boss, "nota": note})
    # prioriza el heroico/normal más accesible: mazmorra > reputación/vendedor > misión > profesión > mundo
    return out[:n]


def meets(req, r, y, b):
    cnt = {"R": r, "Y": y, "B": b}
    if any(cnt[c] < n for c, n in req.get("min", {}).items()):
        return False
    if "more" in req:
        a, c = req["more"]
        return cnt[a] > cnt[c]
    return True


def adapt_weights(sp):
    """Pesos de nivel 80 -> 70 (ver comentario en specs.py)."""
    k = 2.0794 * sp["ref"]["70"] / sp["ref"]["80"]
    w = {}
    calc = []
    for key, v in sp["ws80"].items():
        if key in ("HIT", "CRIT", "HASTE", "ARP", "EXP", "DEF", "DODGE", "PARRY", "BLOCK"):
            w[key] = round(v * k, 3)
            calc.append(f"{ES.get(key, key)}: {v:.2f} x {k:.3f} = {w[key]:.2f}")
        else:
            w[key] = v
    for key, (v, why) in sp.get("w70", {}).items():
        w[key] = v
        calc.append(f"{ES.get(key, key)}: {v:.2f} fijado a mano al 70 ({why})")
    return w, k, calc


def slot_entries(b, sp, slot, w, best, meta_val, badge):
    rows = b.rank_slot(sp, slot, w, best, meta_val, badge)
    out = []
    for v, e, ok, st, dps, socks, notes in rows:
        it = b.ix.items[e]
        srcs = fmt_src(ok)
        rep = b.f.reputation(it)
        out.append({
            "id": e, "nombre_es": b.ix.item_name_es(e), "nombre_en": it["name"], "ep": round(v, 1),
            "faccion": b.f.faction_of(it, ok),
            "fuentes": srcs,
            "reputacion": {"faccion": rep[0][0], "faccion_en": rep[0][1], "nivel": rep[1]} if rep else None,
            "banda_clasica": any(s[0] == "banda clásica" for s in ok),
            "fase_tbc_original": b.f.phase.get(e),
            "nivel_objeto": it["ItemLevel"], "nivel_requerido": it["RequiredLevel"],
            "InventoryType": it["InventoryType"], "estadisticas": st, "dps_arma": dps or None,
            "ranuras": [{2: "roja", 4: "amarilla", 8: "azul", 1: "meta"}[c] for c in socks],
            "bonificacion_ranura": b.bonus.get(it["socketBonus"]) if socks else None,
            "requiere_profesion": it["RequiredSkill"] or None,
            "ligado_al_recoger": it["bonding"] == 1,
            "notas": notes,
        })
    return out


def cap_list(caps, sp):
    """(estadística, tope en índice, peso que le queda pasado el tope) para esta especialización."""
    c = sp["caps"]
    out = []
    if c.get("hit_kind") == "spell":
        out.append(("HIT", caps["golpe con hechizos"]["índice"], sp.get("hit_after_cap", 0.0)))
    elif c.get("hit_kind") == "melee":
        out.append(("HIT", caps["golpe cuerpo a cuerpo"]["índice"], sp.get("hit_after_cap", 0.0)))
    if c.get("exp"):
        out.append(("EXP", caps["pericia (esquiva)"]["índice"], sp.get("exp_after_cap", 0.0)))
    if c.get("tank"):
        out.append(("DEF", caps["defensa (inmunidad a críticos)"]["índice"], sp.get("def_after_cap", 0.0)))
    return out


def capped_value(tot, w0, caps, sp):
    """Valor real de un equipo: lo que pasa del tope vale el peso reducido «después del tope»."""
    cl = cap_list(caps, sp)
    capped = {k for k, _, _ in cl}
    v = sum(x * w0.get(k, 0) for k, x in tot.items() if k not in capped)
    for k, cap, post in cl:
        x = tot.get(k, 0)
        v += min(x, cap) * w0.get(k, 0) + max(0, x - cap) * post
    return v


def choose(b, sp, w, gems, metas, meta_val):
    best = b.best_gems(w, gems)
    lists = {slot: b.rank_slot(sp, slot, w, best, meta_val, False) for slot in sp["slots"]}
    chosen = []
    for slot in sp["slots"]:
        n = 2 if slot in ("Finger", "Trinket") else 1
        chosen += [(slot, x) for x in lists[slot][:n]]
    plans = []
    for v, mid, why in metas[:6]:
        p = b.gem_plan([x[1] for _, x in chosen], w, gems, mid)
        if p:
            plans.append((p[0] + v, mid, why, p))
    plans.sort(key=lambda x: -x[0])
    ench = {}
    for slot in sp["slots"]:
        if slot in ("Neck", "Finger", "Trinket", "Relic", "Waist"):
            continue
        ench[slot] = b.enchants_for(sp, slot, w)
    tot = collections.Counter()
    extra = 0.0
    for slot, (v, e, ok, st, dps, socks, notes) in chosen:
        tot.update(st)
        tot["MH_DPS"] += dps
        ef, _ = effects(b.tt.get(e, "")) if b.ix.items[e]["InventoryType"] in (12, 28) else ({}, [])
        if e in MANUAL_VALUES.get(sp["key"], {}):
            extra += MANUAL_VALUES[sp["key"]][e][0]
        else:
            tot.update(ef)
    _, mid, why, (gv, plan, counts) = plans[0]
    for e, gs in plan:
        it = b.ix.items[e]
        for g in gs:
            tot.update(GEM_LIST[g]["stats"])
        socks = [it[f"socketColor_{i}"] for i in (1, 2, 3) if it[f"socketColor_{i}"] and it[f"socketColor_{i}"] != 1]
        if all(next(iter(FITS[c])) in COLORS[GEM_LIST[g]["color"]] for c, g in zip(socks, gs)):
            tot.update(b.bonus.get(it["socketBonus"], {}))
    tot.update(METAS[mid]["stats"])
    extra += sp.get("meta_extra", {}).get(mid, (0, ""))[0]
    for slot, ens in ench.items():
        if ens:
            tot.update(ws_vec(ens[0][1]["stats"]))
            mv = MANUAL_VALUES.get(sp["key"], {}).get(("spell", ens[0][1]["spellId"]))
            extra += mv[0] if mv else 0
    return lists, chosen, plans, ench, tot, extra


def pick_weapon_config(b, sp, w, gems, meta_val):
    """Para quien puede elegir: compara el mejor arma de dos manos con la mejor de una mano + mano izquierda."""
    alts = sp["weapons"].get("alternativas")
    if not alts:
        return sp
    best = b.best_gems(w, gems)
    res = []
    for alt in alts:
        s2 = dict(sp, weapons=dict(sp["weapons"], **alt))
        v = sum((b.rank_slot(s2, slot, w, best, meta_val, False, 1) or [(0,)])[0][0]
                for slot in ("Weapon", "Off hand") if slot == "Weapon" or alt.get("off"))
        res.append((v, alt, s2))
    res.sort(key=lambda x: -x[0])
    s2 = res[0][2]
    slots = [x for x in sp["slots"] if x != "Off hand" or res[0][1].get("off")]
    s2 = dict(s2, slots=slots, config_armas=[{"armas": a["main"], "mano_izquierda": a.get("off"), "ep": round(v, 1)}
                                              for v, a, _ in res])
    return s2


def build_spec(b, key):
    sp = SPECS[key]
    w0, kf, calc = adapt_weights(sp)
    caps = modelo.caps_70(sp["caps"].get("golpe_talentos", 0.0), sp["caps"].get("pericia_talentos", 0),
                          sp["caps"].get("golpe_hechizo_talentos", 0.0))
    gems, gem_why = b.allowed_gems()
    metas = []
    for mid, m in METAS.items():
        ok, why = b.design_ok(m["name"])
        if ok:
            metas.append((score(m["stats"], w0) + sp.get("meta_extra", {}).get(mid, (0, ""))[0], mid, why))
    metas.sort(reverse=True)
    meta_val = metas[0][0] if metas else 0
    # configuración de armas (lanzadores: bastón o arma de una mano + mano izquierda)
    sp = pick_weapon_config(b, sp, w0, gems, meta_val)
    # búsqueda del peso de golpe/pericia/defensa que da el mejor equipo real con los topes
    cl = cap_list(caps, sp)
    grids = []
    for k, cap, post in cl:
        if k == "HIT":
            grids.append((k, (1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.17)))
        else:
            grids.append((k, (1.0, 0.6, 0.3)))
    best_run = None
    tried = []
    for combo in itertools.product(*[g for _, g in grids]) if grids else [()]:
        w = dict(w0)
        for (k, _), f in zip(grids, combo):
            if k in w:
                w[k] = round(w0[k] * f, 3)
        run = choose(b, sp, w, gems, metas, meta_val)
        tot, extra = run[4], run[5]
        val = capped_value(tot, w0, caps, sp) + tot.get("MH_DPS", 0) * w0.get("MH", 0) + extra
        tried.append({**{f"peso_{k}": w.get(k) for k, _ in grids}, **{k: round(tot.get(k, 0)) for k, _ in grids},
                      "valor_equipo": round(val, 1)})
        if not best_run or val > best_run[0]:
            best_run = (val, w, run)
    val, w, (lists, chosen, plans, ench, tot, extra) = best_run
    best = b.best_gems(w, gems)
    data = {"clase": key[0], "especializacion": key[1], "clase_es": CLASS[sp["class"]]["es"], "spec_es": sp["es"],
            "pesos": {"nivel_80_wowsims": sp["ws80"], "nivel_70": w0, "nivel_70_para_ordenar": w,
                      "factor_indices": round(kf, 3), "calculo": calc, "referencia": sp["ref"],
                      "busqueda_topes": tried},
            "topes": caps, "indices_nivel_70": modelo.RATING70, "talentos": sp["talents"], "huecos": {},
            "configuracion_armas": sp.get("config_armas"),
            "insignias": {}}
    for slot in sp["slots"]:
        data["huecos"][slot] = slot_entries(b, sp, slot, w, best, meta_val, False)
        data["insignias"][slot] = slot_entries(b, sp, slot, w, best, meta_val, True)
    _, mid, why, (gv, plan, counts) = plans[0]
    data["gemas"] = {
        "meta": {"id": mid, "nombre": METAS[mid]["name"], "requisito": METAS[mid]["req"], "extra": METAS[mid]["extra"],
                 "fuente": why, "colores_conseguidos": dict(zip("RYB", counts)),
                 "valor_extra": sp.get("meta_extra", {}).get(mid)},
        "alternativas_meta": [{"id": m, "nombre": METAS[m]["name"], "ep_total_con_gemas": round(t, 1)}
                              for t, m, _, _ in plans[1:4]],
        "por_objeto": {str(e): g for e, g in plan},
        "gemas_permitidas": {str(g): {"nombre": GEM_LIST[g]["name"], "fuente": gem_why[g]} for g in gems},
        "gemas_excluidas": {str(g): {"nombre": GEM_LIST[g]["name"], "motivo": gem_why[g]}
                            for g in GEM_LIST if g not in gems},
    }
    data["encantamientos"] = {
        slot: [{"nombre": en["name"], "spell": en["spellId"], "item": en.get("itemId"), "ep": round(v, 1),
                "comprobacion": how} for v, en, how in ens[:3]] for slot, ens in ench.items()}
    tot = dict(tot)
    tot.pop("MH_DPS", None)
    data["totales_equipo"] = tot
    data["valor_equipo"] = round(val, 1)
    data["equipo_elegido"] = [x[1] for _, x in chosen]
    data["glifos"] = []
    for kind, name, why in sp["glyphs"]:
        ids = b.by_name.get(name, [])
        data["glifos"].append({"tipo": kind, "nombre_en": name, "id": ids[0] if ids else None,
                               "nombre_es": b.ix.item_name_es(ids[0]) if ids else None, "efecto": why,
                               "nota": "Sin Spell.dbc no se pueden ver los reactivos: muchos glifos piden Tinta del mar "
                                       "(hierbas de Rasganorte). Usar solo si el servidor los vende o permite fabricarlos."})
    data["original_tbc"] = b.tbc_lists.get((key[0], sp.get("tbc_spec", key[1])), {})
    data["comparacion"] = compare(b, sp, data, w, best, meta_val)
    return data


def compare(b, sp, data, w, best, meta_val):
    """Lista original del TBC (PreRaid de wowtbc) frente a la de la prefase, hueco a hueco."""
    from emitir import TBC_SLOT
    out = {}
    for tslot, ids in data["original_tbc"].items():
        slot = TBC_SLOT.get(tslot)
        if not slot or slot not in data["huecos"]:
            continue
        now = data["huecos"][slot]
        rows = []
        for e in ids[:2]:
            if e not in b.ix.items:
                rows.append({"id": e, "estado": "no existe en AzerothCore"})
                continue
            ok, bad = b.f.check(e)
            it = b.ix.items[e]
            name = b.ix.item_name_es(e)
            if not ok:
                rows.append({"id": e, "nombre": name, "estado": "fuera", "motivo": ", ".join(sorted(bad)) or "sin fuente"})
                continue
            if all(x[0] == "insignias" for x in ok):
                rows.append({"id": e, "nombre": name, "estado": "insignias", "motivo": "solo con insignias (lista aparte)"})
                continue
            if not b.usable(it, sp["class"], sp["weapons"]):
                rows.append({"id": e, "nombre": name, "estado": "fuera", "motivo": "no lo puede usar la clase"})
                continue
            v = b.evaluate(e, sp, w, best, meta_val)[0]
            pos = next((i for i, x in enumerate(now) if x["id"] == e), None)
            rows.append({"id": e, "nombre": name, "estado": "sigue" if pos is not None else "baja",
                         "puesto": pos + 1 if pos is not None else None, "ep": round(v, 1)})
        out[slot] = {"original": rows,
                     "prefase": [{"id": x["id"], "nombre": x["nombre_es"], "ep": x["ep"]} for x in now[:2]]}
    return out


def main():
    out = Path(sys.argv[1] if len(sys.argv) > 1 else "salida")
    out.mkdir(parents=True, exist_ok=True)
    wanted = [tuple(a.split("/")) for a in sys.argv[2:]] or list(SPECS)
    b = Builder()
    all_data = {}
    for key in wanted:
        print("especialización", key, flush=True)
        all_data[key] = build_spec(b, key)
    import emitir
    emitir.write_json(all_data, out / "bis_prefase.json")
    emitir.write_lua_lists(all_data, out / "Bistooltip_prefase_bislists.lua")
    emitir.write_lua_sources(all_data, out / "Bistooltip_prefase_sources.lua")
    import subprocess
    res = subprocess.run([sys.executable, str(Path(__file__).parent / "validar_prefase.py"), str(out)],
                         capture_output=True, text=True)
    (out / "validacion.txt").write_text(res.stdout + res.stderr, encoding="utf-8")
    emitir.write_revision(all_data, out / "revision.md", res.stdout + res.stderr)
    print(res.stdout)
    print("escrito en", out)


if __name__ == "__main__":
    main()
