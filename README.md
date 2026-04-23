# Mirror Fractal Codec

Lossless compression for neuromorphic event-camera data (DVS/ATIS).

[![PyPI](https://img.shields.io/pypi/v/mfc-codec.svg)](https://pypi.org/project/mfc-codec/)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://pypi.org/project/mfc-codec/)
[![License](https://img.shields.io/badge/license-Proprietary-red.svg)](LICENSE)
[![DOI](https://img.shields.io/badge/DOI-pending-lightgrey.svg)](#citation)

**1.51 bits/event** · **47.6× compression** · **0.55 ms per N-MNIST sample**

*Patent Pending — US Provisional #64/034,974 (filed 10 April 2026).*

> **Note** — this is the public mirror for docs, examples, and issue tracking.
> The Rust source and build pipeline stay private pending the patent grant.
> Install the compiled codec via `pip install mfc-codec`. Bit-exact round-trip
> is verified in the browser demo (original vs. decoded dual-canvas) and in
> the CLI; the Python binding currently exposes the encode + dataset-loader
> surface.

---

## Install

```bash
pip install mfc-codec
```

Pre-built CPython 3.11 wheels:

- Linux — `manylinux_2_34` x86_64
- macOS — `arm64` (Apple Silicon)
- Windows — `amd64`

## Live demo

**https://codec.mirrorfractal.com** — drop a `.bin` / `.aedat` / `.h5` / `.npy` / `.csv` file; it compresses in the browser via WASM, plays back dual-canvas (original vs. decoded, bit-exact).

## Quick start

```python
import mfc

# auto-detect format (.bin, .aedat, .h5/.hdf5, .npy, .evb, .csv, .dat, .raw)
events = mfc.load_events("sample.bin")
# ...or use a format-specific loader: mfc.load_nmnist / load_aedat2 / load_csv

compressed, stats = mfc.compress(
    events,
    width=34, height=34,
    time_bins=16, max_depth=8,
)
print(f"{stats.compression_ratio:.1f}× · {stats.bits_per_event:.2f} bpe "
      f"({stats.encode_us/1000:.2f} ms)")
```

`CompressionResult` fields: `n_events`, `raw_bytes`, `bitstream_bytes`, `n_bits`,
`encode_us`, `decode_us`, `sparsity`, plus computed properties
`compression_ratio` and `bits_per_event`.

See [`examples/`](examples/) for N-MNIST benchmarking and DSEC HDF5 loading.

## Benchmarks

### N-MNIST — 60,000 real samples, 34×34 sensor

| Digit | Samples | Avg events | Ratio | bpe | Encode |
|-------|---------|------------|-------|-----|--------|
| 0     | 5,923   | 5,444      | 53.4× | 1.35 | 0.65 ms |
| 1     | 6,742   | 2,432      | 36.6× | 1.97 | 0.42 ms |
| 2     | 5,958   | 4,708      | 50.3× | 1.43 | 0.58 ms |
| 3     | 6,131   | 4,703      | 50.4× | 1.43 | 0.58 ms |
| 4     | 5,842   | 3,794      | 44.4× | 1.62 | 0.54 ms |
| 5     | 5,421   | 4,372      | 48.7× | 1.48 | 0.56 ms |
| 6     | 5,918   | 4,215      | 47.7× | 1.51 | 0.55 ms |
| 7     | 6,265   | 3,687      | 45.2× | 1.59 | 0.52 ms |
| 8     | 5,851   | 4,702      | 50.0× | 1.44 | 0.58 ms |
| 9     | 5,949   | 3,927      | 46.1× | 1.56 | 0.52 ms |
| **Total** | **60,000** | **4,172** | **47.6×** | **1.51** | **0.55 ms** |

### High-resolution synthetic

| Config       | Events | Raw       | Compressed | Ratio   | Encode |
|--------------|--------|-----------|------------|---------|--------|
| DVS128 100K  | 100K   | 879 KB    | 2.1 KB     | 424×    | 1.8 ms |
| DVS128 500K  | 500K   | 4,395 KB  | 3.9 KB     | 1,117×  | 4.9 ms |
| QVGA 200K    | 200K   | 1,758 KB  | 7.6 KB     | 232×    | 7.0 ms |
| VGA 500K     | 500K   | 4,395 KB  | 10.2 KB    | 430×    | 18.2 ms |
| VGA 2M       | 2M     | 17,578 KB | 20.0 KB    | 878×    | 36.9 ms |
| HD 1M        | 1M     | 8,789 KB  | 8.5 KB     | 1,040×  | 58.2 ms |

### DSEC (automotive, 640×480)

500,000-event window compresses at **9.2×** / **7.85 bpe**, bit-exact round-trip verified.

## Supported formats

| Format    | Extension       | Loader                  |
|-----------|-----------------|-------------------------|
| N-MNIST   | `.bin`          | `mfc.load_nmnist`       |
| AEDAT 2.0 | `.aedat`        | `mfc.load_aedat2`       |
| DSEC HDF5 | `.h5`, `.hdf5`  | `mfc.load_events`       |
| NumPy     | `.npy`          | `mfc.load_events`       |
| Prophesee | `.evb`          | `mfc.load_events`       |
| CSV/Text  | `.csv`, `.txt`  | `mfc.load_csv`          |
| Raw DAT   | `.dat`, `.raw`  | `mfc.load_events`       |

`mfc.load_events(path)` auto-detects the format from the file extension.

## `.mfx` container

Binary container with `MFX1` magic header, multi-frame support, independently decodable frames (random access + parallel decode). See [`docs/formats.md`](docs/formats.md) for the byte layout.

## Contents

```
codec/
├── README.md
├── LICENSE            Proprietary + Patent Pending
├── CITATION.cff
├── examples/
│   ├── quickstart.py        encode a single sample, print stats
│   ├── nmnist_benchmark.py  aggregate stats across the 60k N-MNIST train set
│   └── dsec_load.py         load a DSEC HDF5 recording and encode a window
└── docs/
    └── formats.md     supported input formats and .mfx header
```

## Citation

```bibtex
@software{mfc_codec_2026,
  author  = {Solonskii, Aleksei},
  title   = {Mirror Fractal Codec: Lossless Compression for Neuromorphic Event Camera Streams},
  year    = {2026},
  version = {0.3.28},
  doi     = {ZENODO_DOI_PENDING},
  url     = {https://codec.mirrorfractal.com}
}
```

Machine-readable citation: [`CITATION.cff`](CITATION.cff).

## License

Proprietary — all rights reserved. Patent Pending US 64/034,974.
Binary distributions on PyPI are available under the same proprietary terms
for evaluation and academic use. Commercial licensing inquiries:
**info@mirrorfractal.com**.
