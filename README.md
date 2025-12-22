# Oscie Coherence Toolkit

Lightweight simulators exploring the "coherence physics" concepts referenced in the accompanying PDFs. The repository currently includes two runnable demos:

- `oscie_safeskin_v065.py`: deterministic SafeSkin membrane sandbox with coherence metrics and manifold visualization.
- `llm_vs_aci_a_law.py`: Kuramoto-style oscillator simulation contrasting baseline drift with A-Law governance.

## Requirements

- Python 3.9+
- NumPy, Pillow, Matplotlib
- (Optional) Numba for faster A-Law updates

Install dependencies:

```bash
pip install -r requirements.txt  # or pip install numpy pillow matplotlib numba
```

## Usage

Run the SafeSkin demo and produce a manifold image plus log file:

```bash
python oscie_safeskin_v065.py --demo
```

Animate the LLM vs A-Law simulation:

```bash
python llm_vs_aci_a_law.py --mode anim
```

Benchmark the A-Law governor with large oscillator counts:

```bash
python llm_vs_aci_a_law.py --mode benchmark --backend numba -N 100000 --steps 2000
```

## License

Unless otherwise noted, source code in this repository is provided under the Apache License 2.0 (see `LICENSE`).
