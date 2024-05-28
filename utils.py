import subprocess
import antlr4

def bad_type() -> str:
    return 'bad_type'

def get_type_of_structure(value: str): # [[1,2,3],[4,5,6],[]] good,    [1,2,3],[4,5,6],[] bad
    bracketing = get_bracketing(value)
    if value[0] == '[':
        _type = 'vector'
    elif value[0] == '(':
        _type = 'set'
    elif value[0] == '{':
        _type = 'map'

    _basic_type = 'None'
    for v in bracketing:
        _vtype = get_type_of(v)[0]

        if _basic_type == 'None' and _vtype != 'None':
            _basic_type = _vtype
        elif _vtype != _basic_type and _vtype != 'None':
            return bad_type()

    if _basic_type == 'None':
        return 'None'
    
    return _type + '<' + _basic_type + '>'

def get_type_of(value: str):
    value = value.strip()
    if value in ('None', ''):
        return 'None'

    try:
        int(value)
        _type = 'int'
    except ValueError:
        try:
            float(value)
            _type = 'float'
        except ValueError:
            if value == 'True' or value == 'False':
                _type = 'bool'
            elif value[0] == '"' or value[0] == "'":
                _type = 'string'
            elif value[0] == '[' or value[0] == '(' or value[0] == '{':
                _type = get_type_of_structure(value)
            else:
                return 'None', value
            
    return _type, repair_value(value)

def repair_value(value: str):
    value = value.strip()
    if value[0] == '[' or value[0] == '(' or value[0] == '{':
        bracketing = get_bracketing(value)
        value = '{' + ','.join([repair_value(v) for v in bracketing]) + '}'
    elif value[0] != '"' and value[0] != "'":
        value = value.replace('None', 'null') 
        value = value.replace('True', 'true').replace('False', 'false')
    return value

def get_bracketing(value: str): # [[1,2,3],[4,5,6],[]] good,    [1,2,3],[4,5,6],[] bad
     value = value.strip()[1:-1] 
     result = []
     level = 0

     while value:
         for i in range(len(value)):
             if value[i] in ('[', '(', '{'):
                 level += 1
             elif value[i] in (']', ')', '}'):
                 level -= 1

             if level == 0 and value[i] == ',':
                 result.append(value[:i])
                 value = value[i+1:]
                 break
         else:
             result.append(value)
             value = ''

     return result

def print_tree(tree, parser):
    tree_str = tree.toStringTree(recog=parser)
    print(tree_str)
    formatted_tree = format_tree(tree_str)
    print("FORMATTED TREE:")
    print(formatted_tree)

def format_tree(tree_string):
    stack = []
    formatted_string = ''
    indent = 0
    i = 0
    while i < len(tree_string):
        if tree_string[i] == '(':
            stack.append('(')
            indent = len(stack)
            formatted_string += '\n' + '│   ' * (indent - 1) + '├── '
        elif tree_string[i] == ')':
            if stack:
                stack.pop()
            indent = len(stack)
            if i < len(tree_string) - 1 and tree_string[i+1] != ')':
                formatted_string += '\n' + '│   ' * indent
        elif tree_string[i] == '\\':
            if tree_string[i:i+2] == '\\n':
                formatted_string += '\\\\n'
                i += 1
            elif tree_string[i:i+5] == '<EOF>':
                formatted_string += '<EOF>'
                i += 4
        else:
            formatted_string += tree_string[i]
        i += 1
    return formatted_string

def format_cpp_code(code: str) -> str:
    # Write the C++ code to a temporary file
    with open('temp.cpp', 'w') as temp_file:
        temp_file.write(code)
    
    # Run clang-format on the temporary file
    result = subprocess.run(['clang-format', 'temp.cpp'], capture_output=True, text=True)
    
    # Read the formatted code from the temporary file
    formatted_code = result.stdout
    
    # Clean up the temporary file
    subprocess.run(['rm', 'temp.cpp'])  # Use `del` on Windows
    
    return formatted_code
