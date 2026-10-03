#!/usr/bin/env python3
"""build_mobile.py - derive mobile.html from the built desktop atlas.html.

The mobile page reuses the desktop viewer code (same LOOKUP notes, approaches,
illustrations and data files) but embeds no models: every specimen, including
the core "Brain & cervical spine" model, is downloaded on demand. The phone UI
lives in mobile_layer.html and is injected before </body>.

Run after every rebuild of atlas.html:   python build_mobile.py
Standard library only.
"""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
src = (ROOT / "atlas.html").read_text(encoding="utf-8")
layer = (ROOT / "mobile_layer.html").read_text(encoding="utf-8")
manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))

def sub(pattern, repl, text, what, flags=0):
    out, n = re.subn(pattern, repl, text, count=1, flags=flags)
    if n != 1:
        sys.exit(f"build_mobile: could not find {what} - has the viewer template changed?")
    return out

html = sub(r"const EMBEDDED_MODELS = \[.*?\];", lambda _: "const EMBEDDED_MODELS = [];", src, "EMBEDDED_MODELS", re.S)
html = sub(r'<meta name="viewport" content="[^"]*" />',
           '<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no, viewport-fit=cover" />\n'
           '<meta name="theme-color" content="#0d1317" />', html, "viewport meta")
html = sub(r"<title>([^<]*)</title>", lambda m: "<title>" + m.group(1) + " (mobile)</title>", html, "title")
# surgeon's-view distance scale (portrait phones are narrow)
html = sub(r"r=d\.length\(\)\*\(a\.cat==='Spinal'\?1\.2:1\.9\)", "r=d.length()*(a.cat==='Spinal'?1.2:1.9)*(window.AP_RSCALE||1)", html, "apView distance")
# overlay: only download layers that start switched on; the rest load when toggled
html = sub(r"overlayVis\[L\.label\]=!L\.off;", "overlayVis[L.label]=!L.off;if(window.M_LAZY&&L.off&&L.file&&!L._cache)continue;", html, "overlay loop")

files = {m["file"] for m in manifest.get("models", []) if m.get("file")}
files |= {L["file"] for L in manifest.get("overlay", {}).get("layers", []) if L.get("file")}
files.add("brain_cervical_spine.glb")
sizes = {}
for f in sorted(files):
    p = ROOT / f
    if p.exists():
        sizes[f] = p.stat().st_size
    else:
        print(f"  ! {f} not found next to the page; it will show no size")
boot = "<script>window.M_LAZY=true;window.M_SIZES=" + json.dumps(sizes) + ";</script>\n"
idx = html.rfind("</body>")
if idx < 0:
    sys.exit("build_mobile: no </body>")
html = html[:idx] + boot + layer + "\n" + html[idx:]
(ROOT / "mobile.html").write_text(html, encoding="utf-8")
print(f"Wrote mobile.html ({len(html.encode())/1024:.0f} KB, {len(sizes)} sized files)")
