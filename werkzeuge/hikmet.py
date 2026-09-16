#!/usr/bin/env python3
"""
Werkzeug fuer die Koran-Untersuchung nach der Hikmet-Methode.

Deckt die mechanisch pruefbaren Schritte der Methode ab:
  Schritt 1 (Wortlaut)    -> sura
  Schritt 3 (Begriffe)    -> sura, wurzel
  Schritt 4 (Querbezuege) -> wurzel
  Schritt 8 (Gegenprobe)  -> zaehle

Die Deutungsschritte 2, 5, 6, 7 macht dieses Programm absichtlich nicht.
Sie brauchen Urteil, nicht Statistik.

Datengrundlage: Quranic Arabic Corpus (Morphologie), Text nach Uthmani,
deutsche Uebersetzungen von Bubenheim/Elyas und Khoury.
"""

import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

DATEN = Path(__file__).resolve().parent.parent / "daten"

SUREN_NAMEN = {}  # wird aus den Daten nicht geliefert; nur Nummern werden benutzt


def lade_morphologie():
    """Liest das Morphologie-Korpus. Gibt eine Liste von Segment-Datensaetzen zurueck."""
    eintraege = []
    with open(DATEN / "morphologie.txt", encoding="utf-8") as f:
        for zeile in f:
            zeile = zeile.rstrip("\n")
            if not zeile.strip():
                continue
            teile = zeile.split("\t")
            if len(teile) < 4:
                continue
            ort, form, pos, merkmale = teile[0], teile[1], teile[2], teile[3]
            s, v, w, seg = (int(x) for x in ort.split(":"))
            wurzel = re.search(r"ROOT:([^|]+)", merkmale)
            lemma = re.search(r"LEM:([^|]+)", merkmale)
            eintraege.append({
                "sura": s, "vers": v, "wort": w, "segment": seg,
                "form": form, "pos": pos, "merkmale": merkmale,
                "wurzel": wurzel.group(1) if wurzel else None,
                "lemma": lemma.group(1) if lemma else None,
            })
    return eintraege


def lade_text(datei):
    """Liest eine Text-Edition als dict {(sura, vers): text}."""
    with open(DATEN / datei, encoding="utf-8") as f:
        daten = json.load(f)
    return {(v["chapter"], v["verse"]): v["text"] for v in daten["quran"]}


class Korpus:
    def __init__(self):
        self.morph = lade_morphologie()
        self.arabisch = lade_text("ara-uthmani.json")
        self.bubenheim = lade_text("de-bubenheim.json")
        self.khoury = lade_text("de-khoury.json")

        self.wurzel_orte = defaultdict(list)   # wurzel -> [(sura, vers), ...]
        self.wurzel_gesamt = Counter()         # wurzel -> Anzahl Segmente im ganzen Koran
        for e in self.morph:
            if e["wurzel"]:
                self.wurzel_orte[e["wurzel"]].append((e["sura"], e["vers"]))
                self.wurzel_gesamt[e["wurzel"]] += 1

        self.segmente_gesamt = sum(1 for e in self.morph if e["wurzel"])

    def sura_eintraege(self, n):
        return [e for e in self.morph if e["sura"] == n]

    def verse(self, n):
        return sorted(v for (s, v) in self.arabisch if s == n)


# ---------------------------------------------------------------- Befehl: sura

def befehl_sura(korpus, nummer):
    verse = korpus.verse(nummer)
    if not verse:
        sys.exit(f"Sure {nummer} gibt es nicht (gueltig: 1-114).")

    eintraege = korpus.sura_eintraege(nummer)
    wurzeln_hier = Counter(e["wurzel"] for e in eintraege if e["wurzel"])
    segmente_hier = sum(wurzeln_hier.values())

    print(f"{'=' * 78}\nSURE {nummer}  —  {len(verse)} Verse, {segmente_hier} wurzelfuehrende Woerter\n{'=' * 78}\n")

    print("SCHRITT 1 — WORTLAUT\n")
    for v in verse:
        print(f"  [{nummer}:{v}]")
        print(f"    {korpus.arabisch[(nummer, v)]}")
        print(f"    B/E:    {korpus.bubenheim.get((nummer, v), '—')}")
        print(f"    Khoury: {korpus.khoury.get((nummer, v), '—')}")
        print()

    print(f"\nSCHRITT 3 — BEGRIFFE: Wurzeln dieser Sure\n")
    print(f"  Sortiert nach Seltenheit im Gesamtkoran. Seltene Wurzeln tragen")
    print(f"  die meiste Deutungslast — haeufige wie 'amn' (glauben) sagen wenig ueber")
    print(f"  DIESE Sure aus.\n")
    print(f"  {'Wurzel':<12} {'hier':>5} {'Koran':>7}  Einordnung")
    print(f"  {'-' * 12} {'-' * 5:>5} {'-' * 7:>7}  {'-' * 44}")

    zeilen = []
    for wurzel, anzahl_hier in wurzeln_hier.items():
        gesamt = korpus.wurzel_gesamt[wurzel]
        erwartet = gesamt * segmente_hier / korpus.segmente_gesamt
        zeilen.append((gesamt, wurzel, anzahl_hier, erwartet))

    for gesamt, wurzel, hier, erwartet in sorted(zeilen):
        if gesamt == hier:
            hinweis = "kommt AUSSCHLIESSLICH in dieser Sure vor"
        elif gesamt <= 10:
            hinweis = f"sehr selten — nur {gesamt}x im ganzen Koran"
        elif gesamt <= 40:
            hinweis = f"selten — {gesamt}x im ganzen Koran"
        elif erwartet >= 1.0 and hier / erwartet >= 3:
            hinweis = f"hier gehaeuft (x{hier / erwartet:.1f} gegenueber dem Schnitt)"
        elif erwartet < 1.0:
            hinweis = ""          # Sure zu kurz fuer eine Haeufigkeitsaussage
        else:
            hinweis = ""
        print(f"  {wurzel:<12} {hier:>5} {gesamt:>7}  {hinweis}")

    if segmente_hier < 150:
        print(f"\n  ACHTUNG: Diese Sure hat nur {segmente_hier} Woerter. Haeufigkeitsvergleiche")
        print(f"  mit dem Gesamtkoran sind hier statistisch wertlos — bei so kleinen Zahlen")
        print(f"  wirkt alles 'ueberrepraesentiert'. Verwertbar ist allein die Spalte")
        print(f"  'Koran': wie selten das Wort ueberhaupt ist.")

    print(f"\n  Naechster Schritt: werkzeuge/hikmet.py wurzel <WURZEL>  fuer die Querbezuege.\n")


# -------------------------------------------------------------- Befehl: wurzel

def befehl_wurzel(korpus, wurzel, grenze=60):
    orte = korpus.wurzel_orte.get(wurzel)
    if not orte:
        sys.exit(f"Wurzel {wurzel} kommt im Korpus nicht vor. "
                 f"Schreibweise ohne Vokalzeichen, z.B. ktb als: ك ت ب zusammen.")

    eindeutig = sorted(set(orte))
    formen = Counter(e["form"] for e in korpus.morph if e["wurzel"] == wurzel)
    lemmata = Counter(e["lemma"] for e in korpus.morph if e["wurzel"] == wurzel and e["lemma"])

    print(f"{'=' * 78}\nWURZEL {wurzel}\n{'=' * 78}\n")
    print(f"  {len(orte)} Vorkommen in {len(eindeutig)} Versen, "
          f"verteilt auf {len({s for s, _ in eindeutig})} Suren.\n")

    print("  LEMMATA (Grundformen):")
    for lemma, n in lemmata.most_common():
        print(f"    {lemma:<20} {n:>4}x")

    print(f"\n  SCHRITT 4 — QUERBEZUEGE: alle Stellen\n")
    for i, (s, v) in enumerate(eindeutig):
        if i >= grenze:
            print(f"    ... und {len(eindeutig) - grenze} weitere Verse. "
                  f"Mit --alle vollstaendig anzeigen.")
            break
        print(f"    [{s}:{v}]  {korpus.bubenheim.get((s, v), '—')}")
    print()


# -------------------------------------------------------------- Befehl: zaehle

def befehl_zaehle(korpus, art, wert):
    """
    Zaehlt nach EINER ausdruecklich benannten Regel.

    Der ganze Zweck: Die Regel steht im Befehl und damit VOR dem Ergebnis.
    Genau das fehlt den meisten Zahlen-Behauptungen.
    """
    if art == "wurzel":
        treffer = [e for e in korpus.morph if e["wurzel"] == wert]
    elif art == "lemma":
        treffer = [e for e in korpus.morph if e["lemma"] == wert]
    else:
        sys.exit("art muss 'wurzel' oder 'lemma' sein.")

    if not treffer:
        sys.exit(f"Keine Treffer fuer {art}={wert}.")

    verse = {(e["sura"], e["vers"]) for e in treffer}
    dual = [e for e in treffer if re.search(r"\|(MD|FD)\|", e["merkmale"])]
    plural = [e for e in treffer if re.search(r"\|(MP|FP)\|", e["merkmale"])]
    indefinit = [e for e in treffer if "INDEF" in e["merkmale"]]
    singular = [e for e in treffer if e not in dual and e not in plural]

    print(f"{'=' * 78}\nZAEHLUNG  {art}={wert}\n{'=' * 78}\n")
    print(f"  Jede Zeile ist eine ANDERE Zaehlregel. Alle sind gleich 'richtig'.")
    print(f"  Wer sich die passende aussucht, hat nichts bewiesen.\n")
    print(f"    alle Vorkommen (Segmente) ............... {len(treffer)}")
    print(f"    verschiedene Verse ...................... {len(verse)}")
    print(f"    verschiedene Suren ...................... {len({s for s, _ in verse})}")
    print(f"    nur Singularformen ...................... {len(singular)}")
    print(f"    nur Dualformen .......................... {len(dual)}")
    print(f"    nur Pluralformen ........................ {len(plural)}")
    print(f"    nur indefinite Formen ................... {len(indefinit)}")
    print(f"    nur definite / Status constructus ....... {len(treffer) - len(indefinit)}")
    print()
    print(f"  {len({len(treffer), len(verse), len(singular), len(dual), len(plural), len(indefinit)})} "
          f"verschiedene Zahlen aus einem einzigen Wort.")
    print(f"  Lege die Regel fest, BEVOR du das Ergebnis siehst.\n")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        print("Befehle:")
        print("  hikmet.py sura <1-114>          Wortlaut + Wurzelprofil einer Sure")
        print("  hikmet.py wurzel <wurzel>       alle Stellen einer Wurzel im Koran")
        print("  hikmet.py zaehle <wurzel|lemma> <wert>   Zaehlung nach allen Regeln")
        sys.exit(0)

    befehl = sys.argv[1]
    korpus = Korpus()

    if befehl == "sura":
        befehl_sura(korpus, int(sys.argv[2]))
    elif befehl == "wurzel":
        grenze = 10**9 if "--alle" in sys.argv else 60
        befehl_wurzel(korpus, sys.argv[2], grenze)
    elif befehl == "zaehle":
        befehl_zaehle(korpus, sys.argv[2], sys.argv[3])
    else:
        sys.exit(f"Unbekannter Befehl: {befehl}")


if __name__ == "__main__":
    main()
