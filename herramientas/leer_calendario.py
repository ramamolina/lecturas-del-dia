"""Lee el texto del Calendario litúrgico CEA (pdftotext -layout) y arma, por fecha,
la celebración y las lecturas en bruto.
Uso: python3 -I leer_calendario.py <cal.txt> <año> <salida.json>
"""
import json
import re
import sys

ruta, anio, salida = sys.argv[1], int(sys.argv[2]), sys.argv[3]
MESES = ['ENERO', 'FEBRERO', 'MARZO', 'ABRIL', 'MAYO', 'JUNIO', 'JULIO', 'AGOSTO',
         'SEPTIEMBRE', 'OCTUBRE', 'NOVIEMBRE', 'DICIEMBRE']
DIA = re.compile(r'^(\d{1,2}) (LUNES|MARTES|MIÉRCOLES|JUEVES|VIERNES|SÁBADO|DOMINGO)\b(.*)$')
FIN_LECTURAS = re.compile(r'^(L\. de las Horas|Misa vespertina|Misa matutina|Misa:|Celebración:|Este año|Hoy )')

lineas = open(ruta, encoding='utf-8').read().split('\n')
mes = 1  # el PDF arranca enero sin encabezado de mes
dias = []
actual = None
en_lecturas = False
ignorar = False

for crudo in lineas:
    linea = crudo.strip()
    if linea in MESES:
        mes = MESES.index(linea) + 1
        continue
    m = DIA.match(linea)
    if m and mes:
        num = int(m.group(1))
        fecha = f'{anio}-{mes:02d}-{num:02d}'
        # el 24/12 aparece dos veces (mañana y Navidad vigilia): se agrega como otro bloque
        if actual and actual['fecha'] == fecha:
            actual['bloques'].append({'encabezado': [m.group(3).strip()] if m.group(3).strip() else [], 'lecturas': []})
        else:
            actual = {'fecha': fecha, 'titulo': [m.group(3).strip()] if m.group(3).strip() else [],
                      'bloques': [{'encabezado': [], 'lecturas': []}]}
            dias.append(actual)
        en_lecturas = False
        ignorar = False
        continue
    if not actual or not linea:
        continue
    if 'puede celebrarse' in linea:
        ignorar = True  # misa opcional extra (ej. Santa María junto a la cruz): no va
    if ignorar:
        continue
    if en_lecturas and re.match(r'^(DOMINGO DE PASCUA|MISA |NATIVIDAD|Por la )', linea):
        actual['bloques'].append({'encabezado': [linea], 'lecturas': []})
        en_lecturas = False
        continue
    if linea.startswith('Lecturas') or linea.startswith('. Lecturas') or linea.startswith('.') and 'Lecturas' in linea:
        en_lecturas = True
    if en_lecturas:
        if FIN_LECTURAS.match(linea.lstrip('. ')):
            en_lecturas = False
        else:
            actual['bloques'][-1]['lecturas'].append(linea.lstrip('. ').strip())
            continue
    # encabezados: nombres de misas dentro del día (Por la mañana:, MISA CRISMAL, Noche:, etc.)
    if re.match(r'^(Por la|A partir|MISA|DOMINGO DE PASCUA|ACCIÓN|NATIVIDAD|Misa del día)', linea) and actual['bloques'][-1]['lecturas']:
        actual['bloques'].append({'encabezado': [linea], 'lecturas': []})
    elif not actual['bloques'][-1]['lecturas'] and not linea.startswith(('Misa', 'Celebración', 'L. de')):
        if len(actual['bloques']) == 1:
            actual['titulo'].append(linea)
        else:
            actual['bloques'][-1]['encabezado'].append(linea)

json.dump(dias, open(salida, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('dias:', len(dias), 'primero:', dias[0]['fecha'], 'ultimo:', dias[-1]['fecha'])
sin = [d['fecha'] for d in dias if not any(b['lecturas'] for b in d['bloques'])]
print('dias sin lecturas:', sin)
