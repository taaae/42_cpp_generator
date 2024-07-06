from actions import *
from strings import *
from arguments import *
from dataclasses import dataclass, field
from typing import Iterable, Tuple
import os
import itertools

@dataclass
class Cpp:
    name: str
    to_copy: bool=False
    content: str=""
    def generate(self, foldername: str, prevfoldername: str):
        content = self.content
        cpp_path = os.path.join(foldername, f"{self.name}.cpp")
        if self.to_copy:
            assert not prevfoldername is None
            copy_file(file_from=cpp_path,
                        file_to=os.path.join(self.prevfoldername, f"{self.name}.cpp"),
                        default_content=content)
        else:
            create_file(cpp_path, content)

@dataclass
class Hpp:
    name: str
    to_copy: bool=False
    content: str=""
    def generate(self, foldername: str, prevfoldername: str):
        content = self.content
        hpp_path = os.path.join(foldername, f"{self.name}.hpp")
        if self.to_copy:
            assert not prevfoldername is None
            copy_file(file_from=hpp_path,
                        file_to=os.path.join(self.prevfoldername, f"{self.name}.hpp"),
                        default_content=content)
        else:
            create_file(hpp_path, content)

@dataclass
class Cls:
    name: str
    orthodox: bool=False
    to_copy: bool=False
    
    def hpp_content(self) -> str:
        return class_hpp(self.name, self.orthodox)
    def cpp_content(self) -> str:
        return class_cpp(self.name, self.orthodox)
    def generate(self, foldername: str, prevfoldername: str):
        # header
        content = self.hpp_content()
        hpp_path = os.path.join(foldername, f"{self.name}.hpp")
        if self.to_copy:
            assert not prevfoldername is None
            copy_file(file_from=hpp_path,
                        file_to=os.path.join(self.prevfoldername, f"{self.name}.hpp"),
                        default_content=content)
        else:
            create_file(hpp_path, content)
        # cpp
        content = self.cpp_content()
        cpp_path = os.path.join(foldername, f"{self.name}.cpp")
        if self.to_copy:
            assert not prevfoldername is None
            copy_file(file_from=cpp_path,
                        file_to=os.path.join(self.prevfoldername, f"{self.name}.cpp"),
                        default_content=content)
        else:
            create_file(cpp_path, content)

@dataclass
class Exercise:
    foldername: str
    program_name: str='program'
    classes: Iterable[Cls] = field(default_factory=list) # name, orthodox, to_copy
    sources: Iterable[Cpp] = field(default_factory=list) # name, to_copy
    headers: Iterable[Hpp] = field(default_factory=list) # name, to_copy
    prevfoldername: str=None
    has_makefile: bool=True
    has_main: bool=True
    main_name: str='main.cpp'

    def generate(self):
        # start
        msg(f'Generating {colorize(self.foldername, Color.PURPLE)}')
        # folder
        if not create_dir(self.foldername):
            msg('Ok, stopping')
            return
        # classes, sources, headers
        for file in itertools.chain(self.classes, self.sources, self.headers):
            file.generate(self.foldername, self.prevfoldername)
        # makefile
        if self.has_makefile:
            content = makefile(self.program_name, self.get_sources())
            create_file(os.path.join(self.foldername, 'Makefile'), content)
        # main
        if self.has_main:
            content = main_cpp(self.get_headers())
            create_file(os.path.join(self.foldername, self.main_name), content)
        # end
        msg(f'Finished generating {colorize(self.foldername, Color.PURPLE)}')

    def get_headers(self):
        return [f"{name}.hpp" for name in (f.name for f in itertools.chain(self.classes, self.headers))]
    def get_sources(self):
        return [f"{name}.cpp" for name in (f.name for f in itertools.chain(self.classes, self.sources))] + [self.main_name] * self.has_main

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

exercises = {
    'cpp00': {
        'ex00': Exercise(program_name='megaphone', foldername='ex00', main_name='megaphone.cpp'),
        'ex01' : Exercise(foldername='ex01'),
        'ex02' : Exercise(foldername='ex02', classes=[Cls('Account')], main_name='tests.cpp')
    } # TODO: ex02 requires to put custom text in tests.cpp and Account.cpp
}

Module('cpp01', exercises['cpp00'].values()).generate()
