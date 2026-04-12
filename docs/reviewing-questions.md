# Reviewing Submitted CodeWOF Questions

This guide provides a brief overview of how to review questions for CodeWOF. This is only possible for administrator users.

## Finding questions to review

Submitted questions are currently stored as files on the server. To view them, log into the production server and navigate to `programming/review/`. From here, each individual question has a file in `structure/` which contains the YAML describing it, and a folder in `en/` which contain the question files.

## Reviewing a question
Pick a question from its file in `structure/` - e.g. `question_name.yaml`. This file and the accompanying folder in `en/` (named `question_name/`) are the components of the question. Check the following:
- `structure/question_name.yaml`: this file needs to be valid YAML syntax. It should meet the criteria described in reviewing-questions.md.
- `en/question_name/`: this **must** contain the following files.
    - `question.md`: This should contain the title and the question text, in valid markdown. The only HTML tag that should be visible is <sup>.
    - `solution.py`: This must be valid python code.
    - `test-case-<n>-code.txt` or `test-case-<n>-input.txt`: the file should contain input if the question type is program, otherwise it should contain code. Check that this file is either valid python code, or reasonable input for the question accordingly.
    - `test-case-<n>-output.txt`: this should contain the expected output of test case n
    If the question is a debugging question, the folder must also contain
    - `initial.py`: This should be valid python code which will need to be debugged.
- For the files described above, check that:
    - The question text makes the requirements clear;
    - The solution code correctly answers the question and is stylistically correct (especially check that there is whitespace around operators);
    - The test cases adequately describe the solution (e.g. boundary cases);
    - Any initial code does not pass all test cases;
    - No Python code uses the `round()` function (currently broken)

Additionally, check that the question being reviewed does not contain macros (look for a `macros.yaml` file in the `en/question_name/` directory). These are not currently used when serving questions, so would return broken questions to the user.

### Passing review
To move a question from a review state to being used, copy the contents of `question_name.yaml` to `programming/content/structure/questions.yaml` and delete `question_name.yaml`. Then, move the folder `programming/review/en/question_name/` to `programming/content/en/question_name/`.

To avoid any potential issues with automated deployment, push these changes to the git repository.

### Failing review
If the reviewed question needs some minor work, feel free to make the small changes required and then review the question again. Otherwise, delete the file `question_name.yaml` from `review/structure/` and the folder `question_name/` from `/review/en`.