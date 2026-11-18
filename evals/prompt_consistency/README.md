# Alex prompt consistency: changes and scores by evaluation round

This report explains the saved browser evaluations from the baseline through Eval #16. It is self-contained: you can read the changes, scores, and definitions here without having the local transcripts or Python scripts.

**Best recorded full run:** Eval #13 matched all three titles in **31 of 36 pairs (86%, rounded)**. The target was at least 90%; with 36 pairs, that requires at least 33 matches. No recorded round reached that target. These are consistency scores, not recommendation-quality or participant-satisfaction scores.

The compact spreadsheet is [results.csv](results.csv). Its `change` cells give expanded descriptions; the numerical score fields have been preserved. The detailed histories below explain what each round added, removed, or retained.

## What was compared

Each of 12 fixed test participants (personas) supplied the same six answers in both formats:

| Format | How the answers arrive | Website group (ID) | Website prompt filename | Browser-test label |
|---|---|---|---|---|
| All at once | Six answers in one numbered message | 1 | `hidden_prompt_single_turn.txt` | `single` |
| One at a time | One answer per message, across six exchanges | 2 | `hidden_prompt_multi_turn.txt` | `multi` |

The prompt filenames, browser scripts, saved transcript filenames, and generated summary use the same convention: **single-turn = all at once** and **multi-turn = one at a time**. The 653 saved transcript filenames were corrected from the actual opening messages without changing their contents or any historical scores. Their original archive and a filename/hash receipt are kept under `evals/backups/` on Rico's computer. Historical execution logs retain the original labels printed at the time; transcript readers determine the format from the opening message.

One **chat** is a complete conversation in one format. One **pair** is the same persona and trial in both formats. A quick run has 12 personas × 2 formats × 1 trial = 24 chats / 12 pairs. A full run has 12 × 2 × 3 = 72 chats / 36 pairs. In a full run, trial 1 is paired with trial 1 across formats, and likewise for trials 2 and 3.

The comparison extracts numbered picks from Alex's final message and normalizes the title text: it lowercases it, removes year-and-following metadata when the expected year pattern is present, removes punctuation, and drops a leading “The.” Title order is ignored. The batch scorer compares sets and requires three extracted picks in the one-at-a-time reply; it separately flags a reply with other than three extracted picks. It does not check that all three titles are distinct. This is a text parser, not a verified movie database.

**Example:** `[A, B, C]` versus `[C, A, B]` is an exact match; `[A, B, C]` versus `[A, B, D]` shares 2 of 3 titles but is not an exact match. An explanation can change while the title set stays the same.

## Score table: all rounds

`—` means not applicable or not measured, not a score of zero. Rates are rounded to the nearest whole percent, using the completed pairs as the denominator. Preflight folders are excluded. Three-trial rows below use all three trials, not just their initial quick check.

| Round (ID) | Change summary | Saved chats (count) | Exact matches (pairs / completed pairs) | Match rate (%) |
|---|---|---:|---:|---:|
| Baseline | Original prompts; no common title-selection procedure | 24 | 5/12 | 42 |
| 1 | Shared selection rules; bare questions; fixed summary order | 24 | 5/12 | 42 |
| 2 | Accept vague answers; fame tie-break; default temperature 0 | 24 | 4/12 | 33 |
| 3 | Separate role for each pick; incomplete run | 23 | 6/11 | 55 |
| 4 | Fixed catalog proposed, rejected, and undone; not run | 0 | — (not run) | — |
| 5 | Exact answer restatement; favorite title becomes main guide | 24 | 7/12 | 58 |
| 6 | Similarity guide written before picks; exact answer copying | 24 | 9/12 | 75 |
| 7 | Story-world/creator priority; resolve unclear format | 72 | 21/36 | 58 |
| 8 | Same prompts; force temperature 0 and seed 368 | 24 | 6/12 | 50 |
| 9 | Sequels/spin-offs first; narrower fallback; own-title check | 24 | 7/12 | 58 |
| 10 | Third pick chosen by creator/director | 24 | 6/12 | 50 |
| 11 | Titles before descriptions; remove creator-based third pick | 24 | 5/12 | 42 |
| 12 | Netflix originals only; simplify rules; restore descriptions | 24 | 9/12 | 75 |
| 13 | Write format/original restriction into guide; change fallback | 72 | 31/36 | 86 |
| 14 | Break similarity ties by earlier release | 72 | 30/36 | 83 |
| 15 | Clarify original-series exclusions with concrete examples | 72 | 30/36 | 83 |
| 16 | Same Eval 15 prompts; remove seed and restore old temperature rule | 72 | 26/36 | 72 |

### What the table headers mean

| Header | Definition | Unit / how to read it |
|---|---|---|
| Round (ID) | Baseline or the numbered prompt/settings revision | Identifier, not a score |
| Change summary | Short description of what changed; expanded below | Text |
| Saved chats (count) | Saved conversations included in that round, across both formats | Conversations; one extra unpaired conversation is included in Eval #3 |
| Exact matches (pairs / completed pairs) | Pairs whose normalized title sets are identical, divided by pairs with both chats available | Count / count; `31/36` means 31 matching pairs out of 36 completed pairs |
| Match rate (%) | `100 × exact matching pairs / completed pairs` | Percent, 0–100; it does not mean 86% of individual recommendations were good |

Eval #3 has 23 saved chats: 11 complete pairs and one unpaired chat. Only its 11 pairs enter the match rate. Eval #4 has no conversations and no score.

### Repeatability and identical replies: full runs only

These supplementary measurements describe variation across repeated conversations. The primary success measure remains an exact match of all three recommended titles between formats, ignoring their order. The quick runs have one trial per persona/format, so there is no repeatability comparison for them.

| Round (ID) | One-at-a-time title repeats (matches / comparisons) | All-at-once title repeats (matches / comparisons) | Identical final replies, both formats (matches / comparisons) |
|---|---:|---:|---:|
| 7 | 18/24 | 18/24 | 2/48 |
| 13 | 22/24 | 20/24 | 2/48 |
| 14 | 22/24 | 23/24 | 6/48 |
| 15 | 21/24 | 21/24 | 0/48 |
| 16 | 20/24 | 20/24 | 0/48 |

For **title repeats**, compare trial 1 with trial 2 and trial 1 with trial 3 within the same format and persona. Count a success when the normalized title sets match, ignoring order. Each format has 12 personas × 2 comparisons = **24 comparisons**. For example, `22/24` means the title set repeated in 22 of those 24 comparisons. This is context for model variability, not a mathematical upper bound on agreement between formats.

For **identical final replies**, make those same comparisons across both formats: 12 personas × 2 comparisons × 2 formats = **48 comparisons**. Count a success only when the parsed final reply texts are exactly equal, including wording and title order. A score of `0/48` can coexist with high title repeatability because descriptions or ordering changed. It does not mean zero repeated titles.

### CSV column dictionary

The original machine-readable headers remain unchanged. A blank numeric cell means not measured or not applicable; Eval #4 is explicitly not run.

| CSV header | Meaning | Unit / format |
|---|---|---|
| `eval` | Baseline or round number | Identifier |
| `commit` | Git revision associated with that round's prompt/settings change | Short commit SHA; not deployment proof |
| `change` | Expanded description of the intervention, including important reversals | Text |
| `chats_run` | Saved conversations included in the round | Conversation count |
| `pairs_matched` | Completed cross-format pairs with identical normalized title sets | Pair count |
| `pairs_total` | Cross-format pairs with both conversations available | Pair count |
| `match_pct` | `100 × pairs_matched / pairs_total`, rounded | Percent, 0–100 |
| `repeat_one_by_one` | Title-set repeats against trial 1 in the one-at-a-time format | Matching comparisons / available comparisons; out of 24 for the recorded full runs |
| `repeat_all_at_once` | Title-set repeats against trial 1 in the all-at-once format | Matching comparisons / available comparisons; out of 24 for the recorded full runs |
| `identical_replies_vs_trial1` | Exactly equal parsed final reply texts against trial 1, combining both formats | Matching comparisons / available comparisons; out of 48 for the recorded full runs |

## Detailed change history

The descriptions below were checked against Git diffs for the listed commits. Changes generally carry forward until a later round explicitly removes or replaces them. Several rounds change more than one instruction, so their scores do not isolate the effect of a single sentence. Rounds #1–#15 were recorded on November 16, 2026; #16 on November 17, 2026, using saved transcript dates and commit history.

### Baseline — original prompts (`a98e34f`)

- **Starting behavior:** Alex summarized preferences in its own words and recommended three titles it believed were available on Netflix US. The one-at-a-time version could add a short reaction before the next question. There was no common step-by-step rule for choosing the same titles in both formats.
- **Result:** 5/12 matching pairs (42%), from 24 chats. This is the reference point for the later prompt changes; it has no repeated trials.

### Eval #1 — shared selection rules and bare questions (`1ad375a`)

- **Changed:** In both prompts, make the recently enjoyed title the strongest clue, matching genre/style and country/language. Exclude the enjoyed or already-seen titles, respect format/time/avoidances, and prefer popular Netflix US titles. Require the opening recommendation summary to cover all six answers in question order.
- **Conversation change:** In the one-at-a-time format, remove reactions, thanks, and comments between answers; send only the next question. This also reduces differences in conversational tone before the recommendations.
- **Result:** 5/12 pairs (42%), 24 chats. The recorded title agreement did not improve over the baseline.

### Eval #2 — accept vague answers; stronger popularity rule (`a5cc5bb`)

- **Changed:** Explicitly accept “idk,” “anything,” “not sure,” “whatever,” and “no” as answers rather than asking again. Replace the general popularity rule with the three most famous / most watched fitting titles: “the titles most people would name first.”
- **Settings change:** In `config.js`, change the temperature fallback from `0.2` to `0`. An `OPENAI_TEMPERATURE` environment value still takes precedence, so this commit does not prove the hosted requests actually used zero. There is no seed yet.
- **Result:** 4/12 pairs (33%), 24 chats. This round changed both prompts and the temperature fallback; the score cannot separate their effects.

### Eval #3 — give each pick a different job (`5eaf974`)

- **Changed:** Pick 1 should most resemble the recent favorite. Pick 2 should be a top title in the favorite genre matching the mood. Pick 3 should match the desired format and available time, differing from the first two picks. Choose the more watched title when two candidates tie.
- **Purpose:** Replace an open-ended three-title choice with explicit roles for each position while retaining the existing constraints.
- **Result:** 6/11 pairs (55%), from 23 saved chats. One chat lacks its counterpart; the reason for the missing chat is not established here. Do not read this as a complete 12-pair run.

### Eval #4 — fixed ranked catalog, rejected before testing (`15f29a8`)

- **Proposed:** Embed ranked genre lists of named titles. Select the list using a Korean favorite or the first named genre, filter by format/seen titles/avoidance tags, then take the first three remaining entries, with a “Popular picks” fallback. Mood and time would not affect selection. The one-at-a-time prompt also said to read all six answers together at the recommendation step.
- **Disposition:** This fixed-list approach was rejected and reverted in `f21a872` before testing. The revert restored the earlier selection approach and told the one-at-a-time model to read all six answers together in its choosing instructions.
- **Result:** 0 chats; no pairs or percentage. This is an abandoned change, not a failed evaluation or a measured zero-percent result.

### Eval #5 — copy the answers, then use the favorite as the main guide (`ac2be61`)

- **Changed:** Replace the per-pick jobs with three best-known titles that fans of the recently enjoyed title watch next. Begin with `Got it: [answer 1]; ...; [answer 6].`, copying the answers rather than paraphrasing, and choose only from that written line. Remove the redundant one-at-a-time instruction to read the answers together.
- **Constraints and fallback:** Keep the format and avoidance filters and exclude the enjoyed title. Explicitly stop using mood or time to choose titles. If no favorite is named, use the first genre, then overall Netflix US popularity if no genre is named. Missing/vague answers no longer require assumptions to be mentioned in a free-form summary.
- **Result:** 7/12 pairs (58%), 24 chats. Agreement increased in this run, but selection now deliberately uses less of the participant's stated preferences.

### Eval #6 — write the similarity guide before the picks (`14bb779`)

- **Changed:** Replace “what fans watch next” with similarity in genre, kind of story, and country/language. Make the favorite the only selection guide, with format and avoidance filters; popularity or a match to mood/time alone is insufficient. Retain a popularity fallback when no favorite is given.
- **Presentation:** Require exact copying, including capitalization, in the `Got it` line. Add a second fixed line: `Since you liked [title], here are 3 picks most like it:`; use a popularity introduction if no favorite exists.
- **Result:** 9/12 pairs (75%), 24 chats. The prompt both changes selection wording and makes that selection guide visible before title generation.

### Eval #7 — fixed candidate priority and format fallback (`e0e938c`)

- **Changed:** Prefer titles in the same series, story world, or from the same creators before other popular genre/story matches; break similarity ties by popularity. For “either” or an unclear format, require all picks to have the recent favorite's format, instead of allowing a mixture of movies and shows.
- **Retained:** The copied answers, written similarity guide, format/avoidance filters, and no-favorite fallback from the preceding round.
- **Result:** 21/36 pairs (58%), 72 chats. Its first-trial subset was 9/12; the headline score includes all three trials. Title repeatability was 18/24 in each format; identical final replies were 2/48.

### Eval #8 — force temperature zero and add a seed (`fc627c3`)

- **Changed:** No prompt edits. Set `config.apiTemperature = 0` unconditionally, ignoring the environment override for temperature; add `config.apiSeed = 368` and pass it in `app.js`'s model request. Temperature is a sampling setting, not a percentage; the seed is an integer parameter, not a score.
- **Purpose:** Test whether explicitly controlling request settings would make the title choices more consistent. A fixed setting does not guarantee identical outputs.
- **Result:** 6/12 pairs (50%), 24 chats, using the Eval #7 prompts. Because this round has only one trial per persona/format, it provides no within-format repeatability measurement.

### Eval #9 — remove creator priority; narrow the no-favorite fallback (`b9c3f78`)

- **Changed:** Replace the broader same-series/story-world/creator priority with sequels, prequels, and spin-offs first, then popular genre/story matches. Add an explicit final check that none of the picks repeats the title in `Got it`.
- **Fallback:** If no favorite is named, use popular Netflix original series in the first genre, or popular Netflix original series overall if no genre is given. This restriction applies to the fallback here; it does not yet restrict every recommendation to Netflix originals.
- **Result:** 7/12 pairs (58%), 24 chats. Temperature zero and seed 368 remain in the app code.

### Eval #10 — choose the third title by creator/director (`ff8a6ad`)

- **Changed:** Choose picks 1 and 2 using the prior similarity and story-world priority. Choose pick 3 as the best-known other title by pick 1's creator/director, using pick 2's creator/director if none fits the required format.
- **Exclusions:** Extend the enjoyed-title exclusion to specials, documentaries, and behind-the-scenes titles about it. Retain the explicit final own-title check.
- **Result:** 6/12 pairs (50%), 24 chats. This run did not improve agreement over Eval #9.

### Eval #11 — list all titles before explaining them (`3e9b45e`)

- **Changed:** Remove the creator-based third-pick rule and return all three picks to the previous similarity/story-world procedure. List the three numbered title lines consecutively, then put their descriptions below as unnumbered sentences beginning with the title name.
- **Purpose:** Test a presentation sequence in which explanations do not interrupt generation of the three-title list. Because the selection rule also changed, this is not an isolated formatting test.
- **Result:** 5/12 pairs (42%), 24 chats.

### Eval #12 — Netflix originals only and simpler selection (`0319a43`)

- **Changed:** Restrict all three picks to Netflix originals, described in the prompt as titles made or released by Netflix as an original. Choose by similarity to the favorite with a popularity tie-break; remove the special story-world priority. Restore a description immediately under each title, reversing Eval #11's separate explanation block.
- **Retained / removed:** Keep format/avoidance checks and the favorite/related-special exclusions. Remove the explicit final self-check wording. The no-favorite fallback still uses popular Netflix original series. These were prompt instructions, not checks against a live catalog.
- **Result:** 9/12 pairs (75%), 24 chats. Candidate restriction, simpler selection, and presentation changed together.

### Eval #13 — put format and the original restriction into the guide (`5b8de24`)

- **Changed:** Make the second line say `Since you liked [title], here are 3 Netflix original [movies or TV shows] most like it:`. Require one explicit format, resolving “either” to the favorite's format. State that shows first aired on a TV network are not Netflix originals even if Netflix streams them.
- **Fallback:** If no favorite is given, instruct Alex to use the top three shows, in order, from Netflix's official all-time “Most Popular English TV” list. The app does not fetch that list; this is model instruction text.
- **Result:** 31/36 pairs (86%), 72 chats: the highest recorded full-run agreement. Its first-trial subset was 12/12. Title repeats were 22/24 one at a time and 20/24 all at once; identical replies were 2/48. This still falls short of 33/36, the minimum for the target.

### Eval #14 — earlier release date breaks ties (`6e0e206`)

- **Changed:** For two equally similar Netflix originals, choose the earlier release instead of the more watched title. The rest of Eval #13's prompts and request settings remain unchanged.
- **Purpose:** Replace a model-estimated popularity tie-break with a release-date rule. Release dates are still supplied from model knowledge, not a database lookup.
- **Result:** 30/36 pairs (83%), 72 chats; first-trial subset 11/12. Title repeats were 22/24 one at a time and 23/24 all at once; identical replies were 6/48. Cross-format agreement was one pair lower than Eval #13 despite higher all-at-once repeatability.

### Eval #15 — clarify what counts as a Netflix original (`4f50c36`)

- **Changed:** Expand the exclusion to a show first aired on a TV network in any country, even if Netflix later streams it or labels it an original. Use *Breaking Bad* and *Money Heist* as concrete examples of titles excluded by this experiment's rule. This describes the prompt's chosen definition, not an independently verified catalog classification.
- **Retained:** The earlier-release tie-break, copied answer line, format-specific guide, no-favorite fallback, temperature zero, and seed 368.
- **Result:** 30/36 pairs (83%), 72 chats; first-trial subset 10/12. Title repeats were 21/24 in both formats; identical replies were 0/48. The overall exact-match rate equaled Eval #14, though individual pairs can differ.

### Eval #16 — restore the old settings with Eval #15 prompts (`87e7f0c`)

- **Changed:** Keep the Eval #15 prompts unchanged, remove the seed from requests, and restore the temperature rule `OPENAI_TEMPERATURE` if supplied, otherwise `0.2`. The hosted environment value was not verified, so describe this as the original temperature rule, not a confirmed temperature of 0.2.
- **Result:** 26/36 pairs (72%), 72 chats. Title repeats were 20/24 in each format; identical replies were 0/48. Relative to Eval #15, agreement fell by 4 pairs, or 11.1 percentage points using unrounded rates. This is one run per setting, not a statistical test proving the settings caused the difference.
- **After testing:** Commit `04ac259` restored temperature zero and seed 368. Eval #16 was a settings test, not a new prompt design.

## After Eval #16: tested state versus current branch draft

The historical `main` snapshot at `4cfbbe4` contains the Eval #15 prompts with temperature zero and seed 368 restored. This is a repository snapshot, not a fresh inspection of the deployed website.

Commit `3038eb2` contains a later **untested draft**, included in both inspected remote refs (`main` and `prompt-consistency`) at `8d25ea7`. It removes the Netflix-original-only restriction and replaces the favorite-only guide with an ordered use of all answers: format and avoidances first, then similarity to the favorite, genres/mood, and available time. It uses popularity then earlier release as tie-breaks, changes the guide to `Based on your answers, here are 3 [movies or TV shows] for you:`, and uses genres/mood if no favorite is named. There is no recorded score for this draft, and it is not presented as Eval #17 or assigned any earlier round's score. Its presence on `main` does not independently establish deployment.

## What the results support, and their limits

- The recorded agreement improved from 5/12 at baseline to a best full-run score of 31/36, but the rounds have different sample sizes and many change several rules at once.
- Later high-agreement prompts narrow the candidate pool and prioritize the favorite title over some other preferences. Higher agreement therefore does not demonstrate better personalization.
- The browser rounds measure exact agreement of the three recommended titles. They do not establish recommendation quality, title existence, current Netflix availability, satisfaction, or statistical significance. The same 12 personas were reused while tuning; unseen-persona performance remains unknown.
- The comparison checks normalized title strings, ignores order, and relies on a parser. A shared title set can still have different rankings or explanations. A parser failure can affect a score.
- Model settings and commit references document intended code changes; hosted environment overrides and deployment state were not independently verified here.

## Where the underlying records live

The summary files in this folder are tracked in Git. They were originally under the root folder `prompt_consistency_eval/`; commit `90ad4b1` moved them here. Both inspected remote refs, `main` and `prompt-consistency` at `8d25ea7`, include the move.

Raw transcripts are kept on Rico's computer at `evals/browser_results/baseline/` and `evals/browser_results/eval<N>/`, with small preflight runs in separate folders. There is no Eval #4 transcript folder. Test participants are in `evals/personas.json` on Rico's computer; `evals/run_batch.py` computes the browser scores. These paths refer to Rico's computer; they are not folders a GitHub reader can open from this report. Each transcript includes study completion information, so raw chats have not been added to Git.

For this documentation update, all recorded browser match counts, full-run title-repeat ratios, and identical-reply ratios were recalculated offline from the saved transcripts. Score values were preserved; no new model conversations were run. Commit references were checked against the local Git history.

## Test sessions and saved study results

Browser tests fill questionnaire text fields with `EVAL TEST` and finish the normal study flow. The app's saving code can therefore write test sessions to its configured results destination. An automatic exclusion for that marker was briefly added in `90ad4b1`, then reverted in `9733c54`; the current code does not provide that exclusion.

The workflow recorded in commit `8d25ea7` is to keep testing through the site and have Naama remove the `EVAL TEST` sessions afterwards. This is the documented cleanup responsibility, not evidence that any particular cleanup has already happened.

The number of test rows in any hosted database, their destination, and any cleanup are not verified by this report. Recognizing the marker in the test code on Rico's computer does not prove which remote rows exist or that any rows have been removed.
