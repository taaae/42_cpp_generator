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
    return f"{name}::{name}() {{\n}}\n"

def copy_constructor_def(name: str) -> str:
    return f"{name}::{name}(const {name}& other) {{\n}}\n"

def copy_assignment_def(name: str) -> str:
    return f"{name}& {name}::operator=(const {name}& other) {{\n}}\n"

def desctructor_def(name: str) -> str:
    return f"{name}::~{name}() {{\n}}\n"

def class_decl(name: str, orthodox=True) -> str:
    if orthodox:
        return wrap_class(name, public() + default_constructor_decl(name) + copy_constructor_decl(name) 
                          + copy_assignment_decl(name) + desctructor_decl(name))
    else:
        return wrap_class(name, '')

def class_def(name: str) -> str:
    '''only for orthodox classes!'''
    return default_constructor_def(name) + copy_constructor_def(name)\
          + copy_assignment_def(name) + desctructor_def(name)

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

def makefile(name: str, sources: Iterable, headers: Iterable) -> str:
    return f'''NAME = {name}
CPPFLAGS = -Wall -Wextra -Werror -std=c++98
SRC = {' '.join(s for s in sources)}
INC = {' '.join(h for h in headers)}

all: $(NAME)

$(NAME): $(SRC) $(INC)
\tc++ $(CPPFLAGS) $(SRC) -o $(NAME)

clean:

fclean: clean
\trm -f $(NAME)

re: fclean all

.PHONY: all clean fclean re
'''
class Color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def colorize(msg: str, c: str) -> str:
    return c + msg + Color.END

def msg(msg: str):
    print(msg)

def msg_warning(msg: str):
    print(colorize('Warning: ', Color.YELLOW + Color.BOLD) + msg)

def msg_ask(msg: str, options: list, default: str) -> str:
    '''asks to choose from options and returns the choice, case insensitive'''
    cap_options = [option.upper() for option in options]
    if default not in options:
        raise ValueError('default should be one of the options')
    print(msg, '/'.join(f"[{colorize(option, Color.BOLD + Color.BLUE)}]" if option.upper() == default.upper() else colorize(option, Color.BLUE) for option in options))
    while True:
        choice = input().strip().upper()
        if choice == '':
            return default
        if choice in cap_options:
            return options[cap_options.index(choice)]
import argparse

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
cpp00_ex02_Account_hpp = '''// ************************************************************************** //
//                                                                            //
//                Account.hpp for GlobalBanksters United                //
//                Created on  : Thu Nov 20 19:43:15 1989                      //
//                Last update : Wed Jan 04 14:54:06 1992                      //
//                Made by : Brad "Buddy" McLane <bm@gbu.com>                  //
//                                                                            //
// ************************************************************************** //


#pragma once
#ifndef __ACCOUNT_H__
#define __ACCOUNT_H__

// ************************************************************************** //
//                               Account Class                                //
// ************************************************************************** //

class Account {


public:

	typedef Account		t;

	static int	getNbAccounts( void );
	static int	getTotalAmount( void );
	static int	getNbDeposits( void );
	static int	getNbWithdrawals( void );
	static void	displayAccountsInfos( void );

	Account( int initial_deposit );
	~Account( void );

	void	makeDeposit( int deposit );
	bool	makeWithdrawal( int withdrawal );
	int		checkAmount( void ) const;
	void	displayStatus( void ) const;


private:

	static int	_nbAccounts;
	static int	_totalAmount;
	static int	_totalNbDeposits;
	static int	_totalNbWithdrawals;

	static void	_displayTimestamp( void );

	int				_accountIndex;
	int				_amount;
	int				_nbDeposits;
	int				_nbWithdrawals;

	Account( void );

};



// ************************************************************************** //
// vim: set ts=4 sw=4 tw=80 noexpandtab:                                      //
// -*- indent-tabs-mode:t;                                                   -*-
// -*- mode: c++-mode;                                                       -*-
// -*- fill-column: 75; comment-column: 75;                                  -*-
// ************************************************************************** //


#endif /* __ACCOUNT_H__ */
'''

cpp00_ex02_tests_cpp = '''// ************************************************************************** //
//                                                                            //
//                tests.cpp for GlobalBanksters United                        //
//                Created on  : Thu Nov 20 23:45:02 1989                      //
//                Last update : Wed Jan 04 09:23:52 1992                      //
//                Made by : Brad "Buddy" McLane <bm@gbu.com>                  //
//                                                                            //
// ************************************************************************** //

#include <vector>
#include <algorithm>
#include <functional>
#include "Account.hpp"


int		main( void ) {

	typedef std::vector<Account::t>							  accounts_t;
	typedef std::vector<int>								  ints_t;
	typedef std::pair<accounts_t::iterator, ints_t::iterator> acc_int_t;

	int	const				amounts[]	= { 42, 54, 957, 432, 1234, 0, 754, 16576 };
	size_t const			amounts_size( sizeof(amounts) / sizeof(int) );
	accounts_t				accounts( amounts, amounts + amounts_size );
	accounts_t::iterator	acc_begin	= accounts.begin();
	accounts_t::iterator	acc_end		= accounts.end();

	int	const			d[]			= { 5, 765, 564, 2, 87, 23, 9, 20 };
	size_t const		d_size( sizeof(d) / sizeof(int) );
	ints_t				deposits( d, d + d_size );
	ints_t::iterator	dep_begin	= deposits.begin();
	ints_t::iterator	dep_end		= deposits.end();

	int	const			w[]			= { 321, 34, 657, 4, 76, 275, 657, 7654 };
	size_t const		w_size( sizeof(w) / sizeof(int) );
	ints_t				withdrawals( w, w + w_size );
	ints_t::iterator	wit_begin	= withdrawals.begin();
	ints_t::iterator	wit_end		= withdrawals.end();

	Account::displayAccountsInfos();
	std::for_each( acc_begin, acc_end, std::mem_fun_ref( &Account::displayStatus ) );

	for ( acc_int_t it( acc_begin, dep_begin );
		  it.first != acc_end && it.second != dep_end;
		  ++(it.first), ++(it.second) ) {

		(*(it.first)).makeDeposit( *(it.second) );
	}

	Account::displayAccountsInfos();
	std::for_each( acc_begin, acc_end, std::mem_fun_ref( &Account::displayStatus ) );

	for ( acc_int_t it( acc_begin, wit_begin );
		  it.first != acc_end && it.second != wit_end;
		  ++(it.first), ++(it.second) ) {

		(*(it.first)).makeWithdrawal( *(it.second) );
	}

	Account::displayAccountsInfos();
	std::for_each( acc_begin, acc_end, std::mem_fun_ref( &Account::displayStatus ) );

	return 0;
}


// ************************************************************************** //
// vim: set ts=4 sw=4 tw=80 noexpandtab:                                      //
// -*- indent-tabs-mode:t;                                                   -*-
// -*- mode: c++-mode;                                                       -*-
// -*- fill-column: 75; comment-column: 75;                                  -*-
// ************************************************************************** //
'''
import os
import shutil

def create_dir(dirname: str) -> bool:
    '''returns if the dir was created/overriden'''
    try:
        os.mkdir(dirname)
    except FileExistsError:
        choice = msg_ask(f'Directory {colorize(dirname, Color.BLUE)} already exists. Empty it?',
                        options=['yes', 'no'], default='no')
        if choice == 'no':
            return False
        assert choice == 'yes'
        shutil.rmtree(dirname)
        os.mkdir(dirname)
        msg(f'Cleared directory {colorize(dirname, Color.BLUE)}')
    else:
        msg(f'Created directory {colorize(dirname, Color.BLUE)}')
    return True

def create_file(file: str, content: str):
    '''Created file, asks to override if file exists'''
    if os.path.exists(file):
        choice = msg_ask(f'File {colorize(file, Color.BLUE)} already exists. Override it?', ['yes', 'no'], 'no')
        if choice == 'no':
            msg(f"Kept {colorize(file, Color.BLUE)} as it is")
            return
        assert choice == 'yes'
    open(file, 'w').write(content)
    msg(f"Created {colorize(file, Color.BLUE)}")

def copy_file(file_from: str, file_to: str, default_content: str):
    '''Copies file, creates a default one if source doesn't exist, asks to override if destination exists'''
    if not os.path.exists(file_from):
        msg_warning(f'Could not locate {colorize(file_from, Color.BLUE)}, creating default {colorize(file_to, Color.BLUE)}')
        create_file(file_to, default_content)
        return
    if os.path.exists(file_to):
        choice = msg_ask(f'File {colorize(file_to, Color.BLUE)} already exists. Override it?', ['yes', 'no'], 'no')
        if choice == 'no':
            msg(f"Kept {colorize(file_to, Color.BLUE)} as it is")
            return
        assert choice == 'yes'
        os.remove(file_to)
    shutil.copyfile(file_from, file_to)
    msg(f"Copied {colorize(file_from, Color.BLUE)} to {colorize(file_to, Color.BLUE)}")
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
        'ex02': Exercise(foldername='ex02', prevfoldername='ex01', classes=[Cls('Bureaucrat', to_copy=True), Cls('Form', to_copy=True), Cls('ShrubberyCreationForm'), Cls('RobotomyRequestForm'), Cls('PresidentialPardonForm')], custom_actions=[lambda: msg_warning("please rename Form to AForm in this exercise manually")]), # TODO: maybe latter rename it automatically
        'ex03': Exercise(foldername='ex03', prevfoldername='ex02', classes=[Cls('Bureaucrat', to_copy=True), Cls('AForm', to_copy=True), Cls('ShrubberyCreationForm', to_copy=True), Cls('RobotomyRequestForm', to_copy=True), Cls('PresidentialPardonForm', to_copy=True), Cls('Intern')])
    },
    'cpp06': {
        'ex00': Exercise(program_name='convert', foldername='ex00', classes=[Cls('ScalarConverter', orthodox=False)]),
        'ex01': Exercise(foldername='ex01', classes=[Cls('Serializer', orthodox=False)], headers=[Hpp('Data', content=wrap_header_guards('DATA', ''))]),
        'ex02': Exercise(foldername='ex02', classes=[Cls('Base', orthodox=False)], headers=[Hpp('A', content=class_hpp('A', orthodox=False)),
                                                                                            Hpp('B', content=class_hpp('B', orthodox=False)),
                                                                                            Hpp('C', content=class_hpp('C', orthodox=False))])
    },
    'cpp07': {
        'ex00': Exercise(foldername='ex00', headers=[Hpp('whatever', content=wrap_header_guards('whatever', ''))]),
        'ex01': Exercise(foldername='ex01', headers=[Hpp('Iter', content=wrap_header_guards('Iter', ''))]),
        'ex02': Exercise(foldername='ex02', headers=[Hpp('Array', content=class_hpp('Array'))])
    }
}


if __name__ == '__main__':
    modules = {name: Module(name, exercises[name].values()) for name in exercises.keys()}

    if args.exercise == None:
        modules[args.module].generate()
    else:
        exercises[args.module][args.exercise].generate()

