#!/usr/bin/env python3

import argparse      # For parsing command-line arguments
import time          # For measuring wall-clock time
import resource      # For measuring CPU and memory usage
from pathlib import Path  # For convenient file path handling

import numpy as np                           # Numerical operations on arrays
import matplotlib.pyplot as plt              # Plotting figures and images
import matplotlib.animation as animation     # Creating animated GIFs
from matplotlib.colors import BoundaryNorm   # For discrete colormap normalization
from tqdm import tqdm                        # Progress bar for loops


def life_step_int(grid: np.ndarray, neighbours: np.ndarray) -> np.ndarray:
    """
    Perform a single step (generation) update for Conway's Game of Life.

    Parameters:
    - grid (np.ndarray): 2D uint8 array of shape (N, N) with values 0 (dead) or 1 (alive).
    - neighbours (np.ndarray): 2D uint8 array of same shape used for counting neighbours.

    Returns:
    - np.ndarray: New 2D uint8 array representing next generation.
    """
    neighbours.fill(0)
    for dx, dy in (
        (-1, -1), (-1, 0), (-1, 1),
        ( 0, -1),          ( 0, 1),
        ( 1, -1), ( 1, 0), ( 1, 1),
    ):
        neighbours += np.roll(np.roll(grid, dx, axis=0), dy, axis=1)
    return ((neighbours == 3) | ((grid == 1) & (neighbours == 2))).astype(np.uint8)


def simulate_and_animate(
    N: int,
    timesteps: int,
    p_alive: float,
    output_file: Path,
    interval_ms: int = 200,
    max_display: int = 1080,
    dpi: int = 180
) -> np.ndarray:
    """
    Initialize the Game of Life grid randomly, run simulation, create a GIF,
    and count alive occurrences per cell over time.
    Returns:
    - counts: 2D uint32 array of shape (N, N) with number of times each cell was alive
    """
    rng = np.random.default_rng()
    grid = np.empty((N, N), dtype=np.uint8)
    threshold = int(p_alive * 1_000_000)
    for i in range(N):
        grid[i, :] = (rng.integers(0, 1_000_000, size=N, dtype=np.int32) < threshold).astype(np.uint8)
    neighbours = np.zeros((N, N), dtype=np.uint8)
    counts = np.zeros((N, N), dtype=np.uint32)
    step = 1 if max_display is None or max_display >= N else max(1, N // max_display)
    width_in = max_display / dpi
    fig = plt.figure(figsize=(width_in, width_in), frameon=False)
    fig.patch.set_visible(False)
    ax = fig.add_axes([0, 0, 1, 1], frameon=False)
    ax.set_axis_off()
    small = grid[::step, ::step]
    im = ax.imshow(small, cmap='binary', vmin=0, vmax=1, interpolation='nearest')
    writer = animation.PillowWriter(fps=1000 / interval_ms)
    writer.setup(fig, str(output_file), dpi=dpi)
    for _ in tqdm(range(timesteps), desc="Simulating & writing GIF"):
        counts += grid
        small = grid[::step, ::step]
        im.set_data(small)
        writer.grab_frame()
        grid = life_step_int(grid, neighbours)
    writer.finish()
    plt.close(fig)
    return counts


def plot_heatmap(counts: np.ndarray, output_file: Path = None):
    """
    Generate BOTH a continuous and a 10-level discrete heatmap of cell alive counts.
    Saves to:
      <stem>_continuous<suffix> and <stem>_discrete<suffix>
    or displays interactively if output_file is None.
    """
    # Continuous heatmap
    fig1 = plt.figure(figsize=(6, 6))
    im1 = plt.imshow(counts, cmap='hot', interpolation='nearest')
    plt.colorbar(im1, label='Alive Count')
    plt.title('Cell Alive Counts Heatmap (continuous)')
    plt.axis('off')
    if output_file:
        cont_file = output_file.parent / f"{output_file.stem}_continuous{output_file.suffix}"
        plt.savefig(cont_file, dpi=150, bbox_inches='tight', pad_inches=0)
        print(f"Continuous heatmap saved to {cont_file}")
    else:
        plt.show()
    plt.close(fig1)

    # Discrete (10-level categories) heatmap
    vmin, vmax = counts.min(), counts.max()
    bins = np.linspace(vmin, vmax, 11)  # 11 edges → 10 bins
    # use a categorical colormap (tab10) for distinct colors
    cmap10 = plt.get_cmap('tab10', 10)
    norm10 = BoundaryNorm(bins, ncolors=cmap10.N, clip=True)

    fig2 = plt.figure(figsize=(6, 6))
    im2 = plt.imshow(counts, cmap=cmap10, norm=norm10, interpolation='nearest')
    cbar2 = plt.colorbar(im2, ticks=bins)
    cbar2.set_label('Alive Count')
    plt.title('Cell Alive Counts Heatmap (10 categories)')
    plt.axis('off')
    if output_file:
        disc_file = output_file.parent / f"{output_file.stem}_discrete{output_file.suffix}"
        plt.savefig(disc_file, dpi=150, bbox_inches='tight', pad_inches=0)
        print(f"Discrete heatmap saved to {disc_file}")
    else:
        plt.show()
    plt.close(fig2)


def main():
    parser = argparse.ArgumentParser(description="Game of Life with Heatmap (all-int, streaming HD GIF)")
    parser.add_argument("--size", type=int, default=100, help="Grid dimension (N×N)")
    parser.add_argument("--timesteps", type=int, default=50, help="Number of generations to simulate")
    parser.add_argument("--p-alive", type=float, default=0.2, help="Initial alive probability (0–1)")
    parser.add_argument("--output", type=Path, default=Path("game_of_life_hd.gif"), help="Output GIF filename")
    parser.add_argument("--heatmap", type=Path, default=Path("alive_heatmap.png"), help="Output heatmap filename (PNG)")
    parser.add_argument("--interval", type=int, default=200, help="Frame duration in ms")
    parser.add_argument("--max-display", type=int, default=1080, help="Max side length for display (pixels)")
    parser.add_argument("--dpi", type=int, default=180, help="Resolution (dots per inch) for outputs")
    args = parser.parse_args()

    print(f"[All-int Matplotlib HD + Heatmap] size={args.size}, timesteps={args.timesteps}, p_alive={args.p_alive}")
    start_wall = time.perf_counter()
    rstart = resource.getrusage(resource.RUSAGE_SELF)

    counts = simulate_and_animate(
        N=args.size,
        timesteps=args.timesteps,
        p_alive=args.p_alive,
        output_file=args.output,
        interval_ms=args.interval,
        max_display=args.max_display,
        dpi=args.dpi
    )

    plot_heatmap(counts, args.heatmap)

    end_wall = time.perf_counter()
    rend = resource.getrusage(resource.RUSAGE_SELF)
    elapsed = end_wall - start_wall
    cpu_user = rend.ru_utime - rstart.ru_utime
    cpu_system = rend.ru_stime - rstart.ru_stime
    peak_rss = rend.ru_maxrss / (1024 ** 2)

    print(f"Saved HD GIF to {args.output}")
    print(f"Generated heatmaps to {args.heatmap.stem}_continuous and {args.heatmap.stem}_discrete")
    print("=== Resource usage ===")
    print(f"Wall-clock time : {elapsed:.2f} s")
    print(f"CPU time         : user {cpu_user:.2f} s, system {cpu_system:.2f} s")
    print(f"Peak memory (RSS): {peak_rss:.2f} GB")

if __name__ == "__main__":
    main()
