"""Encode one N-MNIST sample and print the compression stats.

    pip install mfc-codec
    python examples/quickstart.py path/to/sample.bin
"""

from __future__ import annotations

import sys

import mfc


def main(path: str) -> None:
    events = mfc.load_events(path)  # auto-detects .bin, .aedat, .h5, .npy, .csv
    print(f"loaded {len(events):,} events from {path}")

    compressed, stats = mfc.compress(
        events,
        width=34, height=34,
        time_bins=16, max_depth=8,
    )

    print(
        f"  raw        {stats.raw_bytes:>10,} bytes\n"
        f"  compressed {stats.bitstream_bytes:>10,} bytes\n"
        f"  ratio      {stats.compression_ratio:>10.2f}x\n"
        f"  bpe        {stats.bits_per_event:>10.2f}\n"
        f"  encode     {stats.encode_us / 1000:>10.2f} ms\n"
        f"  sparsity   {stats.sparsity:>10.4f}"
    )


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: quickstart.py <sample.bin>")
    main(sys.argv[1])
