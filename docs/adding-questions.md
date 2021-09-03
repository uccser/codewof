# Adding questions to codeWOF

This guide provides a brief overview of how to add questions to codeWOF.
The system we use for storing questions in our repository more complicated than you might expect, but we have used this system successfully for many years as it handles translations very well.

## Writing a question

When writing a question for codeWOF, you will want to keep the main goal of codeWOF in your mind, which is "Strengthen your programming skills, and maintain your coding warrant of fitness."
This website is not for teaching new skills, but reinforcing existing knowledge for the user.

Questions should be quick to complete, easy to understand, short to write, and use basic skills.
The questions on the website are all handwritten, so for each question we recommend creating multiple variants if possible (up to five), with each question expecting different values.

Most questions on the website so far can be completed in a few lines, and only test one or a couple of skills at a time.

Currently only Python 3 questions are supported on the website.

Skills can include:

- Strings (creating, manipulation, etc)
- Numbers (mathematics, etc)
- Input
- Output
- Types (casting, etc)
- Conditionals
- Repetition
- Basic data structures (lists)

Currently we do not test advanced skills, such as:
- Dictionaries
- Sets
- Coding style
- Exceptions

**Note:** *We currently cannot include questions requiring the `round()` function due to a bug.*

## Choosing a question type

There are multiple types of questions available:

- **Program:** Runs the submitted code, and can ask/receive input.
- **Function:** Appends a function call to the submitted code.
- **Parsons:** Drag and drop code creator from a set of given blocks.
- **Debugging:** Existing code with errors, some code is read only.

A question can only be one type, expect for questions that can be both function and parson types.

## Adding a question

There are two stages to adding a question:

1. Add question metadata (language independent)
2. Add question content (language dependent)

### Adding question metadata

Open file: `codewof/programming/content/structure/questions.yaml`

The file contains key information about the question.

*We recommend copying a question with the same type as your new question.*

Each question requires a slug, a unique identifier made from lower case letters, numbers, and dashes.

Each question then has a `type` or `types`.

Each question also has a number of test cases.
Each test case is either `normal` or `exceptional`.
All test cases are normal, but exceptional test cases are when unexpected values are checked (like a wrong data type).
If in doubt, mark a test case as 'normal'.

Parson questions have the following additional item:

- `parsons-extra-lines`

Debugging questions have the following additional items:

- `number_of_read_only_lines_top`
- `number_of_read_only_lines_bottom`

## Adding question content

Open directory: `codewof/programming/content/en/`

Create a directory with the slug you added in the previous step.

Each question directory should have the following files:

- `question.md` - Markdown file containing question title and description.
- `solution.py` - Python file that is the solution to the question.
- Test cases:

  - `test-case-N-input.txt` (program type only) - Input for test case.
  - `test-case-N-code.txt` (non-program types only) - Code to append for test case.
  - `test-case-N-output.txt` - Expected output for test case.

- `initial.py` (debugging type only) - Python file for initial code to display.
