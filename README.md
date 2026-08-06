# Action-Sufficient Representation

**Action-Sufficient Representation: Regulation, Sensorimotor Contingencies, and Latent World Models**
Neil D. Lawrence

---

## What this paper is about

Two views of adaptive behaviour appear, at first sight, to conflict. The **good regulator theorem** (Conant and Ashby, 1970) says every successful regulator must be a *model* of the system it regulates. **Sensorimotor accounts** of perception (O'Regan and Noë, 2001) deny that intelligence requires a stored internal replica of the world; perception is constituted by lawful contingencies between action and sensory change.

This paper argues the conflict is only apparent. A regulator need not represent the world faithfully. It must preserve those distinctions that matter for the consequences of its available actions on the variables it regulates. We call such a representation **action-sufficient**.

### The four contributions

1. The good regulator principle and sensorimotor accounts are compatible once "model" is understood as a generally lossy, task-relative, action-sufficient representation rather than a stored faithful replica.

2. Conant and Ashby's entropy-minimisation argument and the classical MDP result that a deterministic optimal policy exists share the same mechanism: a concave (or linear) objective minimised over the policy polytope is minimised at a vertex, and the vertices are the deterministic policies. The objectives differ; the structural mechanism and conclusion are the same. This connection does not appear to have been made explicit before.

3. Forward and inverse dynamics provide complementary pressures for learning action-sufficient representations: forward prediction preserves consequence-relevant structure, while inverse prediction prevents collapse by preserving action-relevant distinctions.

4. Modern RL architectures can be classified by where they place action-relevant structure — in a policy, a consequence model, online interaction, or a learned representation — yielding a four-way taxonomy.

### Key concepts

- **Action sufficiency**: a representation `R = f(O)` is action-sufficient for outcome `Y` when `p(y | o, a) = p(y | f(o), a)` for all `o, a` — the raw observation adds nothing to predicting action consequences once the representation is known.
- **Consequence equivalence**: two states are consequence-equivalent for outcome `Y` when they share identical action-conditioned consequence distributions `p(y | s, a)` for all actions. The quotient `S / ~_Y` is the coarsest state space sufficient for the task, is determined entirely by the consequence channel (not the state distribution), and is invariant to distributional shift.
- **Outcome variable `Z`**: the regulated variable whose entropy the policy minimises — the thing being regulated, not the reward scalar. For an RL reader: the sufficient statistic for reward, the payoff-relevant projection of the transition.
- **The Nikolic critiques**: the paper explicitly addresses the near-tautology charge (bare determinism `H(A|S) = 0` is a weak sense of "model") and the distribution-fragility charge (the minimal `h` is regime-specific); the consequence-equivalence partition is the distribution-free answer to the second, while the first is acknowledged rather than dissolved.

---

## Files

| File | Status | Description |
|---|---|---|
| `action-sufficient-representation-llm-gist-draft.tex` | **LLM gist draft — proofs not verified** | Main paper. Full argument, all sections, bibliography via `action-sufficient.bib`. Marked with a header warning: proofs and claims generated with LLM assistance and not independently checked. |
| `action-sufficient.bib` | Current | BibTeX bibliography in `Lastname-keywordYY` key format (e.g., `Conant-good70`, `Levine-reinforcement18`). |
| `good-regulator-information-theoretic.tex` | Unpublished companion | "Every Good Regulator of a System Must Be a Model of That System: An Information-Theoretic Reformulation." This shorter paper develops the entropy-minimisation argument and the cause-controlled / error-controlled causal diagrams in more detail. Its ideas are incorporated into the main paper. Not intended for separate submission. |

---

## Building the paper

```bash
pdflatex action-sufficient-representation-llm-gist-draft.tex
bibtex  action-sufficient-representation-llm-gist-draft
pdflatex action-sufficient-representation-llm-gist-draft.tex
pdflatex action-sufficient-representation-llm-gist-draft.tex
```

Requires a standard LaTeX distribution with `amsmath`, `amsthm`, `natbib`, `booktabs`, `tikz`, `enumitem`, `hyperref`, and `xcolor`.

---

## Status and caution

The main `.tex` file carries a prominent header: **LLM Gist Draft — Proofs/Claims Not Verified**. The mathematical structure and argument are intended to be correct, but the proofs and some cross-references were drafted with LLM assistance and should be checked independently before any submission or citation.

The `good-regulator-information-theoretic.tex` companion is a working document and will not be submitted separately; treat it as internal background.

---

## Related work (not in this repo)

The immediate computational motivation for this paper comes from work on **sensorimotor world models** (`Ivashkov-smwm26` in the bibliography) — a concurrent machine-learning paper showing that combining forward latent prediction with inverse dynamics regularization produces compact representations aligned with the controllable structure of an environment. This paper extracts the general principle behind that finding and connects it to the GRT and sensorimotor theory.


