import re

class CConv():
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
    while CConv.line[itt_rev] == "\\":
        itt_rev -= 1
        slash_count += 1
    return bool(slash_count % 2)

# find end of apostrophe or quotation string
# ________________________________________________________________________

def find_text(itt: int, apqu: str):
    itt_inner = itt + 1
    while True:
        if (CConv.line[itt_inner] == apqu and CConv.line[itt_inner-1] == "\\"):
            if not this_is_screening(itt_inner-1):
                break
        elif ((CConv.line[itt_inner] == apqu and CConv.line[itt_inner-1] != "\\") or itt_inner == len(CConv.line)):
            break
        itt_inner += 1
    CConv.strings.append(CConv.line[itt:itt_inner+1])
    CConv.new_line = CConv.new_line.replace(CConv.strings[len(CConv.strings)-1], "_STRINGS_")
    return itt_inner

def c_converter(path_to_file: str, path_to_post: str):

    CConv.file.clear()
    CConv.new_file.clear()

    with open(path_to_file, "r", encoding="utf-8") as FILE:
        CConv.file = FILE.read().splitlines()

    with open("c_keywords.txt", "r", encoding="utf-8") as FILE:
        keywords_list = FILE.read().splitlines()
        count_keywords = 0
        for keyword in keywords_list:
            CConv.keywords_dict[count_keywords] = keyword
            count_keywords += 1
    
    CConv.new_file.append('<div id="code-block">')
    CConv.new_file.append('<table id="code-table">')

    line_num = 1
    for line_b in CConv.file:
        CConv.strings.clear()
        CConv.new_strings.clear()

        CConv.line = line_b
        CConv.new_line = line_b

# find all comments
# ________________________________________________________________________
    
        comments = ""
        itt = 0
        while itt != len(CConv.line):
            if (CConv.line[itt] == "//"):
                CConv.new_line = CConv.new_line.replace(f"{CConv.line[itt:len(CConv.line)+1]}", '_COMMENTS_')
                comments = CConv.line[itt:len(CConv.line)+1]
                break
            itt += 1
            
# find all strings
# ________________________________________________________________________

        itt = 0
        while itt != len(CConv.line):
            if (CConv.line[itt] == "\'"): itt = find_text(itt, "\'")
            if (CConv.line[itt] == "\""): itt = find_text(itt, "\"")
            itt += 1
        
# find and converts all keywords
# ________________________________________________________________________

        for keyword in CConv.keywords_dict:
            keyword_pattern = rf'\b{CConv.keywords_dict.get(keyword)}\b'
            CConv.new_line = re.sub(keyword_pattern, f"_KEYWORD_{keyword}_", CConv.new_line)

        for keyword in CConv.keywords_dict:
            CConv.new_line = CConv.new_line.replace(f"_KEYWORD_{keyword}_", '<span class="keywords">' + CConv.keywords_dict[keyword] + '</span>')

# find and converts all functions
# ________________________________________________________________________

        CConv.functions = re.findall(r"[\d\w_]+\(", CConv.new_line)
        for function in CConv.functions:
            if function not in CConv.new_functions:
                CConv.new_functions.append(function)
        for function in CConv.new_functions:
            CConv.new_line = re.sub(rf"{function[0:len(function)-1]}\(", '<span class="functions">' + function[0:len(function)-1] + '</span>(', CConv.new_line)
    
# converts all strings
# ________________________________________________________________________

        for string in CConv.strings:
            CConv.new_strings.append('<span class="strings">{string}</span>'.format(string=string))
        
        for new_string in CConv.new_strings:
            CConv.new_line = CConv.new_line.replace("_STRINGS_", new_string, 1)

# converts all comments
# ________________________________________________________________________

        CConv.new_line = CConv.new_line.replace("_COMMENTS_", '<span class="comments">' + comments + '</span>')

# place the line into html tags
# ________________________________________________________________________

        CConv.new_file.append('<tr>\n\t<td class="td-line-num">{line_num}</td>\n\t<td class="td-line">{line}</td>\n</tr>\n'.format(line_num=line_num, line=CConv.new_line))
        line_num += 1

    CConv.new_file.append('</table>')
    CConv.new_file.append('</div>')

    with open(path_to_post, "w+", encoding="utf-8") as FILE:
        for line in CConv.new_file:
            FILE.write(line)