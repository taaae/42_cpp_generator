from actions import *
from strings import *
from arguments import *
from dataclasses import dataclass
from typing import Iterable, Tuple
import os
from itertools import chain

@dataclass
class Exercise:
    program_name: str
    foldername: str
    classes: Iterable[Tuple[str, bool, bool]] # name, orthodox, to_copy
    sources: Iterable[Tuple[str, bool]] # name, to_copy
    headers: Iterable[Tuple[str, bool]] # name, to_copy
    prevfoldername: str=None
    has_makefile: bool=True
    has_main: bool=True

    def generate(self):
        msg(f'Generating {colorize(self.foldername, Color.PURPLE)}')
        # folder
        if not create_dir(self.foldername):
            msg('Ok, stopping')
            return
        # classes
        for name, orthodox, to_copy in self.classes:
            # header
            content = class_hpp(name, orthodox)
            hpp_path = os.path.join(self.foldername, f"{name}.hpp")
            if to_copy:
                assert not self.prev is None
                copy_file(file_from=hpp_path,
                            file_to=os.path.join(self.prevfoldername, f"{name}.hpp"),
                            default_content=content)
            else:
                create_file(hpp_path, content)
            # source
            content = class_cpp(name, orthodox)
            cpp_path = os.path.join(self.foldername, f"{name}.cpp")
            if to_copy:
                assert not self.prev is None
                copy_file(file_from=cpp_path,
                            file_to=os.path.join(self.prevfoldername, f"{name}.cpp"),
                            default_content=content)
            else:
                create_file(cpp_path, content)
        # sources
        for name, to_copy in self.sources:
            content = ""
            cpp_path = os.path.join(self.foldername, f"{name}.cpp")
            if to_copy:
                assert not self.prev is None
                copy_file(file_from=cpp_path,
                            file_to=os.path.join(self.prevfoldername, f"{name}.cpp"),
                            default_content=content)
            else:
                create_file(cpp_path, content)
        # headers
        for name, to_copy in self.headers:
            content = ""
            hpp_path = os.path.join(self.foldername, f"{name}.hpp")
            if to_copy:
                assert not self.prev is None
                copy_file(file_from=hpp_path,
                            file_to=os.path.join(self.prevfoldername, f"{name}.hpp"),
                            default_content=content)
            else:
                create_file(hpp_path, content)
        # makefile
        if self.has_makefile:
            content = makefile(self.program_name, self.get_sources())
            create_file(os.path.join(self.foldername, 'Makefile'), content)
        # main
        if self.has_main:
            content = main_cpp(self.get_headers())
            create_file(os.path.join(self.foldername, 'main.cpp'), content)
        # end
        msg(f'Finished generating {colorize(self.foldername, Color.PURPLE)}')

    def get_headers(self):
        return [f"{name}.hpp" for name in chain((c[0] for c in self.classes), [h[0] for h in self.headers])]
    def get_sources(self):
        return [f"{name}.cpp" for name in chain((c[0] for c in self.classes), [src[0] for src in self.sources])] + ['main.cpp'] * self.has_main

@dataclass
class Module:
    name: str
    exercises: Iterable[Exercise]

    def generate(self):
        msg(f'Generating {colorize(self.name, Color.PURPLE)}')
        for exercise in self.exercises:
            exercise.generate()
        msg(f'Finished generating {colorize(self.name, Color.PURPLE)}')

# ex00 = Exercise(program_name='program', foldername='folder', classes=[('Amazing', True, False), ('Notamazing', False, False)], sources=[('src', False)], headers=[('h', False)])
# Module('cpp00', [ex00]).generate()