# Prompt consistency evaluation

## What we were trying to do
Alex recommends 3 movies or TV shows in two versions that should differ only in pacing:

- **All at once**: Alex asks all six questions in one message. Files: `hidden_prompt_single_turn.txt`, `opening_single_turn.txt` (treatment group 1).
- **One at a time**: Alex asks one question per message. Files: `hidden_prompt_multi_turn.txt`, `opening_multi_turn.txt` (treatment group 2).

**Goal:** someone who gives the same six answers should get the **same 3 titles** from both versions, in any order. The target was at least 90%, meaning 33 of 36 pairs match.

**Ground rules we kept:**
- Alex's tone and personality stay the same.
- Every edit goes into both prompts.
- In the one-at-a-time version, Alex says nothing but the next question until the recommendations.
- No fixed list of titles.

## How we tested
- All testing was on the live site, which updates automatically when `main` changes. We had no OpenAI key or Heroku access.
- A script played 12 pretend participants (personas), each with fixed answers, through the site's normal flow.
- **Quick run:** 12 personas × 2 versions = 24 chats.
- **Full run:** 12 personas × 2 versions × 3 trials = 72 chats, giving 36 pairs.
- A pair counts as a match only if both versions gave exactly the same 3 titles.
- **Repeatability** asks how often a version gives the same 3 titles again when the same persona is repeated (trial 1 vs trials 2 and 3). It sets an upper limit, because the two versions can't agree more often than each one agrees with itself.
- Test chats are labelled "EVAL TEST" in the site's results.
- The raw chat transcripts stay local in `evals/` and are not in git, because each one ends with a study completion code.

## Results by change
Every change below was made in both prompts, except Eval #8 and #16, which only changed `config.js` and `app.js`. For the runs with 72 chats, the quick 24-chat scores were 9/12 (#7), 12/12 (#13), 11/12 (#14) and 10/12 (#15). The full numbers are in `results.csv`.

| Eval | Change | Matching pairs |
|---|---|---|
| Baseline | Original prompts | 5/12 (42%) |
| 1 | Shared title-choosing rules; one-at-a-time version asks only the bare questions | 5/12 |
| 2 | Vague answers ("idk", "whatever") count as answers; "most famous" tie-break; default temperature 0 | 4/12 |
| 3 | Each of the 3 picks gets its own job | 6/11 |
| 4 | Fixed list of titles: rejected ("we cannot have a fixed list") and undone, never run | none |
| 5 | Alex writes a "Got it:" line copying the six answers; the title they enjoyed is the main guide | 7/12 |
| 6 | Alex writes one line saying what the picks are based on before listing them | 9/12 |
| 7 | Fixed pick order; "either" means the format of the title they enjoyed | **21/36 (58%)** full |
| 8 | Temperature locked at 0 and a fixed seed (code change) | 6/12 |
| 9 | Picks start from the same story world; narrower default; check against recommending their own title | 7/12 |
| 10 | Third pick by the same creator as the first | 6/12 |
| 11 | List the three titles before any descriptions | 5/12 |
| 12 | Simplest rules, Netflix originals only | 9/12 |
| 13 | Format and "Netflix original" written into the line before the picks | **31/36 (86%)** full, best |
| 14 | Ties go to the earlier release | **30/36 (83%)** full |
| 15 | Clearer definition of a Netflix original | **30/36 (83%)** full |
| 16 | Settings test: original temperature, no seed, Eval #15 prompts unchanged (then undone) | **26/36 (72%)** full |

## What helped and what didn't
- **Helped:**
  - Making Alex write things down before choosing: the "Got it:" line (#5) and the "Since you liked X, here are 3 Netflix original TV shows most like it:" line (#6, #13).
  - Using one guide, the title they enjoyed, instead of weighing all six answers.
  - Allowing only Netflix originals, which shrinks the pool of possible titles (#12).
- **Didn't help:** a "most famous" tie-break, a separate job for each pick, choosing by creator, and listing the titles before the descriptions.
- **Where it stalls:** most remaining misses are near-ties for the third title. Examples:
  - Family night: *Vivo* / *The Sea Beast* vs *Klaus* / *The Willoughbys*
  - Sitcom: *Space Force* vs *Grace and Frankie*
  - Short answers: *The Perfection* vs *Fractured*
  
  Wording that fixed one persona often unsettled another.

## Temperature and seed (Eval #8, tested in Eval #16)
Temperature and seed are values the app's code sends to OpenAI with each message. We changed them in the repo, not in Heroku:

- **Eval #2** set the default temperature to 0. The app uses a Heroku setting first if one exists, so this may not have taken effect.
- **Eval #8** forced temperature 0 and added `seed: 368`.

The saved chats suggest this did not make Alex more repeatable. When the same persona repeated the exact same answers, the final reply was word-for-word identical to trial 1 only 2/48 times before the change (Eval #7) and 2/48, 6/48 and 0/48 times after (Evals #13–#15). The average word overlap stayed around 80–83%.

GPT-4o at temperature 0 is still not fully repeatable, and OpenAI only follows the seed on a "best effort" basis. Because the prompts also changed between those runs, **Eval #16** puts back the original setting and removes the seed with the prompts unchanged. Comparing it with Eval #15 shows whether the settings are worth keeping.

**Eval #16 result: the settings help, so they were put back.**

| | Eval #15 (temp 0 + seed) | Eval #16 (original settings) |
|---|---|---|
| Matching pairs | 30/36 (83%) | 26/36 (72%) |
| Repeatability, one at a time | 21/24 | 20/24 |
| Repeatability, all at once | 21/24 | 20/24 |
| Word overlap with trial 1 | 80% | 74% |
| Word-for-word identical replies | 0/48 | 0/48 |

- Without the settings, the third title wandered more. The Korean-drama persona got four different third picks: *Our Beloved Summer*, *Nevertheless*, *My First First Love* and *Romance Is a Bonus Book*.
- The settings don't make replies identical. They make the picks steadier.
- This comes from one 72-chat run per setting, so part of the 4-pair gap may be chance. Still, every measure points the same way.

## Current state
- The live prompts are Eval #15, with temperature 0 and seed 368 restored after Eval #16. Eval #13 scored highest, 86%.
- The 90% goal was not reached in 15 prompt changes.
- **Remaining option, not tried:** the app could send both versions the six answers in exactly the same format for the recommendation step.

## Not checked
- Whether the recommended titles are real and currently on Netflix.
- How well the picks fit, or Alex's tone.
- Any personas beyond these 12.
