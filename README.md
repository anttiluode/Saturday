# Saturday

A ChatGPT 5.6 Sol thinking repo.

> **Before building another mechanism here, read [`ARCHIVE_MAP.md`](ARCHIVE_MAP.md) and [`KILL_LEDGER.md`](KILL_LEDGER.md).** Saturday is a consolidation repo. The old repositories remain the receipts for mechanisms and failures that Saturday reuses.
>
> In particular: **[Entrain](https://github.com/anttiluode/Entrain) is the audio parent.** Its Stuart–Landau ears, surprise-gated growth, entrainment routing, pruning and live **HEAR ITS EARS** cochlea already implement the resonant/growing front half. Saturday should add missing persistence and delayed material history to Entrain, not rebuild another cochlea.

Saturday starts from one loop:

```text
waves modify matter
        ↓
matter modifies future waves
        ↓
repeated waves modify structure
        └───────────────────────↺
```

The aim is **not** to claim a brain model, a General Relativity model, or a replacement for matrix multiplication.

The aim is to build a very small piece of **computational matter** and see what it can actually do.

The recurring architectural question is:

> **Can the present state of a machine be both the representation and part of the machinery that determines how the next signal is processed?**

## Vocabulary, corrected after the first code review

The first version made the categories too sacred. The code now treats them more carefully.

```text
LOCAL STATE / CAPABILITY                 BETWEEN LOCAL PIECES

slow residue m(t) ──► local clock

ROTATE = one complex-conjugate pole pair ──┐
LATCH  = persistent configuration          ├── ROUTE / sparse geometry ──► other material
PASS   = no special local dynamics         ┘

MASS is cross-cutting: any cell may carry slow residue.
```

`ROTATE` keeps a strict type-level meaning because an earlier result depends on it: one damped complex-conjugate pole pair cannot be replaced exactly by a finite collection restricted to independent pure real decays without changing the operator class. A local complex oscillator, a real 2×2 skew plane, or a resonant eigenplane can all implement that same specification.

`MASS` is different. It is a **property/state**, not a sacred exclusive cell type. Every Saturday cell may write a slowly relaxing residue.

`LATCH` is also not interesting as a scalar gain. It is persistent **configuration**: in the first machine it selects which outgoing route is live.

## Nollas discipline: three things that must stay separate

The first implementation violated one of the archive's own lessons by letting `gamma` influence too many observables.

Saturday now keeps these mechanisms separate:

1. **local execution time** — how much global time a cell requires to advance its own dynamics;
2. **transport delay** — propagation time carried by an edge / path;
3. **coupling / amplitude transfer** — how strongly one piece drives another.

The Clockfield-like law

```text
gamma = 1 / (1 + kappa * m)
```

controls **local execution time only**.

It does not directly alter edge delay, coupling, or output amplitude.

An `Observation` reports cumulative `compute_time` and `transport_time` separately, so a later experiment can disable one mechanism without silently changing the others.

## The first machine

`experiments/first_machine.py` builds:

```text
source -> MASS -> ROTATE -> LATCH
                           /   \
                     out_pos   out_neg
```

The LATCH starts negative, so a weak baseline probe exits through `out_neg`.

Then six stronger positive waves condition the material. They do three different things:

- write a slowly relaxing MASS residue;
- flip the persistent LATCH configuration positive;
- repeatedly use the positive outgoing route, biasing its structural trace.

The same later weak probe now exits through `out_pos`.

The immediate probe also spends more **compute time** in the MASS-loaded material, while its geometric/edge transport time is unchanged.

After a long silent interval, MASS relaxes and execution speeds up again. The LATCH still selects `out_pos`, and the route competition retains a slower structural history.

That is the first useful separation:

```text
fast          wave / ROTATE state
seconds-ish   MASS / unresolved residue
persistent    LATCH / configuration
structural    ROUTE allocation
runtime       event-driven materialization
```

The particular numbers are still mostly a wiring receipt. The important change from v0 is that each number now belongs to a named mechanism.

## Lazy local time

For a slow variable

```text
m(t) = m0 exp(-t / tau)
```

and local clock

```text
gamma(t) = 1 / (1 + kappa m(t)),
```

the accumulated local time over a quiet global interval has a closed form:

```text
Delta_local
  = Delta_global
    + tau * [log(1 + a exp(-Delta_global/tau)) - log(1 + a)]

where a = kappa * m0.
```

Saturday uses that expression directly.

So if a cell is untouched for 10,000 time units, the simulator does **not** execute 10,000 tiny updates. It analytically advances the slow residue and the free local state when the next event finally arrives.

That is the Clockfield idea in its least mythical form:

> **local history changes local dynamical time, and quiet material need not execute merely because a global clock tick occurred.**

This is closer to an event-driven / neuromorphic execution primitive than to a GPU tensor optimization.

## Local capabilities

### MASS / slow residue

A wave can deposit slow residue:

```text
wave -> m increases -> gamma falls -> later local execution takes longer
```

The residue then relaxes in global time.

This is **effective dynamical inertia**, not kilograms and not a claim about gravity.

Most importantly, mass is allowed on ROTATE, LATCH, or PASS cells too. The question is what slow state a local element carries, not which noun was printed on it.

### ROTATE

ROTATE carries a complex fast state with pole pair

```text
dz/dtau_local = (-alpha + i omega) z
```

The specification is the pole structure, not the software representation.

Possible implementations include a local complex oscillator, a real antisymmetric 2-D plane, or a larger resonant structure whose relevant eigenmode has the same pair.

### LATCH

LATCH is persistent configuration.

In v0 it was merely:

```text
gate = 1.0 if latch > 0 else 0.2
```

That branch is now recorded as dead in `KILL_LEDGER.md`.

The current machine instead lets the persistent state select topology:

```text
latch = +1  -> positive route live
latch = -1  -> negative route live
```

That makes “configuration determines what the fast signal means/where it can go” explicit.

### ROUTE

Edges carry propagation delay and coupling. They also have a decaying use trace.

The original route rule was monotone and pathological: every used connection could only strengthen toward a ceiling, while the trace variable was computed and never used.

Current plastic routes compete under a **fixed outgoing coupling budget**. Their decaying traces bias how that budget is divided:

```text
more use of route A
      ↓
more of fixed budget allocated to A
      ↓
less available to competing route B
```

So structural learning is competition, not universal saturation.

## Receivers are allowed inside the machine

The first version treated every receiver as an absorbing terminal:

```text
material -> receiver -> stop
```

That could not express one of the oldest archive lessons: a readout can be part of the causal loop, and changing what is sampled/reinjected can change which dynamical regime exists.

Saturday receivers now have two modes:

```text
absorbing receiver:
    observe -> stop

non-absorbing receiver:
    observe -> process -> forward
```

`ttl` remains on events so cyclic graphs do not run forever by accident.

This is deliberately a small change, but it makes feedback/readout experiments possible without inventing another simulator.

## Run it

No runtime dependencies beyond Python.

```bash
pip install -e .
python experiments/first_machine.py
```

Run the tests:

```bash
python -m unittest discover -s tests
```

The tests now check mechanism separation rather than one lucky headline:

- one lazy 40-unit materialization matches forty 1-unit materializations while executing one local advance instead of forty;
- ROTATE performs true complex-pole rotation;
- changing MASS changes compute time while transport time stays fixed and amplitude is not secretly scaled by `gamma`;
- LATCH survives silence and selects a different outgoing route;
- route plasticity preserves a fixed coupling budget while used and unused routes compete;
- a receiver can be non-absorbing and participate in a causal cycle;
- in the first machine, MASS relaxes while LATCH and route history persist on different timescales.

## Why this is not "replace the matrix"

A per-cell clock is diagonal. It does not tell one cell **which other cell to mix with**.

Saturday therefore keeps sparse coupling / ROUTE explicitly.

The possible saving is elsewhere:

```text
represented material != material executed for every event
```

A large substrate may contain many persistent local possibilities while only an event-relevant causal region needs to be touched.

That idea connects naturally to event-driven machines, sparse local graphs and neuromorphic hardware. On an ordinary GPU, irregular skipping can cost more than dense arithmetic; Saturday makes no contrary performance claim.

## Relation to Entrain

Saturday should not create another audio front end.

Entrain already has the living part:

- Stuart–Landau resonant ears;
- exact/exponential oscillator integration;
- surprise-gated growth;
- harmonic combs and pruning;
- measured entrainment routing;
- phase-bearing ring memory;
- microphone input and **HEAR ITS EARS** output.

The interesting composition is therefore much smaller:

```text
Entrain ears / growth / live audio
          +
slow residue that changes local execution or transfer state
persistent configuration
explicit delayed competitive routes
calibrated probe H(f)
```

Then ask the audible question Entrain did not primarily ask:

> **After the speaker stops, what remains in the material, on which timescale, and how does the same later probe get transformed?**

## Relation to Mamba / SSMs

Input-dependent timescales are already a major idea in modern selective state-space models. Saturday is not claiming to have invented selective memory.

The narrower decomposition here is that the quantity controlling local dynamical time is itself a **persistent relaxing material state** written by previous events:

```text
past wave -> m(t) -> local clock -> response to later wave
```

A sufficiently general recurrent model can emulate such behavior. The question is whether making it first-class gives useful execution, physical mapping, growth, or composition.

That has not been established.

## Archive archaeology is part of the mechanism work

Saturday keeps three related files:

- `ARCHIVE_MAP.md` — compact map of mechanisms already built;
- `ARCHIVE_EXCAVATION.md` — question / AI projection / implementation / residue notes;
- `KILL_LEDGER.md` — dead branches and the conditions under which they died.

The third file matters because dead branches are often more valuable than surviving metaphors. A mechanism should not be rebuilt merely because a new AI gives it a better name.

## What this repo is really about

The older projects kept approaching the same boundary from different directions: waves, geometric neurons, dendritic arbors, Clockfield, persistent blocks, growing sparse machines, little agents living inside learned worlds.

Saturday puts them in one executable sentence:

> **A signal changes the material it traverses; the changed material transforms later signals; repeated transformation can become persistent structure.**

The brain is motivation, not a claim of correspondence.

There is no promise that the answer is "better neural network."

It may instead be a useful wave/audio material, an event-driven runtime, a strange programmable medium, or a clean demonstration of why these ingredients buy nothing beyond ordinary state machines.

For now the rule is simple:

> **Do not build the next thing until the archive says we have not already built — or killed — it.**
