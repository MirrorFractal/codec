# Changelog

All notable changes to Mirror Fractal Codec are documented here.

Format: [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/).
SemVer: pre-1.0, minor releases may break API, patch releases stay compatible.

## [Unreleased]

## [0.3.29] — 2026-05-19

### Fixed
- `requires-python` raised to `>=3.11` to match the cp311 wheel matrix; users on
  3.8 / 3.9 / 3.10 now get a clear pip error instead of a cryptic linker failure.
- Sensor dimension cap unified at `2048` across the WASM client, the conversion
  server, the browser app, the QA harness, and the visible site copy (was a mix
  of `1280` and `2048` previously).
- Root `CITATION.cff` removed — `public/CITATION.cff` is the single source of
  truth and was already at `0.3.28` while the root copy lagged at `0.3.27`.

### Changed
- Server CORS default tightened to `https://codec.mirrorfractal.com`; override
  at run time via `MFC_ALLOWED_ORIGINS` for local dev or alternate frontends.
- WASM release profile strips debug info and the producers section, and runs
  `wasm-opt -Oz --strip-debug --strip-producers --vacuum` after build.

### Security
- New `scripts/ip_audit_public.sh` enforces a hard-ban + review list against the
  `public/` mirror tree; wired into a pre-push git hook (`.githooks/pre-push`).
- WASM build pipeline rejects any leaked Rust source paths or sensitive symbol
  names before the artifact is shipped.
- `scripts/scrub_wheel.py` now verifies wheels are clean of sensitive patterns
  after substitution rather than trusting the substitution alone.

## [0.3.28] — 2026-04-23

### Added
- DSEC automotive (640×480) dataset validation.
- Python bindings via PyO3 0.23.
- WASM `compress_auto()` entry point that detects format from filename.
- Server-side HDF5 conversion endpoint (`server/app.py`).
- Zenodo deposit with DOI `10.5281/zenodo.19704064`.

### Security
- US Provisional patent #64/034,974 filed 2026-04-10.

## [Pre-0.3.28]

Versions before 0.3.28 were published to PyPI without matching git tags.
See <https://pypi.org/project/mfc-codec/#history> for the archive.

[Unreleased]: https://github.com/MirrorFractal/codec/compare/v0.3.29...HEAD
[0.3.29]: https://github.com/MirrorFractal/codec/releases/tag/v0.3.29
[0.3.28]: https://github.com/MirrorFractal/codec/releases/tag/v0.3.28
