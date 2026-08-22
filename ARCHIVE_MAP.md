# Saturday — archive map

Saturday is a **consolidation repo**, not a claim that its ingredients were invented here.

The archive already contains many partial versions of this machine. This file exists to stop Saturday from rebuilding them under new names.

Working rule:

> **Before building a mechanism in Saturday, check whether the archive already contains an executable version, a useful negative result, or a known failure mode. Reuse the parent when possible. Keep the old repo as the receipt.**

Saturday's current sentence is:

```text
waves modify matter
        ↓
matter modifies future waves
        ↓
repeated waves modify structure
        └───────────────────────↺
```

The useful question is not "which old metaphor was right?" It is: **which mechanisms survived, and what composition has not actually been built yet?**

## The most important correction: Entrain is the audio parent

[Entrain](https://github.com/anttiluode/Entrain) already contains most of the front half of the audio-material idea.

It has:

- Stuart–Landau oscillators / damped resonators: Saturday's `ROTATE` family in a much more developed form;
- an exponential oscillator integrator after explicit Euler was killed as a false-resonance source;
- surprise-gated structural growth: the network starts with one randomly tuned ear and grows a resonator at spectral energy it failed to explain;
- harmonic-comb growth and pruning;
- measured entrainment / Arnold tongues and routing by entrainment;
- a self-sustaining ring that retains traveling-wave direction after input release;
- `index.html`, **ENTRAIN LIVE — a cochlea that grows itself**, where microphone input grows ears and **HEAR ITS EARS** plays the resonator bank back.

So Saturday should **not build another cochlea from scratch**.

The important gap is what happens *after the source stops*.

Entrain's live bank mainly tracks the current spectrum. Saturday's missing composition is:

```text
ENTRAIN resonant ears / growth
          +
MASS   = decaying history that changes local dynamical rate
LATCH  = persistent configuration surviving silence
ROUTE  = explicit delayed / competing propagation paths
          +
probe  = measure H(f) before / after / after silence
```

The audible question is therefore not "can resonators sound like the speaker while the speaker is talking?" Entrain already demonstrates that front half.

It is:

> **After the speaker stops, what remains in the material, on which timescale, and how does the same later probe get transformed?**

That is a real composition question rather than a duplicate app.

## Earlier ancestors

| repo | piece that survives | what Saturday should not pretend |
|---|---|---|
| [WaveNeuron](https://github.com/anttiluode/WaveNeuron) | oscillatory units inside a webcam → internal dynamics → action loop | sinusoidal units are not by themselves a new neuron model |
| [ConsciousField](https://github.com/anttiluode/ConsciousField) | machine → sound wave → physical room → microphone → machine feedback loop | the old quantum/consciousness framing is not evidence |
| [DendriticAttentionSystem](https://github.com/anttiluode/DendriticAttentionSystem) | activity changes expected pattern, receptive aperture, dendrite strength and dendrite position: traffic changes future reception | fractal appearance is not the load-bearing result |
| [Geometric-Neuron](https://github.com/anttiluode/Geometric-Neuron) | delay geometry, temporal sampling, structural delay growth; later audit explicitly killed phase-addressed retrieval | phase is not memory for free |
| [GeometricNeuron_V21](https://github.com/anttiluode/GeometricNeuron_V21) | the ECG loop showed feedback + quantization + sampling/readout geometry can select entirely different dynamical regimes | the ECG loop is not secretly the full Geometric Neuron |

## Recent receipts Saturday should inherit, not repeat

| repo | reusable result / boundary | relevance here |
|---|---|---|
| [FunctionalArbors](https://github.com/anttiluode/FunctionalArbors) | learned path geometry genuinely changed independently measured wavefront delay; earlier speed-vs-geometry confusion was killed | `ROUTE`: geometry can carry temporal memory |
| [DifferentMachine](https://github.com/anttiluode/DifferentMachine) | represented machine size need not equal work/event when relevance is locally discoverable; global discovery destroys the saving | Saturday runtime should be event/frontier driven, not globally scanned |
| [BlockNeuron](https://github.com/anttiluode/BlockNeuron) | hysteretic state can write/hold/erase and configure later computation; a plain latch ties the basic capability | `LATCH` is a material organization primitive, not unique computational power |
| [Kaiku](https://github.com/anttiluode/Kaiku) | nonlinear wave mixing really computes higher-order features; fixed continuously stepped wave media are slow | Saturday does not need to prove again that waves can compute; it needs a sparse/sleepable organization |
| [Ristikko](https://github.com/anttiluode/Ristikko) | different references expose different information in the same field; lag and homodyne readouts compose | receivers / probes should be first-class, not passive plotting |
| [KYY](https://github.com/anttiluode/KYY) | local wave geometry does not automatically beat strong generic structured recurrence | do not sell geometry itself as intelligence |
| [TransientWaveCompiler](https://github.com/anttiluode/TransientWaveCompiler) | sparse reciprocal operators and exact sensitivities survived; attractive stochastic physical-adjoint claim did not | possible later physical lowering / diagnosis layer, not proof that Saturday hardware works |

## Clockfield's narrower place

Saturday does not inherit "Clockfield = General Relativity for neural networks" or a universal-operator story.

What it keeps is much smaller:

```text
persistent local state m(t)
        ↓
state-dependent local rate gamma(m)
        ↓
closed-form / otherwise exact free evolution where available
        ↓
quiet material can sleep until touched
```

The first Saturday toy derives an exact quiet-time integral for an exponentially relaxing `MASS` variable. That is useful as a schedulability result. It does not make the material a black hole.

## Things explicitly not to resurrect without new evidence

- phase-addressed associative memory with hardcoded locations;
- "geometry is automatically better than recurrence";
- "hysteresis gives memory ordinary state machines cannot represent";
- "waves replace matrix multiplication";
- universal Clockfield / brain / cosmology identification;
- a fifth from-scratch audio cochlea;
- endless gate ladders whose only output is another gate.

## What Saturday currently adds

Saturday's first machine is still mostly a wiring test. Its value is that it puts several previously separate kinds of state in one executable object:

```text
fast       ROTATE / travelling event
medium     MASS / local relaxation and local-time change
persistent LATCH / configuration
structural ROUTE / coupling and delay
runtime    event-driven materialization where free evolution is solvable
```

The next useful composition is therefore already constrained by the archive:

> **Use Entrain as the living resonant front end. Add MASS, LATCH and delayed/competitive ROUTE. Measure the material's transfer function before speech, immediately after speech, and after silence. Listen to the same probe at each time.**

If that is built, it should be recognizable as **Entrain plus missing persistence**, not as a new cochlea invented by Saturday.

## Why keep the old repos

Saturday should not absorb the evidence and erase its provenance.

The old repositories remain useful because they contain the experiments that established both the mechanisms and their limits. Saturday can say "this mechanism is reused here" while the parent remains the receipt for why it was admitted.

That is how this repo should reduce archive noise without rewriting archive history.