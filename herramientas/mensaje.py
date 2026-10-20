import json, re, sys, datetime
r = json.load(open(sys.argv[1], encoding='utf-8'))
fecha = sys.argv[2]
x = r[fecha]
d = datetime.date.fromisoformat(fecha)
DIAS = ['lunes','martes','miércoles','jueves','viernes','sábado','domingo']
MESES = ['enero','febrero','marzo','abril','mayo','junio','julio','agosto','septiembre','octubre','noviembre','diciembre']
cab = f"*Lecturas del {DIAS[d.weekday()]} {d.day} de {MESES[d.month-1]} de {d.year}*"
cel = re.sub(r'\s*\((Verde|Blanco|Rojo|Morado|Rosa)\)', '', x['titulo'][0]) if x['titulo'] else ''
out = [cab, f"_{cel}_", '']
for l in x['lecturas']:
    cita = l['cita'].replace('S.R. ', 'Salmo ').replace('Cántico: ', '')
    out += [f"*{l['rol']}* — {cita}", l['texto'], '']
print('\n'.join(out).strip())
