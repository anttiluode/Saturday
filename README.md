# Saturday

A ChatGPT 5.6 Sol thinking repo.

Saturday starts from one loop:

```text
waves modify matter
        ↓
matter modifies future waves
        ↓
repeated waves modify structure
        └───────────────────────↺
```

The aim is **not** to claim a brain model, a General Relativity model, or a new replacement for matrix multiplication.

The aim is to build a very small piece of **computational matter** and see what it can actually do.

The first concrete question is:

> Can a heterogeneous dynamical material contain local relaxation, oscillatory phase, persistent configuration and geometric propagation at the same time, while local history also determines how fast each piece needs to evolve?

That gives a first vocabulary:

```text
LOCAL MATERIAL                    BETWEEN MATERIAL

MASS      slow relaxation     ┐
ROTATE    phase trajectory    ├── ROUTE / sparse geometry ──► other material
LATCH     persistent state    ┘

                 ↑
            local clock
      gamma = 1 / (1 + kappa*m)
```

`MASS`, `ROTATE` and `LATCH` are local dynamical types. `ROUTE` is deliberately not another bit type: it is geometry, delay and coupling **between** local pieces.

Clockfield is also not the whole computer. Here it is a scheduling/material law: accumulated local `mass` slows the local clock. A quiet cell can therefore hold unresolved history without being numerically ticked at every global step.

## The first machine

`experiments/first_machine.py` builds one tiny directed material:

```text
source -> MASS -> ROTATE -> LATCH -> receiver
```

Every connection is a sparse `ROUTE` edge with a propagation delay and a slowly plastic coupling.

The experiment does four things:

1. Send a weak probe through fresh material.
2. Send six stronger conditioning waves.
3. Send the same weak probe immediately afterward.
4. Leave a long silent interval, then send the same probe again.

The conditioning waves leave three different kinds of history:

- **MASS:** a relaxing residue that reduces local clock rate and increases dwell time.
- **LATCH:** a persistent switched configuration that survives after the drive disappears.
- **ROUTE structure:** repeated traffic slowly changes edge coupling.

The immediate probe therefore crosses a machine that is physically/dynamically different from the machine seen by the baseline probe.

After long silence, MASS has mostly relaxed and the probe speeds up again, while the LATCH and structural route changes remain.

That separation matters more than the particular toy numbers.

## Lazy local time

For a MASS variable

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

So if a cell is untouched for 10,000 time units, the simulator does **not** execute 10,000 tiny updates. It advances the slow residue and fast local state analytically when the next event finally arrives.

That is the Clockfield idea in its least mythical form:

> local history changes local dynamical time, and quiet material need not be executed merely because a global clock tick occurred.

This is much closer to an event-driven / neuromorphic execution primitive than to a GPU tensor optimization.

## Primitive dynamics

### MASS

MASS is a real relaxing degree of freedom. A wave deposits energy into the local residue; the residue then decays.

```text
wave -> m increases -> gamma falls -> later waves dwell longer
```

This is **effective dynamical mass**, not kilograms.

### ROTATE

ROTATE carries a complex fast state with a conjugate pole pair:

```text
dz/dtau_local = (-alpha + i omega) z
```

It therefore has a phase trajectory that cannot be represented exactly by a collection of independent pure real decays without changing the allowed operator class.

### LATCH

LATCH is a persistent local configuration. In the first implementation it is deliberately simple: a sufficiently strong signed drive writes one of two states and the state survives silence.

The point is not that latches are new. The point is to let a persistent material configuration coexist with relaxing and oscillatory state in the same medium.

### ROUTE

Edges provide sparse coupling and delay. The present wave sees the current coupling; its passage then leaves a slow use trace that can change the coupling seen by later waves.

So repeated signal flow can become structure:

```text
past traffic -> route coupling -> future traffic
```

Higher-level code can also add/remove cells and connect/disconnect routes explicitly. The eventual interesting case is when some of that structural editing can be caused by the material's own activity and consequences rather than by a designer.

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

The tests check the properties, not one lucky printout:

- one lazy 40-unit materialization matches forty 1-unit materializations while executing one local advance instead of forty;
- ROTATE performs a true phase rotation;
- LATCH survives long silence;
- repeated traffic changes ROUTE coupling;
- the conditioned machine slows an immediate probe, MASS later relaxes, while LATCH and ROUTE history persist.

## Why this is not "replace the matrix"

A per-cell clock is diagonal. It does not tell one cell **which other cell to mix with**.

Saturday therefore keeps sparse coupling `J_ij` / ROUTE explicitly.

The possible saving is elsewhere:

```text
represented material != material executed for every event
```

A large substrate may contain many persistent local possibilities while only an event-relevant causal region needs to be touched.

That idea connects naturally to event-driven machines, sparse local graphs and neuromorphic hardware. On an ordinary GPU, irregular skipping can cost more than simply performing dense arithmetic; Saturday makes no contrary performance claim.

## Relation to Mamba / SSMs

Input-dependent timescales are already a major idea in modern selective state-space models. Saturday is not claiming to have invented selective memory.

The narrower decomposition here is that the quantity controlling local dynamical time is itself a **persistent relaxing material state** written by previous events:

```text
past wave -> m(t) -> local clock -> response to later wave
```

A sufficiently general recurrent model can emulate such behavior. The question is whether making it a first-class local primitive gives useful execution, physical mapping, growth or compositional properties.

That has not been established.

## What this repo is really about

The older projects kept approaching the same boundary from different directions: waves, geometric neurons, dendritic arbors, Clockfield, persistent blocks, growing sparse machines.

Saturday puts them in one executable sentence:

> **A signal changes the material it traverses; the changed material transforms later signals; repeated transformation can become persistent structure.**

The brain is motivation, not a claim of correspondence. Real neurons contain many local dynamical timescales, nonlinear compartments, oscillatory activity, persistent biochemical/material state and geometry-dependent propagation. Saturday asks what happens if an artificial computational substrate is organized around those broad facts instead of around a memoryless point unit.

There is no promise that the answer is "better neural network."

It may instead be a useful little wave computer, an event-driven material, a strange programmable medium, or a clean demonstration of why these ingredients do **not** buy anything beyond ordinary state machines.

For now it is alive enough to poke.
