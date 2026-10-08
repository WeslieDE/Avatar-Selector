# Avatar-Selector

Datenquelle für den VRChat-Avatar-Katalog (Udon: `VRCStringDownloader` + `VRCImageDownloader`).

## Avatar hinzufügen

1. `Avatars/<name>.json` anlegen:
   ```json
   {
     "name": "Rusk",
     "creator": "あまとうさぎ",
     "id": "avtr_xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
     "platforms": ["pc", "quest"],
     "tags": ["Chibi"],
     "description": "",
     "added": "2026-10-08"
   }
   ```
   - `name` ist Pflicht. Ohne gültige `id` wird der Avatar angezeigt, kann aber nicht angezogen werden.
   - `tags`: optional, erlaubt sind die Tags aus `tags.json` (gepflegt über die Admin-Website). Unbekannte Tags werden ignoriert.
     Im Katalog (und damit im Board-Filter) erscheinen nur Tags, die mindestens ein Avatar nutzt – höchstens 12.
   - `added` (ISO-Datum, optional) bestimmt die Reihenfolge: neueste zuerst, Einträge ohne Datum danach alphabetisch.
2. Bild mit **demselben Dateinamen** nach `Images/<name>.jpg|png|webp` legen.
   Fehlt das Bild oder die JSON, wird der Eintrag übersprungen (Warnung im Action-Log).
3. Pushen. Die GitHub Action `Build catalog & deploy Pages` erzeugt:
   - `avatars.json`: alle Einträge zusammengefasst, inkl. `atlas` + `index` pro Avatar und dem Array `atlases`
   - `atlas/atlas_XX.jpg`: Vorschaubilder als Atlas, 8 × 8 Zellen à 256 × 192 px (4:3) = **64 pro Atlas**, 2048 × 1536 px

Die generierten Dateien werden nicht committet, sondern direkt als GitHub-Pages-Artefakt veröffentlicht
(Settings → Pages → Source: **GitHub Actions**).

## Feste URLs (für den Unity-Editor)

VRChat erlaubt keine zur Laufzeit erzeugten URLs, deshalb sind alle URLs vorab festgelegt:

- Katalog: `https://wesliede.github.io/Avatar-Selector/avatars.json`
- Atlanten (max. 50 × 64 = 3200 Avatare):

```
https://wesliede.github.io/Avatar-Selector/atlas/atlas_00.jpg
https://wesliede.github.io/Avatar-Selector/atlas/atlas_01.jpg
https://wesliede.github.io/Avatar-Selector/atlas/atlas_02.jpg
https://wesliede.github.io/Avatar-Selector/atlas/atlas_03.jpg
https://wesliede.github.io/Avatar-Selector/atlas/atlas_04.jpg
https://wesliede.github.io/Avatar-Selector/atlas/atlas_05.jpg
https://wesliede.github.io/Avatar-Selector/atlas/atlas_06.jpg
https://wesliede.github.io/Avatar-Selector/atlas/atlas_07.jpg
https://wesliede.github.io/Avatar-Selector/atlas/atlas_08.jpg
https://wesliede.github.io/Avatar-Selector/atlas/atlas_09.jpg
https://wesliede.github.io/Avatar-Selector/atlas/atlas_10.jpg
https://wesliede.github.io/Avatar-Selector/atlas/atlas_11.jpg
https://wesliede.github.io/Avatar-Selector/atlas/atlas_12.jpg
https://wesliede.github.io/Avatar-Selector/atlas/atlas_13.jpg
https://wesliede.github.io/Avatar-Selector/atlas/atlas_14.jpg
https://wesliede.github.io/Avatar-Selector/atlas/atlas_15.jpg
https://wesliede.github.io/Avatar-Selector/atlas/atlas_16.jpg
https://wesliede.github.io/Avatar-Selector/atlas/atlas_17.jpg
https://wesliede.github.io/Avatar-Selector/atlas/atlas_18.jpg
https://wesliede.github.io/Avatar-Selector/atlas/atlas_19.jpg
https://wesliede.github.io/Avatar-Selector/atlas/atlas_20.jpg
https://wesliede.github.io/Avatar-Selector/atlas/atlas_21.jpg
https://wesliede.github.io/Avatar-Selector/atlas/atlas_22.jpg
https://wesliede.github.io/Avatar-Selector/atlas/atlas_23.jpg
https://wesliede.github.io/Avatar-Selector/atlas/atlas_24.jpg
https://wesliede.github.io/Avatar-Selector/atlas/atlas_25.jpg
https://wesliede.github.io/Avatar-Selector/atlas/atlas_26.jpg
https://wesliede.github.io/Avatar-Selector/atlas/atlas_27.jpg
https://wesliede.github.io/Avatar-Selector/atlas/atlas_28.jpg
https://wesliede.github.io/Avatar-Selector/atlas/atlas_29.jpg
https://wesliede.github.io/Avatar-Selector/atlas/atlas_30.jpg
https://wesliede.github.io/Avatar-Selector/atlas/atlas_31.jpg
https://wesliede.github.io/Avatar-Selector/atlas/atlas_32.jpg
https://wesliede.github.io/Avatar-Selector/atlas/atlas_33.jpg
https://wesliede.github.io/Avatar-Selector/atlas/atlas_34.jpg
https://wesliede.github.io/Avatar-Selector/atlas/atlas_35.jpg
https://wesliede.github.io/Avatar-Selector/atlas/atlas_36.jpg
https://wesliede.github.io/Avatar-Selector/atlas/atlas_37.jpg
https://wesliede.github.io/Avatar-Selector/atlas/atlas_38.jpg
https://wesliede.github.io/Avatar-Selector/atlas/atlas_39.jpg
https://wesliede.github.io/Avatar-Selector/atlas/atlas_40.jpg
https://wesliede.github.io/Avatar-Selector/atlas/atlas_41.jpg
https://wesliede.github.io/Avatar-Selector/atlas/atlas_42.jpg
https://wesliede.github.io/Avatar-Selector/atlas/atlas_43.jpg
https://wesliede.github.io/Avatar-Selector/atlas/atlas_44.jpg
https://wesliede.github.io/Avatar-Selector/atlas/atlas_45.jpg
https://wesliede.github.io/Avatar-Selector/atlas/atlas_46.jpg
https://wesliede.github.io/Avatar-Selector/atlas/atlas_47.jpg
https://wesliede.github.io/Avatar-Selector/atlas/atlas_48.jpg
https://wesliede.github.io/Avatar-Selector/atlas/atlas_49.jpg
```

Es werden nur so viele Atlanten erzeugt (und in der Welt geladen), wie nötig sind: `atlasCount = ceil(count / 64)`.

## Lokal testen

```bash
pip install Pillow
python scripts/build_catalog.py --out _site
```
