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
    },
    'cueva': {
        'autor': 'G. K. Chesterton',
        'titulo_es': 'El hombre eterno',
        'titulo_en': 'The Everlasting Man',
        'anio': 1925,
    },
}

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
        return [p.strip() for p in f.read().split('\n\n') if p.strip()]


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

    salida = {'obras': OBRAS, 'textos': textos, 'fechas': fechas}
    with open(os.path.join(BASE, 'meditaciones.json'), 'w', encoding='utf-8') as f:
        json.dump(salida, f, ensure_ascii=False, separators=(',', ':'))
    print('meditaciones.json: %d textos, %d fechas' % (len(textos), len(fechas)))


if __name__ == '__main__':
    main()
