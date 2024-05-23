import antlr4

def getTypeOf(_value : str):
    _type = ''
    try:
        int(_value)
        _type = 'int'
    except ValueError:
        try:
            float(_value)
            _type = 'float'
        except ValueError:
            if _value == 'True' or _value == 'False':
                _type = 'bool'
            else:
                _type = 'string'

    return [_type, _value]

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