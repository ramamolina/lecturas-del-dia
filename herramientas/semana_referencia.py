"""Agrega a cada día que es santo, fiesta o solemnidad la referencia de la semana del
calendario litúrgico (campo 'f'), ej. 'Miércoles de la 32ª semana durante el año'.

Se toma de los otros días de la misma semana (de domingo a sábado) que ya tienen nombre de
feria ('Lunes de la 32ª semana durante el año') o de domingo ('32º domingo durante el año').
Si en esa semana no hay ninguno (octavas, Semana Santa, tiempo de Navidad), no se agrega nada.

Uso:  python3 -I herramientas/semana_referencia.py lecturas.json
(datos_app.py también lo aplica al armar el archivo).
"""
import datetime
import json
import re
import sys

DIAS = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
FERIA = re.compile(r'^(?:Lunes|Martes|Miércoles|Jueves|Viernes|Sábado) de la (\d+)ª semana (.+)$')
DOMINGO = re.compile(r'^(\d+)º domingo (durante el año|de Adviento|de Cuaresma|de Pascua)$')


def agregar(dias):
    for fecha, x in dias.items():
        x.pop('f', None)
        if FERIA.match(x['c']) or DOMINGO.match(x['c']):
            continue  # el nombre ya dice la semana
        d = datetime.date.fromisoformat(fecha)
        if d.month == 12 and d.day >= 25:
            continue  # tiempo de Navidad: la semana de Adviento ya terminó
        inicio = d - datetime.timedelta(days=(d.weekday() + 1) % 7)  # domingo de esa semana
        ref = None
        for i in range(7):
            otro = inicio + datetime.timedelta(days=i)
            y = dias.get(otro.isoformat())
            if not y or (otro.month == 12 and otro.day >= 25):
                continue
            m = FERIA.match(y['c']) or DOMINGO.match(y['c'])
            if m:
                ref = (m.group(1), m.group(2))
                break
        if ref:
            if d.weekday() == 6:
                x['f'] = f'{ref[0]}º domingo {ref[1]}'
            else:
                x['f'] = f'{DIAS[d.weekday()]} de la {ref[0]}ª semana {ref[1]}'
    return dias


if __name__ == '__main__':
    ruta = sys.argv[1]
    datos = json.load(open(ruta, encoding='utf-8'))
    agregar(datos['dias'])
    with open(ruta, 'w', encoding='utf-8') as f:
        json.dump(datos, f, ensure_ascii=False, separators=(',', ':'))
    for k in ['2026-11-01', '2026-11-09', '2026-11-10', '2026-11-11', '2026-11-22', '2026-12-08', '2026-12-24', '2026-12-26', '2027-12-26',
              '2026-03-19', '2026-04-02', '2026-05-31', '2026-06-04', '2026-08-15', '2027-01-06']:
        x = datos['dias'][k]
        print(k, '|', x['c'], '|', x.get('f', '—'))
    print('días con referencia:', sum('f' in x for x in datos['dias'].values()))
