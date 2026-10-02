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
    24030: _g("Runed Living Ruby", "R", SP=9), 24031: _g("Bright Living Ruby", "R", AP=16, RAP=16),
    24032: _g("Subtle Living Ruby", "R", DODGE=8), 24036: _g("Flashing Living Ruby", "R", PARRY=8),
    24047: _g("Brilliant Dawnstone", "Y", INT=8), 24048: _g("Smooth Dawnstone", "Y", CRIT=8),
    24051: _g("Rigid Dawnstone", "Y", HIT=8), 35315: _g("Quick Dawnstone", "Y", HASTE=8),
    24052: _g("Thick Dawnstone", "Y", DEF=8),
    24033: _g("Solid Star of Elune", "B", STA=12), 24035: _g("Sparkling Star of Elune", "B", SPI=8),
    24037: _g("Lustrous Star of Elune", "B", MP5=4),
    24058: _g("Inscribed Noble Topaz", "O", STR=4, CRIT=4), 24061: _g("Glinting Noble Topaz", "O", AGI=4, HIT=4),
    24059: _g("Potent Noble Topaz", "O", SP=5, CRIT=4), 24060: _g("Luminous Noble Topaz", "O", SP=5, INT=4),
    31867: _g("Veiled Noble Topaz", "O", SP=5, HIT=4), 31868: _g("Wicked Noble Topaz", "O", AP=8, RAP=8, CRIT=4),
    35316: _g("Reckless Noble Topaz", "O", SP=5, HASTE=4),
    24054: _g("Sovereign Nightseye", "P", STR=4, STA=6), 24055: _g("Shifting Nightseye", "P", AGI=4, STA=6),
    24056: _g("Glowing Nightseye", "P", SP=5, STA=6), 24057: _g("Royal Nightseye", "P", SP=5, MP5=2),
    31863: _g("Balanced Nightseye", "P", AP=8, RAP=8, STA=6), 35707: _g("Regal Nightseye", "P", DODGE=4, STA=6),
    24065: _g("Dazzling Talasite", "G", INT=4, MP5=2), 24062: _g("Enduring Talasite", "G", DEF=4, STA=6),
    24067: _g("Jagged Talasite", "G", CRIT=4, STA=6), 35318: _g("Forceful Talasite", "G", HASTE=4, STA=6),
}

# Metas: requisitos copiados del tooltip WotLK (3.3.5a). "min": mínimos por color; "more": (A, B) = más A que B.
METAS = {
    32409: {"name": "Relentless Earthstorm Diamond", "stats": {"AGI": 12}, "extra": "3 % daño crítico",
            "req": {"min": {"R": 2, "Y": 2, "B": 2}}},
    34220: {"name": "Chaotic Skyfire Diamond", "stats": {"CRIT": 12}, "extra": "3 % daño crítico",
            "req": {"min": {"B": 2}}},
    25894: {"name": "Swift Skyfire Diamond", "stats": {"AP": 24, "RAP": 24}, "extra": "",
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
        "slots": ["Head", "Neck", "Shoulder", "Back", "Chest", "Wrist", "Hands", "Waist", "Legs", "Feet", "Finger",
                  "Trinket", "Weapon", "Relic"],
        "caps": {"golpe_talentos": 0.0, "pericia_talentos": 0, "hit_kind": "melee"},
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
