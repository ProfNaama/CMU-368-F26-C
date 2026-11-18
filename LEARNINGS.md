# Lessons learned in this project

Short, specific, evidence-backed. Newest first. The shared system reads this file at the start of each session
here and at the monthly review. Never put links, secrets or personal data in it.

## 2026-11-18 · eval-documentation
- **Document local-only evaluation files separately from tracked summaries, and explain each round from its actual changes and saved scores.** _Evidence: the evaluation README was unclear about local folders; file tracking, commit diffs, and offline transcript scoring established the correct structure and round history._

## 2026-11-16 · remove-evals-from-repo
- **Check what a remote branch actually contains before pulling or relying on it.** Read the remote listing directly rather than inferring from local branch output. _Evidence: a pull failed with "couldn't find remote ref" after the assistant misread a local branch line as a remote one._

## 2026-11-16 · alex-opener-and-prompts
- **Show the actual output of a command before saying what it should have printed.** Quote the real lines from the run, and say plainly when an expected line is missing. _Evidence: the user replied "i didnt see this" after the assistant described progress lines it had not shown from the user's run._
