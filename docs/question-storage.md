# Questions in codeWOF

This guide provides a brief overview of how questions are stored in codeWOF.
The system we use for storing questions in our repository more complicated than you might expect, but we have used this system successfully for many years as it handles translations very well.

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

## Question type

There are multiple types of questions available:

- **Program:** Runs the submitted code, and can ask/receive input.
- **Function:** Appends a function call to the submitted code.
- **Parsons:** Drag and drop code creator from a set of given blocks.
- **Debugging:** Existing code with errors, some code is read only.

A question can only be one type, except for questions that can be both function and parson types.

## Components of a question

There are three major components of a question:

1. Question metadata (language independent)
2. Question content (language dependent)
3. Question tags (difficulty, concepts, contexts)

## Question metadata

The file `codewof/programming/content/structure/questions.yaml` contains key information about the question.

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

## Question content

In the directory `codewof/programming/content/en/`, there must be a directory with the slug from `questions.yaml` (see Question metadata).

Each question directory should have the following files:

- `question.md` - Markdown file containing question title and description.
- `solution.py` - Python file that is the solution to the question.
- Test cases:

  - `test-case-N-input.txt` (program type only) - Input for test case.
  - `test-case-N-code.txt` (non-program types only) - Code to append for test case.
  - `test-case-N-output.txt` - Expected output for test case.

- `initial.py` (debugging type only) - Python file for initial code to display.

Question directories may optionally have a `macros.yaml` file. See randomisation.md for more details.

## Question tags

Each question must be tagged by difficulty, and can be tagged by programming concepts and programming contexts.
This allows users to easily search for questions of a specific type.

These are defined in the file `codewof/programming/content/structure/questions.yaml`

Each question **requires** a `difficulty`, either:
- `difficulty-0` - Easy
- `difficulty-1` - Moderate
- `difficulty-2` - Difficult
- `difficulty-3` - Complex

If applicable, one or more `concepts` should be added to the question from the following
(i.e. you cannot have a question with the "Conditionals" concept, it needs to be a sub-category such as `single-condition`):

- `display-text` - Display Text
- `functions` - Functions
- `inputs` - Inputs
- Conditionals
  - `single-condition` - Single Condition
  - `multiple-conditions` - Multiple Conditions
  - `advanced-conditionals` - Advanced Conditionals
- Loops
  - `conditional-loops` - Conditional Loops
  - `range-loops` - Range Loops
- `string-operations` - String Operations
- `lists` - Lists

If applicable, one or more `contexts` should be added to the question from the following
(i.e. you cannot have a question with the "Geometry" context, it needs to be a sub-category such as `basic-geometry`):

- Mathematics
  - Geometry
    - `basic-geometry` - Basic Geometry
    - `advanced-geometry` - Advanced Geometry
  - `simple-mathematics` - Simple Mathematics
  - `advanced-mathematics` - Advanced Mathematics
- `real-world-applications` - Real World Applications

## Draft questions
Draft questions are stored as a more generic instance of a question, and are more strictly typed when submitting. This is to allow drafts to be saved with very little information. Once submitted for review, drafts are stored as files until they have been reviewed (see reviewing-questions.md).