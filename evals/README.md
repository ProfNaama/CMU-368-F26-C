# Alex evaluations: guide to the local files

This is the evaluation workspace on Rico's computer, inside `CMU-368-F26-C/evals/`. It contains the test participants, scripts, saved conversations, and reports used to compare Alex's two conversation formats. Most of this folder is deliberately excluded from GitHub.

**Start with [the round-by-round report](prompt_consistency/README.md)** for what changed from the baseline through Eval #16, the scores, and definitions of every score column. Open [results.csv](prompt_consistency/results.csv) for the same rounds in a spreadsheet.

## Folder structure

The tree below lists the files used for the browser evaluations. Paths are relative to the project root, `CMU-368-F26-C/`, on Rico's computer.

```text
evals/
├── README.md                       This guide, tracked in Git
├── personas.json                   12 test participants, each with 6 fixed answers
├── browser_eval.py                 Runs one test conversation through the website
├── eval_versions.py                Shared single-turn / multi-turn labels and answer grouping
├── test_browser_versions.py        Offline regression checks for format labels
├── run_batch.py                    Runs batches and compares their recommended titles
├── build_table.py                  Builds the older CSV/HTML comparison table
├── prompt_consistency/             The part of evals/ tracked in Git
│   ├── README.md                   Detailed history, scores, definitions, and limits
│   └── results.csv                 One row per round: baseline and Evals #1–#16
├── backups/                        Original transcript archive and rename/hash receipt
└── browser_results/                Saved website tests on Rico's computer
    ├── baseline/                   Original-prompt conversations
    ├── eval1/ ... eval16/           Conversations for each tested round
    ├── eval1_preflight/             Small preliminary check, separate from round scores
    ├── eval2_preflight/             Another preliminary check
    ├── summary.csv                 Older per-persona comparison table
    ├── summary.html                Browser-readable version of that older table
    └── <other files>               Standalone chats and execution logs
```

There is no `browser_results/eval4/`: that proposed change was undone before testing. The scored rounds used browser conversations and compared whether the same three titles were recommended in both formats, ignoring their order.

## What is on GitHub?

This documentation update tracks three files inside `evals/`: this guide, `evals/prompt_consistency/README.md`, and `evals/prompt_consistency/results.csv`. The scripts, personas, full chat transcripts, and generated comparison tables remain on Rico's computer. This is controlled by the project's `.gitignore`.

The summary was originally pushed to `prompt_consistency_eval/` at the project root on `main`. Commit `90ad4b1` moved it into `evals/prompt_consistency/`. The inspected `main` and `prompt-consistency` refs at `8d25ea7` both include that move. The old path is historical, not a second set of experiments.

The round-by-round report contains no links to local-only transcripts: someone reading it on GitHub can understand the findings without having the folders on Rico's computer. The transcripts include study completion codes, so they remain on Rico's computer. A fresh clone does not include enough evaluation files to rerun these tests.

## Conversation formats and filenames

The prompt files, browser scripts, saved transcript filenames, and generated summary now use the same labels: `single` for all six answers at once, and `multi` for one answer at a time.

| Conversation format | Website treatment group (ID) | Prompt and opening filenames | Browser script / transcript label |
|---|---|---|---|
| All six answers in one message | 1 | `hidden_prompt_single_turn.txt`, `opening_single_turn.txt` | `single` |
| One answer per message across six exchanges | 2 | `hidden_prompt_multi_turn.txt`, `opening_multi_turn.txt` | `multi` |

The prompt and opening files are under `experiment_configuration/hidden_prompts_bank/` and `experiment_configuration/opening_messages_bank/`. `treatment_groups_config.csv` maps the files to the website groups. The 653 saved transcript filenames were corrected using the actual opening message to identify the format. Their contents and historical scores were preserved. The original transcript archive and filename/hash receipt are under `evals/backups/` on Rico's computer. Historical execution logs retain the labels printed at the time; the readers classify transcripts from their openings, so older copies can still be read correctly.

For example, `p01_light_comedy_single_t3_20261116_213158.txt` means:

| Filename part | Meaning | Unit / format |
|---|---|---|
| `p01_light_comedy` | Persona ID from `personas.json` | Identifier |
| `single` | All six answers sent together in one message | Category |
| `t3` | Third conversation for that persona in that format | Trial number |
| `20261116_213158` | Save timestamp generated on Rico's computer | `YYYYMMDD_HHMMSS`; filename has no time-zone marker |

## How the browser evaluations work

The baseline and Eval #1–#16 scores come from website conversations saved in `browser_results/` on Rico's computer. The main measure is an exact match of all three recommended titles between the two formats, ignoring title order.

1. `browser_eval.py` opens the website, completes its forms with test answers, and identifies the format from Alex's opening message.
2. It reads a persona's six answers from `personas.json`. In the all-at-once format it combines them into one numbered message; in the one-at-a-time format it sends each answer separately.
3. It saves Alex's messages and the persona's answers in a transcript. It also finishes the study flow, so a real browser run can save a test session to the website's configured results destination.
4. `run_batch.py` pairs trial 1 with trial 1, trial 2 with trial 2, and so on for the same persona across formats. It compares the three recommended titles, ignoring their order.

A **chat** is one complete conversation. A **pair** is two chats: the same persona and trial, one in each format. With 12 personas, one trial per format gives 24 chats and 12 pairs; three trials give 72 chats and 36 pairs.

To re-score existing files without opening the website or calling a model, run this from the project root:

```bash
python3 evals/run_batch.py --score-only --label eval15 --trials 3
```

Change the label to the saved round and use `--trials 1` for a one-trial round. The command prints results; it does not rewrite `prompt_consistency/results.csv`. That historical CSV is maintained separately.

`run_batch.py` also flags a final reply with other than three extracted picks, a recommendation of the persona's stated favorite, and extra reaction text in the one-at-a-time question messages. Those checks are not a full assessment of recommendation quality.

## Which summary should I open?

| File | What one row represents | What it tells you |
|---|---|---|
| `prompt_consistency/results.csv` | One evaluation round | How each prompt or settings revision scored across its completed pairs |
| `browser_results/summary.csv` or `.html` | One persona in one format | The three picks, transcript, and shared-title count for an older standalone run |

`build_table.py` reads only `.txt` files directly in `browser_results/`, keeping the newest file per persona and format. It does not read nested rounds such as `eval15/`, and its filename pattern does not accept the batch `_t1_` trial tag. Its table is not a combined summary of all evaluation rounds.

In that older table, `Pick 1`–`Pick 3` are title descriptions (text); `Offers 'My List'` is a yes/no text check; and `Same titles in both treatments` reports 0–3 shared titles. Offering My List does not prove the app can save anything there.

## What this documentation does not establish

The historical browser scores measure title consistency on these 12 personas. They do not establish participant satisfaction, current Netflix availability, recommendation quality, statistical significance, or the current deployed model/settings. The test-session filter briefly added in `90ad4b1` was reverted in `9733c54`; the current app code does not exclude sessions just because their questionnaire answers contain `EVAL TEST`.

The workflow recorded in commit `8d25ea7` is to continue testing through the site and have Naama remove the `EVAL TEST` sessions afterwards. That records who handles cleanup; it does not verify that any particular database rows have already been deleted.
