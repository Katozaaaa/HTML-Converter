import re

class PyConv():
    file = []
    new_file = []

    line = ''
    new_line = ''
    strings = []
    new_strings = []
    functions = []
    new_functions = []

    keywords_dict = {}

# checks the screening
# ________________________________________________________________________

def this_is_screening(itt_rev: int):
    slash_count = 0
    while PyConv.line[itt_rev] == "\\":
        itt_rev -= 1
        slash_count += 1
    return bool(slash_count % 2)

# find end of apostrophe or quotation string
# ________________________________________________________________________

def find_text(itt: int, apqu: str):
    itt_inner = itt + 1
    while True:
        if (PyConv.line[itt_inner] == apqu and PyConv.line[itt_inner-1] == "\\"):
            if not this_is_screening(itt_inner-1):
                break
        elif ((PyConv.line[itt_inner] == apqu and PyConv.line[itt_inner-1] != "\\") or itt_inner == len(PyConv.line)):
            break
        itt_inner += 1
    PyConv.strings.append(PyConv.line[itt:itt_inner+1])
    PyConv.new_line = PyConv.new_line.replace(PyConv.strings[len(PyConv.strings)-1], "_STRINGS_")
    return itt_inner

def python_converter(path_to_file: str, path_to_post: str):
    
    PyConv.file.clear()
    PyConv.new_file.clear()

    with open(path_to_file, "r", encoding="utf-8") as FILE:
        PyConv.file = FILE.read().splitlines()

    with open("python_keywords.txt", "r", encoding="utf-8") as FILE:
        keywords_list = FILE.read().splitlines()
        count_keywords = 0
        for keyword in keywords_list:
            PyConv.keywords_dict[count_keywords] = keyword
            count_keywords += 1

    PyConv.new_file.append('<div id="code-block">')
    PyConv.new_file.append('<table id="code-table">')

    line_num = 1
    for line_b in PyConv.file:
        PyConv.strings.clear()
        PyConv.new_strings.clear()

        PyConv.line = line_b
        PyConv.new_line = line_b

# find all comments
# ________________________________________________________________________
    
        comments = ""
        itt = 0
        while itt != len(PyConv.line):
            if (PyConv.line[itt] == "#"):
                PyConv.new_line = PyConv.new_line.replace(f"{PyConv.line[itt:len(PyConv.line)+1]}", '_COMMENTS_')
                comments = PyConv.line[itt:len(PyConv.line)+1]
                break
            itt += 1
            
# find all strings
# ________________________________________________________________________

        itt = 0
        while itt != len(PyConv.line):
            if (PyConv.line[itt] == "\'"): itt = find_text(itt, "\'")
            if (PyConv.line[itt] == "\""): itt = find_text(itt, "\"")
            itt += 1
        
# find and converts all keywords
# ________________________________________________________________________

        for keyword in PyConv.keywords_dict:
            keyword_pattern = rf'\b{PyConv.keywords_dict.get(keyword)}\b'
            PyConv.new_line = re.sub(keyword_pattern, f"_KEYWORD_{keyword}_", PyConv.new_line)

        for keyword in PyConv.keywords_dict:
            PyConv.new_line = PyConv.new_line.replace(f"_KEYWORD_{keyword}_", '<span class="keywords">' + PyConv.keywords_dict[keyword] + '</span>')

# find and converts all functions
# ________________________________________________________________________

        PyConv.functions = re.findall(r"[\d\w_]+\(", PyConv.new_line)
        for function in PyConv.functions:
            if function not in PyConv.new_functions:
                PyConv.new_functions.append(function)
        for function in PyConv.new_functions:
            PyConv.new_line = re.sub(rf"{function[0:len(function)-1]}\(", '<span class="functions">' + function[0:len(function)-1] + '</span>(', PyConv.new_line)
    
# converts all strings
# ________________________________________________________________________

        for string in PyConv.strings:
            PyConv.new_strings.append('<span class="strings">{string}</span>'.format(string=string))
        
        for new_string in PyConv.new_strings:
            PyConv.new_line = PyConv.new_line.replace("_STRINGS_", new_string, 1)

# converts all comments
# ________________________________________________________________________

        PyConv.new_line = PyConv.new_line.replace("_COMMENTS_", '<span class="comments">' + comments + '</span>')

# place the line into html tags
# ________________________________________________________________________

        PyConv.new_file.append('<tr>\n\t<td class="td-line-num">{line_num}</td>\n\t<td class="td-line">{line}</td>\n</tr>\n'.format(line_num=line_num, line=PyConv.new_line))
        line_num += 1

    PyConv.new_file.append('</table>')
    PyConv.new_file.append('</div>')

    with open(path_to_post, "w+", encoding="utf-8") as FILE:
        for line in PyConv.new_file:
            FILE.write(line)