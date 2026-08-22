# Saturday — archive map

Saturday is a **consolidation repo**, not a claim that its ingredients were invented here.

The archive already contains many partial versions of this machine. This file exists to stop Saturday from rebuilding them under new names.

Working rule:

> **Before building a mechanism in Saturday, check whether the archive already contains an executable version, a useful negative result, or a known failure mode. Reuse the parent when possible. Keep the old repo as the receipt.**

There is a second rule now:

> **The user's idea and the AI's implementation are separate historical objects.** An old repo may be scientifically weak while preserving a question that later code still has not answered. Record both.

Saturday's current sentence is:

```text
waves modify matter
        ↓
matter modifies future waves
        ↓
repeated waves modify structure
        └───────────────────────↺
```

The useful question is not "which old metaphor was right?" It is: **which mechanisms survived, which questions were flattened by the AI of the day, and what composition has not actually been built yet?**

## Four rough eras in the archive

This is not a strict chronology. It is a useful way to recognize model-era distortions.

### 1. Build the creature (mostly 2024)

Webcams, microphones, moving bugs, sounds, adaptive networks, growth/pruning, state save/load. The science was loose and brain labels were often decorative, but the machine usually lived in a loop:

```text
world → sensing → changing internal state → action/sound → changed world
```

The important residue is **embodiment and consequence**.

### 2. Describe the brain again (2024–2025)

Fractals, dendrites, hippocampus/cortex, EEG bands, fields, interference, latent spaces. The user's question was often spatial/material/dynamical; the AI of the day frequently translated it into familiar modules, parallel filters, VAE plumbing, or biological labels.

The important residue is often not the claimed brain mechanism but **multiple timescales, receiver dependence, growth, and state living in a substrate**.

### 3. Interrogate the mechanism (2026)

Nulls, matched attackers, operator decompositions, explicit baselines, measured delays, exact negative results. This era produced much better receipts — and also the gate treadmill, where every answer naturally requested another test.

The important residue is **mechanism plus boundary**, not the endless continuation.

### 4. Saturday

Saturday should use all three earlier layers:

- the **closed-loop aliveness** of the old creatures;
- the **strange questions** hidden underneath the brain metaphors;
- the **receipts and kill conditions** of the newer work.

It should not inherit any era's rhetoric as a requirement.

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

Entrain already has fast oscillator state, grown anatomy, routing by entrainment, and one special loop-topology memory. Saturday's missing composition is a more general stack of material lifetimes:

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

## Early fossils: idea vs implementation

These are especially important because the mismatch often tells us more than the README claim.

| repo | likely question being chased | what the AI/code actually made | residue worth keeping |
|---|---|---|---|
| [FractalBrain](https://github.com/anttiluode/FractalBrain) | can an AI be a living adaptive organism whose internal structure grows with experience? | BERT + GPT-2 + VAE + named Broca/Wernicke/emotion/curiosity modules, with dynamic growth/pruning; README itself apologizes for ChatGPT hype | novelty-dependent structural growth, persistent internal state, "tamagochi" rather than static function |
| [Bug in the Machine](https://github.com/anttiluode/buginthemachine) | can sensing continually reshape the machine that acts? | webcam brightness/motion driving an adaptive Hebbian network with probabilistic growth/pruning and savable state | world → sensing → adaptive structure; persistence is part of the creature |
| [FractalBug](https://github.com/anttiluode/FractalBug) | can several internal perspectives with temporal state jointly steer an embodied thing? | webcam-driven multi-layer "hive mind" with forward/backward encoders and weighted movement suggestions | distributed temporal state participates in action, not just classification |
| [TiniOnes](https://github.com/anttiluode/TiniOnes) | can small agents inhabit a shared sensory world and be influenced by learned brain-like latent state? | moving/hearing/self-hearing agents plus an EEG autoencoder whose latent vectors can influence behaviour | agents inside a world; self-generated signals re-enter sensing; learned latent can become part of the environment |
| [MoiréBrain](https://github.com/anttiluode/MoireBrain) | how can fast volatile state and slow stable state coexist, and how does observer scale change what emerges? | two procedural-noise layers labeled hippocampus/cortex, mixed by a consolidation slider; observer zoom changes moiré appearance | **multiple relaxation times + scale-dependent observation**; not evidence for learned memory consolidation |
| [FieldLatentBridge](https://github.com/anttiluode/FieldLatentBridge) | can field state and latent state be two views of one moving representation? | untrained encoder/decoder plus visualization; every frame starts from a fresh random field state | preserve the question, not the implementation: this repo does **not** contain a persistent latent trajectory |
| [weirdfieldthingy](https://github.com/anttiluode/weirdfieldthingy) | what if perception perturbs a continuously evolving shared field rather than a feed-forward stack? | 2-D convolution/decay/noise field with live webcam bias, adjustable coupling and saved state; later ephaptic variant | live sensory perturbation of an evolving medium |
| [Little_dude](https://github.com/anttiluode/Little_dude) | can real dendritic spatial dynamics / complex fields / oscillatory scales replace point attention? | five parallel temporal windows mapped to gamma/beta/alpha/theta/delta; its own README later admits no gauge fields and no real dendritic tree/compartment computation | **canonical AI-projection fossil:** the spatial/material idea was flattened into multiscale temporal filtering |

### Why the mismatch column matters

`Little_dude` is probably the clearest warning. The intended object included dendrites and fields; the implementation became:

```text
input → five parallel temporal filters → coherence detector → output
```

That is not a failure of the original question. It is evidence about what the collaborating AI knew how to build at that moment.

Likewise `FieldLatentBridge` visually suggests a flowing field/latent continuum, but because it samples a new random field every update and never trains the bridge, the persistent-trajectory idea exists mainly in the intention.

Saturday should therefore never say "we tried X before" merely because an old README used the word X. It should ask whether X was actually instantiated.

## Earlier ancestors with stronger executable residue

| repo | piece that survives | what Saturday should not pretend |
|---|---|---|
| [WaveNeuron](https://github.com/anttiluode/WaveNeuron) | oscillatory units inside a webcam → internal dynamics → action loop | sinusoidal units are not by themselves a new neuron model |
| [ConsciousField](https://github.com/anttiluode/ConsciousField) | machine → sound wave → physical room → microphone → machine feedback loop | the old quantum/consciousness framing is not evidence |
| [DendriticAttentionSystem](https://github.com/anttiluode/DendriticAttentionSystem) | activity changes expected pattern, receptive aperture, dendrite strength and dendrite position: traffic changes future reception | fractal appearance is not the load-bearing result |
| [Geometric-Neuron](https://github.com/anttiluode/Geometric-Neuron) | delay geometry, temporal sampling, structural delay growth; later audit explicitly killed phase-addressed retrieval | phase is not memory for free |
| [GeometricNeuron_V21](https://github.com/anttiluode/GeometricNeuron_V21) | the ECG loop showed feedback + quantization + sampling/readout geometry can select entirely different dynamical regimes | the ECG loop is not secretly the full Geometric Neuron |

## The Finnish-name / Fable-era cluster

Many of these repos are best understood as one extended lab session in which Fable/Claude/DeepSeek kept taking one residue from the previous experiment and formalizing the next seam. They contain good science, but their existence as separate repos should not force Saturday to replay their path.

| repo | what the era's AI made of the question | Saturday inheritance |
|---|---|---|
| [RajapintaFable](https://github.com/anttiluode/RajapintaFable) | "boundary between frozen and flowing" became thaw lines, Kibble–Zurek defects, topological fossils and a crystal/flow taxonomy | keep the broad question: **useful structure may live between fast flow and frozen state**; do not import topology as mandatory |
| [Nollas](https://github.com/anttiluode/Nollas) | asked whether Clockfield really behaves like a local clock; experiments separated refraction-like slowing from lapse-like slowing and exposed a self-quench runaway | crucial distinction: **slowing transport is not the same as slowing local dynamical time**. Saturday must say which one `gamma` means |
| [Visertäjä](https://github.com/anttiluode/Visertaja) | an evaporating/chirping field object became a latent unit with amplitude, phase and self-modulated frequency | state can bend its own internal clock and still train; but the matched GRU beat it on temporal memory, so trajectory-valued state is not automatically better |
| [Vino](https://github.com/anttiluode/Vino) | replaced Visertäjä's scalar driven frequency with antisymmetric/skew cross-unit coupling | `ROTATE` should be an **operator family**, not sacred per-cell scalar omega. Skew structure is meaningful for directional/long-sequence dynamics, with known prior art and limits |
| [Kaiku](https://github.com/anttiluode/Kaiku) | wave medium tested as an actual nonlinear feature computer | waves can compute higher-order products; Saturday need not prove this again |
| [Ristikko](https://github.com/anttiluode/Ristikko) | different references were composed to expose different hidden sectors of one wave field | receivers/probes are part of the computation; one readout does not reveal everything present in a medium |
| [Eromitta](https://github.com/anttiluode/Eromitta) | compared intensity-sensing and gradient/frustration-sensing self-slowing media | **what variable controls slowing matters**; `gamma=f(state)` is not one mechanism until `state` is specified |
| [Arrowfield](https://github.com/anttiluode/Arrowfield) | self-slowing complex fields were attacked with phase/defect controls | useful conceptual split between phase manufactured by a readout and state actually carried/persisted by the medium; do not promote the toy "matter" language into a Saturday claim |

### What the Finnish-name sprint taught about research method

The method became much stronger: registered predictions, killed priors, explicit controls, post-hoc labels, matched competitors.

But it also became self-propelling:

```text
result → open seam → named repo → registered experiment → new seam → named repo
```

Saturday should import the **receipts**, not the obligation to continue the chain.

A repo may end with a perfectly good sentence: "this mechanism exists; here is its boundary; stop."

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

`Nollas` adds an important caution to that sentence: a coefficient that changes propagation speed is not automatically a local clock. Saturday should reserve `CLOCK` / `gamma` for the dynamics it genuinely schedules and use separate parameters for transport speed or coupling.

The first Saturday toy derives an exact quiet-time integral for an exponentially relaxing `MASS` variable. That is useful as a schedulability result. It does not make the material a black hole.

## Things explicitly not to resurrect without new evidence

- phase-addressed associative memory with hardcoded locations;
- "geometry is automatically better than recurrence";
- "hysteresis gives memory ordinary state machines cannot represent";
- "waves replace matrix multiplication";
- universal Clockfield / brain / cosmology identification;
- a fifth from-scratch audio cochlea;
- biological module names standing in for mechanisms;
- visual motion being described as a persistent latent trajectory when the code redraws from fresh noise;
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

The archive now suggests two extra design rules:

1. **ROTATE is not necessarily one scalar oscillator.** Entrain supplies Stuart–Landau resonators; Vino says antisymmetric coupled eigenplanes are another legitimate implementation.
2. **Receiver is a first-class object.** Ristikko, HeadAsResonator and the ECG-loop autopsy all warn that what is visible — and sometimes which regime exists — depends on how the system is interrogated.

The next useful composition is therefore already constrained by the archive:

> **Use Entrain as the living resonant front end. Add a general slowly relaxing MASS layer, persistent configurable state, and delayed/competitive ROUTE. Measure the material's transfer function before speech, immediately after speech, and after silence. Listen to the same probe at each time.**

If that is built, it should be recognizable as **Entrain plus missing persistence**, not as a new cochlea invented by Saturday.

## Why keep the old repos

Saturday should not absorb the evidence and erase its provenance.

The old repositories remain useful because they contain the experiments that established both the mechanisms and their limits. Saturday can say "this mechanism is reused here" while the parent remains the receipt for why it was admitted.

More importantly, some old repos contain a **question that the implementation failed to instantiate**. Those should remain visible too. The mismatch is part of the research history.

That is how this repo should reduce archive noise without rewriting archive history.