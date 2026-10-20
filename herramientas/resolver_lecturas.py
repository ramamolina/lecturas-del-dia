"""Cruza el calendario (citas en bruto) con la Biblia y arma las lecturas de cada día.
Uso: python3 -I resolver_lecturas.py <biblia.json> <cal_bruto.json> <salida.json>
"""
import json
import re
import sys
import unicodedata

biblia = json.load(open(sys.argv[1], encoding='utf-8'))
dias = json.load(open(sys.argv[2], encoding='utf-8'))
salida = sys.argv[3]


def sin_tildes(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')


LIBROS = {
    'genesis': 'GENESIS', 'exodo': 'EXODO', 'levitico': 'LEVITICO', 'numeros': 'NUMEROS',
    'deuteronomio': 'DEUTERONOMIO', 'josue': 'JOSUE', 'jueces': 'JUECES', 'rut': 'RUT',
    '1 samuel': 'PRIMER LIBRO DE SAMUEL', '2 samuel': 'SEGUNDO LIBRO DE SAMUEL',
    '1 reyes': 'PRIMER LIBRO DE LOS REYES', '2 reyes': 'SEGUNDO LIBRO DE LOS REYES',
    '1 cronicas': 'PRIMER LIBRO DE LAS CRONICAS', '2 cronicas': 'SEGUNDO LIBRO DE LAS CRONICAS',
    'esdras': 'ESDRAS', 'nehemias': 'NEHEMIAS', 'tobias': 'TOBIAS', 'judit': 'JUDIT', 'ester': 'ESTER',
    '1 macabeos': 'PRIMER LIBRO DE LOS MACABEOS', '2 macabeos': 'SEGUNDO LIBRO DE LOS MACABEOS',
    'job': 'JOB', 'sal': 'SALMOS', 'salmo': 'SALMOS', 'proverbios': 'PROVERBIOS',
    'eclesiastes': 'ECLESIASTES', 'cantar': 'CANTAR DE LOS CANTARES', 'sabiduria': 'SABIDURIA',
    'eclesiastico': 'ECLESIASTICO', 'isaias': 'ISAIAS', 'jeremias': 'JEREMIAS',
    'lamentaciones': 'LAMENTACIONES', 'baruc': 'BARUC', 'ezequiel': 'EZEQUIEL', 'daniel': 'DANIEL',
    'oseas': 'OSEAS', 'joel': 'JOEL', 'amos': 'AMOS', 'abdias': 'ABDIAS', 'jonas': 'JONAS',
    'miqueas': 'MIQUEAS', 'nahum': 'NAHUM', 'habacuc': 'HABACUC', 'sofonias': 'SOFONIAS',
    'ageo': 'AGEO', 'zacarias': 'ZACARIAS', 'malaquias': 'MALAQUIAS',
    'mateo': 'EVANGELIO SEGUN SAN MATEO', 'marcos': 'EVANGELIO SEGUN SAN MARCOS',
    'lucas': 'EVANGELIO SEGUN SAN LUCAS', 'juan': 'EVANGELIO SEGUN SAN JUAN',
    'hechos': 'HECHOS DE LOS APOSTOLES', 'romanos': 'CARTA A LOS ROMANOS',
    '1 corintios': 'PRIMERA CARTA A LOS CORINTIOS', '2 corintios': 'SEGUNDA CARTA A LOS CORINTIOS',
    'galatas': 'CARTA A LOS GALATAS', 'efesios': 'CARTA A LOS EFESIOS',
    'filipenses': 'CARTA A LOS FILIPENSES', 'colosenses': 'CARTA A LOS COLOSENSES',
    '1 tesalonicenses': 'PRIMERA CARTA A LOS TESALONICENSES',
    '2 tesalonicenses': 'SEGUNDA CARTA A LOS TESALONICENSES',
    '1 timoteo': 'PRIMERA CARTA A TIMOTEO', '2 timoteo': 'SEGUNDA CARTA A TIMOTEO',
    'tito': 'CARTA A TITO', 'filemon': 'CARTA A FILEMON', 'hebreos': 'CARTA A LOS HEBREOS',
    'santiago': 'CARTA DE SANTIAGO', '1 pedro': 'PRIMERA CARTA DE SAN PEDRO',
    '2 pedro': 'SEGUNDA CARTA DE SAN PEDRO', '1 juan': 'PRIMERA CARTA DE SAN JUAN',
    '2 juan': 'SEGUNDA CARTA DE SAN JUAN', '3 juan': 'TERCERA CARTA DE SAN JUAN',
    'judas': 'CARTA DE SAN JUDAS', 'apocalipsis': 'APOCALIPSIS',
}
SUPLEMENTOS = {'DANIEL': 'DANIEL SUPLEMENTOS GRIEGOS', 'ESTER': 'ESTER SUPLEMENTOS GRIEGOS'}
NOMBRE_LECTURA = {  # cómo se lo nombra en el mensaje
    'EVANGELIO SEGUN SAN MATEO': 'Mateo', 'EVANGELIO SEGUN SAN MARCOS': 'Marcos',
    'EVANGELIO SEGUN SAN LUCAS': 'Lucas', 'EVANGELIO SEGUN SAN JUAN': 'Juan',
}
EVANGELIOS = set(NOMBRE_LECTURA)

CITA = re.compile(r'^(?P<libro>(?:[1-3] )?[A-Za-zÁÉÍÓÚáéíóúñÑ]+),?\s+(?P<resto>\d.*)$')
TITULO_SALMO = re.compile(r'^(Salmo|Del maestro|Canto|Cántico|Himno|Oración|Poema|Para |De David|De Asaf|'
                          r'De los hijos|De Salomón|De Moisés|Instrucción|Lamentación|Canción|Súplica|Plegaria|'
                          r'Alabanza|Al maestro|Con instrumentos|Según)', re.I)


def num(v):
    m = re.search(r'(\d+)', v)
    return int(m.group(1)) if m else None


def versos_de_capitulo(libro, cap):
    caps = biblia.get(libro, {})
    return caps.get(str(cap))


def rango(libro, c1, v1, c2, v2, avisos):
    """Devuelve [(cap, verso, texto)] desde c1:v1 hasta c2:v2 inclusive."""
    out = []
    for c in range(c1, c2 + 1):
        vs = versos_de_capitulo(libro, c)
        if vs is None and libro in SUPLEMENTOS:
            vs = versos_de_capitulo(SUPLEMENTOS[libro], c)
        if vs is None:
            avisos.append(f'no existe {libro} {c}')
            continue
        ini = v1 if c == c1 else 1
        fin = v2 if c == c2 else 10 ** 6
        claves = sorted((k for k in vs if num(k) is not None and ini <= num(k) <= fin), key=lambda k: (num(k), k))
        # versículos que faltan en el capítulo principal (ej. Daniel 3 griego)
        faltan = [n for n in range(ini, min(fin, max([num(k) for k in vs] or [0])) + 1)
                  if not any(num(k) == n for k in claves)]
        if (faltan or not claves) and libro in SUPLEMENTOS:
            sup = versos_de_capitulo(SUPLEMENTOS[libro], c) or {}
            extra = [k for k in sup if num(k) is not None and ini <= num(k) <= fin]
            if extra:
                vs = {**vs, **{k: sup[k] for k in extra}}
                claves = sorted((k for k in vs if num(k) is not None and ini <= num(k) <= fin), key=lambda k: (num(k), k))
        if not claves:
            avisos.append(f'sin versos {libro} {c},{ini}-{fin if fin < 10**6 else "fin"}')
        out += [(c, k, vs[k]) for k in claves]
    return out


def resolver(cita, avisos, es_salmo=False):
    """'Gálatas 4, 22-24.26-27.31—5, 1' -> (libro, [(c, v, texto)])"""
    cita = cita.replace('–', '—').strip().rstrip('.,')
    if es_salmo:
        m = re.match(r'^(?:S\.R\.|Sal\.?)\s*(\d+)\s*[A-Z]?\s*(?:\((\d+)\s*[A-Z]?\))?\s*,?\s*(.*)$', cita)
        if not m:
            avisos.append('salmo no entendido: ' + cita)
            return None, []
        libro, resto = 'SALMOS', f'{m.group(2) or m.group(1)}, {m.group(3)}'
        # un segundo salmo encadenado: "3.5bcd; 42 (43), 3-4"
        resto = re.sub(r';\s*\d+\s*[A-Z]?\s*\((\d+)\s*[A-Z]?\)', r'; \1', resto)
    else:
        m = CITA.match(cita)
        if not m:
            avisos.append('cita no entendida: ' + cita)
            return None, []
        clave = sin_tildes(m.group('libro')).lower()
        libro = LIBROS.get(clave)
        if not libro:
            avisos.append('libro desconocido: ' + m.group('libro'))
            return None, []
        resto = m.group('resto')
    resto = re.sub(r'\s+y\s+', '.', resto)
    versos = []
    cap = None
    for grupo in [g.strip() for g in resto.split(';') if g.strip()]:
        mg = re.match(r'^(\d+)\s*,\s*(.*)$', grupo)
        if mg:
            cap, partes = int(mg.group(1)), mg.group(2)
        else:
            partes = grupo
        if cap is None:
            avisos.append('sin capítulo: ' + cita)
            return libro, []
        for parte in [p.strip() for p in partes.split('.') if p.strip()]:
            if '—' in parte:  # cruza capítulos: "31—5, 1"
                a, b = [x.strip() for x in parte.split('—', 1)]
                va = num(a.split('-')[0])
                mb = re.match(r'^(\d+)\s*,\s*(\d+)', b)
                if mb:
                    c2, v2 = int(mb.group(1)), int(mb.group(2))
                else:
                    c2, v2 = cap, num(b)
                versos += rango(libro, cap, va, c2, v2, avisos)
                cap = c2
            elif '-' in parte:
                a, b = parte.split('-', 1)
                if num(a) is None or num(b) is None:
                    avisos.append('rango raro: ' + parte + ' en ' + cita)
                    continue
                versos += rango(libro, cap, num(a), cap, num(b), avisos)
            else:
                n = num(parte)
                if n is None:
                    avisos.append('verso raro: ' + parte + ' en ' + cita)
                    continue
                versos += rango(libro, cap, n, cap, n, avisos)
    # quitar repetidos manteniendo el orden
    vistos, unicos = set(), []
    for v in versos:
        if (v[0], v[1]) not in vistos:
            vistos.add((v[0], v[1]))
            unicos.append(v)
    return libro, unicos


def texto(libro, versos, es_salmo):
    trozos = []
    for _, _, t in versos:
        if es_salmo:
            lineas = t.split('\n')
            if len(lineas) > 1 and TITULO_SALMO.match(lineas[0]):
                lineas = lineas[1:]
            elif len(lineas) == 1 and TITULO_SALMO.match(lineas[0]) and len(lineas[0]) < 200:
                continue  # verso que es solo el título del salmo
            trozos.append(re.sub(r'\[\s*\w+\s*\]\s*', '', '\n'.join(lineas)))
        else:
            trozos.append(t.replace('\n', ' '))
    return ('\n' if es_salmo else ' ').join(trozos).strip()


PREFIJOS = re.compile(r'^(Lecturas(?: optativas| \(AT\)| \(NT\))?:|o de la feria:|Evangelio propio:|'
                      r'Evangelio \(Pasión\):|Evangelio:|Noche:|Aurora:|Día:|[1-7]ª)\s*')
TIENE_CITA = re.compile(r'\d+\s*(?:[A-Z]\s*)?(?:\(\d+[^)]*\)\s*,?|,)\s*\d')


def clasificar(lineas):
    """Convierte las líneas en una lista de items: grupo, es_salmo, cita."""
    items, grupo = [], 'comun'
    for l in lineas:
        resto = l.lstrip(': ')
        if re.match(r'^(o bien|y en las)', resto) or '(Entrada)' in resto:
            continue  # alternativas y el evangelio de la procesión de Ramos no van
        if resto.startswith('Lecturas optativas de la memoria') and items:
            grupo = 'descartar'  # lecturas propias de una memoria libre: se usan las de la feria
        elif resto.startswith('Lecturas optativas'):
            grupo = 'optativa'
        resto = re.sub(r'^(Lecturas optativas de la memoria|Lecturas propias|Salmo|lectura|Lectura)\s*:\s*', '', resto)
        while True:
            m = PREFIJOS.match(resto)
            if not m:
                break
            p = m.group(1)
            if p.startswith('Lecturas optativas'):
                grupo = 'optativa'
            elif p.startswith('o de la feria'):
                grupo = 'feria'
            elif p.startswith('Evangelio propio'):
                grupo = 'propio'
            elif p in ('Noche:', 'Aurora:', 'Día:'):
                grupo = p[:-1].lower()
            resto = resto[m.end():]
        resto = re.sub(r'^(lectura|Lectura|Salmo)\s*:\s*', '', resto.strip())
        # libros de un solo capítulo se citan sin capítulo: 'Judas 17.20b-25'
        resto = re.sub(r'^(Judas|Filemón|Filemon|2 Juan|3 Juan|Abdías|Abdias)\s+(\d+[^,]*)$', r'\1 1, \2', resto)
        if not TIENE_CITA.search(resto):
            continue
        primera = re.split(r'\s+o bien\s+|,?\s+y en las Misas', resto)[0].strip()
        es_salmo = primera.startswith(('S.R.', 'Sal ', 'Sal.'))
        es_cantico = primera.startswith('C.R.')
        if es_cantico:
            primera = primera[4:].lstrip(': ').strip()
        items.append({'grupo': grupo, 'salmo': es_salmo or es_cantico, 'cantico': es_cantico,
                      'cita': primera, 'alternativas': resto != primera})
    return items


def elegir(items, revisar):
    if any(i['grupo'] == 'descartar' for i in items):
        revisar.append('memoria libre con lecturas propias: se usan las de la feria')
        items = [i for i in items if i['grupo'] != 'descartar']
    grupos = {i['grupo'] for i in items}
    if 'día' in grupos:
        revisar.append('hay varias misas (noche/aurora/día): se usa la del día')
        return [i for i in items if i['grupo'] == 'día']
    if 'feria' in grupos:
        elegidos = [i for i in items if i['grupo'] == 'feria']
        propio = [i for i in items if i['grupo'] == 'propio']
        if propio:
            elegidos = [i for i in elegidos if not (LIBROS.get(sin_tildes(i['cita'].split(' ')[0]).lower()) in EVANGELIOS)]
            elegidos += propio
        revisar.append('memoria con lecturas propias optativas: se usan las de la feria')
        return elegidos
    return items


def citar(item):
    return ('Cántico: ' if item['cantico'] else '') + item['cita']


resultado = {}
total_avisos = 0
for d in dias:
    revisar, avisos = [], []
    bloques = [b for b in d['bloques'] if b['lecturas']]
    if not bloques:
        resultado[d['fecha']] = {'titulo': d['titulo'], 'lecturas': [], 'revisar': ['día sin misa (ej. Sábado Santo)']}
        continue
    if len(bloques) > 1:
        preferido = [b for b in bloques if any(k in ' '.join(b['encabezado']) for k in ('MISA DEL DÍA', 'CENA DEL SEÑOR'))]
        bloque = preferido[0] if preferido else bloques[0]
        revisar.append('el día tiene más de una misa; se eligió: ' + (' / '.join(bloque['encabezado']) or 'la primera'))
    else:
        bloque = bloques[0]
    items = elegir(clasificar(bloque['lecturas']), revisar)
    lecturas = []
    for it in items:
        if it['alternativas']:
            revisar.append('hay lectura alternativa ("o bien"): se usa la primera — ' + it['cita'])
        libro, versos = resolver(('S.R. ' if it['salmo'] and not it['cantico'] and not it['cita'].startswith(('S.R.', 'Sal')) else '') + it['cita'],
                                 avisos, es_salmo=it['salmo'] and not it['cantico'])
        if it['cantico']:
            libro, versos = resolver(it['cita'], avisos)
        if not versos:
            continue
        lecturas.append({'cita': citar(it), 'libro': libro, 'salmo': it['salmo'],
                         'texto': texto(libro, versos, it['salmo'])})
    # rol de cada lectura
    no_salmos = [l for l in lecturas if not l['salmo']]
    for l in lecturas:
        if l['salmo']:
            l['rol'] = 'Salmo' if not l['cita'].startswith('Cántico') else 'Cántico'
        elif l is no_salmos[-1] and l['libro'] in EVANGELIOS:
            l['rol'] = 'Evangelio'
        else:
            n = no_salmos.index(l) + 1
            l['rol'] = 'Primera lectura' if n == 1 else 'Segunda lectura' if n == 2 else f'Lectura {n}'
    if not any(l['rol'] == 'Evangelio' for l in lecturas):
        revisar.append('no se encontró Evangelio')
    total_avisos += len(avisos)
    resultado[d['fecha']] = {'titulo': d['titulo'], 'lecturas': lecturas, 'revisar': revisar, 'errores': avisos}

json.dump(resultado, open(salida, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('dias:', len(resultado), 'errores de cita:', total_avisos)
print('dias a revisar:', sum(1 for r in resultado.values() if r['revisar']))
for f, r in resultado.items():
    if r.get('errores'):
        print(f, r['errores'])
