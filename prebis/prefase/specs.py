"""Configuración de clases y especializaciones: armaduras y armas que pueden usar, pesos de estadística al
nivel 70, talentos, glifos, gemas y valores manuales de efectos que no se pueden leer como estadística."""

# ---------- Clases (máscara de AllowableClass, subclases de armadura y de arma de item_template) ----------
CLOTH, LEATHER, MAIL, PLATE = 1, 2, 3, 4
AXE1, AXE2, BOW, GUN, MACE1, MACE2, POLE, SWORD1, SWORD2, STAFF, FIST, DAGGER, THROWN, XBOW, WAND = \
    0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 13, 15, 16, 18, 19
CLASS = {
    "Warrior": {"mask": 1, "ws": 9, "es": "Guerrero", "armor": {CLOTH, LEATHER, MAIL, PLATE},
                "weapons": {AXE1, AXE2, MACE1, MACE2, POLE, SWORD1, SWORD2, STAFF, FIST, DAGGER, BOW, GUN, XBOW, THROWN}},
    "Paladin": {"mask": 2, "ws": 4, "es": "Paladín", "armor": {CLOTH, LEATHER, MAIL, PLATE}, "relic": 7,
                "weapons": {AXE1, AXE2, MACE1, MACE2, POLE, SWORD1, SWORD2}},
    "Hunter": {"mask": 4, "ws": 2, "es": "Cazador", "armor": {CLOTH, LEATHER, MAIL},
               "weapons": {AXE1, AXE2, SWORD1, SWORD2, POLE, STAFF, FIST, DAGGER, BOW, GUN, XBOW}},
    "Rogue": {"mask": 8, "ws": 6, "es": "Pícaro", "armor": {CLOTH, LEATHER},
              "weapons": {AXE1, MACE1, SWORD1, FIST, DAGGER, BOW, GUN, XBOW, THROWN}},
    "Priest": {"mask": 16, "ws": 5, "es": "Sacerdote", "armor": {CLOTH}, "weapons": {MACE1, STAFF, DAGGER, WAND}},
    "Death knight": {"mask": 32, "ws": 10, "es": "Caballero de la Muerte", "armor": {CLOTH, LEATHER, MAIL, PLATE},
                     "relic": 10, "weapons": {AXE1, AXE2, MACE1, MACE2, POLE, SWORD1, SWORD2}},
    "Shaman": {"mask": 64, "ws": 7, "es": "Chamán", "armor": {CLOTH, LEATHER, MAIL}, "relic": 9,
               "weapons": {AXE1, AXE2, MACE1, MACE2, STAFF, FIST, DAGGER}},
    "Mage": {"mask": 128, "ws": 3, "es": "Mago", "armor": {CLOTH}, "weapons": {SWORD1, STAFF, DAGGER, WAND}},
    "Warlock": {"mask": 256, "ws": 8, "es": "Brujo", "armor": {CLOTH}, "weapons": {SWORD1, STAFF, DAGGER, WAND}},
    "Druid": {"mask": 1024, "ws": 1, "es": "Druida", "armor": {CLOTH, LEATHER}, "relic": 8,
              "weapons": {MACE1, MACE2, POLE, STAFF, FIST, DAGGER}},
}


# ---------- Gemas raras de TBC (valores de 3.3.5a, comprobados en el tooltip WotLK) ----------
def _g(name, color, **st):
    return {"name": name, "color": color, "stats": st}


GEM_LIST = {
    24027: _g("Bold Living Ruby", "R", STR=8), 24028: _g("Delicate Living Ruby", "R", AGI=8),
    24030: _g("Runed Living Ruby", "R", SP=9), 24031: _g("Bright Living Ruby", "R", AP=16),
    24032: _g("Subtle Living Ruby", "R", DODGE=8), 24036: _g("Flashing Living Ruby", "R", PARRY=8),
    24047: _g("Brilliant Dawnstone", "Y", INT=8), 24048: _g("Smooth Dawnstone", "Y", CRIT=8),
    24051: _g("Rigid Dawnstone", "Y", HIT=8), 35315: _g("Quick Dawnstone", "Y", HASTE=8),
    24052: _g("Thick Dawnstone", "Y", DEF=8),
    24033: _g("Solid Star of Elune", "B", STA=12), 24035: _g("Sparkling Star of Elune", "B", SPI=8),
    24037: _g("Lustrous Star of Elune", "B", MP5=4),
    24058: _g("Inscribed Noble Topaz", "O", STR=4, CRIT=4), 24061: _g("Glinting Noble Topaz", "O", AGI=4, HIT=4),
    24059: _g("Potent Noble Topaz", "O", SP=5, CRIT=4), 24060: _g("Luminous Noble Topaz", "O", SP=5, INT=4),
    31867: _g("Veiled Noble Topaz", "O", SP=5, HIT=4), 31868: _g("Wicked Noble Topaz", "O", AP=8, CRIT=4),
    35316: _g("Reckless Noble Topaz", "O", SP=5, HASTE=4),
    24054: _g("Sovereign Nightseye", "P", STR=4, STA=6), 24055: _g("Shifting Nightseye", "P", AGI=4, STA=6),
    24056: _g("Glowing Nightseye", "P", SP=5, STA=6), 24057: _g("Royal Nightseye", "P", SP=5, MP5=2),
    31863: _g("Balanced Nightseye", "P", AP=8, STA=6), 35707: _g("Regal Nightseye", "P", DODGE=4, STA=6),
    24065: _g("Dazzling Talasite", "G", INT=4, MP5=2), 24062: _g("Enduring Talasite", "G", DEF=4, STA=6),
    24067: _g("Jagged Talasite", "G", CRIT=4, STA=6), 35318: _g("Forceful Talasite", "G", HASTE=4, STA=6),
}

# Metas: requisitos copiados del tooltip WotLK (3.3.5a). "min": mínimos por color; "more": (A, B) = más A que B.
METAS = {
    32409: {"name": "Relentless Earthstorm Diamond", "stats": {"AGI": 12}, "extra": "3 % daño crítico",
            "req": {"min": {"R": 2, "Y": 2, "B": 2}}},
    34220: {"name": "Chaotic Skyfire Diamond", "stats": {"CRIT": 12}, "extra": "3 % daño crítico",
            "req": {"min": {"B": 2}}},
    25894: {"name": "Swift Skyfire Diamond", "stats": {"AP": 24}, "extra": "",
            "req": {"min": {"Y": 2, "R": 1}}},
    25890: {"name": "Destructive Skyfire Diamond", "stats": {"CRIT": 14}, "extra": "1 % reflejo",
            "req": {"min": {"R": 2, "Y": 2, "B": 2}}},
    25895: {"name": "Enigmatic Skyfire Diamond", "stats": {"CRIT": 12}, "extra": "",
            "req": {"more": ("R", "Y")}},
    25897: {"name": "Bracing Earthstorm Diamond", "stats": {"SP": 14}, "extra": "-2 % amenaza",
            "req": {"more": ("R", "B")}},
    25901: {"name": "Insightful Earthstorm Diamond", "stats": {"INT": 12}, "extra": "maná por probabilidad",
            "req": {"min": {"R": 2, "Y": 2, "B": 2}}},
    25896: {"name": "Powerful Earthstorm Diamond", "stats": {"STA": 18}, "extra": "",
            "req": {"min": {"B": 3}}},
    25898: {"name": "Tenacious Earthstorm Diamond", "stats": {"DEF": 12}, "extra": "",
            "req": {"min": {"B": 5}}},
    35501: {"name": "Eternal Earthstorm Diamond", "stats": {"DEF": 12}, "extra": "+5 % valor de bloqueo",
            "req": {"min": {"B": 2, "Y": 1}}},
    35503: {"name": "Ember Skyfire Diamond", "stats": {"SP": 14}, "extra": "+2 % intelecto",
            "req": {"min": {"R": 3}}},
    25893: {"name": "Mystical Skyfire Diamond", "stats": {}, "extra": "celeridad por probabilidad",
            "req": {"more": ("B", "Y")}},
    32410: {"name": "Thundering Skyfire Diamond", "stats": {}, "extra": "celeridad por probabilidad",
            "req": {"min": {"R": 2, "Y": 2, "B": 2}}},
}

# ---------- Especializaciones ----------
# Pesos: wowsims/wotlk ui/<spec>/sim.ts (nivel 80). En 3.3.5a un mismo índice de golpe/crítico/celeridad vale a la
# vez para cuerpo a cuerpo y hechizos, así que se suman ambos pesos. Al nivel 70 cada punto de índice da 2,079 veces
# más porcentaje que al 80, pero el daño total (y por tanto lo que vale 1 %) es más bajo: el factor de adaptación
# de los índices es 2,079 x (poder de ataque o de hechizo con bufos al 70 / al 80). Las estadísticas primarias, el
# poder de ataque y el DPS del arma no cambian de escala porque ya se miden en unidades de poder de ataque.
SPECS = {
    ("Paladin", "Retribution"): {
        "key": "ret", "es": "Reprensión", "class": "Paladin",
        "ws80": {"STR": 2.53, "AGI": 1.13, "INT": 0.15, "SP": 0.32, "AP": 1.0, "HIT": 1.96 + 0.41,
                 "CRIT": 1.16 + 0.01, "HASTE": 1.44 + 0.12, "ARP": 0.76, "EXP": 1.80, "MP5": 0.05, "MH": 7.33},
        "ref": {"stat": "poder de ataque con bufos", "70": 3000, "80": 6500},
        "weapons": {"main": ("2h",)},
        "tbc_spec": "Retribution",
        "slots": ["Head", "Neck", "Shoulder", "Back", "Chest", "Wrist", "Hands", "Waist", "Legs", "Feet", "Finger",
                  "Trinket", "Weapon", "Relic"],
        "caps": {"golpe_talentos": 0.0, "pericia_talentos": 0, "hit_kind": "melee", "exp": True},
        # Pasado el 8 % de golpe cuerpo a cuerpo, el índice de golpe aún sirve para Exorcismo y Consagrar hasta el 17 %
        # de hechizos: se deja la parte de hechizo del peso de wowsims (0,41 x factor).
        "hit_after_cap": 0.39,
        "talents": {
            "reparto": "5/5/51",
            "texto": [
                "Sagrado 5: Sellos de los puros 5/5 (+15 % al daño de sellos y sentencias).",
                "Protección 5: Fuerza divina 5/5 (+15 % de Fuerza).",
                "Reprensión 51: Bendición 5/5, Sentencias mejoradas 2/2, Corazón del cruzado 3/3, Vindicación 1/2, "
                "Convicción 5/5, Sello de orden 1/1, Santidad de batalla 3/3, Cruzada 3/3, Especialización en armas "
                "de dos manos 3/3, Reprensión santificada 1/1, Venganza 3/3, El arte de la guerra 2/2, Sentencias de "
                "los sabios 3/3, Fanatismo 3/3, Cólera santificada 2/2, Reprensión presta 3/3, Golpe de cruzado 1/1, "
                "Vaina de luz 3/3, Venganza justa 3/3, Tormenta divina 1/1.",
            ],
            "razon": "Con 61 puntos se llega a Tormenta divina (fila 11, 50 puntos en Reprensión) y quedan 11 puntos. "
                     "Fuerza divina (+15 % Fuerza) y Sellos de los puros (+15 % sellos y sentencias) son los dos "
                     "talentos de daño más baratos fuera del árbol. Dentro de Reprensión se dejan fuera Desviación, "
                     "Ojo por ojo, Arrepentimiento, Persecución de la justicia, Bendición de poderío mejorada, Propósito "
                     "divino y un punto de Vindicación, que no suben el daño en solitario contra un jefe.",
            "golpe_pericia": "Ningún talento de este reparto da golpe ni pericia; el Glifo de Sello de venganza da 10 "
                             "de pericia (si se puede conseguir, ver glifos).",
        },
        "glyphs": [
            ("Mayor", "Glyph of Seal of Vengeance", "+10 de pericia con el sello activo; baja el tope de pericia"),
            ("Mayor", "Glyph of Judgement", "+10 % al daño de Sentencia"),
            ("Mayor", "Glyph of Exorcism", "+20 % al daño de Exorcismo (con El arte de la guerra)"),
            ("Menor", "Glyph of Blessing of Might", "comodidad: Bendición de poderío dura 30 min"),
            ("Menor", "Glyph of Sense Undead", "+1 % de daño contra no-muertos"),
        ],
        "meta_extra": {32409: (55, "3 % de daño crítico: con ~28 % de crítico y críticos al 200 %, ~+1,3 % de DPS; "
                                    "1 % de DPS ~ 45 de poder de ataque al 70 (estimación)"),
                       34220: (55, "3 % de daño crítico, igual que la Relentless")},
    },
}

# Glifos: AzerothCore no trae Spell.dbc, así que no se pueden comprobar los reactivos. Varios glifos mayores usan
# Tinta del mar (pigmento de hierbas de Rasganorte); si Rasganorte está cerrado, solo valen los que el servidor
# venda o los que se fabriquen con tintas de Terrallende o anteriores.
GLYPHS = {}

# Encantamientos que wowsims/wotlk no lista o lista sin estadísticas
ENCHANT_EXTRA = [
    {"effectId": 0, "spellId": 27984, "itemId": 22559, "name": "Mongoose", "type": 13, "stats": []},
]

# Valores manuales en EP (unidades de poder de ataque o de poder con hechizos) para efectos que no son estadística.
# Clave: id de objeto, o ("spell", id) para encantamientos.
MANUAL_VALUES = {
    "ret": {
        ("spell", 27984): (95, "Mangosta: 120 Agilidad y 2 % de celeridad durante 15 s, ~1 PPM; con arma de 3,5-3,6 s "
                               "~40 % de tiempo activo = 48 Agi y 0,8 % de celeridad (~13 índice) = ~75 EP; se redondea"
                               " a 95 por la armadura y la celeridad de los hechizos (estimación)"),
        ("spell", 20034): (60, "Cruzado: 100 Fuerza 15 s, 1 PPM; en 3.3.5a el efecto baja con el nivel por encima de 60"
                               " (estimación)"),
        27484: (40, "Libro de Venganza: 53 índice de crítico 5 s tras cada Sentencia (cada 8 s) = ~33 de crítico de media"),
    },
}


# ---------------------------------------------------------------------------------------------------------------
# Resto de especializaciones
# ---------------------------------------------------------------------------------------------------------------
ARMOR_SLOTS = ["Head", "Neck", "Shoulder", "Back", "Chest", "Wrist", "Hands", "Waist", "Legs", "Feet", "Finger",
               "Trinket"]
CASTER_ALTS = [{"main": ("2h",), "off": None}, {"main": ("1h", "mh"), "off": ("held",)}]
SHIELD_CASTER_ALTS = [{"main": ("2h",), "off": None}, {"main": ("1h", "mh"), "off": ("held", "shield")}]
AP_REF = {"stat": "poder de ataque con bufos", "70": 3000, "80": 6500}
SP_REF = {"stat": "poder con hechizos con bufos", "70": 1150, "80": 2500}
HEAL_REF = {"stat": "poder con hechizos con bufos (sanación)", "70": 1500, "80": 2800}
TANK_REF = {"stat": "salud con bufos", "70": 16000, "80": 32000}
CASTER_HIT = (1.25, "1 % de golpe con hechizos ~ 1 % de daño ~ 16 de poder con hechizos al 70 = 16/12,6 por "
                    "punto de índice; wowsims lo da casi a 0 porque supone el tope")
MELEE_CRIT_META = {32409: (50, "3 % de daño crítico ~ +1,2 % de DPS (estimación)"),
                   34220: (50, "3 % de daño crítico ~ +1,2 % de DPS (estimación)"),
                   32410: (25, "celeridad por probabilidad (estimación)")}
CASTER_META = {34220: (24, "3 % de daño crítico de hechizos ~ +1,5 % de DPS ~ 24 de poder con hechizos (estimación)"),
               25893: (10, "celeridad de lanzamiento por probabilidad (estimación)")}
HEAL_META = {25901: (8, "maná por probabilidad ~ 5 de maná cada 5 s (estimación)"),
             34220: (12, "3 % de sanación crítica (estimación)")}
CRUSADER = {("spell", 20034): (55, "Cruzado: 100 Fuerza 15 s, 1 PPM; en 3.3.5a baja con el nivel (estimación)")}


def spec(key, es, cls, ws80, ref, weapons, extra_slots, caps, reparto, texto, razon, glyphs, **kw):
    d = {"key": key, "es": es, "class": cls, "ws80": ws80, "ref": ref, "weapons": weapons,
         "slots": ARMOR_SLOTS + ["Weapon"] + (["Off hand"] if weapons.get("off") or weapons.get("alternativas") else [])
         + extra_slots,
         "caps": caps, "talents": {"reparto": reparto, "texto": texto, "razon": razon,
                                   "golpe_pericia": kw.pop("golpe_pericia", "")},
         "glyphs": glyphs}
    d.update(kw)
    return d


def _add(cls, name, d):
    SPECS[(cls, name)] = d


# ---------- Caballero de la Muerte ----------
_add("Death knight", "Blood", spec(
    "dk_blood", "Sangre (tanque)", "Death knight",
    {"STA": 1, "STR": 0.33, "AGI": 0.6, "AP": 0.06, "EXP": 0.67, "HIT": 0.67, "CRIT": 0.28, "HASTE": 0.21,
     "ARP": 0.19, "DODGE": 0.7, "PARRY": 0.58, "DEF": 0.8, "ARMOR": 0.05, "BARMOR": 0.03, "MH": 3.10},
    TANK_REF, {"main": ("2h",)}, [],
    {"hit_kind": "melee", "exp": True, "tank": True, "pericia_talentos": 6},
    "51/10/0", ["Sangre 51: Barrera de filos 5/5, Armadura afilada 5/5, Veterano de la Tercera Guerra 3/3 "
                "(+6 de pericia), Marca de sangre, Golpe de runa, Voluntad de la Necrópolis 3/3, Sangre vampírica, "
                "Golpe en el corazón, Arma rúnica danzante.",
                "Escarcha 10: Dureza 5/5 (+10 % de armadura) y Alcance gélido/Toque helado mejorado con el resto."],
    "Con 61 puntos se llega a Arma rúnica danzante (fila 11 de Sangre). Dureza es lo mejor que da Escarcha a un "
    "tanque con 10 puntos. Sin Supervivencia del más apto de los druidas, el caballero necesita 490 de defensa "
    "para no recibir críticos de un jefe +3.",
    [("Mayor", "Glyph of Vampiric Blood", "más salud con Sangre vampírica"),
     ("Mayor", "Glyph of Disease", "renueva enfermedades"), ("Mayor", "Glyph of Rune Tap", "más curación")],
    golpe_pericia="Veterano de la Tercera Guerra da 6 de pericia.", def_after_cap=0.8, exp_after_cap=0.3,
    hit_after_cap=0.0))
_add("Death knight", "Frost", spec(
    "dk_frost", "Escarcha", "Death knight",
    {"STR": 3.22, "AGI": 0.62, "AP": 1, "EXP": 1.13, "HASTE": 1.85, "HIT": 1.92 + 0.80, "CRIT": 0.76 + 0.34,
     "ARP": 0.77, "ARMOR": 0.01, "MH": 3.10, "OH": 1.79},
    AP_REF, {"main": ("1h", "mh"), "off": ("1h", "oh")}, [],
    {"hit_kind": "melee", "exp": True, "golpe_talentos": 3.0},
    "0/51/10", ["Escarcha 51: Toque helado mejorado 3/3, Dominio de poder rúnico, Hielo negro 5/5, Nervios de acero "
                "frío 3/3 (+3 % golpe con dos armas), Hambre glacial, Asesino matador, Acero de sangre fría, Golpe de "
                "escarcha, Garras gélidas, Viento helado/Temblor del invierno y Explosión aullante.",
                "Profano 10: Virulencia 3/3 (+3 % golpe de hechizos), Epidemia 2/2, Muertos voraces 3/3, Golpes "
                "viciosos 2/2."],
    "Explosión aullante cierra el árbol de Escarcha con 51 puntos. Virulencia y Epidemia son lo más barato de Profano "
    "para las enfermedades y el golpe de hechizos.",
    [("Mayor", "Glyph of Obliterate", "+daño de Aniquilar"), ("Mayor", "Glyph of Frost Strike", "-coste de Golpe de escarcha"),
     ("Mayor", "Glyph of Disease", "renueva enfermedades")],
    golpe_pericia="Nervios de acero frío: +3 % golpe con dos armas.", meta_extra=MELEE_CRIT_META,
    hit_after_cap=0.5))
_add("Death knight", "Unholy", spec(
    "dk_unholy", "Profano", "Death knight",
    {"STR": 3.22, "AGI": 0.62, "AP": 1, "EXP": 1.13, "HASTE": 1.85, "HIT": 1.92 + 0.80, "CRIT": 0.76 + 0.34,
     "ARP": 0.77, "ARMOR": 0.01, "MH": 3.10},
    AP_REF, {"main": ("2h",)}, [],
    {"hit_kind": "melee", "exp": True},
    "0/10/51", ["Profano 51: Virulencia 3/3, Epidemia 2/2, Morbilidad 3/3, Muertos voraces 3/3, Plaga del amanecer, "
                "Maestro de los no-muertos, Fuerza impía, Golpe de la Plaga, Sacrificio de ventisca/Ira impía, "
                "Plaga de ébano y Gárgola invocada.",
                "Escarcha 10: Toque helado mejorado 3/3, Dominio de poder rúnico 2/2 y Hielo negro 5/5."],
    "Gárgola invocada (fila 11) y Plaga de ébano son lo que más daño da con 61 puntos; Hielo negro sube todo el "
    "daño de Escarcha y Sombra.",
    [("Mayor", "Glyph of the Ghoul", "necrófago más fuerte"), ("Mayor", "Glyph of Icy Touch", "más daño de Fiebre de escarcha"),
     ("Mayor", "Glyph of Disease", "renueva enfermedades")],
    golpe_pericia="Virulencia: +3 % golpe de hechizos; ningún talento de golpe cuerpo a cuerpo.",
    meta_extra=MELEE_CRIT_META, extra_manual=CRUSADER, hit_after_cap=0.6))

# ---------- Druida ----------
_add("Druid", "Balance", spec(
    "druid_balance", "Equilibrio", "Druid",
    {"INT": 0.43, "SPI": 0.34, "SP": 1, "CRIT": 0.82, "HASTE": 0.80, "HIT": 1.2, "MP5": 0.1},
    SP_REF, {"main": ("2h",), "alternativas": CASTER_ALTS}, ["Relic"],
    {"hit_kind": "spell", "golpe_hechizo_talentos": 4.0},
    "51/0/10", ["Equilibrio 51: Gracia de la Naturaleza, Rapidez de la Naturaleza, Luz de luna 3/3, Poderes de luna, "
                "Equilibrio de poder 2/2 (+4 % golpe), Forma de lechúcico lunar, Euforia lunar, Tifón, Eclipse 3/3 y "
                "Lluvia de estrellas.",
                "Restauración 10: Furor 5/5 (+10 % de Intelecto en forma de lechúcico), Enfoque de la Naturaleza 3/3 y "
                "Marca de lo Salvaje mejorada 2/2."],
    "Lluvia de estrellas llega con 51 puntos y Eclipse es el núcleo del daño. Furor en Restauración da Intelecto.",
    [("Mayor", "Glyph of Starfire", "alarga Fuego lunar"), ("Mayor", "Glyph of Moonfire", "más daño periódico"),
     ("Mayor", "Glyph of Insect Swarm", "+daño de Enjambre de insectos")],
    golpe_pericia="Equilibrio de poder: +4 % golpe con hechizos.", meta_extra=CASTER_META,
    w70={"HIT": CASTER_HIT}, hit_after_cap=0.0, tbc_spec="Balance"))
_add("Druid", "FeralTank", spec(
    "druid_bear", "Feral (tanque)", "Druid",
    {"ARMOR": 3.5665, "BARMOR": 0.5187, "STA": 7.3021, "STR": 2.3786, "AGI": 4.4974, "AP": 1, "EXP": 2.6597,
     "HIT": 2.9282, "CRIT": 1.5143, "HASTE": 2.0983, "ARP": 1.584, "DEF": 1.8171, "DODGE": 2.0196},
    TANK_REF, {"main": ("2h", "1h", "mh")}, ["Relic"],
    {"hit_kind": "melee", "exp": True, "pericia_talentos": 10},
    "0/51/10", ["Feral 51: Ferocidad 5/5, Ferocidad salvaje, Pelaje grueso 3/3, Instinto feral, Supervivencia del más "
                "apto 3/3 (-6 % de probabilidad de recibir críticos), Precisión primigenia 2/2 (+10 de pericia), "
                "Corazón de lo salvaje, Líder de la manada, Protector de la manada, Destrozar, Rabia de rey y "
                "Rabiar.",
                "Restauración 10: Furor 5/5 y Naturalista 5/5."],
    "Supervivencia del más apto quita la necesidad de defensa contra críticos; Rabiar es el talento de fila 11.",
    [("Mayor", "Glyph of Maul", "Magullar golpea a un objetivo más"),
     ("Mayor", "Glyph of Survival Instincts", "más salud con Instintos de supervivencia"),
     ("Mayor", "Glyph of Frenzied Regeneration", "más curación")],
    golpe_pericia="Precisión primigenia: +10 de pericia.", exp_after_cap=0.5, hit_after_cap=0.3,
    tbc_spec="FeralTank"))
_add("Druid", "FeralDps", spec(
    "druid_cat", "Feral (DPS)", "Druid",
    {"STR": 2.40, "AGI": 2.39, "AP": 1, "HIT": 2.51, "CRIT": 2.23, "HASTE": 1.83, "ARP": 2.08, "EXP": 2.44,
     "MH": 16.5},
    AP_REF, {"main": ("2h", "1h", "mh")}, ["Relic"],
    {"hit_kind": "melee", "exp": True, "pericia_talentos": 10},
    "0/51/10", ["Feral 51: Ferocidad 5/5, Ferocidad salvaje, Garras afiladas 3/3, Atacante depredador, Instinto feral, "
                "Precisión primigenia 2/2 (+10 de pericia), Corazón de lo salvaje, Líder de la manada, Rabia de "
                "rey, Destrozar, Rugido salvaje/Desgarrar mejorado y Rabiar.",
                "Restauración 10: Furor 5/5 y Naturalista 5/5."],
    "Rabiar es el último talento feral; Corazón de lo salvaje y Rabia de rey suben todo el poder de ataque.",
    [("Mayor", "Glyph of Shred", "alarga Arañazo"), ("Mayor", "Glyph of Rip", "Destripar dura más"),
     ("Mayor", "Glyph of Savage Roar", "+daño de Rugido salvaje")],
    golpe_pericia="Precisión primigenia: +10 de pericia.", meta_extra=MELEE_CRIT_META, hit_after_cap=0.0,
    tbc_spec="FeralDps"))
_add("Druid", "Restoration", spec(
    "druid_resto", "Restauración", "Druid",
    {"INT": 0.4, "SPI": 0.5, "SP": 1, "CRIT": 0.4, "HASTE": 0.9, "MP5": 1.0},
    HEAL_REF, {"main": ("2h",), "alternativas": CASTER_ALTS}, ["Relic"], {},
    "10/0/51", ["Restauración 51: Furor 5/5, Naturalista, Rapidez de la Naturaleza, Regeneración natural, Don de la "
                "Naturaleza 5/5, Alivio presto, Forma de Árbol de vida, Nutrir mejorado, Rejuvenecimiento mejorado y "
                "Crecimiento salvaje.",
                "Equilibrio 10: Majestad de la Naturaleza 2/2, Génesis 5/5 y Brillo lunar 3/3."],
    "Crecimiento salvaje es la sanación de grupo más eficiente y llega con 51 puntos; Equilibrio da crítico y maná.",
    [("Mayor", "Glyph of Swiftmend", "Alivio presto no consume el efecto"),
     ("Mayor", "Glyph of Wild Growth", "un objetivo más"), ("Mayor", "Glyph of Rejuvenation", "+sanación a heridos")],
    meta_extra=HEAL_META, tbc_spec="Restoration",
    nota_pesos="Pesos de sanador ajustados a mano para el 70 sin bufos de banda (el maná importa más)."))

# ---------- Cazador ----------
HUNTER_W = {"AGI": 2.65, "INT": 1.1, "AP": 1.0, "RAP": 1.0, "HIT": 2, "CRIT": 1.5, "HASTE": 1.39, "ARP": 1.32,
            "RANGED": 6.32}
for name, es, reparto, texto, razon, gl, hitt in [
    ("BeastMastery", "Bestias", "51/10/0",
     ["Bestias 51: Aspecto del halcón mejorado 5/5, Fuego concentrado 2/2, Disciplina de la bestia, Ira bestial, "
      "Ferocidad de la bestia, Intimidación, Instinto asesino 3/3, Frenesí, Bestia interior y Señor de las bestias.",
      "Puntería 10: Disparos letales 5/5 (+5 % crítico), Puntería concentrada 3/3 (+3 % golpe) y Puntería certera 2/3."],
     "Señor de las bestias es el talento de fila 11 de Bestias; Puntería concentrada da el golpe barato.",
     [("Mayor", "Glyph of Bestial Wrath", "Cólera de las bestias más a menudo"),
      ("Mayor", "Glyph of Steady Shot", "+daño de Disparo firme"), ("Mayor", "Glyph of Serpent Sting", "Picadura dura más")], 3.0),
    ("Marksmanship", "Puntería", "7/51/3",
     ["Bestias 7: Aspecto del halcón mejorado 5/5 y Fuego concentrado 2/2.",
      "Puntería 51: Disparos letales 5/5, Puntería concentrada 3/3, Puntería certera 3/3, Disparo de puntería, "
      "Precisión mortal, Disparo de dispersión, Arquero maestro, Disparo silenciador, Asesino desalmado y "
      "Disparo de quimera.", "Supervivencia 3: Rastreo mejorado 3/5."],
     "Disparo de quimera cierra Puntería con 51 puntos; Aspecto del halcón mejorado es lo mejor de Bestias.",
     [("Mayor", "Glyph of Chimera Shot", "Disparo de quimera más a menudo"),
      ("Mayor", "Glyph of Steady Shot", "+daño de Disparo firme"), ("Mayor", "Glyph of Serpent Sting", "Picadura dura más")], 3.0),
    ("Survival", "Supervivencia", "0/10/51",
     ["Puntería 10: Disparos letales 5/5, Puntería concentrada 3/3 y Puntería certera 2/3.",
      "Supervivencia 51: Rastreo mejorado, Trampa de hielo, Instinto de supervivencia, Cazador letal, Muerte "
      "segura, Disparo de bloqueo, Expuesto, Brillo de cazador, Picadura de serpiente con veneno/Mordisco de "
      "dracoleón y Disparo explosivo."],
     "Disparo explosivo llega con 51 puntos; Puntería da crítico y el golpe de Puntería concentrada.",
     [("Mayor", "Glyph of Explosive Shot", "+crítico de Disparo explosivo"),
      ("Mayor", "Glyph of Serpent Sting", "Picadura dura más"), ("Mayor", "Glyph of Steady Shot", "+daño de Disparo firme")], 3.0)]:
    _add("Hunter", name, spec(
        "hunter_" + name.lower(), es, "Hunter", dict(HUNTER_W), AP_REF, {"main": ("2h",), "ranged": ("ranged",)},
        ["Ranged"], {"hit_kind": "melee", "golpe_talentos": hitt}, reparto, texto, razon, gl,
        golpe_pericia="Puntería concentrada: +3 % golpe. El arma cuerpo a cuerpo solo cuenta por sus estadísticas.",
        meta_extra=MELEE_CRIT_META, hit_after_cap=0.0, tbc_spec=name))

# ---------- Mago ----------
MAGE_W = {"INT": 0.48, "SPI": 0.42, "SP": 1, "HIT": 0.38, "CRIT": 0.58, "HASTE": 0.94, "MP5": 0.09}
for name, es, reparto, texto, razon, gl, hitt in [
    ("Arcane", "Arcano", "51/0/10",
     ["Arcano 51: Sutileza arcana, Enfoque arcano 3/3 (+3 % golpe arcano), Concentración arcana 5/5, Mente "
      "giratoria, Poder arcano, Celeridad de la mente, Empoderamiento arcano, Presencia mental, Ráfaga arcana y "
      "Andanada arcana.", "Escarcha 10: Precisión 3/3 (+3 % golpe) y el resto en Témpanos de hielo y Escalofrío."],
     "Andanada arcana y Poder arcano dan casi todo el daño con 51 puntos; Precisión completa el golpe.",
     [("Mayor", "Glyph of Arcane Blast", "más daño por acumulación"), ("Mayor", "Glyph of Arcane Missiles", "+daño crítico"),
      ("Mayor", "Glyph of Molten Armor", "más crítico de la armadura")], 6.0),
    ("Fire", "Fuego", "10/51/0",
     ["Arcano 10: Sutileza arcana 2/2, Concentración arcana 5/5 y Estabilidad arcana 3/5.",
      "Fuego 51: Bola de fuego mejorada, Ignición, Incineración, Llamas potentes, Combustión, Golpe de calor, "
      "Mente ardiente, Piroexplosión, Bomba viviente."],
     "Bomba viviente llega con 51 puntos; Concentración arcana ahorra maná. Fuego no tiene talento de golpe.",
     [("Mayor", "Glyph of Fireball", "-tiempo de lanzamiento"), ("Mayor", "Glyph of Living Bomb", "puede hacer crítico"),
      ("Mayor", "Glyph of Molten Armor", "más crítico de la armadura")], 0.0),
    ("Frost", "Escarcha", "10/0/51",
     ["Arcano 10: Sutileza arcana 2/2, Concentración arcana 5/5 y Estabilidad arcana 3/5.",
      "Escarcha 51: Descarga de Escarcha mejorada, Precisión 3/3 (+3 % golpe), Témpanos de hielo, Venas heladas, "
      "Escarcha penetrante, Arcano de Escarcha, Elemental de agua, Dedos de escarcha, Congelación cerebral, "
      "Congelación profunda."],
     "Congelación profunda cierra el árbol; Precisión da el 3 % de golpe.",
     [("Mayor", "Glyph of Frostbolt", "+daño de Descarga de Escarcha"), ("Mayor", "Glyph of Ice Lance", "+daño a congelados"),
      ("Mayor", "Glyph of Molten Armor", "más crítico de la armadura")], 3.0)]:
    _add("Mage", name, spec(
        "mage_" + name.lower(), es, "Mage", dict(MAGE_W), SP_REF, {"main": ("2h",), "alternativas": CASTER_ALTS,
                                                                    "ranged": ("wand",)},
        ["Ranged"], {"hit_kind": "spell", "golpe_hechizo_talentos": hitt}, reparto, texto, razon, gl,
        meta_extra=CASTER_META, w70={"HIT": CASTER_HIT}, hit_after_cap=0.0, tbc_spec=name))

# ---------- Paladín ----------
_add("Paladin", "Holy", spec(
    "pal_holy", "Sagrado", "Paladin",
    {"INT": 0.6, "SPI": 0.05, "SP": 1, "CRIT": 0.69, "HASTE": 0.77, "MP5": 1.2},
    HEAL_REF, {"main": ("1h", "mh"), "off": ("shield", "held")}, ["Relic"], {},
    "51/10/0", ["Sagrado 51: Intelecto divino 5/5, Iluminación 5/5, Luz sagrada mejorada, Sabiduría santificada, "
                "Favor divino, Luz santificada, Purificación, Choque sagrado, Guía sagrada, Ilustración divina, "
                "Infusión de luz y Señal de la Luz.",
                "Protección 10: Divinidad 5/5, Favor del guardián 2/2 y Estoicismo 3/3."],
    "Señal de la Luz llega con 51 puntos; Divinidad da +5 % de sanación.",
    [("Mayor", "Glyph of Holy Light", "cura a los cercanos"), ("Mayor", "Glyph of Seal of Wisdom", "-coste"),
     ("Mayor", "Glyph of Beacon of Light", "Señal dura más")],
    meta_extra=HEAL_META, tbc_spec="Holy",
    nota_pesos="Pesos de sanador ajustados a mano para el 70 sin bufos de banda (el maná importa más)."))
_add("Paladin", "Protection", spec(
    "pal_prot", "Protección", "Paladin",
    {"ARMOR": 0.07, "BARMOR": 0.06, "STA": 1.14, "STR": 1.00, "AGI": 0.62, "AP": 0.26, "EXP": 0.69, "HIT": 0.79,
     "CRIT": 0.30, "HASTE": 0.17, "ARP": 0.04, "SP": 0.13, "BLOCK": 0.52, "BLOCKV": 0.28, "DODGE": 0.46,
     "PARRY": 0.61, "DEF": 0.54, "MH": 3.33},
    TANK_REF, {"main": ("1h", "mh"), "off": ("shield",)}, ["Relic"],
    {"hit_kind": "melee", "exp": True, "tank": True, "pericia_talentos": 6},
    "0/51/10", ["Protección 51: Divinidad 5/5, Fuerza divina 5/5, Anticipación 5/5, Dureza 5/5, Furia recta "
                "mejorada, Escudo sagrado, Pericia de combate 3/3 (+6 de pericia), Especialización en armas de una "
                "mano, Guardián ardiente, Escudo de vengador, Juicio de los justos y Martillo del honrado.",
                "Reprensión 10: Desviación 5/5, Corazón del cruzado 3/3 y Sentencias mejoradas 2/2."],
    "Martillo del honrado cierra el árbol; Desviación da parada.",
    [("Mayor", "Glyph of Seal of Vengeance", "+10 de pericia"), ("Mayor", "Glyph of Hammer of the Righteous", "un objetivo más"),
     ("Mayor", "Glyph of Divine Plea", "-daño recibido")],
    golpe_pericia="Pericia de combate: +6 de pericia.", def_after_cap=0.55, exp_after_cap=0.3, hit_after_cap=0.2,
    extra_manual=CRUSADER, tbc_spec="Protection"))

# ---------- Sacerdote ----------
_add("Priest", "Discipline", spec(
    "priest_disc", "Disciplina", "Priest",
    {"INT": 0.7, "SPI": 0.5, "SP": 1, "CRIT": 0.75, "HASTE": 0.6, "MP5": 1.4},
    HEAL_REF, {"main": ("2h",), "alternativas": CASTER_ALTS, "ranged": ("wand",)}, ["Ranged"], {},
    "51/10/0", ["Disciplina 51: Disciplinas gemelas 5/5, Fuego interno mejorado, Meditación 3/3, Concentración "
                "mental, Infusión de poder, Palabra de poder: escudo mejorado, Gracia divina, Aegis divino, "
                "Supresión de dolor, Gracia, Rapto y Penitencia.",
                "Sagrado 10: Especialización sagrada 5/5, Enfoque de sanación 2/2 y Renovar mejorado 3/3."],
    "Penitencia y Aegis divino dan la fuerza de Disciplina con 51 puntos.",
    [("Mayor", "Glyph of Power Word: Shield", "cura al escudar"), ("Mayor", "Glyph of Penance", "-reutilización"),
     ("Mayor", "Glyph of Flash Heal", "-coste")],
    meta_extra=HEAL_META, tbc_spec="Holy",
    nota_pesos="Pesos de sanador ajustados a mano para el 70 sin bufos de banda (el maná importa más)."))
_add("Priest", "Holy", spec(
    "priest_holy", "Sagrado", "Priest",
    {"INT": 0.6, "SPI": 0.8, "SP": 1, "CRIT": 0.5, "HASTE": 0.6, "MP5": 1.2},
    HEAL_REF, {"main": ("2h",), "alternativas": CASTER_ALTS, "ranged": ("wand",)}, ["Ranged"], {},
    "10/51/0", ["Disciplina 10: Disciplinas gemelas 5/5, Fuego interno mejorado 3/3 y Voluntad inquebrantable 2/5.",
                "Sagrado 51: Especialización sagrada, Renovar mejorado, Concentración divina, Sanación inspirada, "
                "Espíritu de redención, Guía espiritual, Sanación de la luz, Círculo de sanación, Bendición del "
                "sanador, Plegaria de reparación y Espíritu guardián."],
    "Espíritu guardián cierra Sagrado; Guía espiritual convierte el Espíritu en poder con hechizos.",
    [("Mayor", "Glyph of Prayer of Healing", "cura extra"), ("Mayor", "Glyph of Circle of Healing", "un objetivo más"),
     ("Mayor", "Glyph of Guardian Spirit", "-reutilización")],
    meta_extra=HEAL_META, tbc_spec="Holy",
    nota_pesos="Pesos de sanador ajustados a mano para el 70 sin bufos de banda (el maná importa más)."))
_add("Priest", "Shadow", spec(
    "priest_shadow", "Sombra", "Priest",
    {"INT": 0.11, "SPI": 0.47, "SP": 1, "HIT": 0.87, "CRIT": 0.74, "HASTE": 1.65},
    SP_REF, {"main": ("2h",), "alternativas": CASTER_ALTS, "ranged": ("wand",)}, ["Ranged"],
    {"hit_kind": "spell", "golpe_hechizo_talentos": 6.0},
    "10/0/51", ["Disciplina 10: Disciplinas gemelas 5/5, Fuego interno mejorado 3/3 y Meditación 2/3.",
                "Sombra 51: Enfoque de las Sombras 3/3 (+3 % golpe), Sombras más oscuras, Forma de las Sombras, "
                "Abrazo vampírico, Miseria 3/3 (+3 % golpe), Peste devoradora mejorada, Toque vampírico, Arma "
                "sombría, Dolor y sufrimiento, Torturador y Dispersión."],
    "Dispersión cierra el árbol de Sombra; Enfoque de las Sombras y Miseria dan 6 % de golpe.",
    [("Mayor", "Glyph of Shadow", "+poder con Forma de las Sombras"), ("Mayor", "Glyph of Mind Flay", "+daño"),
     ("Mayor", "Glyph of Shadow Word: Pain", "regenera maná")],
    golpe_pericia="Enfoque de las Sombras y Miseria: +6 % golpe con hechizos.", meta_extra=CASTER_META,
    w70={"HIT": CASTER_HIT}, hit_after_cap=0.0, tbc_spec="Shadow"))

# ---------- Pícaro ----------
ROGUE_W = {"AGI": 1.86, "STR": 1.14, "AP": 1, "HIT": 1.39 + 0.08, "CRIT": 1.32 + 0.28, "HASTE": 1.48, "ARP": 0.84,
           "EXP": 0.98, "MH": 2.94, "OH": 2.45}
for name, es, reparto, texto, razon, gl, msub, osub, exp in [
    ("Assassination", "Asesinato", "51/10/0",
     ["Asesinato 51: Malicia 5/5, Implacable 3/3, Letalidad 5/5, Venenos viles, Ataques sangrientos, "
      "Venenos mejorados, Muerte rápida, Golpes de oportunidad, Mutilar, Rapidez de Asesinato y Hambre de sangre.",
      "Combate 10: Especialización en dos armas 5/5 y Precisión 5/5 (+5 % golpe)."],
     "Hambre de sangre y Mutilar son el núcleo con 51 puntos; Precisión da el golpe que falta.",
     [("Mayor", "Glyph of Mutilate", "-coste"), ("Mayor", "Glyph of Hunger for Blood", "dura más"),
      ("Mayor", "Glyph of Rupture", "dura más")], {DAGGER}, {DAGGER}, 0),
    ("Combat", "Combate", "10/51/0",
     ["Asesinato 10: Malicia 5/5 (+5 % crítico), Implacable 3/3 y Salpicadura de sangre 2/2.",
      "Combate 51: Especialización en dos armas, Precisión 5/5, Pericia con armas 2/2 (+10 de pericia), Agresión, "
      "Tajos y cortes, Movilidad, Subidón de adrenalina, Celeridad de combate, Potencia salvaje, Ataques "
      "implacables y Ola de asesinatos."],
     "Con 61 puntos se llega a Ola de asesinatos (fila 11 de Combate); Malicia es el mejor talento barato de "
     "Asesinato.",
     [("Mayor", "Glyph of Sinister Strike", "más puntos de combo"), ("Mayor", "Glyph of Slice and Dice", "dura más"),
      ("Mayor", "Glyph of Adrenaline Rush", "dura más")], {SWORD1, FIST, MACE1, AXE1}, None, 10),
    ("Subtlety", "Sutileza", "0/10/51",
     ["Combate 10: Especialización en dos armas 5/5 y Precisión 5/5.",
      "Sutileza 51: Asesino implacable, Oportunismo, Golpes inquebrantables, Paso de las Sombras, Preparación, "
      "Hemorragia, Maestro del engaño, Muerte segura, Sombras ocultas, Premeditación y Danza de las Sombras."],
     "Danza de las Sombras cierra el árbol; Precisión da el golpe.",
     [("Mayor", "Glyph of Hemorrhage", "+daño"), ("Mayor", "Glyph of Backstab", "alarga Desgarrar"),
      ("Mayor", "Glyph of Shadow Dance", "dura más")], {DAGGER}, None, 0)]:
    _add("Rogue", name, spec(
        "rogue_" + name.lower(), es, "Rogue", dict(ROGUE_W), AP_REF,
        {"main": ("1h", "mh"), "off": ("1h", "oh"), "main_sub": msub, "off_sub": osub, "ranged": ("ranged",)},
        ["Ranged"], {"hit_kind": "melee", "exp": True, "golpe_talentos": 5.0, "pericia_talentos": exp},
        reparto, texto, razon, gl, golpe_pericia="Precisión: +5 % golpe." + (" Pericia con armas: +10." if exp else ""),
        meta_extra=MELEE_CRIT_META, w70={"HIT": (2.0, "por debajo del 8 % de golpe de ataques especiales el golpe vale "
                                                     "más que en el 80, donde wowsims lo da casi cubierto")},
        hit_after_cap=0.8, tbc_spec="DPS"))

# ---------- Chamán ----------
_add("Shaman", "Elemental", spec(
    "sham_ele", "Elemental", "Shaman",
    {"INT": 0.22, "SP": 1, "CRIT": 0.67, "HASTE": 1.29, "MP5": 0.08, "HIT": 1.2},
    SP_REF, {"main": ("2h",), "alternativas": SHIELD_CASTER_ALTS}, ["Relic"],
    {"hit_kind": "spell", "golpe_hechizo_talentos": 3.0},
    "51/10/0", ["Elemental 51: Convección 5/5, Conmoción 5/5, Llamada de las llamas, Enfoque elemental, Reverberación, "
                "Furia elemental, Precisión elemental 3/3 (+3 % golpe), Maestría elemental, Tormenta de rayos, Tótem "
                "de cólera, Oleaje de lava y Tormenta de truenos.",
                "Mejora 10: Conocimiento ancestral 5/5, Tótems de mejora 3/3 y Escudos mejorados 2/3."],
    "Tótem de cólera y Maestría elemental son lo más importante; Tormenta de truenos llega con 51 puntos.",
    [("Mayor", "Glyph of Flame Shock", "+crítico de Ráfaga de lava"), ("Mayor", "Glyph of Lightning Bolt", "+daño"),
     ("Mayor", "Glyph of Totem of Wrath", "+poder con hechizos")],
    golpe_pericia="Precisión elemental: +3 % golpe con hechizos.", meta_extra=CASTER_META,
    w70={"HIT": CASTER_HIT}, hit_after_cap=0.0, tbc_spec="Elemental"))
_add("Shaman", "Enhancement", spec(
    "sham_enh", "Mejora", "Shaman",
    {"INT": 1.48, "AGI": 1.59, "STR": 1.1, "SP": 1.13, "AP": 1.0, "HIT": 1.38, "CRIT": 0.91 + 0.81,
     "HASTE": 0.37 + 1.61, "ARP": 0.48, "EXP": 1.5, "MH": 5.21, "OH": 2.21},
    AP_REF, {"main": ("1h", "mh"), "off": ("1h", "oh")}, ["Relic"],
    {"hit_kind": "melee", "exp": True, "golpe_talentos": 6.0},
    "10/51/0", ["Elemental 10: Convección 5/5 y Conmoción 5/5.",
                "Mejora 51: Conocimiento ancestral 5/5, Tótems de mejora, Golpes atronadores 5/5, Arma de Viento "
                "Furioso mejorada, Especialización en dos armas 3/3 (+6 % golpe), Golpe de tormenta, Ira desatada, "
                "Rapidez mental, Arma vorágine, Lanza de lava, Espíritus feroces."],
    "Espíritus feroces cierra Mejora; Convección y Conmoción suben los choques.",
    [("Mayor", "Glyph of Stormstrike", "+daño de naturaleza"), ("Mayor", "Glyph of Feral Spirit", "+poder de ataque"),
     ("Mayor", "Glyph of Windfury Weapon", "+poder de ataque")],
    golpe_pericia="Especialización en dos armas: +6 % golpe.", meta_extra=MELEE_CRIT_META,
    w70={"EXP": (1.5, "wowsims la pone a 0 porque supone el tope; al 70 no se llega")}, hit_after_cap=0.6,
    exp_after_cap=0.0, tbc_spec="Enhancement"))
_add("Shaman", "Restoration", spec(
    "sham_resto", "Restauración", "Shaman",
    {"INT": 0.45, "SPI": 0.05, "SP": 1, "CRIT": 0.67, "HASTE": 1.0, "MP5": 1.4},
    HEAL_REF, {"main": ("2h",), "alternativas": SHIELD_CASTER_ALTS}, ["Relic"], {},
    "0/10/51", ["Mejora 10: Conocimiento ancestral 5/5, Escudos mejorados 3/3 y Tótems de mejora 2/3.",
                "Restauración 51: Ola de sanación mejorada, Enfoque de marea, Curación ancestral, Maestría de la "
                "marea, Rapidez de la Naturaleza, Tótem de marea de maná, Escudo de tierra, Despertar ancestral y "
                "Mareas vivas."],
    "Mareas vivas cierra el árbol; Escudo de tierra y Tótem de marea de maná son lo que más aportan.",
    [("Mayor", "Glyph of Earth Shield", "+sanación"), ("Mayor", "Glyph of Chain Heal", "un objetivo más"),
     ("Mayor", "Glyph of Earthliving Weapon", "+probabilidad")],
    meta_extra=HEAL_META, tbc_spec="Restoration",
    nota_pesos="Pesos de sanador ajustados a mano para el 70 sin bufos de banda (el maná importa más)."))

# ---------- Brujo ----------
LOCK_W = {"INT": 0.18, "SPI": 0.54, "SP": 1, "HIT": 0.93, "CRIT": 0.53, "HASTE": 0.81, "STA": 0.01}
for name, es, reparto, texto, razon, gl, hitt in [
    ("Affliction", "Aflicción", "51/0/10",
     ["Aflicción 51: Supresión 3/3 (+3 % golpe), Corrupción mejorada 5/5, Drenaje de alma mejorado, Toque mortal, "
      "Consumir sombras, Maldición de agonía mejorada, Plaga de Sombra, Embrujo de la Sombra, Agonía creciente, "
      "Pandemia, Destino ineludible, Aflicción inestable y Embrujo.",
      "Destrucción 10: Descarga de las Sombras mejorada 5/5 y Pesadilla 5/5."],
     "Embrujo cierra Aflicción con 51 puntos.",
     [("Mayor", "Glyph of Haunt", "+daño de Embrujo"), ("Mayor", "Glyph of Corruption", "Trance de las Sombras"),
      ("Mayor", "Glyph of Life Tap", "+poder con hechizos")], 3.0),
    ("Demonology", "Demonología", "0/51/10",
     ["Demonología 51: Diablillo mejorado, Abrazo demoníaco, Vínculo de alma, Sinergia vil, Poder demoníaco, "
      "Sabiduría maestra, Táctica demoníaca, Guardia vil, Empoderamiento demoníaco, Pacto demoníaco y "
      "Metamorfosis.", "Destrucción 10: Descarga de las Sombras mejorada 5/5 y Pesadilla 5/5."],
     "Metamorfosis llega con 51 puntos; Pacto demoníaco da poder con hechizos al grupo. Sin talento de golpe.",
     [("Mayor", "Glyph of Felguard", "+poder de ataque"), ("Mayor", "Glyph of Life Tap", "+poder con hechizos"),
      ("Mayor", "Glyph of Shadow Bolt", "-coste")], 0.0),
    ("Destruction", "Destrucción", "10/0/51",
     ["Aflicción 10: Supresión 3/3 (+3 % golpe), Corrupción mejorada 5/5 y Drenaje de vida mejorado 2/2.",
      "Destrucción 51: Descarga de las Sombras mejorada, Pesadilla, Devastación, Ruina, Conflagrar, Destrucción, "
      "Abrasar mejorado, Sombra y llama, Reacción explosiva, Fuego y azufre, Furia de las Sombras e Incinerar "
      "mejorado y Descarga de caos."],
     "Descarga de caos cierra Destrucción; Supresión da el 3 % de golpe.",
     [("Mayor", "Glyph of Conflagrate", "no consume Inmolar"), ("Mayor", "Glyph of Incinerate", "+daño"),
      ("Mayor", "Glyph of Life Tap", "+poder con hechizos")], 3.0)]:
    _add("Warlock", name, spec(
        "lock_" + name.lower(), es, "Warlock", dict(LOCK_W), SP_REF,
        {"main": ("2h",), "alternativas": CASTER_ALTS, "ranged": ("wand",)}, ["Ranged"],
        {"hit_kind": "spell", "golpe_hechizo_talentos": hitt}, reparto, texto, razon, gl,
        meta_extra=CASTER_META, w70={"HIT": CASTER_HIT}, hit_after_cap=0.0, tbc_spec=name))

# ---------- Guerrero ----------
WAR_W = {"STR": 2.72, "AGI": 1.82, "AP": 1, "EXP": 2.55, "HIT": 0.79, "CRIT": 2.12, "HASTE": 1.72, "ARP": 2.17,
         "ARMOR": 0.03, "MH": 6.29, "OH": 3.58}
_add("Warrior", "Arms", spec(
    "war_arms", "Armas", "Warrior", dict(WAR_W), AP_REF, {"main": ("2h",), "ranged": ("ranged",)}, ["Ranged"],
    {"hit_kind": "melee", "exp": True, "pericia_talentos": 4},
    "51/10/0", ["Armas 51: Golpe heroico mejorado 3/3, Desviación, Especialización en hachas/espadas/mazas, Fuerza "
                "de las armas 2/2 (+4 de pericia), Golpe mortal, Heridas profundas, Atrasar el tiempo, Desangrar, "
                "Comprensión de traumas, Golpes súbitos, Despedazar mejorado, Filotormenta.",
                "Furia 10: Armadura hasta los dientes 3/3, Crueldad 5/5 y Voz atronadora 2/2."],
    "Filotormenta cierra Armas; Crueldad da crítico.",
    [("Mayor", "Glyph of Rending", "Desgarrar dura más"), ("Mayor", "Glyph of Mortal Strike", "+daño"),
     ("Mayor", "Glyph of Overpower", "Abrumar tras parada")],
    golpe_pericia="Fuerza de las armas: +4 de pericia.", meta_extra=MELEE_CRIT_META, extra_manual=CRUSADER,
    w70={"HIT": (2.3, "por debajo del 8 % el golpe vale casi como la pericia; wowsims lo supone casi cubierto")},
    hit_after_cap=0.0, tbc_spec="Arms"))
_add("Warrior", "Fury", spec(
    "war_fury", "Furia", "Warrior", dict(WAR_W), AP_REF,
    {"main": ("2h",), "off": ("2h",), "ranged": ("ranged",)}, ["Ranged"],
    {"hit_kind": "melee", "exp": True, "golpe_talentos": 3.0},
    "10/51/0", ["Armas 10: Golpe heroico mejorado 3/3, Desviación 2/5, Táctica 5/5.",
                "Furia 51: Armadura hasta los dientes, Crueldad 5/5, Ejecutar mejorado, Precisión 3/3 (+3 % golpe), "
                "Muerte inminente, Flurry, Torbellino mejorado, Sed de sangre, Furia rabiosa, Golpe heroico "
                "salvaje, Embriaguez de sangre y Agarre de titán."],
    "Agarre de titán (fila 11 de Furia, 51 puntos) permite llevar dos armas de dos manos.",
    [("Mayor", "Glyph of Bloodthirst", "+sanación"), ("Mayor", "Glyph of Whirlwind", "-reutilización"),
     ("Mayor", "Glyph of Heroic Strike", "+ira")],
    golpe_pericia="Precisión: +3 % golpe.", meta_extra=MELEE_CRIT_META, extra_manual=CRUSADER,
    w70={"HIT": (2.3, "por debajo del 8 % el golpe vale casi como la pericia; wowsims lo supone casi cubierto")},
    hit_after_cap=0.9, tbc_spec="Fury"))
_add("Warrior", "Protection", spec(
    "war_prot", "Protección", "Warrior",
    {"ARMOR": 0.174, "BARMOR": 0.155, "STA": 2.336, "STR": 1.555, "AGI": 2.771, "AP": 0.32, "EXP": 1.44,
     "HIT": 1.432, "CRIT": 0.925, "HASTE": 0.431, "ARP": 1.055, "BLOCK": 1.320, "BLOCKV": 1.373, "DODGE": 2.606,
     "PARRY": 2.649, "DEF": 3.305, "MH": 6.081},
    TANK_REF, {"main": ("1h", "mh"), "off": ("shield",), "ranged": ("ranged",)}, ["Ranged"],
    {"hit_kind": "melee", "exp": True, "tank": True, "pericia_talentos": 6},
    "10/0/51", ["Armas 10: Golpe heroico mejorado 3/3, Desviación 5/5 y Táctica 2/5.",
                "Protección 51: Escudo mejorado, Anticipación 5/5, Dureza 5/5, Último aguante, Vitalidad 3/3 (+6 "
                "de pericia), Crítico de escudo, Devastar, Protección de seguridad, Muro de escudo mejorado, "
                "Ruptura de daño, Espada y tabla, Golpe de daño crítico y Ola de choque."],
    "Ola de choque cierra el árbol; Vitalidad da pericia y Desviación parada.",
    [("Mayor", "Glyph of Devastate", "aplica dos Sunder"), ("Mayor", "Glyph of Revenge", "Golpe heroico gratis"),
     ("Mayor", "Glyph of Vigilance", "-amenaza transferida")],
    golpe_pericia="Vitalidad: +6 de pericia.", def_after_cap=3.0, exp_after_cap=0.6, hit_after_cap=0.3,
    tbc_spec="Protection"))

# Reliquias: su efecto es una habilidad concreta; valor estimado a mano en EP (efectos copiados del tooltip WotLK).
_R = "estimación a mano del efecto de la reliquia"
RELICS = {
    "ret": {31033: 50, 28065: 40, 33503: 90, 24386: 2, 23203: 5},
    "pal_holy": {25644: 30, 28296: 25, 23201: 12, 33502: 20},
    "pal_prot": {29388: 25, 27917: 15, 22400: 8, 24386: 5},
    "druid_balance": {27518: 30, 31025: 15, 23197: 10, 33510: 35},
    "druid_cat": {28064: 35, 28372: 30, 22397: 15, 29390: 45, 33509: 50, 25940: 3},
    "druid_bear": {28064: 30, 27744: 20, 23198: 15, 33509: 40},
    "druid_resto": {25643: 30, 27886: 28, 22399: 10, 33508: 20},
    "sham_ele": {28248: 35, 23199: 20, 28066: 10, 22395: 8, 33506: 40, 29389: 12},
    "sham_enh": {27815: 35, 31031: 10, 22395: 12, 33507: 55},
    "sham_resto": {27544: 30, 25645: 28, 23200: 15, 24413: 15, 33505: 15, 22396: 20},
}
for _k, _d in RELICS.items():
    for _i, _v in _d.items():
        MANUAL_VALUES.setdefault(_k, {}).setdefault(_i, (_v, _R))

for _sp in SPECS.values():
    if _sp.get("extra_manual"):
        MANUAL_VALUES.setdefault(_sp["key"], {}).update(_sp["extra_manual"])
