# Lessons learned in this project

Short, specific, evidence-backed. Newest first. The shared system reads this file at the start of each session
here and at the monthly review. Never put links, secrets or personal data in it.

## 2026-11-18 · update-eval-prompt-status
- **Refer to the updated single-turn and multi-turn prompt files by name when explaining a Git merge.** _Evidence: calling them “merged prompts” made it unclear whether both conditions still used separate files._
- **Check the earlier prompt before describing an instruction as new.** _Evidence: review confirmed that the recommendation limit already existed in both conditions and that the change removed the separate cap on multi-turn questions._
- **Check which answers the test personas actually send before describing what a rerun would cover.** _Evidence: the standard browser tests send all six answers, so testing partial replies requires different cases._

## 2026-11-18 · single-turn-partial-answers
- **Omit unanswered items from the single-turn summary and choose recommendations using the answers the participant supplied.** _Evidence: the user rejected placeholder text and asked Alex to work with the information in the reply._
- **Keep the link between an answer and its question when shortening a displayed response summary.** _Evidence: review showed that the same one-word preference or avoidance could look identical after the question slots were removed._

## 2026-11-18 · align-treatment-prompts
- **Compare randomized questionnaire content by question identity, including nested items, rather than by display order.** _Evidence: the first condition check treated shuffled Likert items as a content difference. Comparing individual items confirmed that both conditions use the same questionnaires._

## 2026-11-18 · eval-history-readability
- **Explain evaluation changes with before-and-after instructions and labeled examples, and separate untested revisions from measured scores.** _Evidence: the user requested more explicit nontechnical explanations and a clear statement that the latest revision still needs a new evaluation._
- **Present evaluation changes as short action bullets, keep context in separate blocks, and finish with the changes still present in the current version.** _Evidence: the user approved the content but found the per-evaluation descriptions hard to read and requested a final baseline-to-current change list._

## 2026-11-18 · eval-browser-docs
- **When correcting format labels, fix generation, saved filenames, and result readers together while preserving transcript contents and scores.** _Evidence: the filename correction required changes beyond the README; regression checks and transcript hashes verified consistent labels with unchanged results._

## 2026-11-18 · eval-documentation
- **Document local-only evaluation files separately from tracked summaries, and explain each round from its actual changes and saved scores.** _Evidence: the evaluation README was unclear about local folders; file tracking, commit diffs, and offline transcript scoring established the correct structure and round history._

## 2026-11-16 · remove-evals-from-repo
- **Check what a remote branch actually contains before pulling or relying on it.** Read the remote listing directly rather than inferring from local branch output. _Evidence: a pull failed with "couldn't find remote ref" after the assistant misread a local branch line as a remote one._

## 2026-11-16 · alex-opener-and-prompts
- **Show the actual output of a command before saying what it should have printed.** Quote the real lines from the run, and say plainly when an expected line is missing. _Evidence: the user replied "i didnt see this" after the assistant described progress lines it had not shown from the user's run._
