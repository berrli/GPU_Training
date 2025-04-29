import argparse
from pathlib import Path

import numpy as np
import cupy as cp

# ─────────────────────────────────────────────────────────────────────────────
# 1) Core update functions (no plotting/animation)
# ─────────────────────────────────────────────────────────────────────────────

def life_step_numpy(grid: np.ndarray) -> np.ndarray:
    neighbours = (
        np.roll(np.roll(grid, 1, axis=0), 1, axis=1) +
        np.roll(np.roll(grid, 1, axis=0), -1, axis=1) +
        np.roll(np.roll(grid, -1, axis=0), 1, axis=1) +
        np.roll(np.roll(grid, -1, axis=0), -1, axis=1) +
        np.roll(grid, 1, axis=0) +
        np.roll(grid, -1, axis=0) +
        np.roll(grid, 1, axis=1) +
        np.roll(grid, -1, axis=1)
    )
    return np.where((neighbours == 3) | ((grid == 1) & (neighbours == 2)), 1, 0)


def life_step_gpu(grid: cp.ndarray) -> cp.ndarray:
    neighbours = (
        cp.roll(cp.roll(grid, 1, axis=0), 1, axis=1) +
        cp.roll(cp.roll(grid, 1, axis=0), -1, axis=1) +
        cp.roll(cp.roll(grid, -1, axis=0), 1, axis=1) +
        cp.roll(cp.roll(grid, -1, axis=0), -1, axis=1) +
        cp.roll(grid, 1, axis=0) +
        cp.roll(grid, -1, axis=0) +
        cp.roll(grid, 1, axis=1) +
        cp.roll(grid, -1, axis=1)
    )
    return cp.where((neighbours == 3) | ((grid == 1) & (neighbours == 2)), 1, 0)


def life_step_naive(grid: np.ndarray) -> np.ndarray:
    N, M = grid.shape
    new = np.zeros((N, M), dtype=int)
    for i in range(N):
        for j in range(M):
            cnt = 0
            for di in (-1, 0, 1):
                for dj in (-1, 0, 1):
                    if di == 0 and dj == 0:
                        continue
                    ni, nj = (i + di) % N, (j + dj) % M
                    cnt += grid[ni, nj]
            if grid[i, j] == 1:
                new[i, j] = 1 if (cnt == 2 or cnt == 3) else 0
            else:
                new[i, j] = 1 if (cnt == 3) else 0
    return new


# ─────────────────────────────────────────────────────────────────────────────
# 2) Simulation functions (no animation)
# ─────────────────────────────────────────────────────────────────────────────

def simulate_life_numpy(N: int, timesteps: int, p_alive: float = 0.2):
    grid = np.random.choice([0, 1], size=(N, N), p=[1-p_alive, p_alive])
    history = []
    for _ in range(timesteps):
        history.append(grid.copy())
        grid = life_step_numpy(grid)
    return history


def simulate_life_cupy(N: int, timesteps: int, p_alive: float = 0.2):
    grid_gpu = (cp.random.random((N, N)) < p_alive).astype(cp.int32)
    history = []
    for _ in range(timesteps):
        history.append(cp.asnumpy(grid_gpu))
        grid_gpu = life_step_gpu(grid_gpu)
    return history


def simulate_life_naive(N: int, timesteps: int, p_alive: float = 0.2):
    grid = np.random.choice([0, 1], size=(N, N), p=[1-p_alive, p_alive])
    history = []
    for _ in range(timesteps):
        history.append(grid.copy())
        grid = life_step_naive(grid)
    return history


# ─────────────────────────────────────────────────────────────────────────────
# 3) Animation/export
# ─────────────────────────────────────────────────────────────────────────────

def animate_life(history, output_file: Path, interval: int = 200, dpi: int = 80):
    import matplotlib.pyplot as plt
    import matplotlib.animation as animation

    fig, ax = plt.subplots(figsize=(6, 6))
    im = ax.imshow(history[0], cmap='binary')
    ax.set_axis_off()

    def _update(idx):
        im.set_data(history[idx])
        return [im]

    anim = animation.FuncAnimation(
        fig, _update,
        frames=len(history),
        interval=interval,
        blit=True
    )
    anim.save(str(output_file), writer='pillow', dpi=dpi)
    plt.close(fig)


# ─────────────────────────────────────────────────────────────────────────────
# 4) CLI entry-points (only --size and --timesteps)
# ─────────────────────────────────────────────────────────────────────────────

def run_life_numpy():
    p = argparse.ArgumentParser("Game of Life (NumPy)")
    p.add_argument("--size",      type=int, default=100, help="Grid dimension (N×N)")
    p.add_argument("--timesteps", type=int, default=50,  help="Number of generations")
    args = p.parse_args()

    history = simulate_life_numpy(args.size, args.timesteps)
    output = Path("game_of_life_cpu.gif")
    animate_life(history, output)
    print(f"Saved CPU GIF to {output}")


def run_life_cupy():
    p = argparse.ArgumentParser("Game of Life (CuPy)")
    p.add_argument("--size",      type=int, default=100, help="Grid dimension (N×N)")
    p.add_argument("--timesteps", type=int, default=50,  help="Number of generations")
    args = p.parse_args()

    history = simulate_life_cupy(args.size, args.timesteps)
    output = Path("game_of_life_gpu.gif")
    animate_life(history, output)
    print(f"Saved GPU GIF to {output}")


def run_life_naive():
    p = argparse.ArgumentParser("Game of Life (Naive)")
    p.add_argument("--size",      type=int, default=100, help="Grid dimension (N×N)")
    p.add_argument("--timesteps", type=int, default=50,  help="Number of generations")
    args = p.parse_args()

    history = simulate_life_naive(args.size, args.timesteps)
    output = Path("game_of_life_naive.gif")
    animate_life(history, output)
    print(f"Saved Naive GIF to {output}")
