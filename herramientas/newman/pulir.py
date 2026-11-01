import re, sys
def pulir(p):
    p = re.sub(r'\s*\b[\dIOl*]{2,3}[§S;]?\s+(ON CHRISTIAN DOCTRINE|SHORT MEDITATIONS ON THE|STATIONS OF THE CROSS|MEDITATIONS AND INTERCESSIONS|HOPE IN GOD[^a-z]*REDEEMER)\b\s*', ' ', p)
    p = re.sub(r'\s*\b(ON CHRISTIAN DOCTRINE|STATIONS OF THE CROSS)\s+[\dIOl ]{2,4}\b\s*', ' ', p)
    p = re.sub(r'\bGoogle\s*', '', p)
    p = re.sub(r'\s+([;:?!,.])', r'\1', p)
    p = re.sub(r'([‘“])\s+', r'\1', p)
    p = re.sub(r"/(?=\s|$)", '’', p)
    p = re.sub(r"(?<=\w)'(?=\w)", '’', p)
    p = re.sub(r"(^|\s)'", r'\1‘', p)
    p = re.sub(r"'(?=[\s.,;:!?]|$)", '’', p)
    p = re.sub(r'\s{2,}', ' ', p).strip()
    return p
DROP = re.compile(r'^(V\.|[IlR][}j]?\?|ty\.|I}\?|Ij\?|R\.|Pater, Ave|Fidelium|Begin with|\d+\s+Written|o \d|Google$)')
if __name__ == '__main__':
    ps = [x for x in open(sys.argv[1]).read().split('\n\n') if x.strip()]
    out = []
    for x in ps:
        x = pulir(x)
        if DROP.match(x) or not x or re.match(r'^[\\*\d\s.]{1,5}$', x): continue
        if out and out[-1].endswith('-') and re.match(r'[a-z]', x):
            out[-1] = out[-1][:-1] + x; continue
        if out and not re.search(r'[.!?:;’”—)]$', out[-1]) and re.match(r'^[a-z]', x):
            out[-1] = out[-1] + ' ' + x; continue
        out.append(x)
    open(sys.argv[2], 'w').write('\n\n'.join(out) + '\n')
