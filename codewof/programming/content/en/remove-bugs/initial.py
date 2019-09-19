def remove_bugs(buggy_code):
    for i in range(len(buggy_code)):
        if buggy_code[i] != 'bug':
            debugged_code.append(buggy_code[i])
    return buggy_code
