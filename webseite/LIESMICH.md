# Webseite „Wurzeln des Koran"

Dieselbe Untersuchung wie das Kommandozeilenwerkzeug, nur zum Antippen.

**Live:** https://claude.ai/artifact/LnAEC1JUSUCzkKZopj2QwM

## Aufbau

- `kopf.html` — Titel und Gestaltung
- `koerper.html` — Inhalt und Verhalten; `__DATEN__` ist der Platzhalter für das Datenpaket
- Das Datenpaket entsteht aus `daten/` (Morphologie, Uthmani-Text, Übersetzung Bubenheim/Elyas)
  und wird beim Zusammenbauen an die Stelle von `__DATEN__` gesetzt.

Fertige Seite: rund 3 MB, alles eingebettet, läuft ohne Netz.

## Was sie zeigt

Pro Vers: arabischer Text, deutsche Übersetzung, und darunter jede Wurzel als Schaltfläche.
Antippen zeigt die Grundformen, **alle Zählweisen nebeneinander** und **jede Stelle im
Koran**, an der die Wurzel sonst noch steht.

Braun markierte Wurzeln kommen höchstens zehnmal im ganzen Koran vor. Die tragen bei der
Deutung das meiste Gewicht.

Die Seite deutet nichts. Sie zeigt Befunde — Schritt 1, 3, 4 und 8 der Methode.
Die Schritte 2, 5, 6 und 7 bleiben Handarbeit.
