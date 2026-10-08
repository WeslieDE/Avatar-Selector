#!/usr/bin/env python3
"""Build the VRChat avatar catalog from Avatars/*.json + Images/*.

- Every Avatars/<name>.json is one avatar entry; its picture is Images/<name>.<jpg|jpeg|png|webp>.
- Entries without a matching image (or images without JSON) are skipped with a warning.
- Thumbnails are packed into atlas textures (8 x 8 cells of 256 x 192 px = 64 per atlas).
- Output goes to <out>/avatars.json and <out>/atlas/atlas_XX.jpg.

The atlas URLs are fixed (VRChat cannot build VRCUrls at runtime), so only the
MAX_ATLASES predefined file names atlas_00 .. atlas_49 are ever produced.
"""
import argparse
import datetime as dt
import json
import os
import re
import sys
from pathlib import Path

from PIL import Image, ImageOps

COLS, ROWS = 8, 8
CELL_W, CELL_H = 256, 192
PER_ATLAS = COLS * ROWS
MAX_ATLASES = 50
IMAGE_EXTS = (".jpg", ".jpeg", ".png", ".webp")
AVATAR_ID = re.compile(r"^avtr_[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$")
PLATFORMS = {"pc", "quest", "ios"}
TAGS = ["Demo", "Chibi", "Human"]  # filter categories shown in the world
BACKGROUND = (255, 246, 230)  # board cream, shows in empty cells


def warn(msg):
    print(f"::warning::{msg}" if os.environ.get("GITHUB_ACTIONS") else f"WARN: {msg}", file=sys.stderr)


def base_url():
    if os.environ.get("SITE_BASE_URL"):
        return os.environ["SITE_BASE_URL"].rstrip("/") + "/"
    repo = os.environ.get("GITHUB_REPOSITORY", "WeslieDE/Avatar-Selector")
    owner, name = repo.split("/", 1)
    return f"https://{owner.lower()}.github.io/{name}/"


def atlas_url(i):
    return f"{base_url()}atlas/atlas_{i:02d}.jpg"


def load_entries(avatars_dir: Path, images_dir: Path):
    images = {}
    for p in images_dir.iterdir() if images_dir.is_dir() else []:
        if p.suffix.lower() in IMAGE_EXTS:
            if p.stem in images:
                warn(f"multiple images for '{p.stem}', using {images[p.stem].name}")
                continue
            images[p.stem] = p

    entries, seen = [], set()
    for jp in sorted(avatars_dir.glob("*.json")):
        key = jp.stem
        seen.add(key)
        img = images.get(key)
        if img is None:
            warn(f"skip '{key}': no image Images/{key}.(jpg|png|webp)")
            continue
        try:
            data = json.loads(jp.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            warn(f"skip '{key}': invalid JSON ({e})")
            continue
        if not isinstance(data, dict):
            warn(f"skip '{key}': JSON must be an object")
            continue

        name = str(data.get("name", "")).strip()
        if not name:
            warn(f"skip '{key}': 'name' is missing")
            continue
        avatar_id = str(data.get("id", "")).strip()
        if avatar_id and not AVATAR_ID.match(avatar_id):
            warn(f"'{key}': id '{avatar_id}' is not a valid avtr_ id, cleared")
            avatar_id = ""
        if not avatar_id:
            warn(f"'{key}': no avatar id yet (entry is shown but cannot be worn)")
        platforms = [p for p in (str(x).lower() for x in data.get("platforms", ["pc"])) if p in PLATFORMS] or ["pc"]
        tags = []
        for t in data.get("tags", []) or []:
            match = next((x for x in TAGS if x.lower() == str(t).strip().lower()), None)
            if match is None:
                warn(f"'{key}': unknown tag '{t}' ignored (allowed: {', '.join(TAGS)})")
            elif match not in tags:
                tags.append(match)

        entries.append({
            "key": key,
            "name": name,
            "creator": str(data.get("creator", "")).strip(),
            "id": avatar_id,
            "platforms": platforms,
            "tags": tags,
            "description": str(data.get("description", "")).strip(),
            "added": str(data.get("added", "")).strip(),
            "_image": img,
        })

    for key in sorted(set(images) - seen):
        warn(f"skip image '{images[key].name}': no Avatars/{key}.json")
    return entries


def sort_entries(entries):
    # newest first (by "added", ISO date), entries without a date afterwards, then by name
    dated = sorted((e for e in entries if e["added"]), key=lambda e: e["name"].lower())
    dated.sort(key=lambda e: e["added"], reverse=True)  # stable sort keeps names A-Z within a date
    undated = sorted((e for e in entries if not e["added"]), key=lambda e: e["name"].lower())
    return dated + undated


def thumbnail(path: Path):
    with Image.open(path) as im:
        im = ImageOps.exif_transpose(im).convert("RGB")
        # cover-crop to 4:3, biased a little upwards where faces usually are
        return ImageOps.fit(im, (CELL_W, CELL_H), Image.LANCZOS, centering=(0.5, 0.4))


def build(avatars_dir: Path, images_dir: Path, out: Path):
    entries = sort_entries(load_entries(avatars_dir, images_dir))
    capacity = PER_ATLAS * MAX_ATLASES
    if len(entries) > capacity:
        warn(f"{len(entries)} avatars exceed the {capacity} atlas slots; the rest is dropped")
        entries = entries[:capacity]

    atlas_count = (len(entries) + PER_ATLAS - 1) // PER_ATLAS
    (out / "atlas").mkdir(parents=True, exist_ok=True)

    for a in range(atlas_count):
        sheet = Image.new("RGB", (COLS * CELL_W, ROWS * CELL_H), BACKGROUND)
        for i, e in enumerate(entries[a * PER_ATLAS:(a + 1) * PER_ATLAS]):
            sheet.paste(thumbnail(e["_image"]), ((i % COLS) * CELL_W, (i // COLS) * CELL_H))
        sheet.save(out / "atlas" / f"atlas_{a:02d}.jpg", quality=90, optimize=True, progressive=False)

    avatars = []
    for n, e in enumerate(entries):
        e = {k: v for k, v in e.items() if not k.startswith("_")}
        e["atlas"], e["index"] = divmod(n, PER_ATLAS)
        avatars.append(e)

    catalog = {
        "version": 1,
        "generated": dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat(),
        "count": len(avatars),
        "atlasCols": COLS,
        "atlasRows": ROWS,
        "cellWidth": CELL_W,
        "cellHeight": CELL_H,
        "perAtlas": PER_ATLAS,
        "atlasCount": atlas_count,
        "tags": TAGS,
        "atlases": [atlas_url(i) for i in range(atlas_count)],
        "avatars": avatars,
    }
    (out / "avatars.json").write_text(json.dumps(catalog, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"{len(avatars)} avatars -> {atlas_count} atlas texture(s) in {out}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--avatars", default="Avatars")
    ap.add_argument("--images", default="Images")
    ap.add_argument("--out", default="_site")
    a = ap.parse_args()
    build(Path(a.avatars), Path(a.images), Path(a.out))
