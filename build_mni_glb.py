#!/usr/bin/env python3
"""
build_mni_glb.py — convert any open-access MNI152 NIfTI segmentation or
probabilistic atlas (e.g. VENAT 7T veins, CIT168 subcortical nuclei, Harvard AAN
/ Brainstem Navigator, SUIT cerebellar nuclei, PAM50 cord, TopCoW, BraTS) into
a co-registered `.glb` layer ready for `manifest.json` -> `overlay.layers`.

Coordinate convention (matches `FRAME = {ref: [0, 5, 17.5], scale: 0.0494}` in
`atlas-pilot.html` and `mni_shell.glb` / `tracts_hcp1065_*.glb`):
    viewer_x = (mni_x - 0.0)  * 0.0494
    viewer_y = (mni_z - 5.0)  * 0.0494
    viewer_z = (-mni_y - 17.5) * 0.0494

Requirements (install in a separate Python env when building new GLB layers):
    pip install nibabel numpy scikit-image trimesh fast-simplification

Examples
--------
1) Probabilistic continuous NIfTI volume (e.g. VENAT 7T venous density map):
    python build_mni_glb.py --nifti VENAT_DensityMap.nii.gz --threshold 0.18 \\
        --name "Cerebral venous system (VENAT 7T)" --color "#3c6fd6" --out venat_veins.glb

2) Multi-label discrete parcellation NIfTI + JSON/CSV label table (e.g. CIT168 / SUIT):
    python build_mni_glb.py --nifti CIT168_MNI152.nii.gz --labels cit168_labels.json \\
        --out cit168_nuclei.glb
"""
import argparse
import json
import sys
from pathlib import Path

FRAME_REF = (0.0, 5.0, 17.5)
FRAME_SCALE = 0.0494


def hex_to_rgba(hex_str: str) -> list[int]:
    h = hex_str.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return [int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), 255]


def mni_ras_to_viewer(verts_ras, np):
    """Map MNI152 RAS (mm) vertex array (N, 3) into the atlas MNI overlay frame."""
    out = np.empty_like(verts_ras, dtype=np.float32)
    out[:, 0] = (verts_ras[:, 0] - FRAME_REF[0]) * FRAME_SCALE
    out[:, 1] = (verts_ras[:, 2] - FRAME_REF[1]) * FRAME_SCALE
    out[:, 2] = (-verts_ras[:, 1] - FRAME_REF[2]) * FRAME_SCALE
    return out


def extract_surface(vol, affine, level: float, smooth_iters: int, target_faces: int, np, measure, trimesh):
    verts_ijk, faces, _, _ = measure.marching_cubes(vol, level=level)
    ones = np.ones((verts_ijk.shape[0], 1), dtype=np.float64)
    verts_ras = (affine @ np.hstack([verts_ijk, ones]).T).T[:, :3]
    # Ensure outward winding if affine has negative determinant (radiological LAS)
    if np.linalg.det(affine[:3, :3]) < 0:
        faces = faces[:, [0, 2, 1]]
    mesh = trimesh.Trimesh(vertices=verts_ras, faces=faces, process=True)
    if smooth_iters > 0:
        trimesh.smoothing.filter_taubin(mesh, iterations=smooth_iters)
    if target_faces and len(mesh.faces) > target_faces:
        try:
            mesh = mesh.simplify_quadric_decimation(face_count=target_faces)
        except Exception:
            pass
    # Transform RAS -> viewer coordinates (note: y/z swap + -y reflection is proper rotation det=+1)
    mesh.vertices = mni_ras_to_viewer(mesh.vertices, np)
    return mesh


def main():
    ap = argparse.ArgumentParser(description="Convert MNI152 NIfTI atlas to co-registered GLB.")
    ap.add_argument("--nifti", required=True, help="Input .nii or .nii.gz in MNI152 space")
    ap.add_argument("--out", required=True, help="Output .glb path")
    ap.add_argument("--threshold", type=float, default=0.25, help="Iso-surface threshold for probabilistic map")
    ap.add_argument("--name", default="MNI structure", help="Mesh name when converting a single volume")
    ap.add_argument("--color", default="#4a90d9", help="Hex colour for single-volume mode")
    ap.add_argument(
        "--labels",
        default=None,
        help='JSON mapping label integer -> {"name": "...", "color": "#rrggbb"} for discrete atlases',
    )
    ap.add_argument("--smooth", type=int, default=10, help="Taubin smoothing iterations (default: 10)")
    ap.add_argument("--max-faces", type=int, default=25000, help="Target max faces per structure (default: 25000)")
    args = ap.parse_args()

    try:
        import nibabel as nib
        import numpy as np
        from skimage import measure
        import trimesh
    except ImportError as exc:
        sys.exit(
            f"Missing dependency ({exc}). Install with:\n"
            "  pip install nibabel numpy scikit-image trimesh fast-simplification"
        )

    img = nib.load(args.nifti)
    img = nib.as_closest_canonical(img)  # ensure RAS+ orientation
    data = img.get_fdata(dtype=np.float32)
    affine = img.affine

    scene = trimesh.Scene()
    if args.labels:
        spec = json.loads(Path(args.labels).read_text(encoding="utf-8"))
        for k_str, meta in spec.items():
            lbl_id = int(k_str)
            mask = (np.rint(data) == lbl_id).astype(np.float32)
            if mask.sum() < 8:
                continue
            nm = meta["name"] if isinstance(meta, dict) else str(meta)
            col = meta.get("color", args.color) if isinstance(meta, dict) else args.color
            mesh = extract_surface(mask, affine, 0.5, args.smooth, args.max_faces, np, measure, trimesh)
            mesh.visual.vertex_colors = np.tile(hex_to_rgba(col), (len(mesh.vertices), 1))
            mesh.metadata["name"] = nm
            scene.add_geometry(mesh, node_name=nm, geom_name=nm)
            print(f"  + {nm:<42s} {len(mesh.vertices):6,d} verts  {len(mesh.faces):6,d} faces")
    else:
        mesh = extract_surface(data, affine, args.threshold, args.smooth, args.max_faces, np, measure, trimesh)
        mesh.visual.vertex_colors = np.tile(hex_to_rgba(args.color), (len(mesh.vertices), 1))
        mesh.metadata["name"] = args.name
        scene.add_geometry(mesh, node_name=args.name, geom_name=args.name)
        print(f"  + {args.name:<42s} {len(mesh.vertices):6,d} verts  {len(mesh.faces):6,d} faces")

    out_path = Path(args.out)
    out_path.write_bytes(scene.export(file_type="glb"))
    print(f"\nWrote {out_path} ({out_path.stat().st_size / 1024:.1f} KB)")


if __name__ == "__main__":
    main()
