import sys

def main(argv):
    input_code = ''''''
    with open(argv[1], 'r') as f:
        input_code = f.read()

    lines = input_code.split("\n")
    output_code = ""
    indent = 0
    for line in lines:
        line = line.strip()

        if line.startswith("}"):
            indent -= 1
        output_code += "\t" * indent + line + "\n"
        if line.endswith("{"):
            indent += 1

    with open(argv[1], "w") as f:
        f.write(output_code)
        f.close()

if __name__ == "__main__":
    main(sys.argv)