from config import *
import os

# class Action:
#   def execute() -> executes everything from list of Actions

class Module:
    def __init__(self, exercises: tuple):
        self.execrises = exercises
    def execute(self):
        for exercise in self.exercises:
            exercise.execute()

class Exercise:
    def __init__(self, foldername: str, actions: tuple):
        self.foldername = foldername
        self.actions = actions
    def execute(self):
        try:
            os.mkdir(self.foldername)
        except FileExistsError:
            print(f'Folder {self.foldername} already exists, aborting')
            return
        for action in self.actions:
            action.execute()

# strings

def pragma() -> str:
    return "#pragma once\n"

def include(header: str) -> str:
    return f"#include <{header}>\n"

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
            return decl(name).replace('operator', f"{name}::operator", 1).removesuffix(';\n') + f"{DEFINITION_INDENTATION}{{\n\n}}\n"
        return f"{name}::" + decl(name).removesuffix(';\n') + f"{DEFINITION_INDENTATION}{{\n\n}}\n"
    return wrapper

def_constructor_def = decl_to_definition(def_constructor_decl)
copy_constructor_def = decl_to_definition(copy_constructor_decl)
copy_assignment_def = decl_to_definition(copy_assignment_decl)
desctructor_def = decl_to_definition(desctructor_decl)

# string wrappers

def wrap_indentation(code: str) -> str:
    indent_line = lambda line: line if line == '\n' \
                    else PUBLIC_INDENTATION + line if line in ['public:\n', 'private:\n', 'protected:\n'] \
                    else INDENTATION + line
    return ''.join(indent_line(line) for line in code.splitlines(keepends=True))

def wrap_class(code: str, classname: str) -> str:
    return f"class {classname} {{\n" + wrap_indentation(code) + '};\n'

# templates

def class_decl(name: str, orthodox=True) -> str:
    if orthodox:
        return wrap_class(public() + def_constructor_decl(name) + copy_constructor_decl(name) 
                          + copy_assignment_decl(name) + desctructor_decl(name), name)
    else:
        return wrap_class('', name)

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

# module -> exercises
# exercise -> create folder + files
# files -> classes, makefile, main
# copying files
# printing some output

class ClassFiles:
    def __init__(self, classname: str, folder: str, orthodox=True):
        self.classname = classname
        self.folder = folder
        self.orthodox = orthodox
    def execute(self):
        with open(f'{self.folder}/{self.classname}.cpp', 'w') as cpp:
            cpp.write(class_cpp(self.classname, self.orthodox))
        with open(f'{self.folder}/{self.classname}.hpp', 'w') as hpp:
            hpp.write(class_hpp(self.classname, self.orthodox))
