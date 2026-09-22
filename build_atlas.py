#!/usr/bin/env python3
"""
build_atlas.py — embed a folder of GLB/GLTF models into the atlas viewer,
producing a single self-contained HTML page you can publish.

WHY THIS EXISTS
---------------
The viewer stores its models inline (base64) so the published page is one
portable file with no server and no runtime Drive calls. Embedding real-size
anatomy models can't be done by hand through a chat — it has to run where the
files already are. That's this script.

TYPICAL WORKFLOW (Drive stays the source of truth)
--------------------------------------------------
  1. Export regions from Slicer/Blender as .glb  ->  a local folder
  2. (optional) keep them in Drive too, and pull them down with rclone:
         rclone copy "gdrive:Surgical-Atlas-Models" ./models --include "*.glb"
  3. Build the page:
         python build_atlas.py --html atlas-pilot.html --models ./models --out atlas.html
  4. Publish atlas.html (GitHub Pages, Netlify, anywhere static).

OPTIONS
-------
  --html     viewer template to inject into (default: atlas-pilot.html)
  --models   folder containing .glb / .gltf files (default: ./models)
  --out      output HTML file (default: atlas.html)
  --manifest optional manifest.json (Drive-style) controlling order + labels:
             {"models":[{"file":"skull-base.glb","label":"Skull base"}, ...]}
             files not listed are appended alphabetically; listed-but-missing are skipped
  --lookup   optional JSON mapping lowercased structure name -> {"teach":..,"surg":..}
             injected as the viewer's LOOKUP table (your surgical teaching notes)

No third-party packages required — standard library only.
"""
import argparse, base64, json, re, sys
from pathlib import Path

WARN_MB = 15.0  # embedded pages much larger than this get sluggish in-browser

def js_string(s: str) -> str:
    """Safely encode a Python string as a JS double-quoted string literal."""
    return json.dumps(s)  # json.dumps produces a valid JS string literal

def collect_models(models_dir: Path, manifest: Path | None):
    files = {p.name: p for p in sorted(models_dir.glob("*"))
             if p.suffix.lower() in (".glb", ".gltf")}
    if not files:
        sys.exit(f"No .glb/.gltf files found in {models_dir}")
    ordered = []  # list of (label, path)
    used = set()
    if manifest and manifest.exists():
        spec = json.loads(manifest.read_text())
        for entry in spec.get("models", []):
            fn = entry.get("file")
            if fn in files:
                ordered.append((entry.get("label") or Path(fn).stem, files[fn]))
                used.add(fn)
            else:
                print(f"  ! manifest lists '{fn}' but it's not in {models_dir} — skipped")
    for fn, p in files.items():           # append any not covered by the manifest
        if fn not in used:
            ordered.append((p.stem, p))
    return ordered

def main():
    ap = argparse.ArgumentParser(description="Embed GLB models into the atlas viewer.")
    ap.add_argument("--html", default="atlas-pilot.html")
    ap.add_argument("--models", default="./models")
    ap.add_argument("--out", default="atlas.html")
    ap.add_argument("--manifest", default=None)
    ap.add_argument("--lookup", default=None)
    args = ap.parse_args()

    html_path = Path(args.html)
    if not html_path.exists():
        sys.exit(f"Viewer template not found: {html_path}")
    html = html_path.read_text()

    models = collect_models(Path(args.models), Path(args.manifest) if args.manifest else None)

    # build the EMBEDDED_MODELS array
    entries, total = [], 0
    print("Embedding:")
    for label, path in models:
        raw = path.read_bytes()
        b64 = base64.b64encode(raw).decode()
        total += len(b64)
        print(f"  • {label:<28} {len(raw)/1024:8.1f} KB  ({path.name})")
        entries.append("{label:%s,b64:%s}" % (js_string(label), js_string(b64)))
    array_js = "const EMBEDDED_MODELS = [" + ",".join(entries) + "];"

    # replace the existing declaration (base64 alphabet has no ']', so .*?]; is safe)
    new_html, n = re.subn(r"const EMBEDDED_MODELS = \[.*?\];", lambda _: array_js, html, count=1, flags=re.S)
    if n == 0:
        sys.exit("Could not find 'const EMBEDDED_MODELS = [...]' in the template.")

    # optional: inject the LOOKUP teaching-notes table
    if args.lookup:
        lk = json.loads(Path(args.lookup).read_text())
        lookup_js = "const LOOKUP=" + json.dumps(lk) + ";"
        new_html, m = re.subn(r"const LOOKUP=\{.*?\};", lambda _: lookup_js, new_html, count=1, flags=re.S)
        print(f"LOOKUP: {'injected '+str(len(lk))+' entries' if m else 'MARKER NOT FOUND (left unchanged)'}")

    Path(args.out).write_text(new_html)
    mb = total / (1024*1024)
    print(f"\nWrote {args.out}  ({len(models)} model(s), ~{mb:.1f} MB embedded)")
    if mb > WARN_MB:
        print(f"  ⚠ embedded payload is large (>{WARN_MB:.0f} MB). Consider decimating in "
              f"Slicer/Blender or switching to a hosted-manifest build for smoother loading.")

if __name__ == "__main__":
    main()
