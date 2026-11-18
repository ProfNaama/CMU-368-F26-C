# Alex prompt consistency: changes and scores by evaluation round

This report covers the saved browser evaluations from the baseline through Eval #16 and the prompt changes merged since then.

**A new evaluation of the updated single-turn and multi-turn prompts is pending.** The current prompts use the answers participants provide to guide recommendations. Single-turn can recommend after a partial reply, and multi-turn waits for all six answers. The last scored round was Eval #16.

**Best recorded full run:** Eval #13 matched all three titles in **31 of 36 pairs (86%, rounded)**. The target was at least 90%; with 36 pairs, that requires at least 33 matches. No recorded round reached that target. These are consistency scores, not recommendation-quality or participant-satisfaction scores.

The compact spreadsheet is [results.csv](results.csv). Its `change` cells now use short action bullets and separate BEFORE, WHY, and EXAMPLE blocks. In a spreadsheet, turn on Wrap Text to display the line breaks. Historical numerical scores are unchanged. The final row, `latest_not_evaluated`, records the pending change with no match score; it is not a completed Eval #17.

[Jump to the final list of changes still in place today](#changes-still-in-place-today-compared-with-the-baseline).

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
| Baseline | Starting instructions; Alex chooses without a shared step-by-step method | 24 | 5/12 | 42 |
| 1 | Use the same choosing rules; ask only the next question; summarize answers in order | 24 | 5/12 | 42 |
| 2 | Accept vague answers; favor widely watched titles; lower the usual variation setting | 24 | 4/12 | 33 |
| 3 | Give picks 1, 2, and 3 different jobs; one conversation is missing | 23 | 6/11 | 55 |
| 4 | Propose a prewritten menu of titles, then remove it before testing | 0 | — (not run) | — |
| 5 | Copy all answers, but choose mainly from the favorite; stop using mood and time | 24 | 7/12 | 58 |
| 6 | Choose similar stories and say why before listing the picks | 24 | 9/12 | 75 |
| 7 | Prefer related stories or creators; use one movie/show format | 72 | 21/36 | 58 |
| 8 | Keep the prompt; force low-variation settings and add a repeatability seed | 24 | 6/12 | 50 |
| 9 | Prefer sequels and spin-offs; narrow the choices when no favorite is given | 24 | 7/12 | 58 |
| 10 | Choose the third pick from the maker of the first recommendation | 24 | 6/12 | 50 |
| 11 | Write all three title names first; remove the special creator rule for pick 3 | 24 | 5/12 | 42 |
| 12 | Allow only Netflix originals; simplify choosing; explain each title underneath | 24 | 9/12 | 75 |
| 13 | Write “Netflix original” and the movie/show format before naming titles | 72 | 31/36 | 86 |
| 14 | When two titles fit equally well, choose the earlier release | 72 | 30/36 | 83 |
| 15 | Clarify which shows are excluded under the Netflix-original rule | 72 | 30/36 | 83 |
| 16 | Keep Eval #15 instructions; try the older variation settings, then restore them | 72 | 26/36 | 72 |
| Updated prompts awaiting evaluation | Use supplied answers in context, align question wording, and simplify the task instructions | 0 | — (pending) | — |

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

The original machine-readable headers remain unchanged. A blank numeric cell means not measured or not applicable. Eval #4 was not run. The `latest_not_evaluated` row points to the updated version at `3a446a6`, with zero evaluated chats and blank score fields.

| CSV header | Meaning | Unit / format |
|---|---|---|
| `eval` | Baseline, round number, or `latest_not_evaluated` for the pending change | Identifier; the pending row is not a completed evaluation |
| `commit` | Git revision associated with that round's prompt/settings change | Short commit SHA; not deployment proof |
| `change` | Short change bullets, followed by separate before/reason/example blocks | Text with line breaks inside one CSV cell |
| `chats_run` | Saved conversations included in the round | Conversation count |
| `pairs_matched` | Completed cross-format pairs with identical normalized title sets | Pair count |
| `pairs_total` | Cross-format pairs with both conversations available | Pair count |
| `match_pct` | `100 × pairs_matched / pairs_total`, rounded | Percent, 0–100 |
| `repeat_one_by_one` | Title-set repeats against trial 1 in the one-at-a-time format | Matching comparisons / available comparisons; out of 24 for the recorded full runs |
| `repeat_all_at_once` | Title-set repeats against trial 1 in the all-at-once format | Matching comparisons / available comparisons; out of 24 for the recorded full runs |
| `identical_replies_vs_trial1` | Exactly equal parsed final reply texts against trial 1, combining both formats | Matching comparisons / available comparisons; out of 48 for the recorded full runs |

## Detailed change history, in everyday terms

A **prompt** is the set of instructions Alex receives before answering. An **iteration** is a revision of those instructions; Evals #8 and #16 instead changed software settings while leaving the instructions alone. The starting version is called the **baseline**. The short codes in headings identify saved versions in Git, so the original change can be found later.

Each round starts with its recorded result, followed by a short **What changed** list. The **Before**, **Why**, and **Example** paragraphs keep the extra context separate. Examples illustrate the rules; they are **not recorded model replies or new test results**. Several rounds changed more than one thing, so a higher score does not prove which individual change helped. Revisions normally carried forward until a later round removed or replaced them.

The important distinction is between **receiving an answer**, **repeating it in a summary**, and **using it to choose a recommendation**. Alex received the six answers in both formats throughout these evaluations. Starting in Eval #5, it copied them all into a “Got it” sentence, while the choosing rules still centered on the favorite title and sometimes explicitly ignored mood and time.

Rounds #1–#15 were recorded on November 16, 2026; #16 on November 17, 2026. The explanations were checked against the saved instruction changes.

### Baseline — starting instructions (`a98e34f`)

**Recorded result:** 5 of 12 completed pairs matched all three titles (42%, rounded), from 24 saved conversations. This is the reference point, not a result of a prompt change.

**What changed**

- Ask the six questions and summarize the answers in Alex’s own words.
- Choose three titles believed to be available on Netflix US.
- Let Alex decide how to balance the preferences; there is no shared step-by-step choosing method.
- Allow a brief reaction before each next question in the one-at-a-time format.

**Before:** This was the starting version, before the numbered changes.

**Why we tried it:** Establish how often the two formats naturally agreed before trying to make their choices more consistent.

**Example (illustrative):** Two people giving the same answers could receive two different sets of three recommendations because Alex was free to decide how to balance their preferences.

### Eval #1 — give both versions the same choosing rules (`1ad375a`)

**Recorded result:** 5 of 12 completed pairs matched all three titles (42%, rounded), from 24 saved conversations.

**What changed**

- Use the recently enjoyed title as the strongest clue to taste, including its genre, style, country, or language.
- Respect the requested movie/show format, available time, and things the person wants to avoid.
- Exclude titles the person has already seen and prefer widely known choices.
- Mention all six answers in the same question order in the summary.
- In the one-at-a-time format, ask only the next question. Remove reactions and thanks between answers.

**Before:** The starting version described the task but left Alex considerable freedom over how to choose the three titles.

**Why we tried it:** Reduce differences caused by either version inventing its own choosing method or adding extra conversational comments.

**Example (illustrative):** If the person enjoyed a Korean drama, both versions should consider similar Korean dramas. After a genre answer, the one-at-a-time version should ask the mood question directly, without an extra reaction.

### Eval #2 — accept short answers and prefer the most widely watched choices (`a5cc5bb`)

**Recorded result:** 4 of 12 completed pairs matched all three titles (33%, rounded), from 24 saved conversations.

**What changed**

- Accept “idk,” “anything,” “whatever,” and “no” as answers. Continue instead of asking the question again.
- Among suitable titles, prefer the three most famous or most widely watched.
- Change the usual temperature setting from 0.2 to 0 to try to reduce variation.
- A separate website setting could still replace that value. The actual live value was not checked.

**Before:** Vague answers could still lead to inconsistent handling, and the popularity instruction only said to prefer popular titles.

**Why we tried it:** Keep both conversations moving through the same questions and give Alex a clearer way to choose between similar options.

**Example (illustrative):** “Anything” counts as an answer. If several titles fit equally well, Alex should favor the ones it believes more people have watched, rather than choosing freely.

### Eval #3 — give each of the three recommendations a different job (`5eaf974`)

**Recorded result:** 6 of 11 completed pairs matched all three titles (55%, rounded), from 23 saved conversations. Only 11 pairs were complete; the extra conversation had no counterpart. The reason for the missing conversation is not established here.

**What changed**

- Pick 1: choose the closest match to the recently enjoyed title.
- Pick 2: choose a popular title that matches the preferred genre and current mood.
- Pick 3: choose a different title that fits the requested movie/show format and available time.
- When two choices seem equally good, prefer the more widely watched one.

**Before:** Alex was choosing three generally suitable titles without a separate purpose for each position.

**Why we tried it:** Try to make the choice more repeatable by telling Alex exactly what each of the three positions should accomplish.

**Example (illustrative):** The first pick is the closest to the favorite; the second is there because it matches genre and mood; the third is there because it fits the format and time. These are three different reasons for inclusion.

### Eval #4 — propose a fixed menu of titles, then reject it before testing (`15f29a8`)

**Recorded result:** Not run. No conversations were evaluated, so there is no matching-pair count or percentage. This must not be read as a zero-percent score.

**What changed**

- Propose a prewritten, ranked menu of titles grouped by genre.
- Use the Korean-drama list for a Korean favorite; otherwise start with the first genre named.
- Skip titles that conflict with the requested format, things to avoid, or titles already seen. Take the first three remaining entries.
- Do not use mood or time to choose from the menu. Tell the one-at-a-time version to read all six answers together when choosing.
- Reject and remove this fixed-menu proposal before testing it; restore the earlier choosing rules.
- The restored instructions include a reminder to consider the six answers together. No evaluation ran for the fixed menu.

**Before:** Alex could choose from titles it knew, using the selection rules from Eval #3.

**Why we tried it:** A fixed menu could make matching easier, but it would also restrict what Alex was allowed to recommend. That approach was not accepted.

**Example (illustrative):** Instead of thinking of three suitable comedies, Alex would work down a prewritten comedy list and take the first three allowed entries. This approach was never measured.

### Eval #5 — copy all six answers, but choose mainly from the enjoyed title (`ac2be61`)

**Recorded result:** 7 of 12 completed pairs matched all three titles (58%, rounded), from 24 saved conversations.

**What changed**

- Remove the separate job assigned to each recommendation.
- Copy all six answers, in order, into a “Got it” line. Use that written summary when choosing.
- Choose three well-known titles that fans of the recently enjoyed title might watch next.
- Keep the movie/show and avoidance checks. Do not recommend the enjoyed title itself.
- Explicitly stop using mood and available time to choose titles.
- If no favorite is named, use the first genre; if no genre is named either, use general Netflix US popularity.
- Remove the extra instruction to read the answers together; the copied summary now serves that purpose.

**Before:** The three picks had different jobs, including matching mood and available time.

**Why we tried it:** Reduce the number of competing preferences Alex had to balance and give both formats the same written summary before choosing.

**Example (illustrative):** Alex could repeat “I want something light” and “I have one hour” in the summary, while still choosing mostly from fans’ next-watch options for the favorite. Repeating an answer did not mean it was used to choose the titles.

### Eval #6 — say why the picks resemble the enjoyed title before listing them (`14bb779`)

**Recorded result:** 9 of 12 completed pairs matched all three titles (75%, rounded), from 24 saved conversations.

**What changed**

- Replace “what fans watch next” with titles similar in genre, kind of story, and country or language.
- Write the guide sentence before the picks: “Since you liked [title], here are 3 picks most like it:”.
- Copy the exact wording and capitalization of every answer in the “Got it” line.
- Keep movie/show and avoidance checks. A match to mood, time, or a separately named genre alone is not enough; the favorite remains the main choosing guide.
- If no favorite is given, use popular choices in the first genre, or overall popularity if no genre is given.

**Before:** Alex was choosing what fans of the favorite might watch next, which could include titles that were not very similar.

**Why we tried it:** Make the reason for choosing the recommendations more specific and have Alex state that reason before producing the list.

**Example (illustrative):** “Other titles fans watch” becomes “other titles with a similar story and feel.” For a Korean drama, the instruction now explicitly points toward a similar kind of Korean story.

### Eval #7 — prefer related stories and choose one movie/show format (`e0e938c`)

**Recorded result:** 21 of 36 completed pairs matched all three titles (58%, rounded), from 72 saved conversations. Its first-trial subset matched 9/12 pairs; the 21/36 result includes all three trials.

**What changed**

- Look first for titles from the same series, fictional world, or creators as the favorite.
- Then consider popular titles with a similar genre and story. If equally close, favor the more widely watched one.
- If the person says “either” or gives no clear format, make every pick the same format as the favorite.
- Keep the copied-answer line and the guide sentence before the picks.

**Before:** Alex looked for similarity to the favorite, but several kinds of similarity could compete. A person saying “either” could receive a mixture of movies and shows.

**Why we tried it:** Give Alex a clearer order for searching for choices and remove movie-versus-show uncertainty when the answer is “either.”

**Example (illustrative):** If the favorite is a TV show and the person says “either,” all three picks should be TV shows. A related series or a show by the same creators gets considered before a less directly related title.

### Eval #8 — change the software’s variation settings without changing the prompt (`fc627c3`)

**Recorded result:** 6 of 12 completed pairs matched all three titles (50%, rounded), from 24 saved conversations.

**What changed**

- Keep the Eval #7 prompt instructions unchanged.
- Always send temperature 0, even if a different temperature is set elsewhere.
- Add a fixed seed of 368: a repeatability setting intended to make choices steadier.
- These are software settings, not new questions or choosing rules. They do not guarantee identical replies.

**Before:** The temperature setting could be replaced by a website setting, and no repeatability seed was being sent.

**Why we tried it:** Check whether changing the model-request settings, rather than adding more instructions, would make the two formats agree more often.

**Example (illustrative):** The person answers exactly the same questions and Alex reads exactly the same instructions as in Eval #7. Only the settings accompanying the request change. This is a settings round, not a new question or choosing rule.

### Eval #9 — prefer sequels and related stories; make the no-favorite choice narrower (`b9c3f78`)

**Recorded result:** 7 of 12 completed pairs matched all three titles (58%, rounded), from 24 saved conversations.

**What changed**

- Give early priority only to sequels, prequels, and spin-offs from the same series or fictional world.
- Remove “same creators” from that first-priority group. After related stories, use popular titles with a similar genre and story.
- Add a final check that none of the recommendations repeats the enjoyed title.
- If no favorite is named, use popular Netflix original TV series in the first genre, or overall if no genre is given.
- The Netflix-original restriction applies only to the no-favorite case in this round, not to all recommendations.

**Before:** Being made by the same creators was enough to give a title early priority, even if it was a different kind of story. The no-favorite choices were broader.

**Why we tried it:** Make the first choices more directly related to the favorite and reduce the number of possible choices when the person gives little information.

**Example (illustrative):** A spin-off of the favorite gets early priority. A completely different show by the same creator no longer gets that priority simply because of who made it.

### Eval #10 — choose the third recommendation from the maker of the first recommendation (`ff8a6ad`)

**Recorded result:** 6 of 12 completed pairs matched all three titles (50%, rounded), from 24 saved conversations.

**What changed**

- Keep similarity and related-story rules for picks 1 and 2.
- For pick 3, choose another well-known title by the creator or director of pick 1.
- If that creator has no other suitable title in the required format, use the creator or director of pick 2 instead.
- Also exclude specials, documentaries, and behind-the-scenes programs about the favorite. Keep the final check against repeating the favorite.

**Before:** All three recommendations were chosen mainly for resemblance to the person’s favorite.

**Why we tried it:** Try a specific rule for the third pick, which otherwise had several plausible alternatives.

**Example (illustrative):** After choosing recommendation A, Alex should look at who made A and choose another title by that person for pick 3. This refers to the maker of the first recommendation, not automatically the maker of the participant’s favorite.

### Eval #11 — write all three title names before explaining any of them (`3e9b45e`)

**Recorded result:** 5 of 12 completed pairs matched all three titles (42%, rounded), from 24 saved conversations.

**What changed**

- Remove the special creator/director rule for pick 3. Return all three picks to similarity and related-story rules.
- Write the three numbered title lines together, with no explanation between them.
- Put the explanations after the full list. Begin each explanation with its title name and do not number it.

**Before:** Each title was followed immediately by its explanation, and the third pick followed Eval #10’s creator/director rule.

**Why we tried it:** Try choosing the entire three-title list before writing explanations that might influence later choices. Since the third-pick rule was also removed, the round does not isolate the effect of reply order alone.

**Example (illustrative):** Before: title A, explanation A, title B, explanation B, title C. After: title A, title B, title C, followed by all three explanations.

### Eval #12 — allow only Netflix originals and simplify the choosing rules (`0319a43`)

**Recorded result:** 9 of 12 completed pairs matched all three titles (75%, rounded), from 24 saved conversations.

**What changed**

- Allow only titles described as Netflix originals for all three picks.
- Choose well-known originals similar to the favorite. Prefer the more popular title when two are equally close.
- Remove the special priority for sequels and related fictional worlds.
- Put each explanation directly under its title again.
- Keep the format and avoidance checks, plus exclusions for the favorite and programs about it.
- Remove the separate final-check sentence, while keeping the rule against recommending the favorite.
- If no favorite is given, continue using popular Netflix original series.

**Before:** Recommendations could include titles Netflix streamed without making or releasing them as originals. Related stories received special priority, and explanations appeared after the full title list.

**Why we tried it:** Give Alex fewer possible titles and a shorter set of choosing rules to follow. This also changes the range of recommendations the person can receive.

**Example (illustrative):** A suitable title would now be excluded if it did not count as a Netflix original under the prompt’s rule. Matching could improve simply because Alex has a smaller pool of titles to choose from.

### Eval #13 — state “Netflix original” and “movies” or “TV shows” before the picks (`5b8de24`)

**Recorded result:** 31 of 36 completed pairs matched all three titles (86%, rounded), from 72 saved conversations. Its first-trial subset matched 12/12 pairs; the 31/36 result includes all three trials. This is the highest recorded full-run score, but it did not reach the 33/36 matches needed for the 90% target.

**What changed**

- Write either “3 Netflix original movies” or “3 Netflix original TV shows” in the sentence before the picks.
- Choose one format. If the person says “either,” use the favorite’s format.
- Exclude shows that first aired on a TV network, even if Netflix streams them.
- If there is no favorite, use the first three shows on Netflix’s official all-time “Most Popular English TV” list.
- The app does not look up that list. Alex is instructed to rely on its own knowledge of it.

**Before:** The Netflix-original and movie/show restrictions were in the instructions, but Alex’s introductory sentence only promised three similar picks.

**Why we tried it:** Have Alex write the key restrictions immediately before naming titles and give the no-favorite case a more specific starting point.

**Example (illustrative):** The lead-in changes from “here are 3 picks most like it” to “here are 3 Netflix original TV shows most like it.” This makes both the allowed source and the format explicit before the titles appear.

### Eval #14 — when two choices are equally close, pick the older release (`6e0e206`)

**Recorded result:** 30 of 36 completed pairs matched all three titles (83%, rounded), from 72 saved conversations. Its first-trial subset matched 11/12 pairs; the 30/36 result includes all three trials.

**What changed**

- When two titles are equally similar to the favorite, choose the earlier release.
- This replaces the previous instruction to choose the more widely watched title in that situation.
- Keep all other Eval #13 instructions and request settings. Release dates still come from Alex’s knowledge, not a lookup.

**Before:** For two similarly suitable Netflix originals, Alex was told to prefer the one it believed more people had watched.

**Why we tried it:** Try a more specific way to choose between two similar options instead of asking Alex to estimate which is more popular.

**Example (illustrative):** If one equally suitable title was released in 2018 and another in 2020, the instruction says to choose the 2018 title.

### Eval #15 — explain which shows the experiment excludes as Netflix originals (`4f50c36`)

**Recorded result:** 30 of 36 completed pairs matched all three titles (83%, rounded), from 72 saved conversations. Its first-trial subset matched 10/12 pairs; the 30/36 result includes all three trials.

**What changed**

- Exclude a show that first aired on a TV network in any country, even if Netflix later streams it or calls it an original.
- Use Breaking Bad and Money Heist as examples of titles excluded under this experiment’s rule.
- Keep the earlier-release rule, answer copying, favorite-based similarity, temperature 0, and seed 368.

**Before:** The prompt excluded shows that first aired on a TV network, but the rule could still be interpreted differently for shows from other countries or later branded by Netflix.

**Why we tried it:** Reduce disagreement about which titles are allowed, rather than changing what kind of story the person wants. This is the definition written into the prompt, not a fresh check of Netflix’s catalog.

**Example (illustrative):** If a show began on a network outside the US and Netflix later acquired it, Alex should still leave it out under this version of the instructions.

### Eval #16 — try the older software settings with the same Eval #15 instructions (`87e7f0c`)

**Recorded result:** 26 of 36 completed pairs matched all three titles (72%, rounded), from 72 saved conversations. Eval #15 matched 30/36 pairs with the previous settings, compared with 26/36 here: four fewer matches, or 11.1 percentage points lower. This is one full run per setting, not proof that the settings alone caused the difference.

**What changed**

- Keep both Eval #15 prompts exactly the same.
- Stop sending the seed. Use the website’s temperature setting if present, otherwise 0.2.
- The actual website override was not checked, so the live temperature is not confirmed to have been 0.2.
- After testing, restore temperature 0 and seed 368 in commit 04ac259.

**Before:** Alex used the Eval #15 prompts while requests always included temperature 0 and seed 368.

**Why we tried it:** Compare the request settings while holding the instructions constant, so this round focuses on settings rather than another wording change.

**Example (illustrative):** The person sees the same questions and Alex reads the same choosing rules as in Eval #15. Only the settings intended to influence variation are changed; afterwards, the earlier settings are put back.

## Prompt changes since Eval #16

### What is different from the tested versions?

Previously, Alex already saw the six answers, and later versions copied all six into the “Got it” line. However, the selection instructions mainly said to choose titles like the movie or show the person enjoyed. Mood and available time were not independent reasons to choose a title in those later tested versions. Format and things to avoid still acted as requirements.

Commit `3038eb2` added an order of importance for the six answers. The current instructions retain that order and apply it to the answers the participant provided.

| Priority | Answer or answers used | What Alex is instructed to do in everyday terms |
|---|---|---|
| 1 | Movie/show preference and things to avoid — questions 1 and 6 | Every recommendation must be the requested format and avoid the content the person ruled out. If the person says “either,” use the favorite’s format; if there is no favorite either, use TV shows. |
| 2 | Recently enjoyed title — question 4 | Choose a similar kind of story and feel. The favorite remains a strong clue, but it is no longer the only choosing guide. |
| 3 | Genres and current mood — questions 2 and 3 | Also look for the kinds of stories the person enjoys and the experience they want right now. |
| 4 | Available time — question 5 | Prefer choices that fit how long the person has to watch. |

The favorite therefore still has more weight than genre/mood and time; the change does not give all answers equal weight. If the person names no favorite, Alex should choose using genre and mood. If two titles fit equally well, prefer the better-known one, then the older release if still tied. Keep excluding the favorite itself and programs about it.

**Illustrative example:** Someone enjoyed a long crime series, but today asks for a movie, says they want something light, has about 90 minutes, and wants to avoid violence. The new instructions say to respect the movie/no-violence requirements, use the favorite as one clue, and also consider today’s mood, genres, and time. They no longer say to choose only from titles similar to the crime series. This describes what we want Alex to do; we have not yet evaluated whether it follows those priorities consistently.

### What else changed

- Remove the requirement that every title be a Netflix original. Titles should still be real, released, and believed available on Netflix US; there is no live catalog lookup.
- Replace “Since you liked [title], here are 3 Netflix original…” with “Based on your answers, here are 3 [movies or TV shows] for you:”.
- **PR #6 (`7952b2b`)** matched the exact first question in both opening messages and kept the six questions in the same order. It retained the recommendation limit of under 180 words in both conditions and removed the separate cap on multi-turn question messages. It clarified that single-turn can recommend after any answer and multi-turn asks the next unanswered question until all six are answered.
- **PR #7 (`3a446a6`)** gave both prompts the same “Got it” and recommendation rules. Alex copies the answers it received, in question order, and omits unanswered items. It uses each answer's original question to interpret the reply. For example, “Horror” answers a genre preference in question 2 and an avoidance in question 6. The recommendation heading reflects whether the three picks are movies or shows.
- PR #7 also removed “Movie and TV Show Recommendations: Instructions” above the chat. The Scenario, Your Task, and Chatbot Instructions sections appear in both conditions.

**Single-turn example:** If someone replies “A comedy movie,” Alex writes “Got it: A comedy movie” and recommends three titles using that preference. In multi-turn, a reply like “not sure” counts as an answer, and Alex continues until every question has an answer.

### Evaluation status

**The updated single-turn and multi-turn prompts still need their own evaluation.** The last completed round is Eval #16, which scored 26/36 using the older Eval #15 prompts with different request settings. Earlier local Eval #17 attempts predate PRs #6 and #7. The first pass reported 0 of 72 completed chats, and the second log contains timeouts with no saved transcripts. There were zero pairs to score. The CSV leaves match and repeatability fields blank for the updated version at `3a446a6`. The repository prompts were checked locally, and the deployed version was not verified.

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

## Changes still in place today, compared with the baseline

This is the final list of changes that remain in the latest prompt files. It does not include every idea tried along the way. The original version already asked the same six questions and recommended three titles; neither of those is new.

1. **Ask only the next question in the one-at-a-time conversation.** Remove the brief reactions, thanks, and comments that were allowed in the baseline. Added in Eval #1.
2. **Accept short or vague answers and continue.** Explicitly treat “idk,” “anything,” “whatever,” and “no” as answers rather than repeatedly asking the same question. Made explicit in Eval #2.
3. **Copy the answers participants actually gave.** Preserve their wording and capitalization in question order. PR #7 removed empty slots from the “Got it” line and made selection depend on the original question each answer belongs to.
4. **Apply one priority order to the supplied answers.** First honor the requested format and things to avoid, then consider the enjoyed title, genres and mood, and available time. Commit `3038eb2` introduced those priorities. PR #7 made the original answer context explicit.
5. **Resolve “either” and missing answers consistently.** If the person does not choose movies or shows, use the enjoyed title’s format; if there is no enjoyed title either, use TV shows. If no favorite is named, choose using genres and mood. The format rule began in Eval #7 and was expanded in the latest change.
6. **Do not recommend the favorite back to the person.** Also exclude specials, documentaries, and behind-the-scenes programs about it. Introduced in Eval #1 and expanded in Eval #10.
7. **Use clear rules when two titles fit equally well.** Prefer the better-known title; if still equal, prefer the earlier release. The earlier-release rule was introduced in Eval #14; the current two-step order comes from the latest change.
8. **Introduce the list as based on the answers.** Use “Based on your answers, here are 3 [movies or TV shows] for you:” and name the format of the selected titles.
9. **Keep the reduced-variation software settings.** The current code always sends temperature 0 and seed 368. These settings are intended to make choices steadier, but do not guarantee identical replies. Added in Eval #8, temporarily removed for Eval #16, then restored.
10. **Align the opening and when each condition recommends.** Both versions use the same first question and a recommendation limit of under 180 words. Single-turn asks all six questions together and can recommend from a partial reply. Multi-turn asks one unanswered question at a time and recommends once all six are answered.
11. **Start the shared chat instructions at “Scenario.”** PR #7 removed the extra title above the instructions.

### Tried along the way, but not kept in today’s instructions

- **A fixed menu of named titles:** proposed in Eval #4, rejected and removed before testing.
- **A different job for each of the three picks:** tried in Eval #3, removed in Eval #5.
- **Special priority for related series or creators, or a creator-based third pick:** tried across Evals #7–#10; those special choosing rules are no longer present.
- **Writing all title names before any explanations:** tried in Eval #11; explanations returned under each title in Eval #12, as in the baseline.
- **Allowing only Netflix originals:** introduced for all picks in Eval #12 and clarified later; removed in the latest change. Today’s instructions again allow other titles believed available on Netflix US, as the baseline did.
- **Using the favorite as the only main choosing guide, with popularity-list fallbacks when there is no favorite:** replaced by the latest all-six-answer priorities and genre/mood fallback. The favorite remains influential, but it is no longer the only guide.

### The latest version still needs its own new evaluation

**The updated version at `3a446a6` still needs its own evaluation.** The earlier evaluations used the same six questions. A new run would measure title agreement with the current rules for choosing from supplied answers and for handling partial replies. All reported scores come from earlier rounds.
