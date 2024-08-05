# python3 merge.py > generator.py

merge_order = ['strings', 'prompt', 'arguments', 'addons', 'actions', 'modules']

def line_includes_py_file(line: str) -> bool:
    if line.startswith('import') and line.split()[1] in merge_order:
        return True
    if line.startswith('from') and line.split()[1] in merge_order:
        return True
    return False

generator_text = ""
for module in merge_order:
    content = ''.join([line for line in open(f'src/{module}.py', 'r').readlines() if not line_includes_py_file(line)])
    generator_text += content

print(generator_text)
