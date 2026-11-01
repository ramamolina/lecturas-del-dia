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

    salida = {'obras': OBRAS, 'textos': textos, 'fechas': fechas, 'pascua': pascua}
    with open(os.path.join(BASE, 'meditaciones.json'), 'w', encoding='utf-8') as f:
        json.dump(salida, f, ensure_ascii=False, separators=(',', ':'))
    print('meditaciones.json: %d textos, %d fechas' % (len(textos), len(fechas)))


if __name__ == '__main__':
    main()
