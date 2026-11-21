# sinty-words

Word lists with frequencies for the Sinty OS on-screen keyboard: word completion, corrections and swipe typing.

| File | Language |
| --- | --- |
| `data/en.words` | English |
| `data/it.words` | Italian |
| `data/de.words` | German |
| `data/fr.words` | French |
| `data/es.words` | Spanish |
| `data/pt_BR.words` | Brazilian Portuguese |

Each line is `word<TAB>count`, most frequent first, 50,000 words per language. Words keep their usual capitalisation (`Haus`, `I`) and their apostrophes (`don't`, `c'è`). Italian and French elisions are split the way they are typed (`l'` and `acqua`).

## Source

The counts come from the first eight million subtitle lines of each language in OpenSubtitles2018 (http://www.opensubtitles.org/), as distributed by OPUS:

P. Lison and J. Tiedemann, 2016. OpenSubtitles2016: Extracting Large Parallel Corpora from Movie and TV Subtitles. In Proceedings of the 10th International Conference on Language Resources and Evaluation (LREC 2016).

Capitalisation is the most frequent form of a word away from the start of a sentence.

## Regenerating

```
tools/generate.sh
```

It streams each corpus, counts with `tools/count.py` and writes the lists with `tools/build.py`. It needs `curl`, `gzip` and Python 3.

## License

The word lists are released under the Creative Commons Attribution-ShareAlike 4.0 International license (https://creativecommons.org/licenses/by-sa/4.0/). The scripts in `tools/` are under the MIT license. See `LICENSE`.
