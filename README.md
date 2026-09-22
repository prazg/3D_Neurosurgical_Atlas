# 3D Surgical Anatomy Atlas — Brain & Spine

An interactive, browser-based 3D atlas of craniospinal anatomy and neuro-oncological
pathology, built for neurosurgical teaching. Structures are clickable and labelled with
anatomy notes, operative approaches and pitfalls, and pointers to standard reference texts.

> **Educational use only.** This is a teaching aid built from open, de-identified datasets.
> It is not a medical device, is not patient-specific, and must not be used for diagnosis,
> operative planning or navigation. Craniotomy footprints and entry points are schematic
> approximations, not templates.

## What's in it

**Anatomy**

- **Craniospinal specimen** (embedded — works offline): cerebrum, diencephalon, midbrain,
  pons, medulla, cerebellum, spinal cord, C1–C7, occipital bone, vertebral arteries.
- **SPL-PNL brain**: 328 expert-segmented MRI structures, down to individual gyri.
- **SPL Head & Neck CT**: skull, mandible, cervical spine, ribs, neck muscles, cartilage,
  glands, and vessels (carotids, vertebrals, subclavians, jugulars) — plus six schematic
  **craniotomy footprints** projected onto the skull surface (pterional, retrosigmoid,
  midline suboccipital, far-lateral/transcondylar, frontal Kocher flap, subtemporal).
- **Co-registered MNI overlay**: translucent brain shell with white-matter tracts, arterial
  territories, HCP-MMP parcellation, Jülich cytoarchitecture and schematic ventricular
  entry points (Kocher, Keen, Frazier, Dandy), each independently toggleable.

**Pathology**

- **GBM by location** — 16 cases spanning every distinct side/region combination found
  across 80 screened subjects, all on one shared reference brain so corridors can be
  compared directly. Region-specific approach notes for nine territories.
- **Glioma by WHO 2021 molecular class** — 6 cases: glioblastoma IDH-wildtype grade 4;
  astrocytoma IDH-mutant grades 2, 3, 4; oligodendroglioma IDH-mutant 1p/19q-codeleted;
  astrocytoma IDH-wildtype grade 3. The teaching contrast is in the data — the IDH-mutant
  low-grade and codeleted cases have zero enhancing volume.
- **Single GBM case** — enhancing tumour, necrotic core, peritumoural oedema and brain
  surface, with compartment-by-compartment operative notes.
- **Vestibular schwannoma** — three tumours spanning 0.2 → 3.7 → 7.7 mL (intracanalicular
  to brainstem contact), cochlea, and an interval-growth pair from serial imaging.
- **Spinal metastasis** — eleven individually segmented vertebrae, T7–L5, from a planning CT.

**Viewer features:** specimen switcher, per-layer visibility, isolate, opacity and
brightness controls, sagittal/coronal/axial cross-section with a scrub slider,
click-to-label with anatomy + surgical relevance + further reading, and an in-page
*Credits & licence* panel populated from `manifest.json`.

## Run locally

The page loads model files over HTTP, so it will **not** work from `file://`:

```bash
python -m http.server 8000
# open http://localhost:8000/atlas.html
```
## Rebuilding the page

`build_atlas.py` embeds a folder of `.glb` models into the viewer template
(`atlas-pilot.html` is the template; `atlas.html` is the built output):

```bash
python build_atlas.py --html atlas-pilot.html --models ./models --out atlas.html
```

Options: `--manifest` (order/labels), `--lookup` (teaching-note JSON injected as the
viewer's `LOOKUP` table).

## Data sources & licences

| Layer | Source | Licence |
|---|---|---|
| Craniospinal specimen | BodyParts3D, DBCLS | CC BY-SA |
| SPL-PNL brain (328 structures) | Surgical Planning Lab / PNL, Brigham & Women's Hospital | 3D Slicer licence; cite SPL |
| SPL Head & Neck CT (59 structures) | Jakab & Kikinis, SPL; CT from the MANIX/OsiriX dataset | 3D Slicer licence, part B |
| HCP-MMP parcellation (424 areas) | HCPex (Huang et al.); HCP-MMP1 (Glasser et al. 2016) | see source repo |
| White-matter tracts (20 bundles) | JHU ICBM-DTI-81 (Mori/Hua/Wakana), via FSL | research / educational |
| Arterial territories (32) | Liu et al., *Scientific Data* 2023, doi:10.1038/s41597-022-01923-0 | CC BY-SA 4.0 |
| Cytoarchitecture (121 areas) | Jülich histological atlas (Eickhoff et al.), via FSL | **non-commercial** |
| MNI brain shell | ICBM152 2009c | see MNI terms |
| GBM cases | UPenn-GBM (Bakas et al., *Sci Data* 2022;9:453), TCIA | CC BY 4.0 |
| Molecular glioma cases | UCSF-PDGM (Calabrese et al.), TCIA, doi:10.7937/tcia.bdgf-8v37 | CC BY 4.0 |
| Vestibular schwannoma | Vestibular-Schwannoma-SEG (Shapey, Kujawa et al.), TCIA | CC BY 4.0 |
| Spinal metastasis | Spine-Mets-CT-SEG, TCIA | CC BY 4.0 |

Several datasets are **CC BY-SA**, so derived model files and this page inherit
share-alike obligations: keep the attribution visible and redistribute under compatible
terms. The **Jülich** layer is non-commercial — remove it if you publish commercially.

### Patient data

All patient-derived specimens come from open, de-identified, de-faced collections.
Only skull-stripped brain surfaces and derived lesion meshes are redistributed — never a
full head surface. The vestibular schwannoma dataset's patient skull contour was
deliberately excluded for the same reason.

Descriptive text is original, written with reference to Youmans & Winn *Neurological
Surgery* (8th ed.), Figueiredo (ed.) *Brain Anatomy and Neurosurgical Approaches*,
Kobayashi *Neurosurgery of Complex Vascular Lesions and Tumors*, and the WHO
Classification of CNS Tumours (5th ed., 2021). No text is reproduced from those works.

## Code licence

Viewer and build script: MIT (see `LICENSE`). Anatomical and patient-derived model files
retain their own licences — see the table above and `NOTICE`.
