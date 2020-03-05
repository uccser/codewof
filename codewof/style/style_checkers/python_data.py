PYTHON_ISSUES = {
    "E101": {
        "original_message": "indentation contains mixed spaces and tabs",
        "templated": False,
        "title": "This line is indented using a mixture of spaces and tabs.",
        "solution": "You should indent your code using only spaces.",
        "explanation": "Python expects the indentation method to be consistent line to line. Spaces are the preferred indentation method."
    },
    "E111": {
        "original_message": "indentation is not a multiple of four",
        "templated": False,
        "title": "This line has an indentation level that is not a multiple of four.",
        "solution": "Ensure that the first indentation level is 4 spaces, the second indentation level is 8 spaces and so on.",
        "explanation": ""
    },
    "E112": {
        "original_message": "expected an indented block",
        "templated": False,
        "title": "This line is not indented at the correct level.",
        "solution": "Add indentation to this line until it is indented at the correct level.",
        "explanation": ""
    },
    "E113": {
        "original_message": "unexpected indentation",
        "templated": False,
        "title": "This line is indented when it shouldn't be.",
        "solution": "Remove indentation from this line until it is indented at the correct level.",
        "explanation": ""
    },
    "E114": {
        "original_message": "indentation is not a multiple of four (comment)",
        "templated": False,
        "title": "This line has an indentation level that is not a multiple of four.",
        "solution": "Ensure that the first indentation level is 4 spaces, the second indentation level is 8 spaces and so on.",
        "explanation": ""
    },
    "E115": {
        "original_message": "expected an indented block (comment)",
        "templated": False,
        "title": "This line is not indented at the correct level.",
        "solution": "Add indentation to this line until it is indented at the correct level.",
        "explanation": "Comments should be indented relative to the code block they are in."
    },
    "E116": {
        "original_message": "unexpected indentation (comment)",
        "templated": False,
        "title": "This line is indented when it shouldn't be.",
        "solution": "Remove indentation from this line until it is indented at the correct level.",
        "explanation": ""
    },
    "E117": {
        "original_message": "over-indented",
        "templated": False,
        "title": "This line has too many indentation levels.",
        "solution": "Remove indentation from this line until it is indented at the correct level.",
        "explanation": ""
    },
    # E121 ignored by default
    "E121": {
        "original_message": "continuation line under-indented for hanging indent",
        "templated": False,
        "title": "This line is less indented than it should be.",
        "solution": "Add indentation to this line until it is indented at the correct level.",
        "explanation": ""
    },
    "E122": {
        "original_message": "continuation line missing indentation or outdented",
        "templated": False,
        "title": "This line is not indented as far as it should be or is indented too far.",
        "solution": "Add or remove indentation levels until it is indented at the correct level.",
        "explanation": ""
    },
    # E123 ignored by default
    "E123": {
        "original_message": "closing bracket does not match indentation of opening bracket’s line",
        "templated": False,
        "title": "This line has a closing bracket that does not match the indentation level of the line that the opening bracket started on.",
        "solution": "Add or remove indentation of the closing bracket so it matches the indentation of the line that the opening bracket is on.",
        "explanation": ""
    },
    "E124": {
        "original_message": "closing bracket does not match visual indentation",
        "templated": False,
        "title": "This line has a closing bracket that does not match the indentation of the opening bracket.",
        "solution": "Add or remove indentation of the closing bracket so it matches the indentation of the opening bracket.",
        "explanation": ""
    },
    "E125": {
        "original_message": "continuation line with same indent as next logical line",
        "templated": False,
        "title": "This line has a continuation that should be indented one extra level so that it can be distinguished from the next logical line.",
        "solution": "Add an indentation level to the line continuation so that it is indented one more level than the next logical line.",
        "explanation": "Continuation lines should not be indented at the same level as the next logical line. Instead, they should be indented to one more level so as to distinguish them from the next line."
    },
    # E126 ignored by default
    "E126": {
        "original_message": "continuation line over-indented for hanging indent",
        "templated": False,
        "title": "This line is indented more than it should be.",
        "solution": "Remove indentation from this line until it is indented at the correct level.",
        "explanation": ""
    },
    "E127": {
        "original_message": "continuation line over-indented for visual indent",
        "templated": False,
        "title": "This line is indented more than it should be.",
        "solution": "Remove indentation from this line until it is indented at the correct level.",
        "explanation": ""
    },
    "E128": {
        "original_message": "continuation line under-indented for visual indent",
        "templated": False,
        "title": "This line is indented less than it should be.",
        "solution": "Add indentation to this line until it is indented at the correct level.",
        "explanation": ""
    },
    "E129": {
        "original_message": "visually indented line with same indent as next logical line",
        "templated": False,
        "title": "This line has the same indentation as the next logical line.",
        "solution": "Add an indentation level to the visually indented line so that it is indented one more level than the next logical line.",
        "explanation": "A visually indented line that has the same indentation as the next logical line is hard to read."
    },
    "E131": {
        "original_message": "continuation line unaligned for hanging indent",
        "templated": False,
        "title": "This line is not aligned correctly for a hanging indent.",
        "solution": "Add or remove indentation so that the lines are aligned with each other.",
        "explanation": ""
    },
    # E133 ignored by default
    "E133": {
        "original_message": "closing bracket is missing indentation",
        "templated": False,
        "title": "",
        "solution": "",
        "explanation": "",
    },
    "E201": {
        "original_message": "whitespace after '{character}'",
        "templated": True,
        "title": "This line contains {article} {character_description} that has a space after it.",
        "solution": "Remove any spaces that appear after the <code>{character}</code> character.",
        "explanation": ""
    },
    "E202": {
        "original_message": "whitespace before '{character}'",
        "templated": True,
        "title": "This line contains {article} {character_description} that has a space before it.",
        "solution": "Remove any spaces that appear before the <code>{character}</code> character.",
        "explanation": ""
    },
    "E203": {
        "original_message": "whitespace before '{character}'",
        "templated": True,
        "title": "This line contains {article} {character_description} that has a space before it.",
        "solution": "Remove any spaces that appear before the <code>{character}</code> character.",
        "explanation": ""
    },
    "E211": {
        "original_message": "whitespace before '{character}'",
        "templated": True,
        "title": "This line contains {article} {character_description} that has a space before it.",
        "solution": "Remove any spaces that appear before the <code>{character}</code> character.",
        "explanation": ""
    },
    "E221": {
        "templated": False,
        "original_message": "multiple spaces before operator",
        "title": "This line has multiple spaces before an operator.",
        "solution": "Remove any extra spaces that appear before the operator on this line.",
        "explanation": ""
    },
    "E222": {
        "templated": False,
        "original_message": "multiple spaces after operator",
        "title": "This line has multiple spaces after an operator.",
        "solution": "Remove any extra spaces that appear after the operator on this line.",
        "explanation": ""
    },
    "E223": {
        "templated": False,
        "original_message": "tab before operator",
        "title": "This line contains a tab character before an operator.",
        "solution": "Remove any tab characters that appear before the operator on this line. Operators should only have one space before them.",
        "explanation": ""
    },
    "E224": {
        "templated": False,
        "original_message": "tab after operator",
        "title": "This line contains a tab character after an operator.",
        "solution": "Remove any tab characters that appear after the operator on this line. Operators should only have one space after them.",
        "explanation": ""
    },
    "E225": {
        "templated": False,
        "original_message": "missing whitespace around operator",
        "title": "This line is missing whitespace around an operator.",
        "solution": "Ensure there is one space before and after all operators.",
        "explanation": ""
    },
    # E226 ignored by default
    "E226": {
        "templated": False,
        "original_message": "missing whitespace around arithmetic operator",
        "title": "This line is missing whitespace around an arithmetic operator (+, -, / and *).",
        "solution": "Ensure there is one space before and after all arithmetic operators  (+, -, / and *).",
        "explanation": ""
    },
    "E227": {
        "templated": False,
        "original_message": "missing whitespace around bitwise or shift operator",
        "title": "This line is missing whitespace around a bitwise or shift operator (<<, >>, &, |, ^).",
        "solution": "Ensure there is one space before and after all bitwise and shift operators  (<<, >>, &, |, ^).",
        "explanation": ""
    },
    "E228": {
        "templated": False,
        "original_message": "missing whitespace around modulo operator",
        "title": "This line is missing whitespace around a modulo operator (<code>%</code>).",
        "solution": "Ensure there is one space before and after the modulo operator (<code>%</code>).",
        "explanation": ""
    },
    # TODO: Check for specific character
    "E231": {
        "original_message": "missing whitespace after ‘,’, ‘;’, or ‘:’",
        "title": "This line is missing whitespace around one of the following characters: , ; and :.",
        "solution": "Ensure there is one space before and after any of the following characters: , ; and :.",
        "explanation": ""
    },
    # E241 ignored by default
    "E241": {
        "original_message": "multiple spaces after ‘,’",
        "title": "This line has multiple spaces after the ',' character.",
        "solution": "Ensure there is one space before and after any ',' characters.",
        "explanation": ""
    },
    # E242 ignored by default
    "E242": {
        "original_message": "tab after ‘,’",
        "title": "This line contains a tab character after the ',' character.",
        "solution": "Remove any tab characters and ensure there is one space before and after any ',' characters.",
        "explanation": ""
    },
"E251": {
"original_message": "unexpected spaces around keyword / parameter equals",
"title": "This line contains spaces before or after the = in a function definition.",
"solution": "Remove any spaces that appear either before or after the = character in your function definition.",
"explanation": ""
},
"E261": {
"original_message": "at least two spaces before inline comment",
"title": "This line contains an inline comment that does not have 2 spaces before it.",
"solution": "Ensure that your inline comment has 2 spaces before the '#' character.",
"explanation": ""
},
"E262": {
"original_message": "inline comment should start with ‘# ‘",
"title": "Comments should start with a '#' character and have one space between the '#' character and the comment itself.",
"solution": "Ensure that your inline comment starts with a '#' character followed by a space and then the comment itself.",
"explanation": "https://lintlyci.github.io/Flake8Rules/rules/E262.html this rule seems to be more about the space after the pound sign though????"
},
"E265": {
"original_message": "block comment should start with ‘# ‘",
"title": "Comments should start with a '#' character and have one space between the '#' character and the comment itself.",
"solution": "Ensure that your block comment starts with a '#' character followed by a space and then the comment itself.",
"explanation": ""
},
"E266": {
"original_message": "too many leading ‘#’ for block comment",
"title": "Comments should only start with a single '#' character.",
"solution": "Ensure your comment only starts with one '#' character.",
"explanation": ""
},
"E271": {
"original_message": "multiple spaces after keyword",
"title": "This line contains more than one space after a keyword.",
"solution": "Ensure there is only one space after any keywords.",
"explanation": ""
},
"E272": {
"original_message": "multiple spaces before keyword",
"title": "This line contains more than one space before a keyword.",
"solution": "Ensure there is only one space before any keywords.",
"explanation": ""
},
"E273": {
"original_message": "tab after keyword",
"title": "This line contains a tab character after a keyword.",
"solution": "Ensure there is only one space after any keywords.",
"explanation": ""
},
"E274": {
"original_message": "tab before keyword",
"title": "This line contains a tab character before a keyword.",
"solution": "Ensure there is only one space before any keywords.",
"explanation": ""
},
"E275": {
"original_message": "missing whitespace after keyword",
"title": "This line is missing a space after a keyword.",
"solution": "Ensure there is one space after any keywords.",
"explanation": ""
},
"E301": {
"original_message": "expected 1 blank line, found 0",
"title": "This line is missing a blank line between the methods of a class.",
"solution": "Add a blank line in between your class methods.",
"explanation": ""
},
"E302": {
"original_message": "expected 2 blank lines, found 0",
"title": "Two blank lines are expected between functions and classes.",
"solution": "Ensure there are two blank lines between functions and classes.",
"explanation": ""
},
"E303": {
"original_message": "too many blank lines (3)",
"title": "There are too many blank lines.",
"solution": "Ensure there are two blank lines between functions and classes and one blank line between methods of a class.",
"explanation": ""
},
"E304": {
"original_message": "blank lines found after function decorator",
"title": "This line contains a blank line after a function decorator.",
"solution": "Ensure that there are no blank lines between a function decorator and the function it is decorating.",
"explanation": ""
},
"E305": {
"original_message": "expected 2 blank lines after end of function or class",
"title": "Functions and classes should have two blank lines after them.",
"solution": "Ensure that functions and classes should have two blank lines after them.",
"explanation": ""
},
"E306": {
"original_message": "expected 1 blank line before a nested definition",
"title": "Nested definitions should have one blank line before them.",
"solution": "Ensure there is a blank line above your nested definition.",
"explanation": ""
},
"E401": {
"original_message": "multiple imports on one line",
"title": "This line contains imports from different modules on the same line.",
"solution": "Ensure import statements from different modules occur on their own line.",
"explanation": ""
},
"E402": {
"original_message": "module level import not at top of file",
"title": "Module imports should be at the top of the file and there should be no statements in between module level imports.",
"solution": "Ensure all import statements are at the top of the file and there are no statements in between imports.",
"explanation": ""
},
"E501": {
"original_message": "line too long (82 > 79 characters)",
"title": "This line is longer than 79 characters.",
"solution": "You can insert a backslash character (\\) to wrap the text onto the next line.",
"explanation": "Limiting the line width makes it possible to have several files open side-by-side, and works well when using code review tools that present the two versions in adjacent columns."
},
"E502": {
"original_message": "the backslash is redundant between brackets",
"title": "There is no need for a backslash (\\) between brackets.",
"solution": "Remove any backslashes between brackets.",
"explanation": ""
},
"E701": {
"original_message": "multiple statements on one line (colon)",
"title": "This line contains multiple statements.",
"solution": "Make sure that each statement is on its own line.",
"explanation": "This improves readability."
},
"E702": {
"original_message": "multiple statements on one line (semicolon)",
"title": "This line contains multiple statements.",
"solution": "Make sure that each statement is on its own line.",
"explanation": "This improves readability."
},
"E703": {
"original_message": "statement ends with a semicolon",
"title": "This line ends in a semicolon (;).",
"solution": "Remove the semicolon from the end of the line.",
"explanation": ""
},
    # E704 ignored by default
"E704": {
"original_message": "multiple statements on one line (def)",
"title": "This line contains multiple statements.",
"solution": "Make sure multiple statements of a function definition are on their own separate lines.",
"explanation": ""
},
"E711": {
"original_message": "comparison to None should be ‘if cond is None:’",
"title": "Comparisons to objects such as True, False and None should use 'is' or 'is not' instead of '==' and '!='.",
"solution": "Replace != with 'is not' and '==' with 'is'.",
"explanation": ""
},
"E712": {
"original_message": "comparison to True should be ‘if cond is True:’ or ‘if cond:’",
"title": "Comparisons to objects such as True, False and None should use 'is' or 'is not' instead of '==' and '!='.",
"solution": "Replace != with 'is not' and '==' with 'is'.",
"explanation": ""
},
"E713": {
"original_message": "test for membership should be ‘not in’",
"title": "When testing whether or not something is in an object use the form `x not in the_object` instead of `not x in the_object`.",
"solution": "Use the form `not x in the_object` instead of `x not in the_object`.",
"explanation": "This improves readability."
},
"E714": {
"original_message": "test for object identity should be ‘is not’",
"title": "When testing for object identity use the form `x is not None` rather than `not x is None`.",
"solution": "Use the form `x is not None` rather than `not x is None`.",
"explanation": "This improves readability."
},
"E721": {
"original_message": "do not compare types, use ‘isinstance()’",
"title": "You should compare an objects type by using `isinstance()` instead of `==`. This is because `isinstance` can handle subclasses as well.",
"solution": "Use `if isinstance(user, User)` instead of `if type(user) == User`.",
"explanation": ""
},
"E722": {
"original_message": "do not use bare except, specify exception instead",
"title": "",
"solution": "",
"explanation": ""
},
"E731": {
"original_message": "do not assign a lambda expression, use a def",
"title": "This line assigns a lambda expression instead of defining it as a function using `def`.",
"solution": "",
"explanation": "The primary reason for this is debugging. Lambdas show as <lambda> in tracebacks, where functions will display the function’s name."
},
"E741": {
"original_message": "do not use variables named ‘l’, ‘O’, or ‘I’",
"title": "This line uses one of the variables named ‘l’, ‘O’, or ‘I’",
"solution": "Change the names of these variables to something more descriptive.",
"explanation": "Variables named I, O, and l can be very hard to read. This is because the letter I and the letter l are easily confused, and the letter O and the number 0 can be easily confused."
},
"E742": {
"original_message": "do not define classes named ‘l’, ‘O’, or ‘I’",
"title": "This line contains a class named ‘l’, ‘O’, or ‘I’",
"solution": "Change the names of these classes to something more descriptive.",
"explanation": "Classes named I, O, and l can be very hard to read. This is because the letter I and the letter l are easily confused, and the letter O and the number 0 can be easily confused."
},
"E743": {
"original_message": "do not define functions named ‘l’, ‘O’, or ‘I’",
"title": "This line contains a function named ‘l’, ‘O’, or ‘I’",
"solution": "Change the names of these functions to something more descriptive.",
"explanation": "Functions named I, O, and l can be very hard to read. This is because the letter I and the letter l are easily confused, and the letter O and the number 0 can be easily confused."
},
"W191": {
"original_message": "indentation contains tabs",
"title": "This line contains tabs when only spaces are expected.",
"solution": "Replace any tabs in your indentation with spaces.",
"explanation": ""
},
"W291": {
"original_message": "trailing whitespace",
"title": "This line contains whitespace after the final character.",
"solution": "Remove any extra whitespace at the end of each line.",
"explanation": ""
},
"W292": {
"original_message": "no newline at end of file",
"title": "Files should end with a newline.",
"solution": "Add a newline to the end of your file.",
"explanation": ""
},
"W293": {
"original_message": "blank line contains whitespace",
"title": "Blank lines should not contain any tabs or spaces.",
"solution": "Remove any whitespace from blank lines.",
"explanation": ""
},
"W391": {
"original_message": "blank line at end of file",
"title": "There are either zero, two, or more than two blank lines at the end of your file.",
"solution": "Ensure there is only one blank line at the end of your file.",
"explanation": ""
},
    # W503 ignored by default
    # This seems contradicitng... https://lintlyci.github.io/Flake8Rules/rules/W503.html
"W503": {
"original_message": "line break before binary operator",
"title": "",
"solution": "",
"explanation": ""
},
    # W504 ignored by default
    # same as above https://lintlyci.github.io/Flake8Rules/rules/W504.html
"W504": {
"original_message": "line break after binary operator",
"title": "",
"solution": "",
"explanation": ""
},
    # W505 ignored by default
"W505": {
"original_message": "doc line too long (82 > 79 characters)",
"title": "This line is longer than 79 characters.",
"solution": "You can insert a backslash character (\\) to wrap the text onto the next line.",
"explanation": ""
},
"W601": {
"original_message": ".has_key() is deprecated, use ‘in’",
"title": ".has_key() was deprecated in Python 2. It is recommended to use the in operator instead.",
"solution": "",
"explanation": ""
},
"W602": {
"original_message": "deprecated form of raising exception",
"title": "The raise Exception, message form of raising exceptions is no longer supported. Use the new form.",
"solution": "Instead of the form raise ErrorType, 'Error message' use the form raise ErrorType('Error message')",
"explanation": ""
},
"W603": {
"original_message": "‘<>’ is deprecated, use ‘!=’",
"title": "<> has been removed in Python 3.",
"solution": "Replace any occurences of <> with !=.",
"explanation": ""
},
"W604": {
"original_message": "backticks are deprecated, use ‘repr()’",
"title": "Backticks have been removed in Python 3.",
"solution": "Use the built-in function repr() instead.",
"explanation": ""
},
"W605": {
"original_message": "invalid escape sequence ‘x’",
"title": "",
"solution": "",
"explanation": ""
},
"W606": {
"original_message": "‘async’ and ‘await’ are reserved keywords starting with Python 3.7",
"title": "",
"solution": "",
"explanation": ""
},
"D100": {
"original_message": "Missing docstring in public module",
"title": "Modules should have docstrings.",
"solution": "Add a docstring to your module.",
"explanation": ""
},
"D101": {
"original_message": "Missing docstring in public class",
"title": "Classes should have docstrings.",
"solution": "Add a docstring to your class.",
"explanation": ""
},
"D102": {
"original_message": "Missing docstring in public method",
"title": "Methods should have docstrings.",
"solution": "Add a docstring to your method.",
"explanation": ""
},
"D103": {
"original_message": "Missing docstring in public function",
"title": "Functions should have docstrings.",
"solution": "Add a docstring to your function.",
"explanation": ""
},
"D104": {
"original_message": "Missing docstring in public package",
"title": "Packages should have docstrings.",
"solution": "Add a docstring to your package.",
"explanation": ""
},
"D105": {
"original_message": "Missing docstring in magic method",
"title": "Magic methods should have docstrings.",
"solution": "Add a docstring to your magic method.",
"explanation": ""
},
"D106": {
"original_message": "Missing docstring in public nested class",
"title": "Public nested classes should have docstrings.",
"solution": "Add a docstring to your public nested class.",
"explanation": ""
},
"D107": {
"original_message": "Missing docstring in __init__",
"title": "The __init__ method should have a docstring.",
"solution": "Add a docstring to your __init__ method.",
"explanation": ""
},
"D200": {
"original_message": "One-line docstring should fit on one line with quotes",
"title": "Docstrings that are one line long should fit on one line with quotes.",
"solution": "Put your docstring on one line with quotes.",
"explanation": ""
},
"D201": {
"original_message": "No blank lines allowed before function docstring",
"title": "Function docstrings should not have blank lines before them.",
"solution": "Remove any blank lines before your function docstring.",
"explanation": ""
},
"D202": {
"original_message": "No blank lines allowed after function docstring",
"title": "Function docstrings should not have blank lines after them.",
"solution": "Remove any blank lines after your function docstring.",
"explanation": ""
},
"D203": {
"original_message": "1 blank line required before class docstring",
"title": "Class docstrings should have 1 blank line before them.",
"solution": "Insert 1 blank line before your class docstring.",
"explanation": ""
},
"D204": {
"original_message": "1 blank line required after class docstring",
"title": "Class docstrings should have 1 blank line after them.",
"solution": "Insert 1 blank line after your class docstring.",
"explanation": ""
},
"D205": {
"original_message": "1 blank line required between summary line and description",
"title": "There should be 1 blank line between the summary line and the description.",
"solution": "Insert 1 blank line between the summary line and the description.",
"explanation": ""
},
"D206": {
"original_message": "Docstring should be indented with spaces, not tabs",
"title": "Docstrings should be indented using spaces, not tabs.",
"solution": "Make sure your docstrings are indented using spaces instead of tabs.",
"explanation": ""
},
"D207": {
"original_message": "Docstring is under-indented",
"title": "Docstring is under-indented.",
"solution": "Add indentation levels to your docstring until it is at the correct indentation level.",
"explanation": ""
},
"D208": {
"original_message": "Docstring is over-indented",
"title": "Docstring is over-indented.",
"solution": "Remove indentation levels from your docstring until it is at the correct indentation level.",
"explanation": ""
},
"D209": {
"original_message": "Multi-line docstring closing quotes should be on a separate line",
"title": "Docstrings that are longer than one line should have closing quotes on a separate line.",
"solution": "Put the closing quotes of your docstring on a separate line.",
"explanation": ""
},
"D210": {
"original_message": "No whitespaces allowed surrounding docstring text",
"title": "Text in docstrings should not be surrounded by whitespace.",
"solution": "Remove any whitespace from the start and end of your docstring.",
"explanation": ""
},
"D211": {
"original_message": "No blank lines allowed before class docstring",
"title": "Class docstrings should not have blank lines before them.",
"solution": "Remove any blank lines before your class docstring.",
"explanation": ""
},
"D212": {
"original_message": "Multi-line docstring summary should start at the first line",
"title": "Docstrings that are more than one line long should start at the first line.",
"solution": "Ensure your docstring starts on the first line with quotes.",
"explanation": ""
},
"D213": {
"original_message": "Multi-line docstring summary should start at the second line",
"title": "Docstrings that are more than one line long should start at the second line.",
"solution": "Ensure your docstring starts on the second line, which is the first line without quotes.",
"explanation": ""
},
"D214": {
"original_message": "Section is over-indented",
"title": "Section is indented by too many levels.",
"solution": "Remove indentation levels from this section until it is at the correct indentation level.",
"explanation": ""
},
"D215": {
"original_message": "Section underline is over-indented",
"title": "Section underline is indented by too many levels.",
"solution": "Remove indentation levels from this section underline until it is at the correct indentation level.",
"explanation": ""
},
"D300": {
"original_message": "Use “”“triple double quotes”“”",
"title": "Use “”“triple double quotes”“” around docstrings.",
"solution": "Use “”“triple double quotes”“” around your docstring.",
"explanation": ""
},
"D301": {
"original_message": "Use r”“” if any backslashes in a docstring",
"title": "Use r”“” if there are any backslashes in a docstring.",
"solution": "Use r”“” at the beginning of your docstring if it contains any backslashes.",
"explanation": ""
},
"D302": {
"original_message": "Use u”“” for Unicode docstrings",
"title": "Use u”“” for docstrings that contain Unicode.",
"solution": "Use u”“” at the beginning of your docstring if it contains any Unicode.",
"explanation": ""
},
"D400": {
"original_message": "First line should end with a period",
"title": "The first line in docstrings should end with a period.",
"solution": "Add a period to the end of the first line in your docstring.",
"explanation": ""
},
"D401": {
"original_message": "First line should be in imperative mood",
"title": "The first line in docstrings should read like a command.",
"solution": "Ensure the first line in your docstring reads like a command, not a description. For example 'Do this' instead of 'Does this', 'Return this' instead of 'Returns this'.",
"explanation": ""
},
"D402": {
"original_message": "First line should not be the function’s “signature”",
"title": "The first line in docstrings should not be the function’s “signature”.",
"solution": "Move the function’s “signature” to a different line or remove it completely.",
"explanation": ""
},
"D403": {
"original_message": "First line should not be the function’s “signature”",
"title": "The first line in docstrings should not be the function’s “signature”.",
"solution": "Move the function’s “signature” to a different line or remove it completely.",
"explanation": ""
},
"D404": {
"original_message": "First word of the docstring should not be 'This'",
"title": "First word of the docstring should not be 'This'.",
"solution": "Rephrase the docstring so that the first word is not 'This'.",
"explanation": ""
},
"D405": {
"original_message": "Section name should be properly capitalized",
"title": "Section name should be properly capitalised.",
"solution": "Capitalise the section name.",
"explanation": ""
},
"D406": {
"original_message": "Section name should end with a newline",
"title": "Section names should end with a newline.",
"solution": "Add a newline after the section name.",
"explanation": ""
},
"D407": {
"original_message": "Missing dashed underline after section",
"title": "Section names should have a dashed line underneath them.",
"solution": "Add a dashed line underneath the section name.",
"explanation": ""
},
"D408": {
"original_message": "Section underline should be in the line following the section’s name",
"title": "Dashed line should be on the line following the section's name.",
"solution": "Put the dashed underline on the line immediately following the section name.",
"explanation": ""
},
"D409": {
"original_message": "Section underline should match the length of its name",
"title": "Dashed section underline should match the length of the section's name.",
"solution": "Add or remove dashes from the dashed underline until it matches the length of the section name.",
"explanation": ""
},
"D410": {
"original_message": "Missing blank line after section",
"title": "Section should have a blank line after it.",
"solution": "Add a blank line after the section.",
"explanation": ""
},
"D411": {
"original_message": "Missing blank line before section",
"title": "Section should have a blank line before it.",
"solution": "Add a blank line before the section.",
"explanation": ""
},
"D412": {
"original_message": "No blank lines allowed between a section header and its content",
"title": "There should be no blank lines between a section header and its content.",
"solution": "Remove any blank lines that are between the section header and its content.",
"explanation": ""
},
"D413": {
"original_message": "Missing blank line after last section",
"title": "The last section in a docstring should have a blank line after it.",
"solution": "Add a blank line after the last section in your docstring.",
"explanation": ""
},
"D414": {
"original_message": "Section has no content",
"title": "Sections in docstrings must have content.",
"solution": "Add content to the section in your docstring.",
"explanation": ""
},
"D415": {
"original_message": "First line should end with a period, question mark, or exclamation point",
"title": "The first line in your docstring should end with a period, question mark, or exclamation point.",
"solution": "Add a period, question mark, or exclamation point to the end of the first line in your docstring.",
"explanation": ""
},
"D416": {
"original_message": "Section name should end with a colon",
"title": "Section names should end with a colon.",
"solution": "Add a colon to the end of your section name.",
"explanation": ""
},
"D417": {
"original_message": "Missing argument descriptions in the docstring",
"title": "Docstrings should include argument descriptions.",
"solution": "Add argument descriptions to your docstring.",
"explanation": ""
}
# TODO: Add http://www.pydocstyle.org/en/5.0.2/error_codes.html
# TODO: Add https://github.com/PyCQA/pep8-naming#plugin-for-flake8
# TODO: Add https://github.com/zheller/flake8-quotes#warnings
}

CHARACTER_DESCRIPTIONS = {
    '(': 'opening bracket',
    ')': 'closing bracket',
    '[': 'opening square bracket',
    ']': 'closing square bracket',
    '{': 'opening curly bracket',
    '}': 'closing curly bracket',
    "'": 'single quote',
    '"': 'double quote',
    ':': 'colon',
    ';': 'semicolon',
    ' ': 'space',
    ',': 'comma',
    '.': 'full stop',
}

def get_article(word):
    """Return English article for word.

    Returns 'an' if word starts with vowel. Technically
    it should check the word sound, compared to the
    letter but this shouldn't occur with our words.

    Args:
        word (str): Word to create article for.

    Returns:
        'a' or 'an' (str) depending if word starts with vowel.
    """
    if word[0].lower() in 'aeiou':
        return 'an'
    else:
        return 'a'
