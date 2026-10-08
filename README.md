# Avatar-Selector

Datenquelle für den VRChat-Avatar-Katalog (Udon, `VRCStringDownloader` + `VRCImageDownloader`).

- `avatars.json` – Katalog (Name, Ersteller, Avatar-ID, Plattformen, Beschreibung, Thumbnail-Position im Atlas)
- `atlas/atlas_N.png` – Vorschaubilder als Atlas (8 × 10 Zellen à 256 × 192 px, 4:3, max. 2048 px Kantenlänge).
  VRChat lädt höchstens ca. ein Bild pro 5 Sekunden, daher stecken bis zu 80 Thumbnails in einem Bild.

Die aktuellen Einträge sind **Dummy-Daten** zum Testen (Avatar-IDs sind Platzhalter).
