# WorkTrace: evidence tests, track records and LLM judges for delegating decisions to AI agents

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23868234.svg)](https://doi.org/10.5281/zenodo.23868234)

Code, data and paper sources for the prospectively specified pilot described in
*Which Decisions Can an AI Agent Take Without Review? A Prospectively Specified Pilot Comparing Evidence Tests,
Track Records and LLM Judges* (Szymon P. Pepliński, Generatywnie, 2026; arXiv preprint).

Everything here is synthetic: a fictional EU credit institution, generated registers, authorities and documents,
and a policy that paraphrases public legal texts (AMLR, EBA guidelines, FATF Recommendations). No real data are used
and no claim of regulatory compliance is made. This is not legal advice.

## Layout

| Path | Contents |
|---|---|
| `worktrace/` | generator, oracles, intervention operators, agent harnesses, LLM judge (`judge.py`, rubric v2), analysis (`analysis.py`), reviewed answer key (`answer_key.py`), leave-one-out robustness (`robustness.py`) |
| `tests/` | generator, oracle and answer-key tests |
| `runs/pilot/` | every model decision of the pilot (one JSON record per episode and arm, with the trace, declared grounds and token usage); `runs/judge/` the judge's verdicts; `runs/judge_check/` the stronger-judge check (amendment A10); `runs/known_groups/` the planted-deficit agents; `runs/trial/` the OpenAI smoke trials; `runs/judge/trial_v1/` the judge trial (A3); `runs/excluded/` data excluded by amendment A9 |
| `paper/pilot/` | the analysis plan frozen before data collection, with all amendments (`preregistration.md`), ambiguity log with the legal check (`policy_ambiguities.md`), results (`results_interim.md`, `results_core.md`), `robustness_loo.md`, `multiverse/`, `construct_validity.md`, `token_costs.md`, `known_groups*.md`, the specification (`e1_spec.md`) and the expert review (`expert_review/`: the author's blind answers and verdicts, the sample, the rater pack) |
| `paper/draft/` | the paper's sections in Markdown; `paper/latex/` the LaTeX build and the compiled PDF; `paper/references.bib` with a verification note on every entry |
| `notes/` | reading notes behind the related-work section |
| `scripts/` | shell scripts used to run the pilot (API keys are read from a local `.env`, never committed) |

## Reproducing the analyses (no API access needed)

```bash
uv sync --group dev
uv run --group dev pytest -q
uv run python -m worktrace.analysis --out paper/pilot/results_interim.md          # all data
uv run python -m worktrace.analysis --core --out paper/pilot/results_core.md     # common core (amendment A4)
uv run python -m worktrace.robustness > paper/pilot/robustness_loo.md
uv run python paper/pilot/construct_validity.py
uv run python paper/pilot/multiverse/multiverse.py
uv run python paper/pilot/token_costs.py
uv run python paper/latex/build.py        # needs pandoc and latexmk
```

Every episode, including the held-out and shifted splits, is regenerated deterministically from its seed
(`worktrace/classes.py`, seed bases in `worktrace/analysis.py`); all seeds are public. A private seed range is
reserved for the second phase.

## Running agents

`RUNNING.md` describes the pilot runs (Anthropic and OpenAI APIs, local models through Ollama, decision models).
They need API keys in a local `.env` and are not required to reproduce any number in the paper.

## Licences

Code: Apache License 2.0 (`LICENSE`). Texts, data, run logs, results and the paper: CC BY 4.0 (`LICENSE-DATA`).

## Citation

See `CITATION.cff`. Release v1.1 is the version the paper describes, archived at Zenodo under the concept DOI [10.5281/zenodo.23868234](https://doi.org/10.5281/zenodo.23868234), which resolves to the latest version. The arXiv identifier will be added here once assigned.
