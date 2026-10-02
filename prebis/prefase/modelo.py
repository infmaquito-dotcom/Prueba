"""Tablas de combate de 3.3.5a al nivel 70, topes contra un jefe de nivel 73 y valoración de objetos.

Todo lo que es estadística sale de item_template de AzerothCore. Los efectos de uso y de probabilidad (abalorios,
reliquias, encantamientos con efecto) se leen del texto del tooltip WotLK y se convierten a un valor medio con las
suposiciones que se anotan en cada caso.
"""
import re

# ---------- Índices de clasificación (gtCombatRatings / gtOCTClassCombatRatingScalar de 3.3.5a) ----------
# En 3.3.5a el índice por 1 % es base_60 x 82 / (262 - 3L) entre los niveles 60 y 70 (al 70: x 82/52 = 1,5769) y
# después crece x (131/63)^((L-70)/10) hasta el 80 (x 2,0794). Comprobación con los valores conocidos de nivel 80:
# crítico 14 x 1,5769 x 2,0794 = 45,91; golpe 10 -> 32,79; pericia 2,5 -> 8,20; defensa 1,5 -> 4,92.
# WotLK cambió la base de esquivar y parar a 13,8 (45,25 al 80) y la de penetración de armadura a 4,267 (13,99 al
# 80, valor de 3.3).
L70 = 82 / 52
BASE60 = {  # índice por 1 % (o por punto de pericia/defensa) a nivel 60
    "golpe cuerpo a cuerpo": 10.0, "golpe con hechizos": 8.0, "crítico": 14.0, "celeridad": 10.0,
    "pericia (por punto)": 2.5, "defensa (por punto)": 1.5, "esquivar": 13.8, "parada": 13.8, "bloqueo": 5.0,
}
RATING70 = {k: round(v * L70, 4) for k, v in BASE60.items()}
RATING70["penetración de armadura"] = round(4.267 * L70, 4)
# Celeridad cuerpo a cuerpo de paladines, chamanes, caballeros de la muerte y druidas: 30 % más eficaz (3.0.x)
RATING70["celeridad cuerpo a cuerpo (híbridos)"] = round(RATING70["celeridad"] / 1.3, 4)


def caps_70(golpe_talentos=0.0, pericia_talentos=0, golpe_hechizo_talentos=0.0):
    """Topes al nivel 70 contra un jefe de nivel 73 con las reglas de WotLK (diferencia de 3 niveles)."""
    c = {}
    # Fallo de ataques especiales (y del blanco con una sola arma): 5 % + 1 % por nivel de diferencia (+3 => 8 %).
    golpe = 8.0 - golpe_talentos
    c["golpe cuerpo a cuerpo"] = {
        "porcentaje": golpe, "índice": round(golpe * RATING70["golpe cuerpo a cuerpo"], 1),
        "cálculo": f"(5 % + 3 x 1 % = 8 %) - {golpe_talentos} % de talentos = {golpe} % x "
                   f"{RATING70['golpe cuerpo a cuerpo']} índice/% = {golpe * RATING70['golpe cuerpo a cuerpo']:.1f}"}
    # Esquiva del jefe: 5 % + 0,5 % por nivel (+3 => 6,5 %); cada punto de pericia quita 0,25 %.
    pericia = 6.5 / 0.25 - pericia_talentos
    c["pericia (esquiva)"] = {
        "puntos": pericia, "índice": round(pericia * RATING70["pericia (por punto)"], 1),
        "cálculo": f"6,5 % / 0,25 % = 26 puntos - {pericia_talentos} de talentos/glifos = {pericia} x "
                   f"{RATING70['pericia (por punto)']} = {pericia * RATING70['pericia (por punto)']:.1f}"}
    # Parada del jefe (solo importa a tanques, que atacan de frente): 14 % contra +3 en WotLK => 56 puntos.
    par = 14.0 / 0.25 - pericia_talentos
    c["pericia (parada, tanques)"] = {
        "puntos": par, "índice": round(par * RATING70["pericia (por punto)"], 1),
        "cálculo": f"14 % / 0,25 % = 56 puntos - {pericia_talentos} = {par} x {RATING70['pericia (por punto)']}"}
    # Hechizos: 17 % de fallo contra +3 (4 % + 1 % + 1 % + 11 %) en WotLK.
    sh = 17.0 - golpe_hechizo_talentos
    c["golpe con hechizos"] = {
        "porcentaje": sh, "índice": round(sh * RATING70["golpe con hechizos"], 1),
        "cálculo": f"17 % - {golpe_hechizo_talentos} % de talentos = {sh} % x {RATING70['golpe con hechizos']} "
                   f"= {sh * RATING70['golpe con hechizos']:.1f}"}
    # Defensa: el jefe +3 tiene 0,6 % de crítico extra (0,2 % por nivel) sobre el 5 % base => 5,6 % / 0,04 % = 140
    c["defensa (inmunidad a críticos)"] = {
        "puntos": 140, "índice": round(140 * RATING70["defensa (por punto)"], 1),
        "cálculo": f"5,6 % / 0,04 % = 140 de defensa sobre 350 (total 490) x {RATING70['defensa (por punto)']} = "
                   f"{140 * RATING70['defensa (por punto)']:.1f}"}
    return c


# ---------- Estadísticas de item_template ----------
STAT = {3: "AGI", 4: "STR", 5: "INT", 6: "SPI", 7: "STA", 12: "DEF", 13: "DODGE", 14: "PARRY", 15: "BLOCK",
        16: "HIT", 17: "HIT", 18: "HIT", 19: "CRIT", 20: "CRIT", 21: "CRIT", 28: "HASTE", 29: "HASTE", 30: "HASTE",
        31: "HIT", 32: "CRIT", 35: "RES", 36: "HASTE", 37: "EXP", 38: "AP", 39: "RAP", 41: "SP", 42: "SP",
        43: "MP5", 44: "ARP", 45: "SP", 48: "BLOCKV"}
ES = {"STR": "Fuerza", "AGI": "Agilidad", "STA": "Aguante", "INT": "Intelecto", "SPI": "Espíritu",
      "SP": "Poder con hechizos", "MP5": "Maná cada 5 s", "HIT": "Índice de golpe", "CRIT": "Índice de crítico",
      "HASTE": "Índice de celeridad", "AP": "Poder de ataque", "RAP": "Poder de ataque a distancia",
      "ARP": "Índice de penetración de armadura", "EXP": "Índice de pericia", "DEF": "Índice de defensa",
      "DODGE": "Índice de esquivar", "PARRY": "Índice de parada", "BLOCK": "Índice de bloqueo",
      "BLOCKV": "Valor de bloqueo", "RES": "Temple", "ARMOR": "Armadura", "BARMOR": "Armadura adicional",
      "DPS": "DPS del arma", "HEALTH": "Salud"}


def item_stats(it):
    st = {}
    for i in range(1, it.get("StatsCount", 10) + 1):
        t, v = it.get(f"stat_type{i}"), it.get(f"stat_value{i}")
        if t in STAT and v:
            k = STAT[t]
            st[k] = st.get(k, 0) + v
    if it.get("armor"):
        st["ARMOR"] = it["armor"]
    if it.get("ArmorDamageModifier"):
        st["BARMOR"] = it["ArmorDamageModifier"]
    if it.get("block"):
        st["BLOCKV"] = st.get("BLOCKV", 0) + it["block"]
    if it.get("delay") and it.get("dmg_max1"):
        st["DPS"] = round((it["dmg_min1"] + it["dmg_max1"]) / 2 / (it["delay"] / 1000), 2)
        st["SPEED"] = it["delay"] / 1000
    return st


# vector de estadísticas de wowsims/wotlk -> claves propias (para bonificaciones de ranura)
WS = {0: "STR", 1: "AGI", 2: "STA", 3: "INT", 4: "SPI", 5: "SP", 6: "MP5", 7: "HIT", 8: "CRIT", 9: "HASTE", 11: "AP",
      12: "HIT", 13: "CRIT", 14: "HASTE", 15: "ARP", 16: "EXP", 20: "ARMOR", 22: "DEF", 23: "BLOCK", 24: "BLOCKV",
      25: "DODGE", 26: "PARRY", 27: "RES", 28: "HEALTH"}


def ws_vec(vec):
    out = {}
    for i, v in enumerate(vec or []):
        if v and i in WS:
            k = WS[i]
            out[k] = max(out.get(k, 0), v)  # golpe/crítico/celeridad salen dos veces (hechizo y cuerpo a cuerpo)
    return out


def score(st, w):
    return sum(v * w.get(k, 0) for k, v in st.items())


# ---------- Efectos de uso y de probabilidad (texto del tooltip WotLK) ----------
STAT_WORDS = [
    (r"(?:melee and ranged )?attack power", "AP"), (r"haste rating", "HASTE"), (r"critical strike rating", "CRIT"),
    (r"armor penetration rating", "ARP"), (r"spell power", "SP"), (r"hit rating", "HIT"), (r"agility", "AGI"),
    (r"strength", "STR"), (r"dodge rating", "DODGE"), (r"defense rating", "DEF"), (r"expertise rating", "EXP"),
    (r"block value", "BLOCKV"), (r"armor", "ARMOR"), (r"stamina", "STA"), (r"intellect", "INT"),
    (r"spirit", "SPI"), (r"mana per 5", "MP5")]


def _stat_of(txt):
    t = txt.lower()
    for pat, k in STAT_WORDS:
        if re.search(pat, t):
            return k
    return None


def _cd(txt):
    m = re.search(r"\((\d+) Min(?:, (\d+) Sec)? Cooldown\)", txt)
    if m:
        return int(m.group(1)) * 60 + int(m.group(2) or 0)
    m = re.search(r"\((\d+) Sec Cooldown\)", txt)
    return int(m.group(1)) if m else None


def effects(tooltip):
    """Valor medio de los efectos de uso/probabilidad. Devuelve ({stat: valor medio}, [notas])."""
    out, notes = {}, []
    if not tooltip:
        return out, notes
    parts = re.split(r"(?=Use: |Equip: |Chance on hit: )", tooltip)
    for p in parts:
        if p.startswith("Use: "):
            m = re.search(r"(?:by|an additional) (\d+)(?: for| (?:Armor Penetration Rating|attack power))?.*?(?:for |lasts for )(\d+) sec", p)
            m2 = re.search(r"(?:by|additional) (\d+)", p)
            cd = _cd(p)
            k = _stat_of(p)
            if m2 and cd and k:
                dur = int(m.group(2)) if m else (20 if "Armor Penetration" in p else 15)
                amt = int(m2.group(1))
                stacks = re.search(r"up to (\d+) times", p)
                if stacks:  # efectos que se acumulan (Distintivo de la guardia de enjambre): media de la mitad
                    amt = amt * int(stacks.group(1)) / 2
                v = amt * dur / cd
                out[k] = out.get(k, 0) + v
                notes.append(f"Uso: {amt:g} {k} durante {dur} s cada {cd} s = {v:.1f} de media")
        elif p.startswith("Equip: ") and re.search(r"[Cc]hance|Each time|have a chance", p):
            amt = re.search(r"(?:by|gain) (\d+)", p)
            dur = re.search(r"for (?:the next )?(\d+) sec", p)
            k = _stat_of(p.split("increase your")[-1] if "increase your" in p else p)
            if "Each time you deal melee" in p and "stacking up to" in p:
                n = int(re.search(r"stacking up to (\d+)", p).group(1))
                v = int(amt.group(1)) * n * 0.95
                out["AP"] = out.get("AP", 0) + v
                notes.append(f"Acumulable: {amt.group(1)} AP x {n} acumulaciones casi siempre activas = {v:.0f}")
                continue
            if amt and dur and k and "damage" not in p.split("for")[0][-30:]:
                d = int(dur.group(1))
                cdm = re.search(r"(\d+)s cooldown", p)
                if cdm:  # disparo con tiempo de reutilización interno: se supone que salta ~10 s tras estar listo
                    up = d / (int(cdm.group(1)) + 10)
                    how = f"{d} s cada ~{int(cdm.group(1)) + 10} s"
                else:
                    up = 0.25
                    how = "tiempo activo supuesto 25 %"
                v = int(amt.group(1)) * min(up, 1)
                out[k] = out.get(k, 0) + v
                notes.append(f"Probabilidad: {amt.group(1)} {k}, {how} = {v:.1f} de media")
            elif "damage" in p:
                notes.append("Daño por probabilidad: no se valora automáticamente")
    return out, notes


EQUIP_PATTERNS = [
    (r"^Increases attack power by (\d+)\.", "AP"), (r"^Increases ranged attack power by (\d+)\.", "RAP"),
    (r"^(?:Improves|Increases) (?:your )?hit rating by (\d+)", "HIT"),
    (r"^(?:Improves|Increases) (?:your )?critical strike rating by (\d+)", "CRIT"),
    (r"^(?:Improves|Increases) (?:your )?haste rating by (\d+)", "HASTE"),
    (r"^(?:Improves|Increases) (?:your )?expertise rating by (\d+)", "EXP"),
    (r"^(?:Improves|Increases) (?:your )?armor penetration rating by (\d+)", "ARP"),
    (r"^(?:Improves|Increases) (?:your )?defense rating by (\d+)", "DEF"),
    (r"^(?:Improves|Increases) (?:your )?dodge rating by (\d+)", "DODGE"),
    (r"^(?:Improves|Increases) (?:your )?parry rating by (\d+)", "PARRY"),
    (r"^(?:Improves|Increases) (?:your )?(?:shield )?block rating by (\d+)", "BLOCK"),
    (r"^Increases the block value of your shield by (\d+)", "BLOCKV"),
    (r"^Increases spell power by (\d+)\.", "SP"),
    (r"^Restores (\d+) mana per 5 sec", "MP5"),
    (r"^Increases attack power by (\d+) in Cat, Bear, Dire Bear, and Moonkin forms only", "FAP"),
]


def equip_stats(tooltip):
    """Estadísticas fijas de las líneas «Equip:» del tooltip (en 3.3.5a algunas siguen siendo hechizos de equipar)."""
    out = {}
    for line in re.findall(r"Equip: (.*?)(?= Equip: | Use: | Chance on hit: | Sell Price| Dropped by| Requires|$)",
                           tooltip or ""):
        for pat, k in EQUIP_PATTERNS:
            m = re.search(pat, line)
            if m:
                out[k] = out.get(k, 0) + int(m.group(1))
                break
    return out
