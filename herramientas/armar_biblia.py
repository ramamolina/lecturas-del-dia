"""Convierte las páginas del Vaticano (El Libro del Pueblo de Dios) en un JSON:
{ "LIBRO": { "capitulo": { "versiculo": "texto" } } }
Uso: python3 -I armar_biblia.py <carpeta_cap> <salida.json>
"""
import glob
import html
import json
import os
import re
import sys

carpeta, salida = sys.argv[1], sys.argv[2]

PARRAFO = re.compile(r'<p class=(\w+)[^>]*>(.*?)</p>', re.S | re.I)
VERS = re.compile(r'^(\d+)([a-z]?)\s+(.*)$', re.S)


def limpiar(fragmento):
    t = re.sub(r'<[^>]+>', ' ', fragmento)
    t = html.unescape(t)
    t = t.replace('\xa0', ' ')
    return re.sub(r'\s+', ' ', t).strip()


biblia = {}
avisos = []
for f in sorted(glob.glob(os.path.join(carpeta, '*.HTM'))):
    s = open(f, encoding='latin-1').read()
    m = re.search(r'<meta name="part" content="([^"]+)"', s)
    if not m:
        avisos.append((os.path.basename(f), 'sin meta part'))
        continue
    partes = [p.strip() for p in html.unescape(m.group(1)).split('>')]
    # ["El Antiguo Testamento", "LIBRO", "capítulo"] o sin capítulo si el libro tiene uno solo
    libro = partes[1] if len(partes) > 1 else partes[0]
    cap = partes[2] if len(partes) > 2 else '1'
    if not cap.isdigit():
        avisos.append((os.path.basename(f), 'capitulo raro: ' + cap))
    versiculos = biblia.setdefault(libro, {}).setdefault(cap, {})
    actual = None
    for clase, contenido in PARRAFO.findall(s):
        if clase != 'MsoNormal':
            continue  # títulos de libro, capítulo y subtítulos no van
        texto = limpiar(contenido)
        if not texto:
            continue
        mv = VERS.match(texto)
        if mv:
            actual = mv.group(1) + mv.group(2)
            versiculos[actual] = mv.group(3)
        elif actual is not None:
            # continuación (verso poético o párrafo partido): nueva línea
            versiculos[actual] += '\n' + texto
        else:
            avisos.append((os.path.basename(f), 'texto antes del v1: ' + texto[:60]))

json.dump(biblia, open(salida, 'w', encoding='utf-8'), ensure_ascii=False)
total = sum(len(v) for c in biblia.values() for v in c.values())
print('libros:', len(biblia), 'capitulos:', sum(len(c) for c in biblia.values()), 'versiculos:', total)
print('avisos:', len(avisos))
for a in avisos[:40]:
    print(' ', a)
