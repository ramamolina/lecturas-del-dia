"""Arma el archivo de datos que usa la app a partir de lecturasAAAA.json.
Uso: python3 -I datos_app.py <lecturas.json> [<lecturas2.json> ...] <salida.json>
"""
import datetime
import json
import re
import sys

entradas, salida = sys.argv[1:-1], sys.argv[-1]
DIAS = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
CHICAS = {'de', 'del', 'la', 'las', 'los', 'el', 'y', 'e', 'en', 'a', 'al', 'o'}
COLOR = re.compile(r'\s*\((?:[Vv]erde|[Bb]lanco|[Rr]ojo|[Mm]orado|[Rr]osad?o|Morado o Rosado|morado)\)|\s+Rojo$')
TIEMPOS = {'DURANTE EL AÑO': 'durante el año', 'DE CUARESMA': 'de Cuaresma', 'DE PASCUA': 'de Pascua',
           'DE ADVIENTO': 'de Adviento'}


def limpio(t):
    return COLOR.sub('', t).strip()


def titulo_mayus(t):
    """'SAN PEDRO Y SAN PABLO, APÓSTOLES' -> 'San Pedro y San Pablo, Apóstoles'"""
    if t != t.upper():
        return t
    palabras = t.lower().split(' ')
    return ' '.join(p if (i and p in CHICAS) else p[:1].upper() + p[1:] for i, p in enumerate(palabras))


def cristo_rey(anio):
    """Domingo de Jesucristo Rey: el anterior al 1º de Adviento (34º semana durante el año)."""
    navidad = datetime.date(anio, 12, 25)
    adviento4 = navidad - datetime.timedelta(days=(navidad.weekday() + 1) % 7 or 7)
    return adviento4 - datetime.timedelta(days=28)


def ciclo(d):
    """Ciclo dominical: el año litúrgico empieza el 1º domingo de Adviento.
    Año litúrgico que termina en un año con resto 1 al dividir por 3 → A, 2 → B, 0 → C."""
    adviento1 = cristo_rey(d.year) + datetime.timedelta(days=7)
    anio_lit = d.year + 1 if d >= adviento1 else d.year
    return {1: 'A', 2: 'B', 0: 'C'}[anio_lit % 3]


def es_nombre(t):
    return t and not re.match(r'^(Por la|A partir|Este año|Hoy|Lecturas|Misa)', t)


r = {}
for e in entradas:
    r.update(json.load(open(e, encoding='utf-8')))

dias = {}
semana = None  # (número, tiempo) del último domingo reconocido
for fecha in sorted(r):
    x = r[fecha]
    d = datetime.date.fromisoformat(fecha)
    dia = DIAS[d.weekday()]
    t = [limpio(s) for s in x['titulo'] if limpio(s)]
    t0 = t[0] if t else ''
    resto = [s for s in t[1:] if es_nombre(s)]
    memorias = []
    m_dom = re.match(r'^(\d+)º (DURANTE EL AÑO|DE CUARESMA|DE PASCUA|DE ADVIENTO)$', t0)
    if d.weekday() == 6:
        if m_dom:
            semana = (int(m_dom.group(1)), TIEMPOS[m_dom.group(2)])
        elif 'BAUTISMO' in ' '.join(t).upper():
            semana = (1, 'durante el año')  # tras el Bautismo del Señor empieza la 1ª semana
        elif semana and semana[1] == 'de Pascua' and 'PENTECOST' in ' '.join(t).upper():
            semana = (34 - (cristo_rey(d.year) - d).days // 7, 'durante el año')
        elif re.search(r'(\d+)º DOMINGO DE PASCUA', ' '.join(t)):
            semana = (int(re.search(r'(\d+)º DOMINGO DE PASCUA', ' '.join(t)).group(1)), 'de Pascua')
        elif semana:
            semana = (semana[0] + 1, semana[1])  # domingo ocupado por una solemnidad (ej. Ascensión, Trinidad)
        else:
            semana = None
    if m_dom:
        nombre = f'{m_dom.group(1)}º domingo {TIEMPOS[m_dom.group(2)]}'
    elif t0 == 'SANTO':
        nombre = f'{dia} Santo'
    elif t0 == 'DE CENIZA':
        nombre = 'Miércoles de Ceniza'
    elif t0 == 'DE LA OCTAVA DE PASCUA':
        nombre = f'{dia} de la Octava de Pascua'
    elif t0.startswith('Feria'):
        if t0.startswith('Feria después de Ceniza'):
            nombre = f'{dia} después de Ceniza'
        elif semana:
            nombre = f'{dia} de la {semana[0]}ª semana {semana[1]}'
        elif d.month == 1 and d.day >= 7:
            nombre = f'{dia} después de Epifanía'
        elif d.month in (1, 12):
            nombre = f'{dia} del tiempo de Navidad'
        else:
            nombre = f'{dia} (feria)'
        memorias = [titulo_mayus(s.strip('[] ')) for s in resto]
    elif t0 in ('Memoria obligatoria', 'Fiesta', 'Solemnidad', 'Solemnidad con Octava', 'Morado o Negro',
                'Octava de la Natividad del Señor', 'Octava de Pascua') and resto:
        nombre = titulo_mayus(resto[0])
    elif t0.isupper():
        nombre = titulo_mayus(t0)
    else:
        nombre = t0
    lecturas = []
    for l in x['lecturas']:
        cita = l['cita'].replace('S.R. ', 'Salmo ').replace('Cántico: ', '')
        cita = re.sub(r'\s+', ' ', cita).strip()
        txt = re.sub(r'\[\s*[A-ZÁÉÍÓÚ][a-záéíóú]{1,7}\s*\]\s*', '', l['texto'])  # letras hebreas de acrósticos
        txt = re.sub(r'_\d+[a-z]?\s*', '', txt)  # marcas de medio versículo
        txt = txt.replace('[', '').replace(']', '')
        txt = re.sub(r'[ \t]+', ' ', txt).replace(' \n', '\n').strip()
        lecturas.append([l['rol'], cita, txt])
    todo = ' '.join(x['titulo'])
    if 'Rosado' in todo:
        color = 'rosa'
    elif nombre == 'Jueves Santo':
        color = 'blanco'  # se toma la Misa de la Cena del Señor
    else:
        mc = re.search(r'(Verde|Blanco|Rojo|Morado|morado)', todo)
        color = mc.group(1).lower() if mc else ('morado' if nombre == 'Sábado Santo' else 'verde')
    dias[fecha] = {'c': nombre, 'k': color, 'm': memorias, 'l': lecturas}
    if d.weekday() == 6:
        dias[fecha]['y'] = ciclo(d)  # ciclo dominical A, B o C

datos = {
    'desde': min(dias), 'hasta': max(dias),
    'dias': dias,
}
with open(salida, 'w', encoding='utf-8') as f:
    json.dump(datos, f, ensure_ascii=False, separators=(',', ':'))

for f in ['2026-01-01', '2026-02-18', '2026-02-19', '2026-03-29', '2026-04-02', '2026-04-04', '2026-04-06',
          '2026-05-24', '2026-05-25', '2026-10-02', '2026-10-17', '2026-10-18', '2026-10-19', '2026-11-02',
          '2026-12-24', '2026-12-25', '2026-12-29']:
    print(f, '|', dias[f]['c'], '|', dias[f]['m'], '|', [l[0] + ': ' + l[1] for l in dias[f]['l']])
