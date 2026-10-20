import re, sys, time, os, subprocess
d = sys.argv[1]
idx = open(os.path.join(d, '_INDEX.HTM'), encoding='latin-1').read()
links = []
for m in re.finditer(r'href="?(__P[0-9A-Z]+\.HTM)', idx, re.I):
    if m.group(1) not in links:
        links.append(m.group(1))
print('paginas:', len(links), flush=True)
fallas = []
for i, l in enumerate(links):
    dest = os.path.join(d, 'cap', l)
    if os.path.exists(dest) and os.path.getsize(dest) > 500:
        continue
    r = subprocess.run(['curl','-sS','-m','30','--retry','3','-o',dest,'-w','%{http_code}',
                        'https://www.vatican.va/archive/ESL0506/'+l], capture_output=True, text=True)
    if r.stdout != '200':
        fallas.append((l, r.stdout, r.stderr.strip()))
    if i % 100 == 0:
        print(i, flush=True)
    time.sleep(0.25)
print('fallas:', fallas, flush=True)
