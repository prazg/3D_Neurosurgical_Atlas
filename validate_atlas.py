#!/usr/bin/env python3
"""
validate_atlas.py — end-to-end integrity, anatomical classification, lookup
coverage, and build-parity validator for the 3D Neurosurgical Atlas.

Runs with Python's standard library only (plus optional `node --check` if Node
is installed) so it can guard local builds and GitHub Pages CI deployments.
"""
import json
import re
import shutil
import struct
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
GENERIC_MESH_RE = re.compile(
    r"^(geometry|mesh|node|primitive|object|scene|root|default|unnamed|world)([_.\-\s]*\d+)?$",
    re.I,
)


def fail(msg: str, errors: list[str]):
    print(f"  [FAIL] {msg}")
    errors.append(msg)


def clean_mesh_name(s: str) -> str:
    s = s.replace("_", " ")
    s = re.sub(r"\bAnteior\b", "Anterior", s)
    s = re.sub(r"thalamoperfurators", "thalamoperforators", s, flags=re.I)
    return s.strip()


def parse_glb_meshes(path: Path) -> list[str]:
    buf = path.read_bytes()
    magic, _, _ = struct.unpack_from("<III", buf, 0)
    if magic != 0x46546C67:
        raise ValueError(f"{path.name}: invalid GLB magic header")
    chunk_len, _ = struct.unpack_from("<II", buf, 12)
    js = json.loads(buf[20 : 20 + chunk_len].decode("utf-8"))
    nodes = js.get("nodes", [])
    meshes = js.get("meshes", [])
    parent_of = {ch: i for i, nd in enumerate(nodes) for ch in nd.get("children", [])}
    out = []
    for i, nd in enumerate(nodes):
        if "mesh" not in nd:
            continue
        m = meshes[nd["mesh"]]
        ud = (nd.get("extras") or {}).get("name") or (m.get("extras") or {}).get("name")
        if isinstance(ud, str) and ud.strip() and not GENERIC_MESH_RE.match(ud.strip()):
            nm = clean_mesh_name(ud)
        else:
            nm = None
            for cand in (
                nd.get("name"),
                m.get("name"),
                nodes[parent_of[i]].get("name") if i in parent_of else None,
            ):
                if isinstance(cand, str) and cand.strip() and not GENERIC_MESH_RE.match(cand.strip()):
                    nm = clean_mesh_name(re.sub(r"_\d+$", "", cand))
                    break
            if not nm:
                nm = clean_mesh_name(nd.get("name") or m.get("name") or "mesh")
        prims = max(1, len(m.get("primitives", [])))
        out.extend([nm] * prims)
    return out


def system_for(name: str) -> str:
    n = (name or "").lower()
    if re.search(
        r"arter|\bvena\b|venous|vein|jugular|basilar|carotid|subclavian|vascul|aorta|brachiocephalic|\bsinus\b(?!.*(sphenoid|frontal|maxillar|ethmoid|paranasal|piriform|pyriform))|lenticulostriate|thalamoperf|\bchoroidal\b|^superior cerebellar (left|right)$|^inferior cerebellar (left|right)$|torcular|confluens|\bacoma\b|\bpcoma\b|circle of willis|median callosal",
        n,
    ):
        return "vascular"
    if re.search(r"ventricle|cistern|\bcsf\b|ependym|choroid|\baqueduct\b|scala tympani|scala vestibuli|thecal|subarachnoid", n):
        return "csf"
    if re.search(
        r"fasciculus|fascicle|\btract\b|\bnerve\b|rootlet|radiation|\bfibres\b|cingulum|lemniscus|gyrus|sulcus|lobule|cuneus|insula|internal medullary lamina|temporoparietooccipital|area lateral occipital|visual area|visual cortex",
        n,
    ):
        return "neural"
    if re.search(
        r"muscle|\bgland|eyeball|\btongue|pharyn|laryn|trache|oesoph|esoph|parotid|platysma|masseter|temporalis\b|pterygoid|digastric|stylohyoid|sternocleido|trapezius|scalen|longus (colli|capitis)|splenius|semispinalis|longissimus|rectus$|superior oblique$|inferior oblique$|levator palpebrae|veli palatini|palatoglossus|constrictor|^uvula$|hyoglossus|rectus capitis|oblique capitis|zygomaticus|nasalis|levator labii|buccinator|levator scapulae|tympanic membrane|round window|\bdura\b",
        n,
    ):
        return "soft"
    if re.search(
        r"^(cervical|thoracic|lumbar)\d+$|^atlas$|^axis$|vertebra|\bvertebral arch\b|\bbody of vertebra\b|\blamina\b|pedicle|spinous process|transverse process|articular process|mastoid|styloid|clinoid|\bbone|skull|mandible|rib|hyoid|clavicle|sternum|scapula|cartilage|craniotomy|occipit|clivus|dens|odontoid|foramen|maxilla|vomer|suture|\bmalleus\b|\bincus\b|\bstapes\b|ossicle|external auditory canal",
        n,
    ):
        return "skeletal"
    return "neural"


def has_lookup_note(name: str, lk: dict, rules: list) -> bool:
    key = (name or "").lower()
    if key.startswith("approach:"):
        return True
    if key in lk:
        return True
    if re.search(r"spine metastasis case", key):
        return "_spinemet" in lk
    if re.search(r"^interval growth", key):
        return "vs_growth" in lk
    if re.search(r"^cochlea", key):
        return "vs_cochlea" in lk
    if re.search(r"^vestibular schwannoma", key):
        return "vs_tumour" in lk
    for pfx, lkk in [
        ["gbm idh-wt g4", "mol_gbm idh-wt g4"],
        ["astro idh-mut g4", "mol_astro idh-mut g4"],
        ["astro idh-mut g3", "mol_astro idh-mut g3"],
        ["astro idh-mut g2", "mol_astro idh-mut g2"],
        ["oligo 1p19q-codel g2", "mol_oligo 1p19q-codel g2"],
        ["astro idh-wt g3", "mol_astro idh-wt g3"],
    ]:
        if key.startswith(pfx) and lkk in lk:
            return True
    if key.startswith("gbm "):
        for r in [
            "posterior fossa / midline",
            "deep / thalamic-basal ganglia",
            "insular / peri-sylvian",
            "fronto-temporal / peri-sylvian",
            "occipito-temporal",
            "occipital",
            "parietal",
            "temporal",
            "frontal",
        ]:
            if r in key and f"region_{r}" in lk:
                return True
    if re.search(r"craniotomy|flap|footprint", key):
        return "_craniotomy" in lk
    if re.search(r"\bvertebra\b|^vertebral arch|^body of vertebra", key):
        return "_vertebra" in lk
    n2 = re.sub(r"^(left|right)[ -]+", "", key)
    n2 = re.sub(r"\s+(l|r|left|right)$", "", n2).strip()
    if n2 != key and n2 in lk and lk[n2].get("teach"):
        return True
    return any(rx.search(key) and target in lk for rx, target in rules)


def check_html_scripts(errors: list[str]):
    node = shutil.which("node")
    for fn in ("index.html", "atlas-pilot.html", "atlas.html", "mobile.html"):
        p = ROOT / fn
        if not p.exists():
            fail(f"Missing HTML file: {fn}", errors)
            continue
        html = p.read_text(encoding="utf-8")
        scripts = re.findall(r"<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>", html, flags=re.S | re.I)
        if not scripts:
            fail(f"{fn}: no inline <script> blocks found", errors)
            continue
        if node:
            for idx, code in enumerate(scripts):
                # Strip EMBEDDED_MODELS huge base64 literal for fast syntax checking
                fast_code = re.sub(
                    r"const EMBEDDED_MODELS = \[.*?\];",
                    "const EMBEDDED_MODELS = [];",
                    code,
                    flags=re.S,
                )
                with tempfile.NamedTemporaryFile("w", suffix=".js", encoding="utf-8", delete=False) as tf:
                    tf.write(fast_code)
                    tmp_path = Path(tf.name)
                try:
                    res = subprocess.run([node, "--check", str(tmp_path)], capture_output=True, text=True)
                    if res.returncode != 0:
                        fail(f"{fn} script[{idx}] JS syntax error:\n{res.stderr}", errors)
                finally:
                    tmp_path.unlink(missing_ok=True)
    print(f"  [OK] HTML & inline JS syntax checked ({'with node --check' if node else 'basic'})")


def main() -> int:
    errors: list[str] = []
    print("Validating 3D Neurosurgical Atlas...")

    # 1. HTML & JS syntax
    check_html_scripts(errors)

    # 2. Build & template parity
    pilot = (ROOT / "atlas-pilot.html").read_text(encoding="utf-8")
    atlas = (ROOT / "atlas.html").read_text(encoding="utf-8")
    s_pilot = re.sub(r"const EMBEDDED_MODELS = \[.*?\];", "const EMBEDDED_MODELS = [];", pilot, flags=re.S)
    s_atlas = re.sub(r"const EMBEDDED_MODELS = \[.*?\];", "const EMBEDDED_MODELS = [];", atlas, flags=re.S)
    if s_pilot != s_atlas:
        fail("atlas.html is out of sync with atlas-pilot.html — re-run build_atlas.py", errors)
    else:
        print("  [OK] atlas-pilot.html and atlas.html are in exact sync")

    lookup = json.loads((ROOT / "lookup.json").read_text(encoding="utf-8"))
    m_lk = re.search(r"const LOOKUP=(\{.*?\});", atlas, re.S)
    if not m_lk or json.loads(m_lk.group(1)) != lookup:
        fail("Inline LOOKUP in atlas.html differs from lookup.json — re-run build_atlas.py", errors)
    else:
        print(f"  [OK] lookup.json ({len(lookup)} entries) matches inline LOOKUP")
    for lk_k, lk_v in lookup.items():
        if lk_k == "_rules" or not isinstance(lk_v, dict):
            continue
        for fld in ("teach", "surg", "ref"):
            val = lk_v.get(fld) or ""
            if "**" in val or "`" in val:
                fail(f"lookup.json '{lk_k}.{fld}' contains raw Markdown syntax (** or `)", errors)
            if re.search(r"[\u0400-\u04FF]", val):
                fail(f"lookup.json '{lk_k}.{fld}' contains unexpected Cyrillic characters", errors)

    # 3. Manifest & GLB mesh/note/system validation
    manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
    glb_list = [m["file"] for m in manifest.get("models", []) if m.get("file")]
    glb_list += [L["file"] for L in manifest.get("overlay", {}).get("layers", []) if L.get("file")]
    glb_list.append("brain_cervical_spine.glb")
    rules = [(re.compile(r[0]), r[1]) for r in lookup.get("_rules", [])]

    glb_meshes: dict[str, list[str]] = {}
    total_meshes = 0
    for fn in sorted(set(glb_list)):
        p = ROOT / fn
        if not p.exists():
            fail(f"Manifest references missing GLB: {fn}", errors)
            continue
        names = parse_glb_meshes(p)
        glb_meshes[fn] = names
        total_meshes += len(names)
        for nm in names:
            if GENERIC_MESH_RE.match(nm):
                fail(f"{fn}: unresolved generic mesh name '{nm}'", errors)
            if not has_lookup_note(nm, lookup, rules):
                fail(f"{fn}: structure '{nm}' has no teaching note in lookup.json", errors)
            # Guard against known cortex-as-bone regressions
            sy = system_for(nm)
            nl = nm.lower()
            if sy == "skeletal" and any(w in nl for w in ("gyrus", "sulcus", "fascic", "medullary lamina")):
                fail(f"{fn}: neural structure '{nm}' misclassified as skeletal", errors)
    print(f"  [OK] {len(glb_meshes)} GLB files ({total_meshes:,} meshes) verified: 100% named, classified & noted")

    # 4. Approaches, syndromes, pathways & dissections
    appr_data = json.loads((ROOT / "approaches.json").read_text(encoding="utf-8"))
    approaches = appr_data.get("approaches", [])
    for a in approaches:
        aid = a["id"]
        spec = a.get("specimen")
        spec_names = glb_meshes.get(spec, [])
        spec_lower = {n.lower() for n in spec_names}
        non_appr = [n for n in spec_names if not n.lower().startswith("approach:")]
        tags = {dm["tag"] for dm in a.get("meshes", [])}
        for dm in a.get("meshes", []):
            if dm["name"].lower() not in spec_lower:
                fail(f"Approach '{aid}': missing mesh '{dm['name']}' in {spec}", errors)
        for si, st in enumerate(a.get("steps", [])):
            for rev in st.get("reveal") or []:
                if rev not in tags:
                    fail(f"Approach '{aid}' step {si}: unknown reveal tag '{rev}'", errors)
            for fld in ("lesion", "show"):
                pat = st.get(fld)
                if pat and not any(re.search(pat, n, re.I) for n in non_appr):
                    fail(f"Approach '{aid}' step {si}: {fld} regex /{pat}/ matched 0 meshes in {spec}", errors)
        for rk in a.get("risks", []):
            if rk.get("match") and not any(re.search(rk["match"], n, re.I) for n in non_appr):
                fail(f"Approach '{aid}': risk '{rk['label']}' regex /{rk['match']}/ matched 0 meshes", errors)
        # Guard against unparsed Markdown in plain-text approach fields
        ap_texts = [a.get("summary") or "", a.get("title") or ""]
        ap_texts += [st.get("t") or "" for st in a.get("steps", [])]
        ap_texts += [rk.get("why") or "" for rk in a.get("risks", [])]
        ap_texts += (a.get("pearls") or []) + (a.get("pitfalls") or []) + (a.get("indications") or [])
        for tx in ap_texts:
            if "**" in tx or "`" in tx:
                fail(f"Approach '{aid}' contains raw Markdown (** or `) in plain-text field", errors)
                break
    print(f"  [OK] {len(approaches)} approaches, syndromes, pathways & dissections verified")

    # 5. Figures & Rhoton plates
    figs = json.loads((ROOT / "figures.json").read_text(encoding="utf-8"))
    for fid, fobj in figs.get("figures", {}).items():
        if not (ROOT / "img" / "smart" / fobj.get("file", "")).exists():
            fail(f"figures.json '{fid}' missing file img/smart/{fobj.get('file')}", errors)
    rhoton = json.loads((ROOT / "rhoton.json").read_text(encoding="utf-8"))
    for pl in rhoton.get("plates", []):
        if not (ROOT / pl.get("file", "")).exists():
            fail(f"rhoton.json plate {pl.get('n')} missing file {pl.get('file')}", errors)
    print(
        f"  [OK] {len(figs.get('figures', {}))} Servier figures & {len(rhoton.get('plates', []))} Rhoton plates verified"
    )

    if errors:
        print(f"\nValidation FAILED with {len(errors)} error(s).")
        return 1
    print("\nAll checks PASSED.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
