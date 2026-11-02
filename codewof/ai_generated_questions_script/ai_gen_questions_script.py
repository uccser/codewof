"""
Generate new questions for CodeWOF using an AI agent via OpenRouter.

Guide: https://openrouter.ai/docs/quickstart#using-the-openrouter-api

This script:
  1. Reads every file in the programming/content folder (existing questions)
     plus the adding-questions.md guide, so the model knows the structure new
     questions should follow.
  2. Sends one prompt asking the model to generate new CodeWOF questions
     (question folder contents + the YAML segment needed to register each one).
  3. Writes each new question folder directly into the content folder and
     appends the YAML segments to the end of questions.yaml.

NOTE: OPENROUTER_API_KEY is read from a .env
"""

import json
import os
import re
from datetime import timezone, datetime
from pathlib import Path
import csv
import requests
import yaml


try:
    import dotenv
except ImportError:  # dotenv is optional
    dotenv = None

def get_api_key() -> str:
    # -----------Instead uncomment this and add your API_KEY------------------
    # return "<your-api-key>"
    # ------------------DO NOT PUSH YOUR API KEY-------------------------------
    if dotenv:
        dotenv.load_dotenv()  # loads OPENROUTER_API_KEY from a .env file in this directory
    key = os.getenv("OPENROUTER_API_KEY")
    if not key:
        raise RuntimeError("OPENROUTER_API_KEY not found - check your .env file has it set.")
    return key




BASE_DIR = Path(__file__).parent
CONTEXT_DIR = BASE_DIR.parent / "programming" / "content"
QUESTIONS_DIR = CONTEXT_DIR / "en"
QUESTION_YAML = CONTEXT_DIR / "structure" / "questions.yaml"
RAW_RESPONSE_FILE = BASE_DIR / "generated_questions_raw.json"
ADD_QUESTION_GUIDE = BASE_DIR.parent.parent / "docs" / "adding-questions.md"
NUMBER_OF_QUESTIONS = 20  # this is the number of new questions be generated. Keep this number under 100, run this script it batches if you wish to generate more than 100.
TEXT_SUFFIXES = {".md", ".py", ".yaml", ".yml", ".txt", ".json"}  # Only pull in files we can sensibly read as text.
AI_MODEL = "anthropic/claude-opus-5"
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
USAGE_LOG_FILE = BASE_DIR / "script_token_log.csv"
USAGE_LOG_FIELDS = [
    "timestamp", "model", "prompt_tokens", "completion_tokens",
    "cost", "questions_requested", "questions_written", "files_written",
]
SLUG_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
FILE_RE = re.compile(r"^(question\.md|solution\.py|initial\.py|test-case-\d+-(input|code|output)\.txt)$")
ERROR_FILE = BASE_DIR / "generated_questions_errors.json"



def load_context_files() -> str:
    """Read every text file under CONTEXT_DIR, plus the adding-questions guide,
    and bundle it all into one blob."""
    if not CONTEXT_DIR.exists():
        raise FileNotFoundError(f"Context folder not found: {CONTEXT_DIR}")

    sections = []

    # The guide describing how questions must be structured and registered.
    if not ADD_QUESTION_GUIDE.exists():
        raise FileNotFoundError(f"Add question guide not found: {ADD_QUESTION_GUIDE}")
    guide_content = ADD_QUESTION_GUIDE.read_text(encoding="utf-8")
    sections.append(f"### File: {ADD_QUESTION_GUIDE.name} (guide)\n```\n{guide_content}\n```")

    for path in sorted(CONTEXT_DIR.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue  # skip anything that isn't plain text
        relative = path.relative_to(CONTEXT_DIR)
        sections.append(f"### File: {relative}\n```\n{content}\n```")

    if len(sections) <= 1:
        raise RuntimeError(f"No readable files found in {CONTEXT_DIR}")

    return "\n\n".join(sections)


def build_prompt(context_blob: str) -> str:
    return f"""You are helping generate new questions for CodeWOF.

Below is context: example questions that already exist in CodeWOF, and the
adding-questions.md guide describing how new questions must be structured and
registered.

{context_blob}

Generate questions:
Generate {NUMBER_OF_QUESTIONS} new questions for CodeWOF with a range of difficulties, types, and
contexts. I want an approximately even amount of questions of each type and difficulty,
i.e. equal number or programming, function, parsons and debug questions and equal number of easy, moderate, hard and complex questions.
Make sure all the questions generated have the concept tag 'ai-generated'.
Make sure all new questions are unique and are not exactly the same as the question already existing in the given context-files, you must not give duplicates.
Use the existing questions above as a guide for style, structure and format.
Make some question contexts have relevance to New Zealand culture and if using Te reo Māori words ensure they are spelt correctly with macrons where necessary and used in a culturally appropriate context.
Each question's folder must contain exactly these files, matching
the real CodeWOF question format:
  - "question.md"
  - "solution.py"
  - "test-case-1-code.txt" or "test-case-1-input.txt" input files are required instead of code files for testing exercises that include inputs. For an example of an input question see repeated-add-10 in the context-files.
  - "test-case-1-output.txt" (and -2-, -3- etc, at least 3 test cases per question)
  - the exact YAML segment needed to register the question (as a string)

Respond with ONLY raw JSON (no markdown fences, no commentary before or
after) matching this schema. Include every file for the question (question.md,
solution.py and all the test case files) inside "files":

{{
  "questions": [
    {{
      "folder_name": "kebab-case-slug-for-the-question",
      "files": {{
        "question.md": "full file content as a string",
        "solution.py": "full file content as a string",
        "test-case-1-code.txt": "full file content as a string",
        "test-case-1-output.txt": "full file content as a string"
      }},
      "yaml_segment": "the exact YAML snippet to register this question, as a string"
    }}
  ]
}}

All string values must have newlines escaped as \\n so the whole response is
valid, parseable JSON. Do not wrap the JSON in ```json fences.
"""

def request_completion(prompt: str, api_key: str, model: str = AI_MODEL, post=requests.post) -> dict:
    response = post(
        url=OPENROUTER_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        data=json.dumps(
            {
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
            }
        ),
        timeout=480,
    )
    if not response.ok:
        print(f"OpenRouter error {response.status_code}: {response.text}")
    response.raise_for_status()
    return response.json()

def format_usage(token_usage: dict):
    token_usage = token_usage or {}
    cost = token_usage.get("cost")
    prompt_tokens = token_usage.get("prompt_tokens")
    completion_tokens = token_usage.get("completion_tokens")
    if token_usage:
        summary = f"Usage: {prompt_tokens} input tokens, {completion_tokens} output tokens"
        print(summary if cost is None else f"{summary}, cost: ${cost:.5f}")
    return cost, prompt_tokens, completion_tokens


def log_run_to_csv(prompt_tokens, completion_tokens, cost, questions_written, files_written):
    write_header = not USAGE_LOG_FILE.exists() or USAGE_LOG_FILE.stat().st_size == 0
    with USAGE_LOG_FILE.open("a", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=USAGE_LOG_FIELDS)
        if write_header:
            writer.writeheader()
        writer.writerow({
            "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "model": AI_MODEL,
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "cost": cost,
            "questions_requested": NUMBER_OF_QUESTIONS,
            "questions_written": questions_written,
            "files_written": files_written
        })




def extract_json(text: str) -> dict:
    """Parse the model's reply as JSON, tolerating stray ```json fences."""
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("```", 2)[1]
        if cleaned.startswith("json"):
            cleaned = cleaned[len("json"):]
        cleaned = cleaned.rsplit("```", 1)[0]
    return json.loads(cleaned.strip())

def get_existing_slugs() -> set:
    """Return slugs already used, from both the content folders and questions.yaml."""
    slugs = set()
    if QUESTIONS_DIR.exists():
        slugs |= {p.name for p in QUESTIONS_DIR.iterdir() if p.is_dir()}
    if QUESTION_YAML.exists():
        slugs |= set(yaml.safe_load(QUESTION_YAML.read_text(encoding="utf-8")) or {})
    return slugs

def write_questions(data: dict):
    """Write each new question folder into QUESTIONS_DIR and append the YAML
    segments to the end of QUESTION_YAML."""
    questions = data.get("questions", [])
    if not questions:
        print("Warning: no 'questions' found in the response.")
        return 0, 0

    QUESTIONS_DIR.mkdir(parents=True, exist_ok=True)
    existing_slugs = get_existing_slugs()
    yaml_segments = []
    questions_written = 0
    files_written = 0
    for question in questions:
        errors = validate_question(question, existing_slugs)
        if len(errors) > 0:
            print(f"Skipping {question.get('folder_name')!r}: " + "; ".join(errors))
            continue

        folder_name = question["folder_name"]
        question_dir = QUESTIONS_DIR / folder_name

        # Never overwrite an existing question.
        if question_dir.exists():
            print(f"Skipping '{folder_name}': folder already exists at {question_dir}")
            continue
        question_dir.mkdir(parents=True)

        for filename, content in question["files"].items():
            (question_dir / filename).write_text(content, encoding="utf-8")
            files_written += 1

        yaml_segments.append(question["yaml_segment"].rstrip())
        questions_written += 1
        print(f"Wrote question folder: {question_dir}")

    if yaml_segments:
        QUESTION_YAML.parent.mkdir(parents=True, exist_ok=True)
        existing = QUESTION_YAML.read_text(encoding="utf-8") if QUESTION_YAML.exists() else ""
        separator = "" if not existing or existing.endswith("\n") else "\n"
        with QUESTION_YAML.open("a", encoding="utf-8") as yaml_file:
            yaml_file.write(separator + "\n".join(yaml_segments) + "\n")
        print(f"Appended {len(yaml_segments)} YAML segments to: {QUESTION_YAML}")

    return questions_written, files_written


def validate_question(question: dict, existing_slugs: set) -> list:
    """Return a list of problems with a generated question (empty if it looks valid)."""
    errors = []
    slug, files = question.get("folder_name"), question.get("files")
    if not isinstance(slug, str) or not SLUG_RE.match(slug):
        errors.append(f"invalid folder_name: {slug!r}")
    elif slug in existing_slugs:
        errors.append(f"slug already exists: {slug}")
    if not isinstance(files, dict):
        return errors + ["'files' missing or not an object"]
    errors += [f"unexpected file name: {n!r}" for n in files if not FILE_RE.match(n)]
    errors += [f"missing {r}" for r in ("question.md", "solution.py") if r not in files]
    if sum(n.endswith("-output.txt") for n in files) < 3:
        errors.append("fewer than 3 test cases")
    try:
        parsed = yaml.safe_load(question.get("yaml_segment") or "")
    except yaml.YAMLError as exc:
        return errors + [f"invalid YAML: {exc}"]
    if not isinstance(parsed, dict) or list(parsed) != [slug]:
        errors.append("yaml_segment must have exactly one top-level key equal to folder_name")
    else:
        details = parsed[slug]
        concepts = details.get("concepts") if isinstance(details, dict) else None
        if not isinstance(concepts, list) or "ai-generated" not in concepts:
            errors.append("yaml_segment must list 'ai-generated' under concepts")
    return errors



def main() -> int:
    """Run the generator and return a process exit code."""
    api_key = get_api_key()
    prompt = build_prompt(load_context_files())
    print("Sending request to OpenRouter...")
    result = request_completion(prompt, api_key)
    cost, prompt_tokens, completion_tokens = format_usage(result.get("usage", {}))

    questions_written = files_written = 0
    try:
        try:
            message = result["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError):
            ERROR_FILE.write_text(json.dumps(result, indent=2), encoding="utf-8")
            print(f"Unexpected API response shape. Saved to {ERROR_FILE}")
            return 1

        RAW_RESPONSE_FILE.write_text(message, encoding="utf-8")
        try:
            data = extract_json(message)
        except json.JSONDecodeError as exc:
            print(f"Failed to parse JSON: {exc}. Raw response saved to {RAW_RESPONSE_FILE}")
            return 1

        questions_written, files_written = write_questions(data)
    finally:
        log_run_to_csv(prompt_tokens, completion_tokens, cost, questions_written, files_written)

    print("Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
