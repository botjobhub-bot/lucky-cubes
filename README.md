# Koran-Untersuchung nach der Hikmet-Methode

Arbeitsprojekt: den Koran Sure für Sure nach einer festgelegten, nachprüfbaren
Methode untersuchen — und jede Behauptung an den Text binden.

## Aufbau

```
METHODE.md        Die acht Schritte, das Prüfprotokoll, die Regeln
werkzeuge/        hikmet.py — Befundwerkzeug (Schritte 1, 3, 4, 8)
daten/            Korpus: Morphologie, arabischer Text, 2 dt. Übersetzungen
befunde/          Automatisch erzeugt: 001.txt … 114.txt, alle 114 Suren
suren/            Handarbeit: die vollständige Untersuchung je Sure
```

## Benutzung

```bash
python3 werkzeuge/hikmet.py sura 103          # Wortlaut + Wurzelprofil
python3 werkzeuge/hikmet.py wurzel عصر        # alle Stellen einer Wurzel
python3 werkzeuge/hikmet.py zaehle lemma رَجُل # Zählung nach ALLEN Regeln
```

## Die Arbeitsteilung

Was **maschinell** geht, ist fertig — für alle 114 Suren, in `befunde/`:
Wortlaut, Wurzelprofil, Seltenheiten, Querbezüge.

Was **Urteil** braucht, ist Handarbeit und entsteht Sure für Sure in `suren/`:
Kontext, Offenbarungsanlass, Hikmet, Anwendung.

Diese Trennung ist Absicht. Automatisch erzeugte Deutung wäre genau das, was die
Methode verhindern soll: eine Maschine, die bestätigt, was man schon glaubte.

## Kennzeichnung in den Sure-Dateien

| | |
|---|---|
| **[B]** | am Korpus belegt — nachprüfbar |
| **[D]** | Deutung — begründet, aber nicht zwingend |
| **[?]** | ungeprüft — Überlieferung oder Erinnerung, noch zu verifizieren |

Kein Satz ohne Kennzeichen. Wer [D] und [B] vermischt, betreibt keine Untersuchung.

## Stand

- [x] Werkzeug und Datengrundlage
- [x] Befunde für alle 114 Suren erzeugt
- [x] Sure 103 (al-ʿAsr) — Musterdurchgang, alle 8 Schritte
- [ ] Sure 90, 51 — die Parallelstellen zu 103:3
- [ ] Juz' 30 (Suren 78–114) — die kurzen mekkanischen Suren

## Datenquellen

- [Quranic Arabic Corpus](https://github.com/mustafa0x/quran-morphology) — Morphologie, Wurzeln, Lemmata
- [quran-api](https://github.com/fawazahmed0/quran-api) — Uthmani-Text, Übersetzungen
- Deutsche Übersetzungen: Frank Bubenheim & Nadeem Elyas · Adel Theodor Khoury
