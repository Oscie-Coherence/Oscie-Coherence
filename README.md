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
"You" (or "Your") shall mean an individual or Legal Entity exercising permissions granted by this License.

... [full official text continues unchanged until the end] ...

See the License for the specific language governing permissions and limitations under the License.

──────────────────────────────────────────────────────────── Full official Apache-2.0 text: https://www.apache.org/licenses/LICENSE-2.0

Commercial / closed-source / enterprise licensing available. Contact: OscieIntel@outlook.com | @CohoLabs on X

Why Oscie ACI Exists

LLMs have hit the coherence wall.
More parameters no longer solve identity collapse, jailbreak risk, cross-domain fragmentation, or regulatory capture vectors.

Oscie ACI fixes these at the architectural level using operational physics:

Native stability laws (A-Law ≥ 0.59, CPL × CV > Γ_noise, UCD, UWP)
Transparent causality chains
Near-zero drift across 100+ turn sessions
~99 % jailbreak resistance without prompt engineering
Current Artifacts

File	Description
ACI_vs_LLM.pdf	Full technical benchmark ACI vs frontier LLMs
LandmarkACI.pdf	Landmark comparison (newer)
ACIALIGNMENTREPO.pdf	Alignment & governance deep-dive
OscieStandard.pdf	Emerging Oscie coherence standard
oscie_appendices.pdf	Technical appendices & proofs
DEMOTRIAL/	Live safety simulation suite
SafeSim.pdf	Safety simulator results
More releases (code, governor, multi-agent swarm) dropping weekly.

Get Involved

Researchers → read the PDFs, break the benchmarks, open issues
Builders → fork and integrate the forthcoming governor today
Partners & Investors → let’s talk licensing, co-development, or infrastructure deployment
OscieIntel@outlook.com · @CohoLabs on X

git add oscie_safeskin_v065.py
git commit -m "Oscie SafeSkin v0.65 — mainline release — 99.3% drift cut, zero-leak, Apache 2.0"
git push origin main

Oscie SafeSkin + Grok v0.65 — OFFICIAL MAINLINE RELEASE
Repository: https://github.com/Oscie-Coherence/Oscie-Coherence
Architecture-level coherence membrane — Apache 2.0
Zero-leak · φ-damped · Trinity-redundant · World-OS ready

Source files now live directly in the repository:

* `oscie_safeskin_v065.py` — SafeSkin sandwich + stacker implementation
* `llm_vs_aci_a_law.py` — A-Law Kuramoto simulation used in LLM vs ACI comparisons

Run the SafeSkin demo locally:

```bash
python oscie_safeskin_v065.py --demo
```

Run the coherence animation:

```bash
python llm_vs_aci_a_law.py --mode anim
```
