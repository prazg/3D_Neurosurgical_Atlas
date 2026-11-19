#!/usr/bin/env python3
"""
build_atlas.py — embed a folder of GLB/GLTF models into the atlas viewer,
producing a single self-contained HTML page you can publish.

WHY THIS EXISTS
---------------
The viewer stores its core model inline (base64) so the published page is one
portable file with offline core viewing. Embedding real-size anatomy models
has to run where the files already are. That's this script.

TYPICAL WORKFLOW
----------------
  1. Export regions from Slicer/Blender as .glb  ->  ./models
  2. Build the desktop page:
         python build_atlas.py --html atlas-pilot.html --models ./models --out atlas.html
  3. Build the mobile page:
         python build_mobile.py
  4. Validate all assets, notes and cross-references:
         python validate_atlas.py

OPTIONS
-------
  --html          viewer template to inject into (default: atlas-pilot.html)
  --models        folder containing .glb / .gltf files (default: ./models)
  --out           output HTML file (default: atlas.html)
  --manifest      optional manifest.json controlling order + labels
  --lookup        optional JSON mapping lowercased structure name -> {"teach":..,"surg":..}
                  (defaults to lookup.json next to --html when present)
  --no-lookup     keep the template's inline LOOKUP table untouched
  --sync-template also update the inline LOOKUP table inside --html

No third-party packages required — standard library only.
"""
import argparse
import base64
import json
import re
import sys
from pathlib import Path

WARN_MB = 15.0  # embedded pages much larger than this get sluggish in-browser


def js_string(s: str) -> str:
    """Safely encode a Python string as a JS double-quoted string literal."""
    return json.dumps(s)


def collect_models(models_dir: Path, manifest: Path | None):
    files = {
        p.name: p
        for p in sorted(models_dir.glob("*"))
        if p.suffix.lower() in (".glb", ".gltf")
    }
    if not files:
        sys.exit(f"No .glb/.gltf files found in {models_dir}")
    ordered = []  # list of (label, path)
    used = set()
    if manifest and manifest.exists():
        spec = json.loads(manifest.read_text(encoding="utf-8"))
        for entry in spec.get("models", []):
            fn = entry.get("file")
            if fn in files:
                ordered.append((entry.get("label") or Path(fn).stem, files[fn]))
                used.add(fn)
            else:
                print(f"  ! manifest lists '{fn}' but it's not in {models_dir} — skipped")
    for fn, p in files.items():  # append any not covered by the manifest
        if fn not in used:
            ordered.append((p.stem, p))
    return ordered


def inject_lookup(html: str, lookup_path: Path) -> tuple[str, int]:
    lk = json.loads(lookup_path.read_text(encoding="utf-8"))
    lookup_js = "const LOOKUP=" + json.dumps(lk, ensure_ascii=False) + ";"
    new_html, m = re.subn(r"const LOOKUP=\{.*?\};", lambda _: lookup_js, html, count=1, flags=re.S)
    if m == 0:
        sys.exit("Could not find 'const LOOKUP={...};' marker in the template.")
    return new_html, len(lk)


def main():
    ap = argparse.ArgumentParser(description="Embed GLB models into the atlas viewer.")
    ap.add_argument("--html", default="atlas-pilot.html")
    ap.add_argument("--models", default="./models")
    ap.add_argument("--out", default="atlas.html")
    ap.add_argument("--manifest", default=None)
    ap.add_argument("--lookup", default=None)
    ap.add_argument("--no-lookup", action="store_true", help="Do not auto-inject lookup.json")
    ap.add_argument("--sync-template", action="store_true", help="Also sync LOOKUP into --html")
    args = ap.parse_args()

    html_path = Path(args.html)
    if not html_path.exists():
        sys.exit(f"Viewer template not found: {html_path}")
    html = html_path.read_text(encoding="utf-8")

    # Resolve lookup path (explicit --lookup, or sibling lookup.json unless --no-lookup)
    lookup_path = None
    if not args.no_lookup:
        if args.lookup:
            lookup_path = Path(args.lookup)
            if not lookup_path.exists():
                sys.exit(f"Lookup file not found: {lookup_path}")
        else:
            cand = html_path.parent / "lookup.json"
            if cand.exists():
                lookup_path = cand

    if lookup_path:
        html, lk_count = inject_lookup(html, lookup_path)
        print(f"LOOKUP: injected {lk_count} entries from {lookup_path.name}")
        if args.sync_template:
            html_path.write_text(html, encoding="utf-8")
            print(f"Template synced: updated LOOKUP in {html_path}")

    models = collect_models(Path(args.models), Path(args.manifest) if args.manifest else None)

    entries, total = [], 0
    print("Embedding:")
    for label, path in models:
        raw = path.read_bytes()
        b64 = base64.b64encode(raw).decode("ascii")
        total += len(b64)
        print(f"  - {label:<28} {len(raw)/1024:8.1f} KB  ({path.name})")
        entries.append("{label:%s,b64:%s}" % (js_string(label), js_string(b64)))
    array_js = "const EMBEDDED_MODELS = [" + ",".join(entries) + "];"

    new_html, n = re.subn(
        r"const EMBEDDED_MODELS = \[.*?\];",
        lambda _: array_js,
        html,
        count=1,
        flags=re.S,
    )
    if n == 0:
        sys.exit("Could not find 'const EMBEDDED_MODELS = [...]' in the template.")

    Path(args.out).write_text(new_html, encoding="utf-8")
    mb = total / (1024 * 1024)
    print(f"\nWrote {args.out}  ({len(models)} model(s), ~{mb:.1f} MB embedded)")
    if mb > WARN_MB:
        print(
            f"  ! embedded payload is large (>{WARN_MB:.0f} MB). Consider decimating in "
            f"Slicer/Blender or switching to a hosted-manifest build for smoother loading."
        )


if __name__ == "__main__":
    main()
