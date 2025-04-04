# Randomisation in CodeWOF questions

CodeWOF has the ability to **save** macros to be substituted in at question generation, however as yet it does not make use of these. Macros are intended to be chosen by index to form combinations, e.g. all values with index 0 would be chosen.

## Storage
Macros are stored as `macros.yaml` in the `en/question_name/` directory of the question, with the following format:
`placeholder-0`:
    - `value-00`
    - `value-01`
`placeholder-1`:
    - `value-10`
    - `value-11`

## Selection
The intended functionality for macros is for index-based combinations. The above example gives two possible variations, with either `value-00` and `value-10` being chosen together or `value-01` and `value-11` being chosen together.

Currently, macros are not utilised by the CodeWOF system.