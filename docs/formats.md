# Supported input formats

Every common neuromorphic dataset format is recognised. Pick the
format-specific loader when you know what you have, or let
`mfc.load_events(path)` auto-detect from the extension.

## N-MNIST — `.bin`

Classic Orchard 2015 format. Fixed 5 bytes per event (`x`, `y`, 3-byte
`polarity|timestamp` big-endian).

```python
events = mfc.load_nmnist(path)
# or
events = mfc.load_events(path)
```

## AEDAT 2.0 — `.aedat`

jAER format, 8 bytes per event, big-endian. MFC parses the ASCII
comment header, then splits each 32-bit address into `(x, y, polarity)`
per the DVS spec.

```python
events = mfc.load_aedat2(path)
```

## DSEC — `.h5` / `.hdf5`

Gehrig 2021. Events under `/events/{x, y, t, p}`. MFC transparently
handles Blosc + LZ4 + zstd HDF5 filter plugins (bundled into the
browser build; the Python binding uses the system HDF5 library, install
the filters separately if missing).

```python
events = mfc.load_events(path)
```

See [`examples/dsec_load.py`](../examples/dsec_load.py) for window-sliced
loading via `h5py`.

## NumPy — `.npy`

Structured arrays or plain 2-D `(x, y, t, p)` tables. MFC ranks the
columns by value range to auto-identify which axis is which — works
on Prophesee-style `(t, x, y, p)` as well as `(x, y, t, p)`.

```python
events = mfc.load_events(path)
```

## Prophesee — `.evb`

Event-based binary with 32-bit address + 32-bit timestamp, little-endian.

```python
events = mfc.load_events(path)
```

## CSV / text — `.csv`, `.txt`

Four columns `x, y, t, p`, separator auto-detected (`,`, tab,
whitespace). Header row optional.

```python
events = mfc.load_csv(path)
```

## Raw DAT / RAW — `.dat`, `.raw`

32-bit packed events, legacy DAVIS format.

```python
events = mfc.load_events(path)
```

---

## Building events manually

```python
import mfc

events = [
    mfc.Event(10, 20, 1_000, 1),
    mfc.Event(11, 20, 1_010, 0),
    # ...
]
compressed, stats = mfc.compress(
    events, width=34, height=34, time_bins=16, max_depth=8,
)
```

## `.mfx` container layout

MFC's output container. 15-byte header:

| Offset | Size | Field                          |
|--------|------|--------------------------------|
| 0      | 4    | Magic `MFX1` (ASCII)            |
| 4      | 2    | Format version (u16 LE)         |
| 6      | 2    | Sensor width (u16 LE)           |
| 8      | 2    | Sensor height (u16 LE)          |
| 10     | 2    | Temporal resolution (u16 LE)    |
| 12     | 1    | Encoder level (u8)              |
| 13     | 2    | Number of frames (u16 LE)       |

Each frame is independently decodable — random access and parallel
decode are supported by design.

## `CompressionResult` fields

The second value returned from `mfc.compress(...)` / `compress_sequence(...)`:

| Attribute            | Meaning                                         |
|----------------------|-------------------------------------------------|
| `n_events`           | number of input events                          |
| `raw_bytes`          | equivalent size at `n_events × 5` (N-MNIST) or sensor-specific baseline |
| `bitstream_bytes`    | compressed payload size                         |
| `n_bits`             | bit count of the compressed payload             |
| `encode_us`          | wall-clock encode time (microseconds)           |
| `decode_us`          | wall-clock decode time (microseconds, CLI path) |
| `sparsity`           | fraction of empty cells in the spatiotemporal grid |
| `compression_ratio`  | `raw_bytes / bitstream_bytes` (property)        |
| `bits_per_event`     | `bitstream_bytes × 8 / n_events` (property)     |
