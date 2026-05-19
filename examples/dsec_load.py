"""Load a DSEC HDF5 recording (Gehrig 2021, 640x480 automotive events)
and compress a window with MFC.

    pip install mfc-codec h5py
    python examples/dsec_load.py path/to/events.h5 [window_size]

The Python binding accepts any file `mfc.load_events(path)` recognises
(which includes DSEC HDF5), so you can skip the manual h5py hop for the
common case. This script shows the explicit path for subset-loading.
"""

from __future__ import annotations

import sys

import h5py
import mfc


def main(path: str, window: int = 500_000) -> None:
    # Explicit slicing via h5py so we can pick an arbitrary window.
    with h5py.File(path, "r") as f:
        # DSEC layout: /events/{x, y, t, p} as separate datasets.
        xs = f["events/x"][:window]
        ys = f["events/y"][:window]
        ts = f["events/t"][:window]
        ps = f["events/p"][:window]

    events = [
        mfc.Event(int(x), int(y), int(t), int(p))
        for x, y, t, p in zip(xs, ys, ts, ps)
    ]
    print(f"loaded {len(events):,} events from {path}")

    _, stats = mfc.compress(
        events,
        width=640, height=480,
        time_bins=32, max_depth=16,
    )
    print(
        f"  ratio  {stats.compression_ratio:.2f}x\n"
        f"  bpe    {stats.bits_per_event:.2f}\n"
        f"  encode {stats.encode_us / 1000:.2f} ms"
    )


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("usage: dsec_load.py <events.h5> [window_size]")
    window = int(sys.argv[2]) if len(sys.argv) > 2 else 500_000
    main(sys.argv[1], window)
