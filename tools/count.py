import sys, re, collections, html
lang, limit, out = sys.argv[1], int(sys.argv[2]), sys.argv[3]
word = re.compile(r"[^\W\d_]+(?:['\-][^\W\d_]+)*")
total = collections.Counter()
forms = collections.defaultdict(collections.Counter)
n = 0
for raw in sys.stdin.buffer:
    n += 1
    if n > limit: break
    line = html.unescape(raw.decode('utf-8', 'replace')).replace('’', "'").replace('‘', "'")
    start = True
    pos = 0
    for m in word.finditer(line):
        gap = line[pos:m.start()]
        if any(c in gap for c in '.!?'): start = True
        w = m.group(0)
        if len(w) > 24: start = False; pos = m.end(); continue
        k = w.lower()
        total[k] += 1
        if not start: forms[k][w] += 1
        start = False
        pos = m.end()
with open(out, 'w') as f:
    for k, c in total.most_common():
        if c < 3: break
        best = forms[k].most_common(1)[0][0] if forms[k] else k
        f.write(f"{best}\t{c}\n")
print(lang, n, len(total), file=sys.stderr)
