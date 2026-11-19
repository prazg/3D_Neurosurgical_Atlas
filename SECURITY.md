# Security & Clinical Safety Policy

## Educational Non-Clinical Scope

The **Advanced 3D Surgical Anatomy Atlas — Brain & Spine** is an open-source teaching resource built from open, de-identified, and de-faced anatomical and imaging datasets.

- **Not a medical device:** Must never be used for clinical diagnosis, patient counselling, stereotactic targeting, operative planning, or surgical navigation.
- **Approximate geometry:** Craniotomy footprints, burr-hole entry points, working corridors, 3D caliper measurements (`mm` / `ΔR/A/S`), and registered tracts/vessels are schematic teaching approximations.
- **De-identified data:** No patient-identifiable surfaces (scalp/face) are included. If you believe any redistributed mesh raises a privacy or de-identification concern, report it immediately via the channel below.

## Supported Versions

Security, dependency-integrity (SRI), and data-safety fixes are applied to the latest `main` branch deployed to GitHub Pages:

| Branch / Release | Supported |
| --- | --- |
| `main` (latest GitHub Pages build) | Yes |
| Older commits / forks | Best-effort — update to `main` |

## Security Architecture Notes

- Static client-side WebGL application (`index.html`, `atlas.html`, `mobile.html`) with no backend server, user authentication, or patient data upload to external servers (local `+ .glb` files are parsed strictly in-browser via `FileReader` and never leave the user's device).
- Third-party CDN scripts (`three.min.js` and `GLTFLoader.js` r128) are pinned with SHA-384 Subresource Integrity (`integrity="sha384-..."`), `crossorigin="anonymous"`, and `referrerPolicy="no-referrer"`.
- Runtime asset paths from `manifest.json`, `figures.json`, and `rhoton.json` are restricted by strict allowlist validators (`safeFile`, `safeJson`, `safeImg`, `rhSafe`), and DOM updates use `textContent` / safe DOM constructors rather than untrusted `innerHTML`.

## Reporting a Vulnerability or Data Concern

Please report security vulnerabilities (such as XSS, Subresource Integrity issues, or supply-chain concerns) or dataset attribution/de-identification concerns privately via **GitHub Security Advisories** on [`prazg/3D_Neurosurgical_Atlas`](https://github.com/prazg/3D_Neurosurgical_Atlas/security/advisories/new) before opening a public issue.

We aim to acknowledge reports within **7 days** and publish a fix or mitigation to `main` promptly once verified.
