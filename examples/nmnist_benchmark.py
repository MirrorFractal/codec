"""Benchmark MFC across every N-MNIST training sample, per digit.

Expects the classic N-MNIST directory layout:

    Train/0/*.bin, Train/1/*.bin, ..., Train/9/*.bin

    pip install mfc-codec
    python examples/nmnist_benchmark.py /path/to/N-MNIST/Train
"""

from __future__ import annotations

import statistics
import sys
from pathlib import Path

import mfc


def bench_digit(digit_dir: Path) -> dict:
    ratios, bpes, times = [], [], []
    samples = 0
    total_events = 0

    for bin_path in digit_dir.glob("*.bin"):
        events = mfc.load_nmnist(str(bin_path))
        _, stats = mfc.compress(
            events, width=34, height=34, time_bins=16, max_depth=8,
        )
        ratios.append(stats.compression_ratio)
        bpes.append(stats.bits_per_event)
        times.append(stats.encode_us / 1000.0)
        total_events += stats.n_events
        samples += 1

    def mean(xs):
        return statistics.mean(xs) if xs else 0.0

    return {
        "samples": samples,
        "avg_events": total_events // max(samples, 1),
        "ratio": mean(ratios),
        "bpe": mean(bpes),
        "encode_ms": mean(times),
    }


def main(root: Path) -> None:
    print(f"{'digit':>5} {'samples':>8} {'avg_events':>12} "
          f"{'ratio':>8} {'bpe':>6} {'encode':>10}")

    total_samples = 0
    for digit in range(10):
        d = root / str(digit)
        if not d.is_dir():
            print(f"{digit:>5}  (no directory {d})")
            continue
        s = bench_digit(d)
        print(
            f"{digit:>5} {s['samples']:>8,} {s['avg_events']:>12,} "
            f"{s['ratio']:>7.1f}x {s['bpe']:>6.2f} {s['encode_ms']:>8.2f} ms"
        )
        total_samples += s["samples"]

    print(f"\ntotal: {total_samples:,} samples")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: nmnist_benchmark.py <path-to-Train-dir>")
    main(Path(sys.argv[1]))
