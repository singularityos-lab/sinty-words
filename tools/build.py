import sys, collections

ELIDING = {
    "it": {"l", "un", "dell", "nell", "all", "dall", "sull", "quell", "bell", "c", "d", "m", "t", "s", "v", "n", "anch", "com", "dov", "quand", "cos", "tutt", "buon", "sant", "mezz", "dev", "senz"},
    "fr": {"l", "d", "j", "m", "t", "s", "c", "n", "qu", "lorsqu", "puisqu", "jusqu", "quoiqu", "presqu", "quelqu", "aujourd"},
}
KEEP = {"it": {"c'è", "po'"}, "fr": {"aujourd'hui", "quelqu'un", "presqu'île"}}

lang, src, out = sys.argv[1], sys.argv[2], sys.argv[3]
limit = int(sys.argv[4]) if len(sys.argv) > 4 else 50000
counts = collections.Counter()
forms = {}
for line in open(src, encoding="utf-8"):
    word, count = line.rstrip("\n").split("\t")
    count = int(count)
    parts = [word]
    if "'" in word and word.lower() not in KEEP.get(lang, ()):
        head, _, tail = word.partition("'")
        if head.lower() in ELIDING.get(lang, ()) and tail:
            parts = [head + "'", tail]
    for part in parts:
        key = part.lower()
        counts[key] += count
        forms.setdefault(key, part)
with open(out, "w", encoding="utf-8") as f:
    for key, count in counts.most_common(limit):
        if count < 5:
            break
        f.write(f"{forms[key]}\t{count}\n")
