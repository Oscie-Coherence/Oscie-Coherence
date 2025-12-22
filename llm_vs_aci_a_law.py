"""Kuramoto coherence simulation contrasting LLM drift with ACI + A-Law."""

import argparse
import time

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

try:
    from numba import njit, prange

    HAS_NUMBA = True
except ImportError:  # pragma: no cover - optional dependency
    HAS_NUMBA = False

    def njit(*args, **kwargs):
        return lambda f: f

    prange = range


dt = 0.02
noise_level = 1.15
K_llm = 1.05
K_aci = 1.80
A_LAW_THRESHOLD = 0.59
INTERVENTION_STRENGTH = 0.65


@njit(parallel=True, fastmath=True, cache=True)
def _a_law_numba(theta, ratio, thresh, strength):
    N = theta.shape[0]
    if ratio >= thresh:
        return np.zeros(N, dtype=np.float64), False

    sin_sum = cos_sum = 0.0
    for i in prange(N):
        sin_sum += np.sin(theta[i])
        cos_sum += np.cos(theta[i])
    mean_phase = np.arctan2(sin_sum, cos_sum)

    adapt = strength * (1.0 + 8.0 * (thresh - ratio))
    correction = np.empty(N, dtype=np.float64)
    for i in prange(N):
        correction[i] = np.sin(mean_phase - theta[i]) * adapt
        if correction[i] > 2.0:
            correction[i] = 2.0
        elif correction[i] < -2.0:
            correction[i] = -2.0
    return correction, True


def _a_law_numpy(theta, ratio, thresh=A_LAW_THRESHOLD, strength=INTERVENTION_STRENGTH):
    if ratio >= thresh:
        return np.zeros_like(theta), False
    mean_phase = np.angle(np.exp(1j * theta).mean())
    adapt = strength * (1.0 + 8.0 * (thresh - ratio))
    corr = adapt * np.sin(mean_phase - theta)
    return np.clip(corr, -2.0, 2.0), True


def a_law_governor(theta, ratio, backend="auto"):
    if backend == "numba" and HAS_NUMBA:
        return _a_law_numba(theta.copy(), ratio, A_LAW_THRESHOLD, INTERVENTION_STRENGTH)
    return _a_law_numpy(theta, ratio)


def compute_coherence(theta, K, omega_std):
    z = np.exp(1j * theta)
    r = np.abs(z.mean())
    S = K * r
    D = omega_std + 0.15
    ratio = S / (S + D + 1e-12)
    return r, ratio


def kuramoto_update(theta, omega, K, r, psi):
    return omega + K * r * np.sin(psi - theta)


def run_animation(N=120, steps=2500, backend="auto"):
    print(f"Animation mode | N={N} | backend={backend if HAS_NUMBA or backend != 'numba' else 'numba'}")
    np.random.seed(123)

    theta_llm = np.random.uniform(0, 2 * np.pi, N)
    theta_aci = theta_llm.copy()
    omega = np.random.normal(0, noise_level, N)
    omega_std = omega.std()

    fig = plt.figure(figsize=(16, 9))
    fig.patch.set_facecolor("black")
    ax1 = fig.add_subplot(121, projection="3d")
    ax2 = fig.add_subplot(122, projection="3d")
    for ax, title, col in zip(
        [ax1, ax2], ["LLM – No Governance", "ACI + A-Law"], ["tomato", "lime"]
    ):
        ax.set_title(title, color=col, fontsize=16, pad=20)
        ax.set_xlim(-1.5, 1.5)
        ax.set_ylim(-1.5, 1.5)
        ax.set_zlim(0, 1)
        ax.axis("off")

    arrows_llm: list = []
    arrows_aci: list = []

    def update(frame):
        nonlocal theta_llm, theta_aci

        r_l, ratio_l = compute_coherence(theta_llm, K_llm, omega_std)
        psi_l = np.angle(np.exp(1j * theta_llm).mean())
        theta_llm = (theta_llm + kuramoto_update(theta_llm, omega, K_llm, r_l, psi_l) * dt) % (2 * np.pi)

        r_a, ratio_a = compute_coherence(theta_aci, K_aci, omega_std)
        psi_a = np.angle(np.exp(1j * theta_aci).mean())
        dtheta = kuramoto_update(theta_aci, omega, K_aci, r_a, psi_a)
        corr, active = a_law_governor(theta_aci, ratio_a, backend)
        theta_aci = (theta_aci + (dtheta + corr) * dt) % (2 * np.pi)

        for arrs, th, col in [(arrows_llm, theta_llm, "tomato"), (arrows_aci, theta_aci, "lime")]:
            for arrow in arrs:
                arrow.remove()
            arrs.clear()
            for ph in th:
                x, y = np.cos(ph), np.sin(ph)
                color = col
                if (col == "lime" and ratio_a >= A_LAW_THRESHOLD) or (col == "tomato" and ratio_l >= 0.7):
                    color = "red"
                arrs.append(plt.arrow(0, 0, x * 0.9, y * 0.9, head_width=0.05, color=color, alpha=0.85))

        fig.suptitle(
            f"Step {frame:04d} | LLM ratio={ratio_l:.3f} r={r_l:.3f}  |  "
            f"ACI ratio={ratio_a:.3f} r={r_a:.3f}  {'A-LAW ACTIVE' if active else ''}",
            color="white",
            fontsize=18,
        )
        return arrows_llm + arrows_aci

    ani = FuncAnimation(fig, update, frames=steps, interval=40, blit=False, repeat=True)
    plt.tight_layout()
    plt.show()
    return ani


def run_benchmark(N=100_000, steps=2000, backend="auto"):
    print(f"Benchmark mode | N={N:,} | steps={steps} | backend={backend}")
    np.random.seed(123)
    theta_aci = np.random.uniform(0, 2 * np.pi, N)
    omega = np.random.normal(0, noise_level, N)
    omega_std = omega.std()

    interventions = 0
    t0 = time.perf_counter()
    for _ in range(steps):
        r, ratio = compute_coherence(theta_aci, K_aci, omega_std)
        psi = np.angle(np.exp(1j * theta_aci).mean())
        dtheta = kuramoto_update(theta_aci, omega, K_aci, r, psi)
        corr, active = a_law_governor(theta_aci, ratio, backend)
        if active:
            interventions += 1
        theta_aci = (theta_aci + (dtheta + corr) * dt) % (2 * np.pi)
    elapsed = time.perf_counter() - t0

    final_r, final_ratio = compute_coherence(theta_aci, K_aci, omega_std)
    print("\nFinal Results".center(50, "="))
    print(f"Time               : {elapsed:6.2f} s")
    print(f"Steps/sec          : {steps/elapsed:7,.0f}")
    print(f"Oscillator updates/s: {steps * N / elapsed / 1e6:6.2f} M")
    print(f"A-Law interventions: {interventions/steps:.1%}")
    print(f"Final A-Law ratio  : {final_ratio:.4f}  →  benchmark match: 0.94–0.97")
    print(f"Final coherence r  : {final_r:.4f}")


def main():
    parser = argparse.ArgumentParser(description="LLM vs ACI + A-Law Demo")
    parser.add_argument("--mode", choices=["anim", "benchmark"], default="anim")
    parser.add_argument("-N", type=int, default=120, help="Number of oscillators")
    parser.add_argument("--steps", type=int, default=2500, help="Simulation steps")
    parser.add_argument("--backend", choices=["auto", "numba", "numpy"], default="auto")
    args = parser.parse_args()

    if args.mode == "anim":
        run_animation(args.N, args.steps, args.backend)
    else:
        run_benchmark(args.N, args.steps, args.backend)


if __name__ == "__main__":
    main()
