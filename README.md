# Advanced 3D Surgical Anatomy Atlas — Brain & Spine

Created and compiled by **Prajwal Ghimire**

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
- **SPL-PNL brain**: 327 expert-segmented MRI structures, down to individual gyri
  (the atlas's outer skin surface is removed; head and neck muscles start hidden).
- **SPL Head & Neck CT**: skull, mandible, cervical spine, ribs, neck muscles, cartilage,
  glands, and vessels (carotids, vertebrals, subclavians, jugulars) — plus six schematic
  **craniotomy footprints** projected onto the skull surface (pterional, retrosigmoid,
  midline suboccipital, far-lateral/transcondylar, frontal Kocher flap, subtemporal).
- **Co-registered MNI overlay**: translucent brain shell with the HCP-1065 population tractography atlas
  (87 bundles in two layers: association tracts and cranial nerves on by default; projection,
  commissural and cerebellar tracts off), the original 20 JHU tracts, arterial
  territories, HCP-MMP parcellation, Jülich cytoarchitecture and schematic ventricular
  entry points (Kocher, Keen, Frazier, Dandy), each independently toggleable.

**Skull and craniometric keypoints**

- **Skull bones specimen** (BodyParts3D): 20 individually coloured cranial and facial bones with
  suture bands (coronal, sagittal, lambdoid, squamous, sphenoparietal, sphenofrontal,
  sphenosquamosal, occipitomastoid, frontozygomatic, frontonasal) computed from where the bones meet.
- **17 craniometric keypoints** computed from bone junctions: bregma, lambda, nasion, glabella, inion,
  opisthion, basion, and pterion, asterion, frontozygomatic suture, MacCarty keyhole (placed by the
  classic 1 cm rule) and mastoid tip on each side.
- **Cortical surface projections** on the approaches specimen: superior and inferior Rolandic points
  and anterior and posterior Sylvian points on both sides, computed from that model's gyri.

**Learning tools**: *Labels* (decluttered on-model labels), *Quiz* (Find-it and Name-it self-test on
whatever is shown, with side-aware feedback), double-click or pick from a list to fly the camera to a
structure, *3D* red-cyan anaglyph stereo, and *VR* on WebXR headsets (button appears only when supported).
Approach cards include *Watch and learn* links to free external lecture and video collections.

**Fibre dissection walkthrough (BraDiPho)**

- **Klingler fibre dissection, left hemisphere** — twelve photogrammetric 3D models of a real
  fibre dissection (BraDiPho specimen 19), from intact cortex through sulcal decortication, the
  posterior transverse system, the SLF and arcuate fasciculus, removal of the opercula and insula,
  the frontal, occipital and temporal projections of the ventral system, to the lentiform nucleus
  and the stem of the ventral system. Opens as a 12-step walkthrough.
- The dissectors' manual annotations of the exposed superior longitudinal system (stages 4–6) are
  painted onto the specimen surface, and 16 tractography bundles (HCP842 and SCIL atlases,
  registered to the specimen by the BraDiPho team) appear with the matching stage. *Ghost specimen*
  and *Show all tracts* let you compare dissected fibres with tractography.

**Guided surgical approaches (teaching)**

- **Approaches specimen** — a composite head built for approach teaching: the SPL Head & Neck CT
  skull, neck vessels and cervical spine; the SPL-PNL brain registered into that skull (affine fit
  to the inner table, a smooth radial warp, then a local correction that keeps every structure
  inside the cranial cavity); HCP-1065 tracts and cranial nerves and intracranial arteries from a CC0 MRA atlas
  (Mouches & Forkert 2019) mapped from MNI space; schematic dural venous sinuses.
- **34 guided approaches** with step-by-step cards, a surgeon's-view camera, progressive reveal
  (incision → bone opening → corridor/trajectory) and highlighted structures at risk:
  - *Cranial:* pterional, orbitozygomatic, supraorbital keyhole, bifrontal subfrontal, anterior
    interhemispheric transcallosal, subtemporal, retrosigmoid, midline suboccipital/telovelar,
    far-lateral, supracerebellar infratentorial.
  - *Skull base & endoscopic:* endoscopic transsphenoidal, extended transplanum/transtuberculum,
    transclival, anterior petrosal (Kawase), presigmoid retrolabyrinthine, translabyrinthine, transcochlear.
  - *Ventricular & functional:* EVD at Kocher point, Keen, Frazier and Dandy points, ETV, and DBS
    trajectories to STN, GPi and Vim.
  - *Spinal:* ACDF C5–C6, C5 corpectomy, C1–C2 posterior fixation (Goel–Harms) and posterior cervical
    laminectomy with lateral mass screws (on the approaches specimen); T10–T11 pedicle screws, TLIF L4–L5, L4 laminectomy, L4–L5 pedicle screws and T9 costotransversectomy (on the
    spinal metastasis specimen).
- Content lives in `approaches.json`; deep links work as `atlas.html#approach=pterional`.
- Registration check: SPL and MNI-derived deep landmarks agree to roughly 4–10 mm in the skull
  frame; flaps, corridors, incisions, entry points and angles are schematic and illustrative.

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

**Reference illustrations** — 56 captioned 2D illustrations from Servier Medical Art (CC BY 4.0), shown under
"Illustration" when a matching structure is clicked and as "Illustrations" in each approach card (click to enlarge).
Mapping lives in `figures.json`; images in `img/smart/`.

**Lesion localisation** — 19 clinical syndrome cards in the Approaches list ("Lesion localisation"), run on the
Approaches specimen: lateral and medial medullary, Millard–Gubler, facial colliculus/Foville, locked-in, Weber,
Benedikt, Claude, Parinaud, cerebellopontine angle, Dejerine–Roussy, artery of Percheron, Foster Kennedy, cavernous
sinus, superior orbital fissure/orbital apex, Gradenigo, jugular foramen (Vernet/Collet–Sicard), Gerstmann, and uncal
herniation with the Kernohan notch. Each card steps through the lesion: structures in the lesion turn orange, a
magenta sphere marks the (schematic) lesion site, affected end-organs or spared structures are shown plainly, and
structures the atlas does not model (e.g. cranial nerve nuclei IV, VI, IX–XII, spinothalamic tract) are listed as
"not modelled" rather than drawn. Text is original and each card cites open-access sources (StatPearls / PMC).
The card format was inspired by the syndrome browser in NeuroAxis (github.com/linkbag/neuroaxis-atlas, MIT); no
text or data were copied. Teaching summaries only: real lesions rarely respect these boundaries.

**Rhoton Collection plates** — 102 cadaveric photographs (1,171 outlined structures) from the *Rhoton Collection
Top 100* slide set. Courtesy of the Rhoton Collection, American Association of Neurological Surgeons
(AANS)/Neurosurgical Research and Education Foundation (NREF). Click a structure and matching plates appear under
"Rhoton Collection"; each approach card lists the relevant plates; the **Rhoton** button opens a gallery with a
structure search. In the plate viewer you can step through every outlined structure, view the original stereo pair
side by side or as red–cyan 3D, and test yourself ("Test me"). Every plate links to the
[Rhoton Collection YouTube channel](https://www.youtube.com/@RhotonCollection) via a topic search (these are channel
searches, not hand-picked videos). Data in `rhoton.json`, images in `img/rhoton/` (each file is one stereo pair,
left eye | right eye). Watermarks are retained; images are only resized; the outlines are the slide set's own
vector outlines converted to SVG. A few source spellings were normalised (e.g. "Gryus" → "Gyrus"), and two plates
filed under "Bones of the Orbit" in the source outline are shown as temporal-bone plates because of what they label.

**Viewer features:** specimen switcher, per-layer visibility, isolate, opacity and
brightness controls, sagittal/coronal/axial cross-section with a scrub slider,
click-to-label with anatomy + surgical relevance + further reading, and an in-page
*Credits & licence* panel populated from `manifest.json`.

**Mobile version (`mobile.html`):** a phone-first edition with the same content —
specimens, guided approaches, teaching notes and illustrations — laid out for touch:
a bottom tab bar (Specimens, Approaches, Layers, Find, Tools), pull-up note cards, a
compact step card for approaches, structure search, two-finger pan and pinch zoom.
Nothing is embedded: each specimen downloads when opened (sizes shown), and overlay
layers download only when switched on. The landing page and the desktop atlas point
phone users to it; `#approach=<id>` deep links work in both versions.

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

Then regenerate the mobile edition from the built page (it reuses the same viewer
code and notes, and injects the phone UI from `mobile_layer.html`):

```bash
python build_mobile.py
```

`brain_cervical_spine.glb` is a hosted copy of the embedded core model, for the mobile page.

## Data sources & licences

| Layer | Source | Licence |
|---|---|---|
| Craniospinal specimen | BodyParts3D, DBCLS | CC BY-SA |
| SPL-PNL brain (327 structures) | Surgical Planning Lab / PNL, Brigham & Women's Hospital | 3D Slicer licence; cite SPL |
| SPL Head & Neck CT (59 structures) | Jakab & Kikinis, SPL; CT from the MANIX/OsiriX dataset | 3D Slicer licence, part B |
| HCP-MMP parcellation (424 areas) | HCPex (Huang et al.); HCP-MMP1 (Glasser et al. 2016) | see source repo |
| White-matter tracts (20 bundles) | JHU ICBM-DTI-81 (Mori/Hua/Wakana), via FSL | research / educational |
| Tracts & cranial nerves (87 bundles) | HCP-1065 tractography atlas, Yeh FC, *Nat Commun* 2022;13:4933, doi:10.1038/s41467-022-32595-4 | CC BY-SA 4.0 |
| Arterial territories (32) | Liu et al., *Scientific Data* 2023, doi:10.1038/s41597-022-01923-0 | CC BY-SA 4.0 |
| Cytoarchitecture (121 areas) | Jülich histological atlas (Eickhoff et al.), via FSL | **non-commercial** |
| MNI brain shell | ICBM152 2009c | see MNI terms |
| GBM cases | UPenn-GBM (Bakas et al., *Sci Data* 2022;9:453), TCIA | CC BY 4.0 |
| Molecular glioma cases | UCSF-PDGM (Calabrese et al.), TCIA, doi:10.7937/tcia.bdgf-8v37 | CC BY 4.0 |
| Vestibular schwannoma | Vestibular-Schwannoma-SEG (Shapey, Kujawa et al.), TCIA | CC BY 4.0 |
| Spinal metastasis | Spine-Mets-CT-SEG, TCIA | CC BY 4.0 |
| 2D reference illustrations (56) | Servier Medical Art, smart.servier.com (adapted: resized) | CC BY 4.0 |
| Fibre dissection specimen (12 stages, annotations, registered tractography) | BraDiPho, Fondazione Bruno Kessler — Vavassori et al., *Nat Commun* 2025;16:9801, doi:10.1038/s41467-025-64788-y; https://bradipho.eu | **CC BY-NC-SA 4.0** (non-commercial, share-alike) |
| Cadaveric plates (102 stereo photographs) | Rhoton Collection Top 100 — Courtesy of the Rhoton Collection, American Association of Neurological Surgeons (AANS)/Neurosurgical Research and Education Foundation (NREF); https://nref.org/education/The-Rhoton-Collection/ | Educational/media re-use with credit; **watermarks must not be removed**; commercial or non-educational use needs NREF permission |
| Skull bones specimen (20 bones), sutures and keypoints | BodyParts3D 4.0 — “BodyParts3D, © The Database Center for Life Science licensed under CC Attribution 4.0 International” (Mitsuhashi et al., *Nucleic Acids Res* 2009) — adapted | CC BY 4.0 |
| Intracranial arteries (approaches specimen) | Mouches & Forkert, *Sci Data* 2019;6:29, doi:10.1038/s41597-019-0034-5 (figshare vessel occurrence atlas) | CC0 |

Several datasets are **CC BY-SA**, so derived model files and this page inherit
share-alike obligations: keep the attribution visible and redistribute under compatible
terms. The **Jülich** layer and the **BraDiPho** dissection specimen are non-commercial — remove
them if you publish commercially. The adapted `bradipho_spc19.glb` is shared under CC BY-NC-SA 4.0.
The **Rhoton Collection** plates may be re-used only for educational or media purposes with the credit line above;
remove `img/rhoton/` and `rhoton.json` (or ask NREF) before any commercial or non-educational use.

### Patient data

All patient-derived specimens come from open, de-identified, de-faced collections.
For the TCIA pathology cases, only derived lesion meshes and a brain surface are redistributed.
The source T1 volumes are **not** skull-stripped, so the brain surface is produced by an in-house
skull strip (intensity threshold, erosion to separate scalp, largest component, merged with the
tumour segmentation) and checked by volume (~1.3 L) and by slice overlay; it contains no scalp or
face. The vestibular schwannoma dataset's patient skull contour was deliberately excluded.
The SPL Head & Neck atlas, a published SPL teaching atlas, includes a skull surface derived from
the public MANIX sample CT; it contains no skin or face surface. The SPL-PNL brain atlas's skin
surface has been removed.

Descriptive text is original, written with reference to Youmans & Winn *Neurological
Surgery* (8th ed.), Figueiredo (ed.) *Brain Anatomy and Neurosurgical Approaches*,
Kobayashi *Neurosurgery of Complex Vascular Lesions and Tumors*, and the WHO
Classification of CNS Tumours (5th ed., 2021). No text is reproduced from those works.

## Code licence

Viewer and build script: MIT (see `LICENSE`). Anatomical and patient-derived model files
retain their own licences — see the table above and `NOTICE`.
