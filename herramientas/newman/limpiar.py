import re, sys
JUNK = [r'^\s*Digitized\s+by', r'^\s*\d[\d ]*\s*$', r'^\s*[oO0]\s*\d*\s*$', r'^\s*[IVXLCivxl]{1,6}\s*$']
def limpiar(lineas, cabeceras):
    """lineas: texto crudo; cabeceras: regex de títulos corridos de página."""
    out = []
    for l in lineas:
        s = l.rstrip('\n')
        t = s.strip()
        if any(re.search(j, s) for j in JUNK): out.append(''); continue
        if re.match(r'^\s*[\'‘]?\s*(\d[\d ]{0,3}\s+)?(' + cabeceras + r')(\s+[\dIl;/ ]{1,5})?\s*[,;\']?\s*$', s): out.append(''); continue
        out.append(re.sub(r'\s{2,}', ' ', t))
    # bloques = párrafos provisorios
    bloques, cur = [], []
    for l in out:
        if l == '':
            if cur: bloques.append(cur); cur = []
        else: cur.append(l)
    if cur: bloques.append(cur)
    def unir(ls):
        txt = ''
        for l in ls:
            if txt.endswith('-') and re.match(r'[a-z]', l): txt = txt[:-1] + l
            elif txt: txt += ' ' + l
            else: txt = l
        return txt
    pars = [unir(b) for b in bloques]
    # unir párrafos cortados por salto de página
    res = []
    for p in pars:
        if res and not re.search(r'[.!?:;’”\'"—)]$', res[-1]) and re.match(r'^[a-z(‘\'“]', p):
            prev = res.pop()
            p = (prev[:-1] + p) if prev.endswith('-') else prev + ' ' + p
        res.append(p)
    return res
if __name__ == '__main__':
    a, b = int(sys.argv[2]), int(sys.argv[3])
    lin = open(sys.argv[1]).read().split('\n')[a-1:b]
    for p in limpiar(lin, sys.argv[4]): print(p + '\n')
