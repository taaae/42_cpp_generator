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
