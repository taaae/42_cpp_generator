import argparse
from prompt import msg_warning

module_exercises = {
    'cpp00': 3,
    'cpp01': 7,
    'cpp02': 4,
    'cpp03': 4,
    'cpp04': 4,
    'cpp05': 4,
    'cpp06': 3,
    'cpp07': 3,
    'cpp08': 3,
    'cpp09': 3
}
module_exercises = {key: ['ex0' + str(i) for i in range(value)]for (key, value) in module_exercises.items()}

parser = argparse.ArgumentParser(description='Generate files for 42 cpp modules', epilog='Github repo: https://github.com/taaae/42_cpp_generator')
parser.add_argument('module', choices=['cpp00', 'cpp01', 'cpp02', 'cpp03', 'cpp04', 'cpp05', 'cpp06', 'cpp07', 'cpp08', 'cpp09'], metavar='cpp_module')
parser.add_argument('exercise', type=str, nargs='?')
args = parser.parse_args()
if args.exercise == None: # TODO: exclude modules that doesn't require copypasting
    msg_warning(f'Generating the whole {args.module} at once. Generate exercises one by one to avoid manual copypasting. Example: py {parser.prog} cpp02 ex00')
elif args.exercise not in module_exercises[args.module]:
    parser.error(f"argument exercise: invalid choice: '{args.exercise}' (choose from {module_exercises[args.module]})")

# TODO: add codestyle choice argument
