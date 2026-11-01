import email, sys, html, re
from email import policy
m = email.message_from_binary_file(open(sys.argv[1],'rb'), policy=policy.default)
for part in m.walk():
    if part.get_content_type()=='text/html':
        h = part.get_payload(decode=True).decode('utf-8'); break
pre = re.search(r'<pre[^>]*>(.*?)</pre>', h, re.S)
t = html.unescape(re.sub(r'<[^>]+>','', pre.group(1)))
open(sys.argv[2],'w').write(t)
print(len(t))
