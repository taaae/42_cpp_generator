from config import *
import os
from typing import Iterable
import shutil

# class Action:
#   def execute() -> executes everything from list of Actions
class Module:
    def __init__(self, exercises: Iterable):
        self.execrises = exercises
    def execute(self):
        for exercise in self.exercises:
            exercise.execute()

gl_current_folder = '.'

class Exercise:
    def __init__(self, foldername: str, actions: Iterable):
        self.foldername = foldername
        self.actions = actions
    def execute(self):
        global gl_current_folder
        try:
            os.mkdir(self.foldername)
        except FileExistsError:
            print(f'Folder {self.foldername} already exists, aborting')
            return
        gl_current_folder = self.foldername
        for action in self.actions:
            action.execute()
        gl_current_folder = '.'

# strings

def pragma() -> str:
    return "#pragma once\n"

def include(header: str) -> str:
    return f'#include "{header}"\n'

def public() -> str:
    return "public:\n"

def def_constructor_decl(name: str) -> str:
    return f"{name}();\n"

def copy_constructor_decl(name: str) -> str:
    return f"{name}(const {name}& other);\n"

def copy_assignment_decl(name: str) -> str:
    return f"{name}& operator=(const {name}& other);\n"

def desctructor_decl(name: str) -> str:
    return f"~{name}();\n"

def decl_to_definition(decl) -> str:
    def wrapper(name: str) -> str:
        if 'operator' in decl(name):
            return decl(name).replace('operator', f"{name}::operator", 1).removesuffix(';\n') + " {\n\n}\n"
        return f"{name}::" + decl(name).removesuffix(';\n') + " {\n\n}\n"
    return wrapper

def_constructor_def = decl_to_definition(def_constructor_decl)
copy_constructor_def = decl_to_definition(copy_constructor_decl)
copy_assignment_def = decl_to_definition(copy_assignment_decl)
desctructor_def = decl_to_definition(desctructor_decl)

# string wrappers

def wrap_indentation(code: str) -> str:
    indent_line = lambda line: line if line == '\n' \
                    else ' ' + line if line in ['public:\n', 'private:\n', 'protected:\n'] \
                    else '  ' + line
    return ''.join(indent_line(line) for line in code.splitlines(keepends=True))

def wrap_class(classname: str, code: str) -> str:
    return f"class {classname} {{\n" + wrap_indentation(code) + '};\n'

def wrap_function(functionname: str, code: str) -> str:
    return functionname + '() {\n' + wrap_indentation(code) + '}\n'

# templates

def class_decl(name: str, orthodox=True) -> str:
    if orthodox:
        return wrap_class(name, public() + def_constructor_decl(name) + copy_constructor_decl(name) 
                          + copy_assignment_decl(name) + desctructor_decl(name))
    else:
        return wrap_class(name, '')

def class_def(name: str) -> str:
    '''only for orthodox classes!'''
    return def_constructor_def(name) + copy_constructor_def(name)\
          + copy_assignment_def(name) + desctructor_def(name)

def class_hpp(name: str, orthodox=True) -> str:
    return pragma() + '\n' + class_decl(name, orthodox)

def class_cpp(name: str, orthodox=True) -> str:
    if orthodox:
        return include(f"{name}.hpp") + '\n' + class_def(name)
    else:
        return include(f"{name}.hpp")

def main_text(headers: Iterable) -> str:
    return ''.join(include(h) for h in headers) + '\n' + wrap_function('int main', '')

def makefile_text(name: str, sources: Iterable) -> str:
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

# module -> exercises
# exercise -> create folder + files
# files -> classes, makefile, main
# copying files
# printing some output

class ClassFiles:
    def __init__(self, classname: str, orthodox=True):
        self.classname = classname
        self.orthodox = orthodox
    def execute(self):
        global gl_current_folder
        with open(f'{gl_current_folder}/{self.classname}.cpp', 'w') as cpp:
            cpp.write(class_cpp(self.classname, self.orthodox))
        with open(f'{gl_current_folder}/{self.classname}.hpp', 'w') as hpp:
            hpp.write(class_hpp(self.classname, self.orthodox))

class MakeFile:
    def __init__(self, name: str, sources: Iterable):
        self.name = name
        self.sources = sources
    def execute(self):
        global gl_current_folder
        with open(f'{gl_current_folder}/Makefile', 'w') as makefile:
            makefile.write(makefile_text(self.name, self.sources))

class MainCpp:
    def __init__(self, headers: Iterable):
        self.headers = headers
    def execute(self):
        global gl_current_folder
        with open(f'{gl_current_folder}/main.cpp', 'w') as main:
            main.write(main_text(self.headers))
class CopyPaste:
    def __init__(self, cp_from: str, cp_to: str):
        self.cp_from = cp_from
        self.cp_to = cp_to
    def execute(self):
        shutil.copy(self.cp_from, self.cp_to)

# ClassFiles('MyClass', 'temp', True).execute()
# MakeFile('program', ('MyClass.cpp', 'main.cpp'), 'temp').execute()
# MainCpp(('MyClass.hpp',), 'temp').execute()
# CopyPaste('temp_from/a.cpp', 'temp/a.cpp').execute()
Exercise('temp', [
    ClassFiles('MyClass', True),
    MakeFile('program', ['MyClass.cpp', 'main.cpp']),
    MainCpp(['MyClass.hpp']),
    CopyPaste('temp_from/a.cpp', 'temp/a.cpp')
    ]).execute()
