# Running the AI question generation script

`ai_gen_questions_script.py` uses an AI model (via [OpenRouter](https://openrouter.ai/)) to generate new CodeWOF questions.
It reads the existing questions and the [adding questions guide](../../docs/adding-questions.md) so the model knows the format, then writes each new question into `programming/content/en/` and registers it in `programming/content/structure/questions.yaml`.

## Requirements

- An OpenRouter account with funds attached. A default run (32 questions) costs just under $2 (as of October 2026).
- Python 3
- An OpenRouter API key

## Setup

1. Create a `.env` file in this directory, using the same structure as `.env.example`:

   ```
   OPENROUTER_API_KEY=<your-api-key>
   ```

2. In a terminal, go to this directory and create a virtual environment:

   ```
   cd codewof/ai_generated_questions_script
   python3 -m venv .venv
   source .venv/bin/activate
   ```

   On Windows, activate it with `.venv\Scripts\activate` instead.

3. Install the dependencies:

   ```
   pip install python-dotenv requests pyyaml
   ```

## Running the script

```
python ai_gen_questions_script.py
```

The script prints the token usage and cost of the request, then lists each question folder it writes.
It exits with code `0` on success and `1` if the API response could not be used.

To change how many questions are generated, or which model is used, edit `NUMBER_OF_QUESTIONS` and `AI_MODEL` near the top of the script.
Try a small number (for example 2 or 3) first to check your setup cheaply.

### Without a virtual environment or `python-dotenv`

`python-dotenv` is optional. The script only uses it to read your `.env` file.
If it isn't installed, set the key in your terminal instead:

```
export OPENROUTER_API_KEY=<your-api-key>
python ai_gen_questions_script.py
```

`requests` and `pyyaml` are always required.

As a last resort you can hard-code the key by uncommenting the `return "<your-api-key>"` line at the top of `get_api_key()` in the script.
**Never commit your API key.** Undo this change before you commit.

## What the script does

1. Reads every text file in `programming/content` and the adding questions guide.
2. Sends one request asking the model for the new questions.
3. Checks each generated question and skips any that fail (see below).
4. Writes each valid question folder into `programming/content/en/`.
5. Appends the matching YAML entries to the end of `programming/content/structure/questions.yaml`.
6. Adds a row to the usage log.

### Checks applied to each generated question

A question is skipped, and nothing is written for it, if:

- its folder name is not a lowercase kebab-case slug (for example `my-question`)
- its slug already exists as a folder or in `questions.yaml`
- it contains a file other than `question.md`, `solution.py`, `initial.py` or `test-case-N-input.txt` / `-code.txt` / `-output.txt`
- `question.md` or `solution.py` is missing
- it has fewer than 3 test cases
- its YAML entry is invalid, or does not have exactly one top-level key matching the folder name

Existing questions are never overwritten.

## Files created

| File | Contents | Created when |
| --- | --- | --- |
| `programming/content/en/<question-slug>/` | The new question files | Each valid question |
| `programming/content/structure/questions.yaml` | New entries appended | At least one valid question |
| `script_token_log.csv` | One row per run (see below) | Every run |
| `generated_questions_raw.json` | The model's raw reply, for inspection | The API returned a reply |
| `generated_questions_errors.json` | The full API response | The response had an unexpected shape |

### Usage log

`script_token_log.csv` gets one new row each time the script runs, including failed runs, because the request is still charged.

| Column | Meaning |
| --- | --- |
| `timestamp` | When the run finished (UTC) |
| `model` | The model used |
| `prompt_tokens` | Input tokens |
| `completion_tokens` | Output tokens |
| `cost` | Cost reported by OpenRouter (blank if not reported) |
| `questions_requested` | The value of `NUMBER_OF_QUESTIONS` |
| `questions_written` | Questions that passed the checks and were written |
| `files_written` | Total files written across those questions |

## After running

The questions are AI-generated, so they must be reviewed by a person before they are merged:

- Read each `question.md` to check it is clear and at the right difficulty.
- Check that each `solution.py` produces the expected output for every test case.
- Check any te reo Māori is spelt correctly (including macrons) and used appropriately.
- Check the questions load: the content test in CI runs `manage.py update_data`, which will fail on invalid question data.

Before committing, check `git status`. Do not commit your `.env` file, `generated_questions_raw.json` or `generated_questions_errors.json`.
