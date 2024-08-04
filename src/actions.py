import os
import shutil
from prompt import *

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
