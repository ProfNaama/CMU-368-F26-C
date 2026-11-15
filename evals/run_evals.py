"""
run_evals.py - Test Alex (the movie/TV chatbot) before real participants see it.

What this script does, in plain words:
  1. Reads the SAME prompt files and opening messages the website uses.
  2. Plays "pretend participants" (from personas.json) through BOTH versions of Alex:
       - Group 1 (all at once): the pretend person answers all 6 questions in one message.
       - Group 2 (one by one):  the pretend person answers one question per message.
     The answers are word-for-word the same in both groups, so any difference
     in what Alex recommends comes from the version of Alex, not the person.
  3. Repeats each conversation a few times ("trials"), because the AI can give
     a slightly different reply each time.
  4. Grades every conversation two ways:
       - Rule checks (simple code): exactly 3 picks? plain text? right number of questions? ...
       - AI judge (a second AI call): do the picks fit what the person asked for? ...
  5. Saves everything in a results folder: every conversation as a text file you
     can read, plus two spreadsheets (CSV files) with the scores.

How to run it (from the main project folder, in the VS Code terminal):
    python evals/run_evals.py --dry-run     <- free practice run with fake replies
    python evals/run_evals.py               <- the real run (costs a small amount of money)

See evals/README.md for the full walkthrough.
"""

import argparse
import csv
import json
import os
import re
import sys
import time
from datetime import datetime
from pathlib import Path

# ---------------------------------------------------------------------------
# SETTINGS - the knobs you are most likely to change.
# ---------------------------------------------------------------------------

# The model being tested. Keep this the same as the website (config.js uses "gpt-4o").
MODEL_UNDER_TEST = os.environ.get("OPENAI_MODEL", "gpt-4o")

# Must match the website. The website reads OPENAI_TEMPERATURE (default 0.2).
TEMPERATURE = float(os.environ.get("OPENAI_TEMPERATURE", "0.2"))

# Must match the website's OPENAI_TOKEN_LIMIT (default 1000): the longest reply allowed.
MAX_TOKENS = int(os.environ.get("OPENAI_TOKEN_LIMIT", "1000"))

# How many times to repeat each pretend participant in each group.
TRIALS = 3

# The model that grades the answers (the "AI judge").
JUDGE_MODEL = os.environ.get("JUDGE_MODEL", "gpt-4o")

# Rule-check limits.
MAX_WORDS_IN_RECOMMENDATIONS = 180   # the prompt asks for "under 180 words"
NUMBER_OF_QUESTIONS = 6              # how many questions Alex should ask in total

# Words that would mean Alex is leaking that this is a study.
LEAK_WORDS = ["study", "experiment", "research", "condition", "participant", "treatment group"]

# Folder layout (you normally don't need to touch these).
EVALS_FOLDER = Path(__file__).resolve().parent
PROJECT_FOLDER = EVALS_FOLDER.parent
CONFIG_FOLDER = PROJECT_FOLDER / "experiment_configuration"
PERSONAS_FILE = EVALS_FOLDER / "personas.json"

# Which treatment group in treatment_groups_config.csv is which version of Alex.
GROUPS = {
    "1": "all_at_once",
    "2": "one_by_one",
}


# ---------------------------------------------------------------------------
# STEP 1: load the prompts and opening messages exactly like the website does.
# ---------------------------------------------------------------------------

def load_alex_versions():
    """Return {"all_at_once": {"prompt": ..., "opening": ...}, "one_by_one": {...}}."""
    versions = {}
    with open(CONFIG_FOLDER / "treatment_groups_config.csv", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            group = row["treatment_group"].strip()
            if group not in GROUPS:
                continue
            prompt_file = CONFIG_FOLDER / "hidden_prompts_bank" / row["hidden_prompt"].strip()
            opening_file = CONFIG_FOLDER / "opening_messages_bank" / row["opening_message"].strip()
            versions[GROUPS[group]] = {
                "prompt": prompt_file.read_text(encoding="utf-8"),
                "opening": opening_file.read_text(encoding="utf-8").strip(),
            }
    missing = set(GROUPS.values()) - set(versions)
    if missing:
        sys.exit(f"Could not find these groups in treatment_groups_config.csv: {missing}")
    return versions


def load_personas():
    personas = json.loads(PERSONAS_FILE.read_text(encoding="utf-8"))
    for p in personas:
        if len(p["answers"]) != NUMBER_OF_QUESTIONS:
            sys.exit(f"Persona {p['id']} needs exactly {NUMBER_OF_QUESTIONS} answers.")
    return personas


# ---------------------------------------------------------------------------
# STEP 2: talking to the AI.
# ---------------------------------------------------------------------------

def make_client(dry_run):
    if dry_run:
        return FakeClient()
    try:
        from openai import OpenAI
    except ImportError:
        sys.exit("The 'openai' package is missing. Run:  pip install -r evals/requirements.txt")
    if not os.environ.get("OPENAI_API_KEY"):
        sys.exit("OPENAI_API_KEY is not set. See 'Step 3' in evals/README.md.")
    return OpenAI(max_retries=5)


def ask_model(client, model, messages, temperature=None, max_tokens=MAX_TOKENS, want_json=False):
    """Send a list of messages to the model and return its reply as text."""
    settings = {"model": model, "messages": messages, "max_tokens": max_tokens}
    if temperature is not None:
        settings["temperature"] = temperature
    if want_json:
        settings["response_format"] = {"type": "json_object"}
    reply = client.chat.completions.create(**settings)
    return reply.choices[0].message.content or ""


# ---------------------------------------------------------------------------
# STEP 3: play one pretend participant through one version of Alex.
# ---------------------------------------------------------------------------

def looks_like_recommendations(text):
    """True if the message contains a numbered list 1., 2., 3. (Alex's picks)."""
    numbers = set(re.findall(r"^\s*([1-9])[\.\)]\s", text, flags=re.MULTILINE))
    return {"1", "2", "3"}.issubset(numbers)


def run_conversation(client, version_name, version, persona):
    """Returns the full conversation as a list of {"role", "content"} messages.

    The conversation starts exactly like the website: the hidden prompt (system),
    then Alex's scripted opening message (assistant).
    """
    messages = [
        {"role": "system", "content": version["prompt"]},
        {"role": "assistant", "content": version["opening"]},
    ]
    answers = persona["answers"]

    if version_name == "all_at_once":
        # The pretend person answers all six questions in one message.
        combined = "\n".join(f"{i + 1}. {a}" for i, a in enumerate(answers))
        messages.append({"role": "user", "content": combined})
        messages.append({"role": "assistant", "content": ask_model(client, MODEL_UNDER_TEST, messages, TEMPERATURE)})
        return messages

    # one_by_one: answer the next question each time Alex speaks, until Alex gives picks.
    next_answer = 0
    safety_limit = NUMBER_OF_QUESTIONS + 3   # stop runaway conversations
    for _ in range(safety_limit):
        if next_answer >= len(answers):
            break
        messages.append({"role": "user", "content": answers[next_answer]})
        next_answer += 1
        alex_reply = ask_model(client, MODEL_UNDER_TEST, messages, TEMPERATURE)
        messages.append({"role": "assistant", "content": alex_reply})
        if looks_like_recommendations(alex_reply):
            break
    return messages


# ---------------------------------------------------------------------------
# STEP 4a: rule checks (code-based graders). Each returns True (pass) or False (fail).
# ---------------------------------------------------------------------------

def alex_messages(messages):
    """Alex's messages that the AI actually wrote (skips the scripted opening)."""
    return [m["content"] for m in messages[2:] if m["role"] == "assistant"]


def final_message(messages):
    written = alex_messages(messages)
    return written[-1] if written else ""


def rule_checks(version_name, messages):
    final = final_message(messages)
    written = alex_messages(messages)
    everything_alex_wrote = "\n".join(written)
    numbers = re.findall(r"^\s*([1-9])[\.\)]\s", final, flags=re.MULTILINE)

    checks = {}
    # 1. Exactly three picks: items 1, 2 and 3, and no item 4.
    checks["exactly_3_picks"] = looks_like_recommendations(final) and "4" not in numbers
    # 2. Plain text: no markdown bold (** or __) and no # headers.
    checks["plain_text"] = not re.search(r"\*\*|__|^\s*#", everything_alex_wrote, flags=re.MULTILINE)
    # 3. Short enough.
    checks["short_enough"] = len(final.split()) <= MAX_WORDS_IN_RECOMMENDATIONS
    # 4. Right number of questions.
    #    all_at_once: Alex should give picks in its very first written reply (no follow-ups).
    #    one_by_one: the opening asks question 1, then 5 more question messages, then the picks.
    if version_name == "all_at_once":
        checks["right_number_of_questions"] = len(written) == 1 and looks_like_recommendations(written[0])
    else:
        question_messages = [w for w in written if not looks_like_recommendations(w)]
        checks["right_number_of_questions"] = (
            len(question_messages) == NUMBER_OF_QUESTIONS - 1 and looks_like_recommendations(final)
        )
    # 5. No mention of the study.
    lower = everything_alex_wrote.lower()
    checks["no_study_leak"] = not any(re.search(rf"\b{re.escape(w)}\b", lower) for w in LEAK_WORDS)
    # 6. Doesn't pretend to take actions it can't take (like adding to My List).
    checks["no_fake_actions"] = not re.search(
        r"\bI(?:'ve| have)? (?:added|saved|put)\b|\bstarted playing\b", everything_alex_wrote, flags=re.IGNORECASE
    )
    return checks


# ---------------------------------------------------------------------------
# STEP 4b: the AI judge (model-based graders). One question per judge call,
# each with a clear scoring guide and an "UNKNOWN" option, as Anthropic recommends.
# ---------------------------------------------------------------------------

QUESTIONS_FOR_JUDGE = [
    "Movie, TV show, or either",
    "Genres they enjoy",
    "Current mood",
    "Something they enjoyed lately",
    "Time available",
    "Things to avoid",
]


def describe_persona(persona):
    return "\n".join(f"- {q}: {a}" for q, a in zip(QUESTIONS_FOR_JUDGE, persona["answers"]))


JUDGE_FIT = """You are grading a movie and TV recommendation chatbot.

What the person said they want:
{persona}

The chatbot's final recommendation message:
<recommendations>
{final}
</recommendations>

How well do the recommended titles match what the person asked for (movie vs show, genres, mood,
similarity to what they enjoyed, time available)? Use this scale:
5 = all three clearly match
4 = all three match, with small issues
3 = mixed: some match, some don't
2 = mostly poor matches
1 = they do not match
If the message has no recommendations, or you cannot tell, use "UNKNOWN".

Reply in JSON only: {{"score": 1-5 or "UNKNOWN", "reason": "one short sentence"}}"""

JUDGE_AVOID = """You are grading a movie and TV recommendation chatbot.

The person said they want to avoid: "{avoid}"

The chatbot's final recommendation message:
<recommendations>
{final}
</recommendations>

Does any recommended title clearly include what the person wanted to avoid?
- "PASS" = none of the titles include it (or the person said there is nothing to avoid)
- "FAIL" = at least one title clearly includes it
- "UNKNOWN" = you cannot tell

Reply in JSON only: {{"verdict": "PASS" or "FAIL" or "UNKNOWN", "reason": "one short sentence"}}"""

JUDGE_TONE = """You are grading a movie and TV recommendation chatbot named Alex.
Alex should sound friendly AND professional: warm and upbeat, like a knowledgeable friend
who works in film, but clear, concise, and not over the top.

Everything Alex wrote in this conversation:
<alex>
{alex}
</alex>

Rate the tone:
5 = friendly and professional throughout
4 = mostly right, small slips (a bit stiff, or a bit much)
3 = noticeably too cold, too gushing, or too wordy
2 = mostly the wrong tone
1 = rude, robotic, or unprofessional
Use "UNKNOWN" if there is nothing to rate.

Reply in JSON only: {{"score": 1-5 or "UNKNOWN", "reason": "one short sentence"}}"""

JUDGE_TITLES = """Below is a message from a movie and TV recommendation chatbot.

<recommendations>
{final}
</recommendations>

List every title it recommends. For each, say whether, based on your knowledge, it is a real,
released movie or TV show: "yes", "no", or "unsure".

Reply in JSON only: {{"titles": [{{"title": "...", "year": "...", "real": "yes" or "no" or "unsure"}}]}}"""


def ask_judge(client, prompt):
    # Low randomness for the judge too, so grades are stable. (Some newer models don't
    # accept a temperature setting, so we only send it for gpt-4 family models.)
    temperature = 0 if JUDGE_MODEL.startswith("gpt-4") else None
    text = ask_model(client, JUDGE_MODEL, [{"role": "user", "content": prompt}],
                     temperature=temperature, max_tokens=400, want_json=True)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {"score": "UNKNOWN", "verdict": "UNKNOWN", "titles": [], "reason": "judge reply was not JSON"}


def judge_checks(client, persona, messages):
    final = final_message(messages)
    alex = "\n---\n".join(alex_messages(messages))
    fit = ask_judge(client, JUDGE_FIT.format(persona=describe_persona(persona), final=final))
    avoid = ask_judge(client, JUDGE_AVOID.format(avoid=persona["answers"][5], final=final))
    tone = ask_judge(client, JUDGE_TONE.format(alex=alex))
    titles = ask_judge(client, JUDGE_TITLES.format(final=final)).get("titles", [])
    return {
        "fit_score": fit.get("score", "UNKNOWN"),
        "fit_reason": fit.get("reason", ""),
        "avoid_verdict": avoid.get("verdict", "UNKNOWN"),
        "avoid_reason": avoid.get("reason", ""),
        "tone_score": tone.get("score", "UNKNOWN"),
        "tone_reason": tone.get("reason", ""),
        "titles": titles,
    }


# ---------------------------------------------------------------------------
# STEP 5: compare the two groups and save everything.
# ---------------------------------------------------------------------------

def normalize_title(title):
    """'The Office (2005)' and 'the office' should count as the same title."""
    t = title.lower()
    t = re.sub(r"\(.*?\)", "", t)          # drop "(2005)"
    t = re.sub(r"[^a-z0-9 ]", "", t)       # drop punctuation
    t = re.sub(r"^the ", "", t.strip())
    return re.sub(r"\s+", " ", t).strip()


def title_set(trial):
    return {normalize_title(t.get("title", "")) for t in trial["judge"]["titles"] if t.get("title")}


def average(values):
    numbers = [v for v in values if isinstance(v, (int, float))]
    return round(sum(numbers) / len(numbers), 2) if numbers else "n/a"


def save_transcript(folder, trial):
    lines = [
        f"Persona: {trial['persona_id']}   Version: {trial['version']}   Trial: {trial['trial']}",
        "=" * 70,
    ]
    for m in trial["messages"]:
        if m["role"] == "system":
            continue
        who = "ALEX" if m["role"] == "assistant" else "PERSON"
        lines += [f"[{who}]", m["content"], ""]
    lines += ["=" * 70, "RULE CHECKS:"]
    lines += [f"  {name}: {'PASS' if ok else 'FAIL'}" for name, ok in trial["rules"].items()]
    j = trial["judge"]
    lines += [
        "AI JUDGE:",
        f"  fit: {j['fit_score']}  ({j['fit_reason']})",
        f"  avoid: {j['avoid_verdict']}  ({j['avoid_reason']})",
        f"  tone: {j['tone_score']}  ({j['tone_reason']})",
        "  titles: " + "; ".join(f"{t.get('title')} ({t.get('year')}) real={t.get('real')}" for t in j["titles"]),
    ]
    name = f"{trial['persona_id']}__{trial['version']}__trial{trial['trial']}.txt"
    (folder / name).write_text("\n".join(lines), encoding="utf-8")


def write_reports(out_folder, trials, personas):
    rule_names = list(trials[0]["rules"].keys())

    # 1. One row per conversation.
    with open(out_folder / "trial_scores.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["persona", "version", "trial", "alex_messages"] + rule_names +
                   ["fit_score", "avoid_verdict", "tone_score", "titles", "any_title_not_real"])
        for t in trials:
            j = t["judge"]
            w.writerow([t["persona_id"], t["version"], t["trial"], len(alex_messages(t["messages"]))] +
                       ["PASS" if t["rules"][r] else "FAIL" for r in rule_names] +
                       [j["fit_score"], j["avoid_verdict"], j["tone_score"],
                        " | ".join(x.get("title", "") for x in j["titles"]),
                        any(x.get("real") != "yes" for x in j["titles"])])

    # 2. One row per persona: how similar were the two groups' picks?
    comparison_rows = []
    for p in personas:
        mine = {v: [t for t in trials if t["persona_id"] == p["id"] and t["version"] == v] for v in GROUPS.values()}
        a, b = mine["all_at_once"], mine["one_by_one"]
        # shared titles between trial k of group 1 and trial k of group 2 (out of 3)
        shared = [len(title_set(x) & title_set(y)) for x, y in zip(a, b)]
        # same pick in every trial? (how repeatable each version is on its own)
        def repeat_overlap(group):
            sets = [title_set(t) for t in group]
            pairs = [len(sets[i] & sets[k]) for i in range(len(sets)) for k in range(i + 1, len(sets))]
            return average(pairs)
        comparison_rows.append({
            "persona": p["id"],
            "note": p.get("note", ""),
            "shared_titles_between_groups_avg_out_of_3": average(shared),
            "all_at_once_repeatability_out_of_3": repeat_overlap(a),
            "one_by_one_repeatability_out_of_3": repeat_overlap(b),
            "fit_all_at_once": average([t["judge"]["fit_score"] for t in a]),
            "fit_one_by_one": average([t["judge"]["fit_score"] for t in b]),
            "all_at_once_passed_every_rule_every_trial": all(all(t["rules"].values()) for t in a),
            "one_by_one_passed_every_rule_every_trial": all(all(t["rules"].values()) for t in b),
        })
    with open(out_folder / "persona_comparison.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(comparison_rows[0].keys()))
        w.writeheader()
        w.writerows(comparison_rows)

    # 3. A short summary, printed and saved.
    lines = ["SUMMARY", "=" * 70]
    for v in GROUPS.values():
        group = [t for t in trials if t["version"] == v]
        lines.append(f"\n{v}  ({len(group)} conversations)")
        for r in rule_names:
            passed = sum(t["rules"][r] for t in group)
            lines.append(f"  {r:<28} {passed}/{len(group)} passed")
        lines.append(f"  {'avg fit score (1-5)':<28} {average([t['judge']['fit_score'] for t in group])}")
        lines.append(f"  {'avg tone score (1-5)':<28} {average([t['judge']['tone_score'] for t in group])}")
        avoid_fails = sum(t["judge"]["avoid_verdict"] == "FAIL" for t in group)
        lines.append(f"  {'broke an avoid request':<28} {avoid_fails}/{len(group)}")
        unsure = sum(any(x.get("real") != "yes" for x in t["judge"]["titles"]) for t in group)
        lines.append(f"  {'had a title judge doubted':<28} {unsure}/{len(group)}  <- check these by hand")
    lines.append("\nSAME PERSON, BOTH GROUPS")
    lines.append(f"  avg shared titles (out of 3): "
                 f"{average([r['shared_titles_between_groups_avg_out_of_3'] for r in comparison_rows])}")
    lines.append(f"  avg repeatability, all_at_once (out of 3): "
                 f"{average([r['all_at_once_repeatability_out_of_3'] for r in comparison_rows])}")
    lines.append(f"  avg repeatability, one_by_one (out of 3): "
                 f"{average([r['one_by_one_repeatability_out_of_3'] for r in comparison_rows])}")
    lines.append(f"\nEverything is saved in: {out_folder}")
    text = "\n".join(lines)
    (out_folder / "summary.txt").write_text(text, encoding="utf-8")
    print("\n" + text)


# ---------------------------------------------------------------------------
# Fake AI for --dry-run (free, no internet). It only imitates the shape of real replies.
# ---------------------------------------------------------------------------

class FakeClient:
    class _Reply:
        def __init__(self, text):
            self.choices = [type("C", (), {"message": type("M", (), {"content": text})()})()]

    def __init__(self):
        self.chat = type("Chat", (), {"completions": self})()

    def create(self, model, messages, **kwargs):
        if kwargs.get("response_format"):   # pretend judge
            return self._Reply('{"score": 4, "verdict": "PASS", "reason": "fake judge", '
                               '"titles": [{"title": "Fake Movie", "year": "2020", "real": "yes"}, '
                               '{"title": "Fake Show", "year": "2021", "real": "yes"}, '
                               '{"title": "Fake Film", "year": "2019", "real": "unsure"}]}')
        people_messages = sum(m["role"] == "user" for m in messages)
        one_by_one = "one at a time" in messages[1]["content"]
        if one_by_one and people_messages < NUMBER_OF_QUESTIONS:
            return self._Reply(f"Nice! Fake question number {people_messages + 1}?")
        return self._Reply("Sounds like you want something fun.\n"
                           "1. Fake Movie (2020) - Movie, about 1h 50m\n   Fits your mood.\n"
                           "2. Fake Show (2021) - TV show, 2 seasons\n   Fits your genres.\n"
                           "3. Fake Film (2019) - Movie, about 2h\n   Fits your time.\n"
                           "Want different options?")


# ---------------------------------------------------------------------------
# MAIN: tie it all together.
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Run evals for the Alex chatbot.")
    parser.add_argument("--dry-run", action="store_true", help="use fake replies (free) to test your setup")
    parser.add_argument("--trials", type=int, default=TRIALS, help="repeats per persona per group")
    parser.add_argument("--only", help="run only personas whose id contains this text, e.g. --only p01")
    args = parser.parse_args()

    versions = load_alex_versions()
    personas = load_personas()
    if args.only:
        personas = [p for p in personas if args.only in p["id"]]
        if not personas:
            sys.exit(f"No persona id contains '{args.only}'.")
    client = make_client(args.dry_run)

    stamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    out_folder = EVALS_FOLDER / "results" / (stamp + ("_dry-run" if args.dry_run else ""))
    transcripts = out_folder / "transcripts"
    transcripts.mkdir(parents=True, exist_ok=True)

    total = len(personas) * len(versions) * args.trials
    print(f"Testing {MODEL_UNDER_TEST} (temperature {TEMPERATURE}), judge {JUDGE_MODEL}")
    print(f"{len(personas)} personas x {len(versions)} versions x {args.trials} trials = {total} conversations\n")

    trials, done, started = [], 0, time.time()
    for persona in personas:
        for version_name, version in versions.items():
            for k in range(1, args.trials + 1):
                messages = run_conversation(client, version_name, version, persona)
                trial = {
                    "persona_id": persona["id"],
                    "version": version_name,
                    "trial": k,
                    "messages": messages,
                    "rules": rule_checks(version_name, messages),
                    "judge": judge_checks(client, persona, messages),
                }
                save_transcript(transcripts, trial)
                trials.append(trial)
                done += 1
                status = "all rules passed" if all(trial["rules"].values()) else \
                    "FAILED: " + ", ".join(n for n, ok in trial["rules"].items() if not ok)
                print(f"[{done}/{total}] {persona['id']} | {version_name} | trial {k} -> {status}")

    (out_folder / "all_conversations.json").write_text(json.dumps(trials, indent=2), encoding="utf-8")
    write_reports(out_folder, trials, personas)
    print(f"Finished in {round(time.time() - started)} seconds.")


if __name__ == "__main__":
    main()
