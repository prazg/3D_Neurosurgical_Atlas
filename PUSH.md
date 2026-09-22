# Pushing to GitHub

The folder contains the repository **files** but no `.git` directory — deliberately.
Git LFS must be configured **before** the first commit, otherwise the `.glb` models are
written into history as ordinary blobs and stay there permanently; `git lfs track` cannot
retroactively fix a commit that already exists.

Total: 24 files, ~111 MB (largest single file 17.7 MB — under GitHub's 50 MB warning,
but well past the point where plain Git is sensible).

## Recommended: LFS from the first commit

```bash
cd %USERPROFILE%\Documents\surgical-atlas

git init
git lfs install
git lfs track "*.glb"        # .gitattributes already contains this; this registers the hooks

git add -A
git commit -m "3D surgical anatomy atlas: anatomy, MNI overlay and pathology case libraries"

git remote add origin git@github.com:<you>/surgical-atlas.git
git branch -M main
git push -u origin main
```

Verify the models really went to LFS before you push again:

```bash
git lfs ls-files | wc -l     # expect 13
```

## Then enable GitHub Pages

Settings → Pages → deploy from `main`, root.
Live at `https://<you>.github.io/surgical-atlas/atlas.html`.

`.nojekyll` is included so Pages serves the files unprocessed.

## Notes and caveats

- **LFS bandwidth.** GitHub's free LFS quota is 1 GB storage and 1 GB/month bandwidth.
  A public teaching atlas that gets traffic will exceed the bandwidth quota, because every
  page view pulls the `.glb` files. If that happens, host the `.glb` files on object
  storage or a CDN and point `manifest.json` at them — note that the viewer's `safeFile()`
  guard currently permits same-directory filenames only, so relax it deliberately at that
  point rather than by accident.
- **Alternative to LFS:** GitHub Pages will serve plain (non-LFS) files fine, and nothing
  here exceeds 50 MB. The cost is permanent history bloat on every future model revision.
  LFS is the better default; plain Git is defensible if you never expect to revise models.
- **Jülich layer is non-commercial** (`juelich.glb`). Remove it and its `manifest.json`
  entry before any commercial publication.
- **Verify the render.** The MNI overlay alignment and the craniotomy footprint positions
  were built and validated structurally but never rendered in a browser during
  development. Open `atlas.html` and check them before teaching from it.
