"""
All-Integer Game of Life with Streaming GIF Output

This script simulates Conway’s Game of Life on an N×N grid using only integer
operations and memory-lean downsampling. It writes frames directly to disk via
matplotlib’s PillowWriter, avoiding large in-memory histories.

Functions:
- life_step_int: Compute the next generation using integer arrays.
- simulate_and_animate: Run the simulation, stream frames to a GIF.
- main: CLI entry point; parses arguments, times execution, reports resource usage.
"""


# ─────────────────────────────────────────────────────────────────────────────
# Library imports
# ─────────────────────────────────────────────────────────────────────────────
import argparse
import time
import resource
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from tqdm import tqdm


# ─────────────────────────────────────────────────────────────────────────────
# 1) Core update function (all-integer)
# ─────────────────────────────────────────────────────────────────────────────

def life_step_int(grid: np.ndarray, neighbours: np.ndarray) -> np.ndarray:
    """
    Compute one generation of Conway’s Game of Life on an integer grid.

    This function uses a reusable neighbours buffer to minimize allocations.
    All arrays are dtype uint8 (0 or 1).

    Args:
        grid (np.ndarray): 2D uint8 array of shape (N, N) with 0 or 1.
        neighbours (np.ndarray): 2D uint8 array of same shape, used as scratch.

    Returns:
        np.ndarray: New 2D uint8 array for the next generation.
    """
    neighbours.fill(0)
    for dx, dy in (
        (-1, -1), (-1, 0), (-1, 1),
        ( 0, -1),          ( 0, 1),
        ( 1, -1), ( 1, 0), ( 1, 1),
    ):
        neighbours += np.roll(np.roll(grid, dx, axis=0), dy, axis=1)
    # birth on exactly 3 neighbours; survive if alive and exactly 2 neighbours
    return ((neighbours == 3) | ((grid == 1) & (neighbours == 2))).astype(np.uint8)

# ─────────────────────────────────────────────────────────────────────────────
# 2) Simulation & streaming animation
# ─────────────────────────────────────────────────────────────────────────────


def simulate_and_animate(N: int, timesteps: int, p_alive: float, output_file: Path, interval_ms: int = 200, max_display: int = 2000, dpi: int = 80):
    """
    Run the Game of Life simulation and stream frames to a GIF file.

    Initializes a random grid, downsamples for display if N > max_display,
    and writes each frame directly to disk.

    Args:
        N (int): Grid dimension (N × N).
        timesteps (int): Number of generations to simulate.
        p_alive (float): Probability that a cell starts alive (0–1).
        output_file (Path): Path to the output GIF.
        interval_ms (int): Frame duration in milliseconds.
        max_display (int): Maximum display side length; grid is downsampled
                           by step = max(1, N // max_display).
        dpi (int): Resolution of the saved GIF.
    """
    # ─── Initialize full-size grid & neighbour buffers ─────────────────────────
    rng = np.random.default_rng()
    grid = np.empty((N, N), dtype=np.uint8)
    thresh = int(p_alive * 1_000_000)
    for i in range(N):
        row = rng.integers(0, 1_000_000, size=N, dtype=np.int32)
        grid[i, :] = (row < thresh).astype(np.uint8)
    neighbours = np.zeros((N, N), dtype=np.uint8)

    # ─── Compute downsample step so display ≤ max_display×max_display ──────────
    step = 1 if max_display is None or max_display >= N else max(1, N // max_display)

    # ─── Set up Matplotlib figure/axes (edge-to-edge, no border) ──────────────
    fig = plt.figure(figsize=(6, 6), frameon=False)
    fig.patch.set_visible(False)
    ax = fig.add_axes([0, 0, 1, 1], frameon=False)
    ax.set_axis_off()
    small = grid[::step, ::step]
    im = ax.imshow(small, cmap='binary', vmin=0, vmax=1)

    # ─── Set up streaming PillowWriter ─────────────────────────────────────────
    writer = animation.PillowWriter(fps=1000/interval_ms)
    writer.setup(fig, str(output_file), dpi=dpi)

    # ─── Main loop with tqdm ──────────────────────────────────────────────────
    for _ in tqdm(range(timesteps), desc="Simulating & writing GIF"):
        small = grid[::step, ::step]
        im.set_data(small)
        writer.grab_frame()       # streams frame straight to disk
        grid = life_step_int(grid, neighbours)

    writer.finish()
    plt.close(fig)

def main():
    p = argparse.ArgumentParser("Game of Life (all-int, streaming GIF, memory-lean)")
    p.add_argument("--size",        type=int,   default=100,   help="Grid dimension (N×N)")
    p.add_argument("--timesteps",   type=int,   default=50,    help="Number of generations")
    p.add_argument("--p-alive",     type=float, default=0.2,   help="Initial alive probability (0–1)")
    p.add_argument("--output",      type=Path,  default=Path("game_of_life.gif"),
                   help="Output GIF filename")
    p.add_argument("--interval",    type=int,   default=200,   help="Frame duration in ms")
    p.add_argument("--max-display", type=int,   default=2000,
                   help="Max side length for display (downsampling factor)")
    args = p.parse_args()

    print(f"[All-int Matplotlib] size={args.size}, timesteps={args.timesteps}, p_alive={args.p_alive}")

    # start wall-clock & CPU timing
    start_wall = time.perf_counter()
    rstart     = resource.getrusage(resource.RUSAGE_SELF)

    simulate_and_animate(
        N=args.size,
        timesteps=args.timesteps,
        p_alive=args.p_alive,
        output_file=args.output,
        interval_ms=args.interval,
        max_display=args.max_display
    )

    # end timing and read resource usage
    end_wall = time.perf_counter()
    rend     = resource.getrusage(resource.RUSAGE_SELF)

    elapsed   = end_wall - start_wall
    cpu_user  = rend.ru_utime - rstart.ru_utime
    cpu_system= rend.ru_stime - rstart.ru_stime
    peak_rss  = rend.ru_maxrss      # on Linux: kilobytes
    peak_mb   = peak_rss / 1024

    print(f"Saved GIF to {args.output}\n")
    print("=== Resource usage ===")
    print(f"Wall-clock time : {elapsed:.2f} s")
    print(f"CPU time         : user {cpu_user:.2f} s, system {cpu_system:.2f} s")
    print(f"Peak memory (RSS): {peak_mb:.2f} MB")

if __name__ == "__main__":
    main()
