from actions import *
from strings import *
from arguments import *
from addons import *
from dataclasses import dataclass, field
from typing import Iterable, Callable
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
            copy_file(file_from=os.path.join(prevfoldername, f"{self.name}.cpp"),
                      file_to=cpp_path,
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
            copy_file(file_from=os.path.join(prevfoldername, f"{self.name}.hpp"),
                      file_to=hpp_path,
                        default_content=content)
        else:
            create_file(hpp_path, content)

@dataclass
class Cls:
    name: str
    orthodox: bool=True
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
            copy_file(file_from=os.path.join(prevfoldername, f"{self.name}.hpp"),
                      file_to=hpp_path,
                        default_content=content)
        else:
            create_file(hpp_path, content)
        # cpp
        content = self.cpp_content()
        cpp_path = os.path.join(foldername, f"{self.name}.cpp")
        if self.to_copy:
            assert not prevfoldername is None
            copy_file(file_from=os.path.join(prevfoldername, f"{self.name}.cpp"),
                      file_to=cpp_path,
                        default_content=content)
        else:
            create_file(cpp_path, content)

@dataclass
class Exercise:
    foldername: str
    program_name: str='program'
    classes: Iterable[Cls] = field(default_factory=list)
    sources: Iterable[Cpp] = field(default_factory=list)
    headers: Iterable[Hpp] = field(default_factory=list)
    prevfoldername: str=None
    has_makefile: bool=True
    has_main: bool=True
    main_name: str='main.cpp'
    custom_actions: Iterable[Callable] = field(default_factory=list)

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
            content = makefile(self.program_name, self.get_sources(), self.get_headers())
            create_file(os.path.join(self.foldername, 'Makefile'), content)
        # main
        if self.has_main:
            content = main_cpp(self.get_headers())
            create_file(os.path.join(self.foldername, self.main_name), content)
        # end
        for action in self.custom_actions:
            action()
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
        'ex00': Exercise(foldername='ex00', program_name='megaphone', main_name='megaphone.cpp'),
        'ex01' : Exercise(foldername='ex01'),
        'ex02' : Exercise(foldername='ex02', headers=[Hpp('Account', content=cpp00_ex02_Account_hpp)], sources=[Cpp('Account', content=class_cpp('Account', orthodox=False))], has_main=False)
    },
    'cpp01': {
        'ex00': Exercise(foldername='ex00', classes=[Cls('Zombie', orthodox=False)], sources=[Cpp('newZombie', content=f'{include("Zombie.hpp")}\n'), Cpp('randomChump', content=f'{include("Zombie.hpp")}\n')]),
        'ex01': Exercise(foldername='ex01', prevfoldername='ex00', classes=[Cls('Zombie', orthodox=False, to_copy=True)], sources=[Cpp('zombieHorde', content=f'{include("Zombie.hpp")}\n')]),
        'ex02': Exercise(foldername='ex02'),
        'ex03': Exercise(foldername='ex03', classes=[Cls('Weapon', orthodox=False), Cls('zombieA', orthodox=False), Cls('zombieB', orthodox=False)]),
        'ex04': Exercise(foldername='ex04'),
        'ex05': Exercise(foldername='ex05', classes=[Cls('Harl', orthodox=False)]),
        'ex06': Exercise(foldername='ex06', program_name='harlFilter', prevfoldername='ex05', classes=[Cls('Harl', orthodox=False, to_copy=True)])
    },
    'cpp02': {
        'ex00': Exercise(foldername='ex00', classes=[Cls('Fixed')]),
        'ex01': Exercise(foldername='ex01', prevfoldername='ex00', classes=[Cls('Fixed', to_copy=True)]),
        'ex02': Exercise(foldername='ex02', prevfoldername='ex01', classes=[Cls('Fixed', to_copy=True)]),
        'ex03': Exercise(foldername='ex03', prevfoldername='ex02', classes=[Cls('Fixed', to_copy=True), Cls('Point')], sources=[Cpp('bsp')])
    },
    'cpp03': {
        'ex00': Exercise(foldername='ex00', classes=[Cls('ClapTrap')]),
        'ex01': Exercise(foldername='ex01', prevfoldername='ex00', classes=[Cls('ClapTrap', to_copy=True), Cls('ScavTrap')]),
        'ex02': Exercise(foldername='ex02', prevfoldername='ex01', classes=[Cls('ClapTrap', to_copy=True), Cls('ScavTrap', to_copy=True), Cls('FragTrap')]),
        'ex03': Exercise(foldername='ex03', prevfoldername='ex02', classes=[Cls('ClapTrap', to_copy=True), Cls('ScavTrap', to_copy=True), Cls('FragTrap', to_copy=True), Cls('DiamondTrap')])
    },
    'cpp04': {
        'ex00': Exercise(foldername='ex00', classes=[Cls('Animal'), Cls('Dog'), Cls('Cat')]),
        'ex01': Exercise(foldername='ex01', prevfoldername='ex00', classes=[Cls('Animal', to_copy=True), Cls('Dog', to_copy=True), Cls('Cat', to_copy=True), Cls('Brain')]),
        'ex02': Exercise(foldername='ex02', prevfoldername='ex01', classes=[Cls('Animal', to_copy=True), Cls('Dog', to_copy=True), Cls('Cat', to_copy=True), Cls('Brain', to_copy=True)]),
        'ex03': Exercise(foldername='ex03', classes=[Cls('AMateria'), Cls('Ice'), Cls('Cure'), Cls('ICharacter'), Cls('Character'), Cls('ImateriaSource'), Cls('MateriaSource')]) # TODO: check if AMateria.cpp & ICharacter.cpp & IMateriaSource.cpp are necessary
    },
    'cpp05': {
        'ex00': Exercise(foldername='ex00', classes=[Cls('Bureaucrat')]),
        'ex01': Exercise(foldername='ex01', prevfoldername='ex00', classes=[Cls('Bureaucrat', to_copy=True), Cls('Form')]),
        'ex02': Exercise(foldername='ex02', prevfoldername='ex01', classes=[Cls('Bureaucrat', to_copy=True), Cls('Form', to_copy=True), Cls('ShrubberyCreationForm'), Cls('RobotomyRequestForm'), Cls('PresidentialPardonForm')], custom_actions=[lambda: msg_warning("please rename Form to AForm in this exercise manually")]),
        'ex03': Exercise(foldername='ex03', prevfoldername='ex02', classes=[Cls('Bureaucrat', to_copy=True), Cls('Form', to_copy=True), Cls('ShrubberyCreationForm', to_copy=True), Cls('RobotomyRequestForm', to_copy=True), Cls('PresidentialPardonForm', to_copy=True), Cls('Intern')])
    }
}


if __name__ == '__main__':
    modules = {name: Module(name, exercises[name].values()) for name in exercises.keys()}

    if args.exercise == None:
        modules[args.module].generate()
    else:
        exercises[args.module][args.exercise].generate()
