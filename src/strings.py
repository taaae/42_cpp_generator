from typing import Iterable

def wrap_header_guards(header: str, content: str) -> str:
    '''header with no extension'''
    header = f'{header.upper()}_HPP'
    return f'''#ifndef {header}
#define {header}

{content}
#endif //{header}\n'''

def wrap_indentation(code: str) -> str:
    indent_line = lambda line: line if line == '\n' \
                    else f' {line}' if line in ['public:\n', 'private:\n', 'protected:\n'] \
                    else f'  {line}'
    return ''.join(indent_line(line) for line in code.splitlines(keepends=True))

def wrap_class(classname: str, code: str) -> str:
    return f"class {classname} {{\n{wrap_indentation(code)}}};\n"

def wrap_function(functionname: str, code: str) -> str:
    return functionname + f'() {{\n{wrap_indentation(code)}}}\n'

def include(header: str) -> str:
    return f'#include "{header}"\n'

def public() -> str:
    return "public:\n"

def protected() -> str:
    return "protected:\n"

def private() -> str:
    return "private:\n"

def default_constructor_decl(name: str) -> str:
    return f"{name}();\n"

def copy_constructor_decl(name: str) -> str:
    return f"{name}(const {name}& other);\n"

def copy_assignment_decl(name: str) -> str:
    return f"{name}& operator=(const {name}& other);\n"

def desctructor_decl(name: str) -> str:
    return f"~{name}();\n"

def default_constructor_def(name: str) -> str:
    return f"{name}::{name}() {{\n\n}}\n"

def copy_constructor_def(name: str) -> str:
    return f"{name}::{name}(const {name}& other) {{\n\n}}\n"

def copy_assignment_def(name: str) -> str:
    return f"{name}& {name}::operator=(const {name}& other) {{\n\n}}\n"

def desctructor_def(name: str) -> str:
    return f"{name}::~{name}() {{\n\n}}\n"

def class_decl(name: str, orthodox=True) -> str:
    if orthodox:
        return wrap_class(name, public() + default_constructor_decl(name) + copy_constructor_decl(name) 
                          + copy_assignment_decl(name) + desctructor_decl(name))
    else:
        return wrap_class(name, '')

def class_def(name: str) -> str:
    '''only for orthodox classes!'''
    return default_constructor_def(name) + '\n' + copy_constructor_def(name)\
          + '\n' + copy_assignment_def(name) + '\n' + desctructor_def(name)

# vvv use only those vvv

def class_hpp(name: str, orthodox=True) -> str:
    return wrap_header_guards(name, class_decl(name, orthodox))

def class_cpp(name: str, orthodox=True) -> str:
    if orthodox:
        return include(f"{name}.hpp") + '\n' + class_def(name)
    else:
        return include(f"{name}.hpp")

def main_cpp(headers: Iterable) -> str:
    return ''.join(include(h) for h in headers) + '\n' + wrap_function('int main', '')

def makefile(name: str, sources: Iterable) -> str:
    return f'''NAME = {name}
CPPFLAGS = -Wall -Wextra -Werror -std=c++98
SRC = {' '.join(s for s in sources)}

all: $(SRC)
\tc++ $(CPPFLAGS) $(SRC) -o $(NAME)

clean:

fclean: clean
\trm -f $(NAME)

re: fclean all

.PHONY: all clean fclean re
'''
