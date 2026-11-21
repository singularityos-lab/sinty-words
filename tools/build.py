import sys, collections, unicodedata

ELIDING = {
    "it": {"l", "un", "dell", "nell", "all", "dall", "sull", "quell", "bell", "c", "d", "m", "t", "s", "v", "n", "anch", "com", "dov", "quand", "cos", "tutt", "buon", "sant", "mezz", "dev", "senz"},
    "fr": {"l", "d", "j", "m", "t", "s", "c", "n", "qu", "lorsqu", "puisqu", "jusqu", "quoiqu", "presqu", "quelqu", "aujourd"},
}
KEEP = {"it": {"c'è", "po'"}, "fr": {"aujourd'hui", "quelqu'un", "presqu'île"}}

lang, src, out = sys.argv[1], sys.argv[2], sys.argv[3]
limit = int(sys.argv[4]) if len(sys.argv) > 4 else 50000
def fold(text):
    return "".join(c for c in unicodedata.normalize("NFD", text) if not unicodedata.combining(c))


def plain_case(form):
    return form.islower() or form.isupper() or form[:1].isupper() and form[1:].islower()


counts = collections.Counter()
form_counts = collections.defaultdict(collections.Counter)
for line in open(src, encoding="utf-8"):
    word, count = line.rstrip("\n").split("\t")
    count = int(count)
    parts = [word]
    if "'" in word and word.lower() not in KEEP.get(lang, ()):
        head, _, tail = word.partition("'")
        if head.lower() in ELIDING.get(lang, ()) and tail:
            parts = [head + "'", tail]
        elif lang in ELIDING:
            continue
    for part in parts:
        if "-" in part.strip("-") or not plain_case(part.replace("'", "")):
            continue
        key = part.lower()
        counts[key] += count
        form_counts[key][part] += count

strongest = collections.Counter()
for key, count in counts.items():
    folded = fold(key)
    strongest[folded] = max(strongest[folded], count)

with open(out, "w", encoding="utf-8") as f:
    written = 0
    for key, count in counts.most_common():
        if count < 5 or written == limit:
            break
        top = strongest[fold(key)]
        if count * 20 < top or key == fold(key) and len(key) >= 5 and count * 3 < top * 2:
            continue
        forms = form_counts[key]
        form = key if forms[key] * 4 >= max(forms.values()) else forms.most_common(1)[0][0]
        f.write(f"{form}\t{count}\n")
        written += 1
