import os
from typing import Iterable
import shutil
from dataclasses import dataclass

# TODO: make sure it's not cheating to generate all the declarations
# and also maybe it's not cheating to generate delcaration from subjects (like Zombie* newZombie( std::string name );)

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
            print(f'Created folder {self.foldername}') # TODO: better print
        except FileExistsError:
            pass
        gl_current_folder = self.foldername
        for action in self.actions:
            action.execute()
        gl_current_folder = '.'

# strings

# TODO: use standart header guards instead (google codestyle)
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

# TODO: this is ugly
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
        # TODO: add check that file already exists (and ask if you want to override it)
        with open(f'{gl_current_folder}/{self.classname}.cpp', 'w') as cpp:
            cpp.write(class_cpp(self.classname, self.orthodox))
        with open(f'{gl_current_folder}/{self.classname}.hpp', 'w') as hpp:
            hpp.write(class_hpp(self.classname, self.orthodox))

class MakeFile:
    # TODO: maybe make makefile automatically collect all the sources
    # So it should 'know' about Exercise class
    def __init__(self, name: str, sources: Iterable):
        self.name = name
        self.sources = sources
    def execute(self):
        global gl_current_folder
        # TODO: add check that file already exists (and ask if you want to override it)
        with open(f'{gl_current_folder}/Makefile', 'w') as makefile:
            makefile.write(makefile_text(self.name, self.sources))

class MainCpp:
    # TODO: make main know about all the headers
    def __init__(self, headers: Iterable):
        self.headers = headers
    def execute(self):
        # TODO: add check that file already exists (and ask if you want to override it)
        global gl_current_folder
        with open(f'{gl_current_folder}/main.cpp', 'w') as main:
            main.write(main_text(self.headers))
class CopyPaste:
    def __init__(self, cp_from: str, cp_to: str):
        self.cp_from = cp_from
        self.cp_to = cp_to
    def execute(self):
        # TODO: add check that file already exists (and ask if you want to override it)
        # TODO: add check that file cp_from exists
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

Cpp01_Ex00 = Exercise('ex00', [
    MakeFile('program', ['main.cpp', 'Zombie.cpp', 'newZombie.cpp', 'randomChump.cpp']),
    MainCpp(['Zombie.hpp']),
    ClassFiles('Zombie', False)])

# Seems like I need more general methods to generate files
# Maybe action that creates a file with content string inside
# Strings should concatenate (includes, pragmas, functions (with class wrappers))
# Also Exercise class should pass itself in its Actions (so that Makefile, main.cpp knows about .h, .cpp files)
# Better structure: class Exercise has fields like Classes, .hpp, .cpp

# Don't add copy flag, just make it generate file by default and write a warning message if not avaliable

# Exercise:
# files: name, copy_from, type: [class_header/source(orthdodox), main, makefile, source]

# Cpp01_Ex01 = Exercise('ex01', [File(')])

# Features:
# Generating Files
# Generating Makefile
# Generating includes, header_guards
# Generating class declarations
# Generating class orthodox functions declarations
# Generating other function declarations

# strings
# files (cpp/hpp/make)

# maybe exercise should generate files itself
# Exercise
# foldername: str -> creates a folder (and also adds this prefix to all sources/headers etc)
# sources: list[file(name, cp_from, code)] -> code just holds info about itself, generation in Exercise
# headers: list[file(name, cp_from, code)]
# makefile: bool (to generate/not) -> generates it useing sources
# main: bool (to generate/not)

# better: files with type in it

@dataclass
class Exercise:
    foldername: str
    classes: Iterable
    sources: Iterable
    headers: Iterable
    has_makefile: bool=True
    has_main: bool=True

    def generate(self):
        pass
    def get_headers(self):
        pass
    def get_sources(self):
        pass

# Need to pass text function somehow

# idk I might just write some crappy working code at the end (don't want to waste too much time)

class Feedback:
    # bunch of functions
    def created_folder():
        pass
    def should_continue():
        pass
    # smth like this
