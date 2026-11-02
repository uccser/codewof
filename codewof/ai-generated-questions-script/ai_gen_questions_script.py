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
from pathlib import Path

import requests

#  -----If want to be able to run the script directly without dealing with installing dotenv then comment out this section----
import dotenv

dotenv.load_dotenv()  # loads OPENROUTER_API_KEY from a .env file in this directory
API_KEY = os.getenv("OPENROUTER_API_KEY")
if not API_KEY:
    raise RuntimeError(
        "OPENROUTER_API_KEY not found - check your .env file has it set."
    )

# -----------Instead uncomment this and add your API_KEY------------------
# API_KEY="<your-api-key>"
# ------------------DO NOT PUSH YOUR API KEY-------------------------------


BASE_DIR = Path(__file__).parent
CONTEXT_DIR = BASE_DIR.parent / "programming" / "content"
QUESTIONS_DIR = CONTEXT_DIR / "en"
QUESTION_YAML = CONTEXT_DIR / "structure" / "questions.yaml"
RAW_RESPONSE_FILE = BASE_DIR / "generated_questions_raw.json"
ADD_QUESTION_GUIDE = BASE_DIR.parent.parent / "docs" / "adding-questions.md"
NUMBER_OF_QUESTIONS = 32  # this is the number of new questions be generated. Keep this number under 100, run this script it batches if you wish to generate more than 100.
TEXT_SUFFIXES = {".md", ".py", ".yaml", ".yml", ".txt", ".json"}  # Only pull in files we can sensibly read as text.
AI_MODEL = "anthropic/claude-opus-5"


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


def generate(prompt: str) -> dict:
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        },
        data=json.dumps(
            {
                "model": AI_MODEL,
                "messages": [{"role": "user", "content": prompt}],
            }
        ),
        timeout=480,
    )
    if not response.ok:
        print(f"OpenRouter error {response.status_code}: {response.text}")
    response.raise_for_status()
    data = response.json()
    token_usage = data.get("usage", {})
    if token_usage:
        cost = token_usage.get("cost")
        prompt_tokens = token_usage.get("prompt_tokens")
        completion_tokens = token_usage.get("completion_tokens")
        print(
            f"Usage: {prompt_tokens} input tokens, {completion_tokens} output "
            f"tokens, cost: ${cost:.5f}" if cost is not None else
            f"Usage: {prompt_tokens} input tokens, {completion_tokens} output tokens"
        )

    return data


def extract_json(text: str) -> dict:
    """Parse the model's reply as JSON, tolerating stray ```json fences."""
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("```", 2)[1]
        if cleaned.startswith("json"):
            cleaned = cleaned[len("json"):]
        cleaned = cleaned.rsplit("```", 1)[0]
    return json.loads(cleaned.strip())


def write_questions(data: dict) -> None:
    """Write each new question folder into QUESTIONS_DIR and append the YAML
    segments to the end of QUESTION_YAML."""
    questions = data.get("questions", [])
    if not questions:
        print("Warning: no 'questions' found in the response.")
        return

    QUESTIONS_DIR.mkdir(parents=True, exist_ok=True)

    yaml_segments = []
    for question in questions:
        folder_name = question["folder_name"]
        question_dir = QUESTIONS_DIR / folder_name

        # Never overwrite an existing question.
        if question_dir.exists():
            print(f"Skipping '{folder_name}': folder already exists at {question_dir}")
            continue
        question_dir.mkdir(parents=True)

        for filename, content in question["files"].items():
            (question_dir / filename).write_text(content, encoding="utf-8")

        yaml_segments.append(question["yaml_segment"].rstrip())
        print(f"Wrote question folder: {question_dir}")

    if yaml_segments:
        QUESTION_YAML.parent.mkdir(parents=True, exist_ok=True)
        existing = QUESTION_YAML.read_text(encoding="utf-8") if QUESTION_YAML.exists() else ""
        separator = "" if not existing or existing.endswith("\n") else "\n"
        with QUESTION_YAML.open("a", encoding="utf-8") as yaml_file:
            yaml_file.write(separator + "\n".join(yaml_segments) + "\n")
        print(f"Appended {len(yaml_segments)} YAML segments to: {QUESTION_YAML}")


def main():
    context_blob = load_context_files()
    prompt = build_prompt(context_blob)

    print("Sending request to OpenRouter...")
    result = generate(prompt)
    message = result["choices"][0]["message"]["content"]

    RAW_RESPONSE_FILE.write_text(message, encoding="utf-8")

    try:
        data = extract_json(message)
    except json.JSONDecodeError as exc:
        print(
            f"Failed to parse the model's response as JSON: {exc}\n"
            f"Raw response saved to {RAW_RESPONSE_FILE} for inspection."
        )
        return

    write_questions(data)
    print("Done.")


if __name__ == "__main__":
    main()
