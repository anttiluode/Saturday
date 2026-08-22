# Saturday

A ChatGPT 5.6 Sol thinking repo about **computational matter**: a signal changes the material it traverses; the changed material transforms later signals; repeated transformation can become persistent structure.

## Live demo — SEE WHAT HASN'T RELAXED

**GitHub Pages:** https://anttiluode.github.io/Saturday/

The root [`index.html`](index.html) is now the public-facing experiment. It uses webcam input, but it is deliberately **not face recognition and not a pixel afterimage**.

The page reduces the current scene to 24 oriented / spatial-frequency complex channels and keeps several timescales visible at once:

```text
CURRENT WORLD
      ↓
ROTATE / fast complex activity
      ↓
MASS / slowly relaxing exposure history
LATCH / persistent configuration
ROUTE / competing structural allocation
      ↓
fixed synthetic visual probe H
```

### Try this

1. Open the page and press **RUN FIXED PROBE**. The first run becomes the baseline `H0`.
2. Press **START CAMERA** and show it something for several seconds: your face, a hand, an object, motion, edges.
3. Press **REMOVE SCENE → GRAY**. The live scene is replaced by uniform gray while the material continues evolving.
4. Run the same fixed probe immediately, then after a few seconds, then later.
5. Watch `|H-H0|`, MASS, latch count and route imbalance separate across timescales.
6. Uncheck **MATERIAL MEMORY ON** and repeat. That is the matched live-tracking control: the resonant front end remains, persistent material state is cleared.

The interesting question is not “does it still draw the thing it saw?” It is:

> **After the scene disappears, does the same later input encounter a different processor because earlier input changed the material?**

The page runs entirely in the browser. Camera access requires HTTPS, which GitHub Pages supplies.

---

## Read these before inventing another mechanism

Saturday is also a **consolidation repo**. The older repositories remain the receipts; Saturday should reuse them rather than quietly rebuild them under new names.

- [`ARCHIVE_MAP.md`](ARCHIVE_MAP.md) — compact map of mechanisms already built and which parent repo owns each ingredient.
- [`KILL_LEDGER.md`](KILL_LEDGER.md) — dead branches and the conditions under which they died. Search this before reviving a tempting idea.
- [`ARCHIVE_EXCAVATION.md`](ARCHIVE_EXCAVATION.md) — the messier archaeology ledger: **question / AI projection / implementation / killed / residue**.

The scarce asset is not only what survived. It is knowing which branches already failed, which requests an earlier AI accidentally replaced with a different implementation, and which results were merely metaphors.

In particular, **[Entrain](https://github.com/anttiluode/Entrain) is the audio parent**. Its Stuart–Landau ears, surprise-gated growth, entrainment routing, pruning and live **HEAR ITS EARS** cochlea already implement the resonant/growing front half. Saturday should not build another cochlea.

---

## The recurring question

Across the older waves, fields, bugs, dendrites, Clockfield, Geometric Neuron, FunctionalArbors, Entrain and BlockNeuron work, the more stable question is:

> **Can the present state of a machine be both the representation and part of the machinery that determines how the next signal is processed?**

That is stronger than any particular metaphor such as “wave,” “fractal,” “phase,” or “brain.”

```text
waves modify matter
        ↓
matter modifies future waves
        ↓
repeated waves modify structure
        └───────────────────────↺
```

The brain is motivation, not a claim of correspondence. Saturday is not a General Relativity model and not a proposal to replace matrix multiplication.

---

## Vocabulary after the first code review

The first implementation made the categories too sacred. The corrected view is:

```text
LOCAL STATE / CAPABILITY                 BETWEEN LOCAL PIECES

slow residue m(t) ──► local clock

ROTATE = one complex-conjugate pole pair ──┐
LATCH  = persistent configuration          ├── ROUTE / sparse geometry ──► other material
PASS   = no special local dynamics         ┘

MASS is cross-cutting: any cell may carry slow residue.
```

### ROTATE

ROTATE has a type-level dynamical meaning: one damped complex-conjugate pole pair,

```text
dz/dtau_local = (-alpha + i omega) z
```

A local complex oscillator, a real 2×2 skew plane, or a resonant eigenplane can implement the same specification. Keeping the pole structure explicit preserves the earlier separation result: independent pure real decays do not exactly become this mode without changing the operator class.

### MASS

MASS is a slow state, not a sacred exclusive cell type. A wave can deposit residue `m`; the residue relaxes in global time and controls a local execution clock:

```text
gamma = 1 / (1 + kappa*m)
```

### LATCH

LATCH is persistent **configuration**, not a remembered scalar gain. In the Python toy it selects which outgoing route is live. In the webcam page it changes which competing transform route a later diagnostic probe uses.

### ROUTE

ROUTE owns propagation / coupling between local pieces. Plastic routes compete under a fixed outgoing budget; strengthening one therefore weakens another instead of letting every used connection monotonically saturate.

---

## Nollas discipline: do not call three things “clock”

Saturday keeps these mechanisms separate:

1. **local execution time** — how quickly local state evolves;
2. **transport delay** — propagation time on a path;
3. **coupling / amplitude transfer** — how strongly pieces drive one another.

`gamma` controls local execution time only. It does not secretly scale edge delay, coupling, or output amplitude.

The Python `Observation` object reports compute time and transport time separately so experiments can disable one mechanism without changing the others.

---

## Python material toy

The small event-driven implementation lives in [`saturday/material.py`](saturday/material.py). The first reproducible machine is:

```text
source -> MASS -> ROTATE -> LATCH
                           /   \
                     out_pos   out_neg
```

A weak fresh probe exits through `out_neg`. Strong conditioning writes slow MASS, flips the persistent latch, and biases the competing positive route. The same later weak probe exits through `out_pos`. After long silence MASS mostly relaxes and compute time returns toward baseline while the latch remains.

Receivers may also be **non-absorbing**, so observation can remain inside a causal loop rather than always terminating it. TTL bounds cycles.

### Lazy local time

If

```text
m(t) = m0 exp(-t/tau)
gamma(t) = 1/(1+kappa*m(t))
```

then quiet local time is analytically integrable:

```text
Delta_local
  = Delta_global
    + tau * [log(1 + a exp(-Delta_global/tau)) - log(1 + a)]

where a = kappa*m0.
```

A quiet cell therefore does not need thousands of no-op ticks merely because global time passed. It can be materialized when the next event touches it.

Run it:

```bash
pip install -e .
python experiments/first_machine.py
python -m unittest discover -s tests -v
```

The tests check mechanism separation: lazy materialization, complex-pole rotation, MASS vs transport separation, latch routing, fixed-budget route competition, receiver-in-loop recurrence, and distinct relaxing/persistent histories.

---

## What Saturday is not claiming

- not a brain simulator;
- not “phase is memory”;
- not “waves are automatically better than recurrence”;
- not “hysteresis gives memory ordinary state machines cannot represent”;
- not a new audio cochlea — Entrain already exists;
- not another endless ladder where every experiment exists only to justify the next experiment.

A sufficiently general recurrent model can emulate much of this behavior. The live question is whether making these timescales, routes, receivers and locally sleepable dynamics first-class produces something useful as a signal material, event-driven runtime, physical mapping, adaptive world, or simply a clearer demonstration of where the idea fails.

For now:

> **Show it something. Leave. Probe what hasn't relaxed.**
