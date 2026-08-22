# Saturday — archive excavation ledger

This is the scratchpad behind `ARCHIVE_MAP.md`.

The map is the compact index. This file can grow messily as old repositories are reread.

For every repo, keep four things separate:

1. **Question** — what Antti appears to have been trying to make happen.
2. **AI projection** — how the collaborating model translated that question into the vocabulary it knew.
3. **Implementation** — what the code actually contains.
4. **Residue** — what Saturday should remember, reuse, or explicitly avoid rebuilding.

An old metaphor is not evidence that the mechanism existed. An old failed implementation is not evidence that the question was bad.

---

## Layer A — early creatures and loops

### FractalBrain

**Question:** can the AI be a changing organism rather than a fixed function — something whose internal structure, novelty response and memory develop while it interacts?

**AI projection:** classic early-ChatGPT module stacking: BERT for comprehension, GPT-2 as Broca, VAE latent, Wernicke, emotions, curiosity, explainability, long-term memory. The README itself says it was mostly written by ChatGPT and apologizes for the hype.

**Implementation residue:** recursive/fractal nodes that can grow/prune, novelty/curiosity signals, persistent saved state, continuous-learning machinery.

**Saturday reading:** discard the pretend neuroanatomy. Keep the older instinct that a machine should **change what machinery exists** as experience arrives.

### Bug in the Machine

**Question:** can live perception continually alter the internal machine that produces behaviour?

**AI projection:** generic adaptive-network vocabulary.

**Implementation:** webcam brightness/motion; Hebbian connections; probabilistic node growth; pruning by success; savable network state; movement/vision-facing GUI.

**Residue:** early closed-loop adaptive structure. Crude, but closer to computational matter than a static classifier.

### FractalBug

**Question:** can multiple internal temporal perspectives jointly drive an embodied creature?

**AI projection:** "hive mind," forward/backward encoders, collective intelligence.

**Implementation:** webcam input, multiple network layers, temporal weighting, visual memory, weighted movement suggestions, reinforcement of successful movement.

**Residue:** distributed temporal state participates directly in action.

### TiniOnes

**Question:** can learned internal signals become part of a world inhabited by small agents rather than merely labels produced by a model?

**AI projection:** EEG-inspired little neural creatures.

**Implementation:** agents move, see through adjustable cones, hear one another and themselves, make sound from neural activity; a separately trained EEG autoencoder provides latent vectors that can influence behaviour.

**Residue:** **agents inhabit a substrate / learned representation can become environment**. This is an ancestor of the later desire for intelligent things to live inside model weights or SplatWorld.

---

## Layer B — field / brain-substrate imagination

### WaveNeuron

**Question:** what if processing is ongoing oscillatory activity rather than static activations?

**Implementation:** sinusoidal units with frequency/phase/damping inside a webcam-to-behaviour loop.

**Residue:** ROTATE ancestor plus embodiment. The brain-area labels are decorative.

### ConsciousField

**Question:** can internal waves leave the machine, traverse a physical medium, and re-enter as transformed state?

**AI projection:** "quantum consciousness" narrative.

**Implementation:** continuously evolving oscillator state → loudspeaker waveform → room/body/apparatus → microphone → FFT → new state.

**Residue:** a real **machine → medium → receiver → machine** loop. Throw away the quantum/consciousness claim.

### weirdfieldthingy

**Question:** what if sensory data perturbs one continuously evolving shared field?

**Implementation:** 2-D field with convolution, decay, noise, coupling and live webcam bias; state can be saved/reset. Later ephaptic variant added after a paper prompted another interpretation.

**Residue:** perception as perturbation of ongoing medium state rather than feed-forward input.

### PolyrhythmicSea

**Question:** can stable localized things emerge as excitations of an active coupled substrate?

**AI projection:** PreQM, Born-rule/statistical-foundation story, FLSDAFL gravity analogy.

**Implementation:** multiple coupled nonlinear 2-D/3-D fields with diffusion, damping, self-interaction, drive, state-dependent wave speed, poking, and detection/tracking of persistent localized structures.

**Residue:** **localized persistent structures as states of an active medium**. No PreQM inference travels with it.

### Ying-Yang-Of-NeuralFields

**Question:** can the field between units be computational state rather than merely a communication wire?

**AI projection:** yin/yang ordering-vs-noise language plus ephaptic-brain motivation.

**Implementation:** 2-D LIF neurons with adaptation plus a shared field whose curvature influences firing.

**Residue:** the shared medium simultaneously carries state and changes local unit dynamics.

### MoiréBrain

**Question:** how can fast volatile traces coexist with slow stable traces, and why does observation scale alter the apparent structure?

**AI projection:** hippocampus/cortex as two fbm noise layers; consolidation as a slider; thoughts as moiré patterns.

**Implementation:** procedural noise visualization, not learned memory transfer.

**Residue:** two relaxation scales + observer-scale dependence. Do not cite it as evidence for biological consolidation.

### FieldLatentBridge

**Question:** can "field" and "latent" be two views of one continuously moving internal object?

**AI projection:** VAE bridge plus flowing 3-D visualization.

**Implementation:** untrained encoder/decoder; every animation update starts from a fresh random field vector.

**Residue:** almost entirely a **question fossil**. The persistent trajectory was not implemented.

### Little_dude

**Question:** can spatial dendritic / field dynamics and multiple oscillatory scales create a richer computational object than point attention?

**AI projection:** five brainwave bands mapped directly onto temporal windows.

**Implementation:** parallel 4/8/16/32/64-token processors plus a coherence detector. The repo's own later Claude conversation explicitly admits there are no gauge fields, real dendritic trees, spatial compartments or local dendritic spikes.

**Residue:** canonical example of AI compression. Do not call this a failed dendritic computer; it never really built one.

---

## Layer C — Fable / Finnish-name mechanism sprint

The names changed, but the research style is recognizably the ancestor of the current gate method: one result exposes a seam; a new repo attacks it; predictions are registered; kills are preserved; the next seam becomes another repo.

This produced excellent receipts and too much path length.

### Entrain

**Question:** can a resonant network grow the sensing structure it needs by failing to hear parts of its environment?

**Implementation:** Stuart–Landau resonators, exponential integrator, surprise/Clutch gate, frequency-targeted growth, harmonic combs, pruning, measured Arnold tongues, entrainment router, phase-bearing ring memory, live microphone cochlea.

**Residue:** Saturday audio parent. ROTATE + structure growth + routing already exist. Do not rebuild.

### RajapintaFable

**Question:** where is useful structure between fast change and frozen persistence?

**AI projection:** thaw line, Kibble–Zurek, topology, crystal-vs-flow taxonomy.

**Implementation:** multiple toy experiments on defect counts, storage geometries, and winding retention.

**Residue:** keep the general boundary question. Topology is one realization, not a required Saturday ontology.

### Nollas

**Question:** when Clockfield says "slower," what is actually slower?

**Implementation/result:** separated a refraction-style coefficient that changes transport from a lapse-style coefficient that rescales the local force/dynamics; exposed runaway self-quenching in one self-consistent lapse model; later thermostat audit corrected an apparent anomalous heat exponent.

**Residue:** extremely important naming discipline for Saturday: **transport speed, coupling strength and local execution time are different knobs**. Never call all of them `gamma` or "clock."

### Visertäjä

**Question:** what if representation is a trajectory with an internal frequency that the state itself changes?

**AI projection/implementation:** amplitude + phase + frequency latent unit, with state feedback into dω/dt; chirping templates as resonant readout.

**Receipt:** the unit really chirps and trains, phase is load-bearing for one readout, but on row-sequential MNIST a parameter-matched GRU wins by 4.28% and the resonant trajectory readout does not beat the endpoint.

**Residue:** self-bending internal clocks are implementable. They do not earn superiority by being physically pretty.

### Vino

**Question:** where should rotation/direction actually come from if scalar oscillator phase is not enough?

**Implementation:** antisymmetric/skew generator vs symmetric/full controls and matched GRU.

**Residue:** ROTATE should be viewed as a **family of generators**. Skew coupling has a principled role in direction and long-sequence gradient preservation; it is also established prior art (AntisymmetricRNN), so Saturday should use it as a tool, not a novelty claim.

### Kaiku

**Question:** can the wave medium itself perform useful nonlinear algebra?

**Receipt:** interference produces lower-order products; nonlinear mixing enables higher-order products; symmetry controls expose what a detector cannot read.

**Residue:** waves can compute. Saturday does not need another "prove wave computing" benchmark.

### Ristikko

**Question:** can two different reference/receiver mechanisms reveal independent information carried by one field?

**Receipt:** lagged self-reference and external homodyne reference expose different sectors and compose.

**Residue:** receivers/probes belong in the architecture, not just in plotting code.

### Arrowfield / Eromitta

**Question:** what should a self-slowing medium respond to — intensity, gradients, frustration — and what state is genuinely carried by the medium versus manufactured by the observer?

**AI projection:** matter/defects/gravity language.

**Residue:** `gamma=f(state)` is underspecified until the controlling state is named. Also preserve the observer-phase vs medium-state distinction. Do not import particle/cosmology claims into Saturday.

### ResonantCortex

**Question:** can cyclic/phase geometry and frustration-driven structural growth provide a useful representational bias?

**AI projection:** "computation is geometry; intelligence is resonance," complex-valued neurons, grokking as crystallization, neurogenesis.

**Current status in this excavation:** ancestry only. The README reports striking modular-arithmetic/Lorenz results, but Saturday should not treat those numbers as admitted receipts until their controls/history are separately audited.

**Residue for now:** frustration-triggered growth and complex phase geometry are recurring mechanisms; performance story remains quarantine.

---

## Layer D — newer receipts that constrain Saturday

- **Geometric-Neuron / V21:** sampling/readout geometry can change dynamical regime; original phase-memory retrieval was killed; structural delay growth survives.
- **FunctionalArbors:** geometry really changes measured delay when path length changes.
- **DifferentMachine:** represented capacity can greatly exceed work per event only when relevant state is locally discoverable.
- **BlockNeuron:** hysteresis is useful persistent configuration, but an explicit latch ties its basic memory capability.
- **KYY:** wave/local geometry is not automatically superior to strong structured recurrence.
- **TransientWaveCompiler:** sparse reciprocal-operator compiler/diagnosis survived; attractive stochastic physical-adjoint hardware claim did not.

---

## Recurrent question underneath the archive

Across very different AI interpretations, one question keeps returning:

> **Can the present physical/computational state of the machine be both the representation and the machinery that determines how the next signal is processed?**

That appears as:

```text
FractalBrain        experience changes structure
Bug/FractalBug      sensing changes an embodied adaptive machine
TiniOnes            agents inhabit and perturb a shared representational world
MoiréBrain          fast/slow traces coexist
weirdfieldthingy    sensory input perturbs an ongoing medium
DendriticAttention  traffic changes future receptive geometry
Entrain             failures grow new ears
GeometricNeuron     experience grows delay geometry
FunctionalArbors    geometry changes future arrival time
BlockNeuron         transient input changes persistent configuration
Clockfield/Saturday unresolved history changes local evolution rate
```

This is stronger than the recurring words "wave," "field," "fractal" or "phase." Those may be implementations or metaphors. The recurring architectural desire is **computation that changes the future computer**.

---

## Audit queue

Do not turn this into a gate ladder. This is simply a list of fossils worth rereading when their ingredient becomes relevant.

### Early brain / creature fossils
- `DendriticAttentionSystem` deeper code pass
- `Fractalvision`
- `ManyWaysToDoAI`
- `EigenCortex`
- `AnttisBrain2`
- `TheMycelialCortex`

### Field / resonance fossils
- `GaugeRopeTheory` — likely visual thought experiment; separate geometry intuition from gauge claims
- `One_formula_three_domains` — check structural analogy vs causal claim
- `CabbageFarm` / Janus Cabbage — representation-as-continuous-function / phase addressing
- `neural-phase-fields`
- `PolyrhythmicSea` code rather than README
- `Ying-Yang-Of-NeuralFields` implementation audit

### Time / persistence line
- `PresentMoment`
- `WidePresent`
- `TheWorld`
- `MorphogeneticNeuronChatGPTSol`
- `ClockfieldMeetsGeometricNeuron`

### Learned-world / inhabitants line
- `SplatStack`
- `SplatWorld`
- `WorldModel`
- `TinyAvatar` / `TinyAvatar2`
- `SplatWorldGeometricNeuronFusion`

The queue is not a promise to build anything. Its only purpose is to make it harder to accidentally reinvent an old mechanism under a new name.
