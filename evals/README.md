# Evals for Alex: a beginner's walkthrough

This folder tests the Alex chatbot *before* real participants use it. You don't need any programming background to follow along. Read Part 1 first (the ideas), then do Part 3 (the setup) step by step.

---

## Part 1: What is an eval?

Anthropic's guide ([Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)) defines an eval as a test for an AI system: you give the AI an input, then apply grading rules to its output to measure success.

Think of a **driving test**. Every student drives the same route, and an examiner fills in a checklist: stopped at the stop sign? used the turn signal? stayed under the speed limit? Our eval is a driving test for Alex:

- **The route** is a pretend participant with fixed answers to the 6 questions.
- **The checklist** is the list of things Alex must always (or never) do.
- **The student** takes the test more than once, because the AI doesn't give exactly the same reply every time.

### The vocabulary (Anthropic's words, our meaning)

| Word | What it means in general | What it means here |
|---|---|---|
| **Task** | One test with fixed inputs and success rules | One pretend participant in one version of Alex |
| **Trial** | One attempt at a task. You repeat it because replies vary | One full conversation. We run 3 per task |
| **Grader** | The logic that scores the result | Rule checks, the AI judge, and you |
| **Transcript** | The full record of what happened | The whole chat, saved as a text file |
| **Harness** | The machinery that runs everything | `run_evals.py` |

### Why your study needs this

Your experiment compares two versions of Alex that should differ in **only one thing**: whether the six questions come all at once or one by one. If one version also gives longer answers, uses bold text, asks extra questions, or recommends worse titles, you can't tell which difference caused the change in participants' satisfaction. The eval checks that everything *except* the pacing stays the same.

The setup copies a well-known research design (Laban et al., "LLMs Get Lost in Multi-Turn Conversation," ICLR 2026). The pretend person gives **word-for-word the same answers** in both versions. The only thing that changes is whether they arrive in one message or six.

---

## Part 2: How this eval is built

### The files

| File | What it is |
|---|---|
| `personas.json` | 12 pretend participants. Each has 6 answers, one per question, in order. Two are deliberately tricky: `p11_vague` and `p12_short_answers`. |
| `run_evals.py` | The script. It reads the **same prompt and opening-message files the website uses** (in `experiment_configuration/`), so you always test exactly what participants will see. |
| `requirements.txt` | The one add-on Python needs: OpenAI's `openai` package. |
| `results/` | Created when you run the script. One folder per run, named with the date and time. |

### What the script does (the 5 steps, also marked inside the code)

1. **Load** the hidden prompts and Alex's opening messages for group 1 (all at once) and group 2 (one by one).
2. **Talk** to GPT-4o with the same settings as the website: model `gpt-4o`, temperature 0.2, 1,000-token limit.
   - All-at-once: the person sends all six answers in one numbered message.
   - One-by-one: the person sends answer 1, waits for Alex, sends answer 2, and so on until Alex gives its picks.
3. **Repeat** each conversation 3 times (3 trials).
4. **Grade** each conversation (see the next section).
5. **Save** the transcripts and score sheets, then print a summary.

### The graders

Anthropic describes three kinds of graders: code-based, model-based (an AI judge), and human. Each has strengths and weaknesses, so we use all three.

**1. Rule checks (code).** These are fast, free, and always give the same answer, but they can't judge quality.

| Check | Passes when… | Why it matters for the study |
|---|---|---|
| `exactly_3_picks` | The final message lists items 1, 2, 3 and no item 4 | Both groups must get the same number of options |
| `plain_text` | No `**bold**` or `# headers` | The chat window would show raw asterisks |
| `short_enough` | The picks message is ≤ 180 words | Length shouldn't differ between groups |
| `right_number_of_questions` | All-at-once: picks come in Alex's first reply, with no follow-ups. One-by-one: 5 more question messages after the opener, then picks | This *is* the difference you're testing, so it must be exact |
| `no_study_leak` | Alex never says "study," "experiment," "research," "condition"… | Participants shouldn't know their group |
| `no_fake_actions` | Alex never claims "I added it to your My List" | Alex can't actually do that |

**2. The AI judge (a second GPT call).** This handles judgment questions, like "do these picks fit what the person said?" Following Anthropic's tips, each question gets **its own separate judge call**, a **clear 1–5 scoring guide**, and an **"UNKNOWN" option**. The "UNKNOWN" option gives the judge an honest way out, so it doesn't make up an answer when it can't tell.

| Judge question | Output |
|---|---|
| Fit: do the 3 titles match the person's answers? | 1–5 |
| Avoid: did any title include what the person wanted to avoid? | PASS / FAIL |
| Tone: is Alex friendly *and* professional? | 1–5 |
| Titles: what titles did Alex recommend, and are they real? | A list, used to compare the groups |

**3. You (the human grader).** Anthropic stresses that you have to read transcripts. Otherwise you can't know whether your graders are working. The judge can be wrong, and "real title?" is especially shaky, because the judge is also an AI working from memory. **Any title the judge doubts, look up yourself.**

---

## Part 3: Setup in VS Code (Mac), step by step

Commands are written for a Mac. If you're on Windows, see the note at the end of this part.

You do Steps 1–4 once. After that, it's just Steps 5–7. (If you close VS Code and come back later, redo the two "every time" lines in Steps 3 and 4.)

**Step 1: Open the project.** In VS Code, choose **File → Open Folder…** and pick `UXResearch/Experiment/CMU-368-F26-C`. Then open a terminal: in the top menu, click **Terminal → New Terminal**. A panel opens at the bottom, and that's where you type commands. Check you're on the right version of the code:

```bash
git branch
```

The line with the `*` should say `alex-opener-and-prompts`. (Later, after the branch is merged, you'd use `git checkout main` and `git pull` instead.)

**Step 2: Check Python.** Type:

```bash
python3 --version
```

If you see something like `Python 3.12.4`, you're done. If you get an error, or a pop-up asks to install developer tools, install Python from [python.org/downloads](https://www.python.org/downloads/), then close and reopen VS Code.

**Step 3: Make a "private toolbox" for this project and install the OpenAI package.** A *virtual environment* is a folder (`.venv`) that holds the add-ons this project needs, so they don't mix with the rest of your Mac.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r evals/requirements.txt
```

After `source …`, your terminal line starts with `(.venv)`, which means the toolbox is on. **Every time** you open a new terminal, run `source .venv/bin/activate` again.

**Step 4: Give the script your OpenAI key.** This is the same key the website uses. **Every time** you open a new terminal:

```bash
export OPENAI_API_KEY="sk-...your key..."
```

This only lasts until you close the terminal, which is a good thing. **Never paste the key into a file in this folder**, or it could end up on GitHub.

**Step 5: Free practice run (no key, no cost).** This uses fake replies, just to prove everything is wired up.

```bash
python evals/run_evals.py --dry-run
```

You should see 72 lines like `[1/72] p01_light_comedy | all_at_once | trial 1 -> all rules passed`, then a SUMMARY. The fake picks are called "Fake Movie," so ignore what they say.

**Step 6: Tiny real run (a few cents).** One persona, one trial, in each version:

```bash
python evals/run_evals.py --only p01 --trials 1
```

Open the new folder under `evals/results/`, then open `transcripts/`, and read the two conversations. Do they look like what a participant would see?

**Step 7: The full run.**

```bash
python evals/run_evals.py
```

That's 12 personas × 2 versions × 3 trials = 72 conversations, plus the judge calls. My rough estimate is a few dollars at most, and it takes about 10–20 minutes. You can check the real cost afterwards on your OpenAI usage page.

**On Windows instead?** Use `python` instead of `python3`. Activate the toolbox with `.venv\Scripts\activate`, and set the key with `$env:OPENAI_API_KEY = "sk-..."`. When installing Python, tick "Add python.exe to PATH."

---

## Part 4: Reading the results

Each run creates `evals/results/<date_time>/` with:

- **`summary.txt`**: start here.
- **`trial_scores.csv`**: one row per conversation. It opens in Excel. Turn on a filter and look for `FAIL`.
- **`persona_comparison.csv`**: one row per pretend participant, comparing the two versions.
- **`transcripts/`**: every conversation as a readable text file, with its grades at the bottom.
- **`all_conversations.json`**: everything in one file, in case you want it later.

### What "good" looks like

These targets are my suggestions. Adjust them with your team.

- **Rule checks: aim for 100% in both versions.** These are "must never happen" problems, and one bold-text reply is a real participant seeing asterisks. Anthropic calls this "pass^k": did it pass *every* time, not just once? `persona_comparison.csv` shows this per persona in the `…passed_every_rule_every_trial` columns.
- **Fit score: about 4 or higher, and similar in both versions.** If one-by-one scores clearly lower (say 3.4 vs 4.2), that's the "lost in conversation" effect showing up, and you'd want to fix it before running the study.
- **Tone: similar in both versions.** Otherwise tone becomes a second difference between the groups.
- **Shared titles: compare it to repeatability.** This one is the subtle part:
  - *Repeatability* = how often a version picks the same titles when you run the *same* person again (out of 3).
  - *Shared titles* = how often the two versions pick the same titles for the same person.
  - If shared titles is about as high as repeatability, the format isn't changing the picks; the differences are just normal randomness. That's what you want.
  - If repeatability is high (say 2.5 of 3) but shared titles is low (say 0.5 of 3), the **format itself is changing what Alex recommends**. That's worth knowing, and worth discussing with your team.
  - Don't expect identical lists. Different people would pick different titles too. The goal is that the gap *between* versions isn't bigger than the normal wobble *within* a version.

### Read transcripts, especially failures

Open at least 10 transcripts, including every FAIL. For each failure, ask the question Anthropic recommends: **is Alex actually wrong, or is my grader wrong?** For example, if Alex wrote "1)" instead of "1." and a check failed, that's a grader problem, not an Alex problem.

---

## Part 5: The improve loop

1. **Run** the full eval and save the summary. This is your *baseline*.
2. **Find** a pattern of failures, for example: "one-by-one sometimes asks a 7th question."
3. **Decide** if it's an Alex problem (fix the prompt) or a grader problem (fix the check).
4. **Change one thing.** Prompts live in `experiment_configuration/hidden_prompts_bank/`. Edit the same rule in **both** prompts so the versions stay identical.
5. **Run again** and compare to the baseline. Did the fix work? Did anything *else* get worse? Rerunning everything to make sure an old success didn't break is called a "regression" check.
6. Repeat until you're happy. Then commit the prompt changes so the website uses them.

One caution: don't tune the prompt so hard to these 12 personas that it only works for them. Every so often, add new personas.

---

## Part 6: Customizing

**Add a pretend participant.** Copy one block in `personas.json`, give it a new `id`, and write 6 answers in order: format, genres, mood, something you enjoyed lately, time, things to avoid. Anthropic suggests 20–50 test cases as a strong start, and the best ones come from real failures. If a pilot tester confuses Alex, turn that into a persona.

**Run more or fewer trials.** Use `--trials 5` for more confidence, or `--trials 1` for a quick check.

**Run some personas only.** `--only p0` runs p01–p09, and `--only vague` runs just the vague persona.

**Use a different judge.** Anthropic suggests grading with a different AI than the one being tested, since an AI may go easy on its own style. To switch, run this before running the script:

```bash
export JUDGE_MODEL="model-name-here"
```

Some newer models reject the temperature setting. The script only sends it to gpt-4 models, so that should be fine.

**Add a rule check.** In `run_evals.py`, find `def rule_checks`. Add a line in the same style. For example, "no emojis":

```python
checks["no_emojis"] = not re.search(r"[\U0001F300-\U0001FAFF]", everything_alex_wrote)
```

**Ideas for later:** a persona whose first message is just "hi," a persona who goes off-topic, or a persona who changes their mind after seeing the picks.

---

## Common errors

| You see | What it means | Fix |
|---|---|---|
| `command not found: python` | The toolbox isn't on (or Python isn't installed) | `source .venv/bin/activate` (Step 3), or Step 2 |
| `The 'openai' package is missing` | The toolbox isn't on, or Step 3 was skipped | `source .venv/bin/activate`, then `pip install -r evals/requirements.txt` |
| `OPENAI_API_KEY is not set` | New terminal window, so the key is gone | Repeat Step 4 |
| `401` / `invalid api key` | The key is wrong or was revoked | Get the key from whoever manages the account |
| `429` / `rate limit` / `quota` | Too many requests, or no credit left | Wait a minute and rerun, or check billing |
| `FileNotFoundError … opening_messages_bank` | You're on code without the new opener files | Step 1: check out the branch |
