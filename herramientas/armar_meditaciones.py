"""Arma meditaciones.json a partir de los textos de la carpeta meditaciones/.

meditaciones/en/<id>.txt  texto original (dominio público, Standard Ebooks)
meditaciones/es/<id>.txt  traducción libre hecha por Claude
Párrafos separados por una línea en blanco; _texto_ = cursiva.

Uso:  python3 herramientas/armar_meditaciones.py
"""
import json
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CARPETA = os.path.join(BASE, 'meditaciones')

OBRAS = {
    'carol': {
        'autor': 'Charles Dickens',
        'titulo_es': 'Canción de Navidad',
        'titulo_en': 'A Christmas Carol',
        'anio': 1843,
        'fuente': 'Standard Ebooks',
    },
    'cueva': {
        'autor': 'G. K. Chesterton',
        'titulo_es': 'El hombre eterno',
        'titulo_en': 'The Everlasting Man',
        'anio': 1925,
        'fuente': 'Standard Ebooks',
    },
    'orto': {
        'autor': 'G. K. Chesterton',
        'titulo_es': 'Ortodoxia',
        'titulo_en': 'Orthodoxy',
        'anio': 1908,
        'fuente': 'Standard Ebooks',
    },
    'newman': {
        'autor': 'John Henry Newman',
        'titulo_es': 'Meditaciones y devociones',
        'titulo_en': 'Meditations and Devotions',
        'anio': 1893,
        'fuente': 'Internet Archive, 1893 edition (OCR corrected)',
    },
}

# Cuaresma y Semana Santa (Newman). Claves: días respecto del Domingo de Pascua (-46 = Miércoles de Ceniza).
VIA_CRUCIS = [
    ('Jesús es condenado a muerte', 'Jesus is Condemned to Death'),
    ('Jesús recibe la Cruz', 'Jesus receives His Cross'),
    ('Jesús cae por primera vez', 'Jesus falls the first time beneath the Cross'),
    ('Jesús se encuentra con su Madre', 'Jesus meets His Mother'),
    ('Simón de Cirene ayuda a Jesús a llevar la Cruz', 'Simon of Cyrene helps Jesus to carry the Cross'),
    ('Jesús y la Verónica', 'Jesus and Veronica'),
    ('Jesús cae por segunda vez', 'Jesus falls a second time'),
    ('Jesús consuela a las mujeres de Jerusalén', 'Jesus comforts the Women of Jerusalem'),
    ('Jesús cae por tercera vez', 'Again, a third time, Jesus falls'),
    ('Jesús es despojado de sus vestiduras', 'Jesus is stripped and drenched with gall'),
    ('Jesús es clavado en la Cruz', 'Jesus is nailed to the Cross'),
    ('Jesús muere en la Cruz', 'Jesus dies upon the Cross'),
    ('Jesús es bajado de la Cruz y puesto en brazos de María', 'Jesus is taken from the Cross, and laid in Mary’s Bosom'),
    ('Jesús es puesto en el sepulcro', 'Jesus is laid in the Tomb'),
]
ORDINAL = ['Primera', 'Segunda', 'Tercera', 'Cuarta', 'Quinta', 'Sexta', 'Séptima', 'Octava', 'Novena',
           'Décima', 'Undécima', 'Duodécima', 'Decimotercera', 'Decimocuarta']
ORDINAL_EN = ['First', 'Second', 'Third', 'Fourth', 'Fifth', 'Sixth', 'Seventh', 'Eighth', 'Ninth',
              'Tenth', 'Eleventh', 'Twelfth', 'Thirteenth', 'Fourteenth']
REDENTOR = (  # (desde, hasta, título es, título en)
    (1, 3, 'Los sufrimientos interiores de nuestro Señor', 'The Mental Sufferings of Our Lord'),
    (4, 12, 'Nuestro Señor renuncia al consuelo humano', 'Our Lord refuses Sympathy'),
    (13, 14, 'Los sufrimientos corporales de nuestro Señor', 'The Bodily Sufferings of Our Lord'),
)
VIERNES = {
    1: ('Jesús, Cordero de Dios', 'Jesus the Lamb of God'),
    4: ('Jesús, autor y consumador de la fe', 'Jesus the Author and Finisher of Faith'),
    5: ('Jesús, Señor de los ejércitos', 'Jesus the Lord of Armies'),
    6: ('Jesús, Hijo unigénito', 'Jesus the Only Begotten Son'),
    7: ('Jesús, Rey eterno', 'Jesus the Eternal King'),
    8: ('Jesús, principio de la nueva creación', 'Jesus the Beginning of the New Creation'),
    9: ('Jesús, amante de las almas', 'Jesus the Lover of Souls'),
    10: ('Jesús, nuestro guía y custodio', 'Jesus our Guide and Guardian'),
    11: ('Jesús, Hijo de María', 'Jesus Son of Mary'),
    12: ('Jesús, nuestro sacrificio cotidiano', 'Jesus our Daily Sacrifice'),
}
SEMANA_SANTA = [(-7, [1, 4]), (-6, [5, 6]), (-5, [7, 8]), (-4, [9, 10]), (-3, [12]), (-2, [11])]

# Mayo: (título latino de la Letanía, título en español, título en inglés)
MAYO = [
    ('', 'El mes de María (1/2)', 'The Month of Mary (1/2)'),
    ('', 'El mes de María (2/2)', 'The Month of Mary (2/2)'),
    ('Virgo Purissima', 'Virgen purísima', 'Most Pure Virgin'),
    ('Virgo Prædicanda', 'Virgen digna de alabanza', 'Virgin to be Proclaimed'),
    ('Mater Admirabilis', 'Madre admirable', 'Mother Most Admirable'),
    ('Domus Aurea', 'Casa de oro', 'House of Gold'),
    ('Mater Amabilis', 'Madre amable', 'Mother Most Amiable'),
    ('Virgo Veneranda', 'Virgen venerable', 'Virgin Most Venerable'),
    ('Sancta Maria', 'Santa María', 'Holy Mary'),
    ('Regina Angelorum', 'Reina de los Ángeles', 'Queen of Angels'),
    ('Speculum Justitiæ', 'Espejo de justicia', 'Mirror of Justice'),
    ('Sedes Sapientiæ', 'Trono de la sabiduría', 'Seat of Wisdom'),
    ('Janua Cœli', 'Puerta del cielo', 'Gate of Heaven'),
    ('Mater Creatoris', 'Madre del Creador', 'Mother of the Creator'),
    ('Mater Christi', 'Madre de Cristo', 'Mother of Christ'),
    ('Mater Salvatoris', 'Madre del Salvador', 'Mother of the Saviour'),
    ('Regina Martyrum', 'Reina de los mártires', 'Queen of Martyrs'),
    ('Vas Insigne Devotionis', 'Vaso insigne de devoción', 'Singular Vessel of Devotion'),
    ('Vas Honorabile', 'Vaso digno de honor', 'Vessel of Honour'),
    ('Vas Spirituale', 'Vaso espiritual', 'Spiritual Vessel'),
    ('Consolatrix Afflictorum', 'Consuelo de los afligidos', 'Comforter of the Afflicted'),
    ('Virgo Prudentissima', 'Virgen prudentísima', 'Most Prudent Virgin'),
    ('Turris Eburnea', 'Torre de marfil', 'Tower of Ivory'),
    ('Sancta Dei Genitrix', 'Santa Madre de Dios', 'Holy Mother of God'),
    ('Mater Intemerata', 'Madre inmaculada', 'Mother Undefiled'),
    ('Rosa Mystica', 'Rosa mística', 'Mystical Rose'),
    ('Turris Davidica', 'Torre de David', 'Tower of David'),
    ('Virgo Potens', 'Virgen poderosa', 'Virgin Most Powerful'),
    ('Auxilium Christianorum', 'Auxilio de los cristianos', 'Help of Christians'),
    ('Virgo Fidelis', 'Virgen fiel', 'Virgin Most Faithful'),
    ('Stella Matutina', 'Estrella de la mañana', 'Morning Star'),
]

# Meditaciones sobre la doctrina cristiana (Newman, tercera parte). nw-dNN en el orden del libro.
DOCTRINA = {
    1: ('Dios y el alma (1/3): Dios, felicidad del alma', 'God and the Soul (1/3): God the Blessedness of the Soul'),
    2: ('Dios y el alma (2/3): Jesucristo, el mismo ayer y hoy', 'God and the Soul (2/3): Jesus Christ Yesterday and To-day'),
    3: ('Dios y el alma (3/3): Un acto de amor', 'God and the Soul (3/3): An Act of Love'),
    4: ('El pecado (1/7): Contra Ti solo pequé', 'Sin (1/7): Against Thee Only Have I Sinned'),
    5: ('El pecado (2/7): Contra Ti solo pequé', 'Sin (2/7): Against Thee Only Have I Sinned'),
    6: ('El pecado (3/7): Los efectos del pecado', 'Sin (3/7): The Effects of Sin'),
    7: ('El pecado (4/7): El mal del pecado', 'Sin (4/7): The Evil of Sin'),
    8: ('El pecado (5/7): La gravedad del pecado', 'Sin (5/7): The Heinousness of Sin'),
    9: ('El pecado (6/7): La esclavitud del pecado', 'Sin (6/7): The Bondage of Sin'),
    10: ('El pecado (7/7): Todo pecado tiene su castigo', 'Sin (7/7): Every Sin has its Punishment'),
    11: ('El poder de la Cruz', 'The Power of the Cross'),
    12: ('La Resurrección (1/3): Templos del Espíritu Santo', 'The Resurrection (1/3): The Temples of the Holy Ghost'),
    13: ('La Resurrección (2/3): Solo Dios', 'The Resurrection (2/3): God Alone'),
    14: ('La Resurrección (3/3): La paciencia de Jesús', 'The Resurrection (3/3): The Forbearance of Jesus'),
    15: ('Dios con nosotros (1/3): La cercanía de Jesús', 'God with Us (1/3): The Familiarity of Jesus'),
    16: ('Dios con nosotros (2/3): Jesús, el Dios escondido', 'God with Us (2/3): Jesus the Hidden God'),
    17: ('Dios con nosotros (3/3): Jesús, luz del alma', 'God with Us (3/3): Jesus the Light of the Soul'),
    18: ('Dios, que basta para todo', 'God All-Sufficient'),
    19: ('Solo Dios es inmutable', 'God Alone Unchangeable'),
    20: ('Dios es amor', 'God is Love'),
    21: ('La santidad de Dios', 'The Sanctity of God'),
    22: ('Los cuarenta días (1/4): El reino de Dios', 'The Forty Days’ Teaching (1/4): The Kingdom of God'),
    23: ('Los cuarenta días (2/4): Abandono en la voluntad de Dios', 'The Forty Days’ Teaching (2/4): Resignation to God’s Will'),
    24: ('Los cuarenta días (3/4): La despedida del Señor', 'The Forty Days’ Teaching (3/4): Our Lord’s Parting with His Apostles'),
    25: ('Los cuarenta días (4/4): Los caminos de Dios no son los nuestros', 'The Forty Days’ Teaching (4/4): God’s Ways not our Ways'),
    26: ('La Ascensión (1/4): Subió', 'The Ascension (1/4): He Ascended'),
    27: ('La Ascensión (2/4): Subió al cielo', 'The Ascension (2/4): He Ascended into Heaven'),
    28: ('La Ascensión (3/4): Nuestro Abogado en el cielo', 'The Ascension (3/4): Our Advocate Above'),
    29: ('La Ascensión (4/4): Nuestro Abogado en el cielo', 'The Ascension (4/4): Our Advocate Above'),
    30: ('El Paráclito (1/4): Vida de todas las cosas', 'The Paraclete (1/4): The Life of All Things'),
    31: ('El Paráclito (2/4): Vida de la Iglesia', 'The Paraclete (2/4): The Life of the Church'),
    32: ('El Paráclito (3/4): Vida de mi alma', 'The Paraclete (3/4): The Life of my Soul'),
    33: ('El Paráclito (4/4): Fuente del amor', 'The Paraclete (4/4): The Fount of Love'),
    34: ('El santo Sacrificio (1/3): La Misa', 'The Holy Sacrifice (1/3): The Mass'),
    35: ('El santo Sacrificio (2/3): La Comunión', 'The Holy Sacrifice (2/3): Holy Communion'),
    36: ('El santo Sacrificio (3/3): El alimento del alma', 'The Holy Sacrifice (3/3): The Food of the Soul'),
    37: ('El Sagrado Corazón', 'The Sacred Heart'),
    38: ('La perfección infinita de Dios', 'The Infinite Perfection of God'),
    39: ('El conocimiento infinito de Dios', 'The Infinite Knowledge of God'),
    40: ('La providencia de Dios', 'The Providence of God'),
    41: ('Dios es todo en todos', 'God is All in All'),
    42: ('Dios, perfección incomunicable', 'God the Incommunicable Perfection'),
    43: ('Dios comunicado a nosotros', 'God Communicated to Us'),
    44: ('Dios, único sostén para la eternidad', 'God the Sole Stay for Eternity'),
    45: ('Conclusión: «Escribo con la muerte a la vista»', 'Conclusion: ‘I write in the direct view of death’'),
}
# Tiempo pascual: del Domingo de Pascua a Pentecostés, en los días libres (no mayo)
SERIE_PASCUA = [12, 13, 14, 15, 16, 17, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 18, 19, 20, 21]
# Corpus Christi (domingo, en Argentina) y Sagrado Corazón: días respecto de la Pascua
FIESTAS = {63: 34, 64: 35, 65: 36, 68: 37}
# Tiempo ordinario, primer tramo: del 9 de enero al martes antes de Ceniza
# (el segundo tramo, de Pentecostés al 30 de noviembre, queda para Chesterton y otros)
SERIE_ORDINARIO = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 38, 39, 40, 41, 42, 43, 44, 45]

# Ortodoxia (Chesterton): capítulos (cantidad de partes, título es, título en). orto-NN seguidos.
ORTODOXIA = [
    (2, 'Introducción en defensa de todo lo demás', 'Introduction in Defence of Everything Else'),
    (6, 'El loco', 'The Maniac'),
    (6, 'El suicidio del pensamiento', 'The Suicide of Thought'),
    (7, 'La ética de los cuentos de hadas', 'The Ethics of Elfland'),
    (6, 'La bandera del mundo', 'The Flag of the World'),
    (8, 'Las paradojas del cristianismo', 'The Paradoxes of Christianity'),
    (8, 'La revolución eterna', 'The Eternal Revolution'),
    (6, 'El romance de la ortodoxia', 'The Romance of Orthodoxy'),
    (7, 'La autoridad y el aventurero', 'Authority and the Adventurer'),
]
ROMANOS = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX']

# Estrofas de A Christmas Carol: (cuántos trozos tiene, título en español, título en inglés)
ESTROFAS = [
    (5, 'Primera estrofa: El fantasma de Marley', "Stave One: Marley's Ghost"),
    (5, 'Segunda estrofa: El primero de los tres espíritus', 'Stave Two: The First of the Three Spirits'),
    (7, 'Tercera estrofa: El segundo de los tres espíritus', 'Stave Three: The Second of the Three Spirits'),
    (5, 'Cuarta estrofa: El último de los espíritus', 'Stave Four: The Last of the Spirits'),
    (2, 'Quinta estrofa: El final de todo', 'Stave Five: The End of It'),
]


def leer(idioma, ident):
    with open(os.path.join(CARPETA, idioma, ident + '.txt'), encoding='utf-8') as f:
        ps = [p.strip() for p in f.read().split('\n\n') if p.strip()]
    # Versalitas del libro impreso al comienzo de párrafo («LEAVING the House…» → «Leaving the House…»)
    import re
    return [re.sub(r'^([‘“]?(?:\d+\. )?)([A-Z])([A-Z]+)\b(?= [a-z(‘])', lambda m: m.group(1) + m.group(2) + m.group(3).lower(), p) for p in ps]


def sin_titulo(ps, titulo):
    """Saca el párrafo con el título del capítulo (ya va en el título de la meditación)."""
    return [p for p in ps if p.strip('_') != titulo]


def fecha_mas(mmdd, n):
    """Suma n días a una fecha MM-DD de un año no bisiesto (alcanza para dic-ene)."""
    import datetime
    d = datetime.date(2027, int(mmdd[:2]), int(mmdd[3:])) + datetime.timedelta(days=n)
    return d.strftime('%m-%d')


def main():
    textos, fechas = {}, {}

    # Canción de Navidad: del 1 al 24 de diciembre (fechas fijas, siempre antes de Navidad)
    n = 0
    for e, (cant, tit_es, tit_en) in enumerate(ESTROFAS):
        for k in range(1, cant + 1):
            n += 1
            ident = 'carol-%02d' % n
            en, es = leer('en', ident), leer('es', ident)
            if k == 1:  # el primer trozo de cada estrofa empieza con su título
                en, es = en[1:], es[1:]
            parte = ' (%d/%d)' % (k, cant) if cant > 1 else ''
            textos[ident] = {
                'obra': 'carol', 'tiempo': 'Hacia la Navidad',
                'titulo_es': tit_es + parte, 'titulo_en': tit_en + parte,
                'es': es, 'en': en, 'sigue': n < 24,
            }
            fechas[fecha_mas('12-01', n - 1)] = ident

    # El hombre eterno, «El Dios en la cueva»: del 25 de diciembre al 8 de enero
    for k in range(1, 16):
        ident = 'cueva-%02d' % k
        textos[ident] = {
            'obra': 'cueva', 'tiempo': 'Tiempo de Navidad',
            'titulo_es': 'El Dios en la cueva (%d/15)' % k,
            'titulo_en': 'The God in the Cave (%d/15)' % k,
            'es': leer('es', ident), 'en': leer('en', ident), 'sigue': k < 15,
        }
        fechas[fecha_mas('12-25', k - 1)] = ident

    pascua = {}

    def nw(ident, tiempo, tit_es, tit_en, sigue, es=None, en=None):
        textos[ident] = {
            'obra': 'newman', 'tiempo': tiempo, 'titulo_es': tit_es, 'titulo_en': tit_en,
            'es': es if es is not None else leer('es', ident), 'en': en if en is not None else leer('en', ident),
            'sigue': sigue,
        }

    dia = -46
    for k in range(1, 5):  # Miércoles de Ceniza a sábado: Esperanza en Dios Creador
        ident = 'nw-cre-%02d' % k
        nw(ident, 'Cuaresma', 'Esperanza en Dios Creador (%d/4)' % k, 'Hope in God — Creator (%d/4)' % k, k < 4)
        pascua[str(dia)] = ident; dia += 1
    for k in range(1, 15):  # 1er domingo de Cuaresma en adelante: Vía Crucis
        ident = 'nw-est-%02d' % k
        es_t, en_t = VIA_CRUCIS[k - 1]
        nw(ident, 'Cuaresma', 'Vía Crucis · %s estación: %s' % (ORDINAL[k - 1], es_t),
           'Stations of the Cross · The %s Station: %s' % (ORDINAL_EN[k - 1], en_t), k < 14)
        pascua[str(dia)] = ident; dia += 1
    for k in range(1, 8):  # Vía Crucis breve, dos estaciones por día
        ident = 'nw-cor-%02d' % k
        nw(ident, 'Cuaresma', 'Vía Crucis breve · estaciones %d y %d' % (2 * k - 1, 2 * k),
           'Short Meditations on the Stations · %d and %d' % (2 * k - 1, 2 * k), k < 7)
        pascua[str(dia)] = ident; dia += 1
    for k in range(1, 15):  # Esperanza en Dios Redentor
        ident = 'nw-red-%02d' % k
        for (a, b, tes, ten) in REDENTOR:
            if a <= k <= b:
                parte = ' (%d/%d)' % (k - a + 1, b - a + 1)
                nw(ident, 'Cuaresma', tes + parte, ten + parte, k < 14)
        pascua[str(dia)] = ident; dia += 1
    assert dia == -7
    for (d, nums) in SEMANA_SANTA:  # Doce meditaciones para el Viernes Santo
        es, en = [], []
        for n in nums:
            es += ['_%s_' % VIERNES[n][0]] + leer('es', 'nw-vie-%02d' % n)
            en += ['_%s_' % VIERNES[n][1]] + leer('en', 'nw-vie-%02d' % n)
        ident = 'nw-ss%d' % (-d)
        nw(ident, 'Semana Santa', ' · '.join(VIERNES[n][0] for n in nums),
           ' · '.join(VIERNES[n][1] for n in nums), True, es, en)
        pascua[str(d)] = ident
    nw('nw-sab-01', 'Sábado Santo', 'Está cumplido', 'It is Consummated', False)
    pascua['-1'] = 'nw-sab-01'

    # Mes de María (Newman, primera parte): un título de la Letanía por día, del 1 al 31 de mayo
    for k, (lat, es_t, en_t) in enumerate(MAYO, 1):
        ident = 'nw-may-%02d' % k
        tit = lat + ' · ' if lat else ''
        nw(ident, 'Mes de María', tit + es_t, tit + en_t, k < 31)
        fechas['05-%02d' % k] = ident

    # Doctrina cristiana (Newman): series de Pascua y tiempo ordinario, más Corpus y Sagrado Corazón
    def doc(k, tiempo):
        ident = 'nw-d%02d' % k
        nw(ident, tiempo, DOCTRINA[k][0], DOCTRINA[k][1], False)
        return ident
    series = [
        {'nombre': 'pascua', 'tramos': [[0, 49]], 'textos': [doc(k, 'Tiempo pascual') for k in SERIE_PASCUA]},
        {'nombre': 'ordinario-enero', 'tramos': [['01-09', -47]],
         'textos': [doc(k, 'Tiempo ordinario') for k in SERIE_ORDINARIO]},
    ]
    # Tiempo ordinario, segundo tramo: lunes después de Pentecostés → 30 de noviembre
    ordinario, n = [], 0
    for c, (cant, tes, ten) in enumerate(ORTODOXIA):
        for j in range(1, cant + 1):
            n += 1
            ident = 'orto-%02d' % n
            if not os.path.exists(os.path.join(CARPETA, 'es', ident + '.txt')):
                continue  # todavía sin traducir
            parte = ' (%d/%d)' % (j, cant)
            textos[ident] = {
                'obra': 'orto', 'tiempo': 'Tiempo ordinario',
                'titulo_es': '%s. %s%s' % (ROMANOS[c], tes, parte), 'titulo_en': '%s. %s%s' % (ROMANOS[c], ten, parte),
                'es': sin_titulo(leer('es', ident), tes), 'en': sin_titulo(leer('en', ident), ten), 'sigue': n < 56,
            }
            ordinario.append(ident)
    series.append({'nombre': 'ordinario', 'tramos': [[50, '11-30']], 'textos': ordinario})

    for d, k in FIESTAS.items():
        pascua[str(d)] = doc(k, 'Sagrado Corazón' if k == 37 else 'Corpus Christi')

    salida = {'obras': OBRAS, 'textos': textos, 'fechas': fechas, 'pascua': pascua, 'series': series}
    with open(os.path.join(BASE, 'meditaciones.json'), 'w', encoding='utf-8') as f:
        json.dump(salida, f, ensure_ascii=False, separators=(',', ':'))
    print('meditaciones.json: %d textos, %d fechas' % (len(textos), len(fechas)))


if __name__ == '__main__':
    main()
