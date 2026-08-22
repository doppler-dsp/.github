# doppler-dsp/.github

Org-level GitHub configuration for [doppler-dsp](https://github.com/doppler-dsp).
Nothing here is part of the library — the code lives in
[doppler-dsp/doppler](https://github.com/doppler-dsp/doppler).

## What is in here

| path | what it does |
|------|--------------|
| `profile/README.md` | The **organization profile page** — what you see at [github.com/doppler-dsp](https://github.com/doppler-dsp). GitHub reads it from this exact path in a repo named `.github`; that is why it is in a subfolder and not this file. |
| `scripts/sync_readme.py` | Regenerates `profile/README.md` from doppler's own `README.md`. |
| `.github/workflows/sync-readme.yml` | Runs that script on a schedule. |
| `LICENSE` | MIT, matching the library. |

## The profile README is generated — do not hand-edit it

`profile/README.md` is a rewritten copy of
[doppler's `README.md`](https://github.com/doppler-dsp/doppler/blob/main/README.md),
which is itself generated from `docs/index.md`. Edits made here are silently
overwritten the next time the sync runs.

To change what the org page says, edit the readme-sync region of
`docs/index.md` in the doppler repo and run `make docs-relink` there.

The sync exists because the profile page cannot use doppler's relative links:
a profile README does not get repo-relative link resolution the way a repo's
own README does, so every relative target has to be rewritten to an absolute
`https://github.com/doppler-dsp/doppler/blob/main/...` URL. It polls on a
schedule rather than reacting to a push, because the source lives in another
repo and polling avoids needing a cross-repo write token.

## Why this file exists

The repo had no root README, so anyone opening it saw a bare file listing and
no way to tell that `profile/README.md` is the org profile rather than a
stray document — or that editing it directly would be undone.
