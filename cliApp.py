
'''
    A small Helper Class for building menu based CLI apps

'''
import os
from platform import system
from colorama import init, Fore, Back, Style

init()

class CommandlineApp:

    DEFAULT_MENU = { # Default Menu template since we want to use default args for other things
            'items':[],
            'text':[],
            'gaps':1,
            'print_':False
    }

    def __init__(self, windowTitle="", autoWipeAfter=0) -> None:
        
        self.TITLE_TRAY = [] # To keep lines making up our title
        self.SECTION_TRAY = [] # To store lines making up our section
        self.BUFFER_TRAY = [] # To store menus and other prints right after sections
        self.DELAYED_PRINTS = [] # To store prints that will be printed out whenever self.refresh will be called
        self.BUFFER = '' # This is the final buffer that gets printed with all the different items on it

        self.MENUS = {} # Key value pair to manage menus with their identifier
        self.AUTO_WIPE_COUNT = autoWipeAfter # Auto wipe count to manage after how many times we have to automatically wipe the extra prints
        self.WIPE_COUNT = 0

        self.refresh() # method that will build output in self.BUFFER and print it out
        if windowTitle != "":
            if system() == "Windows":
                os.system(f'title {windowTitle}')
            else:
                pass

    def __del__(self):
        self.__clear()

    def execute(self, command):
        os.system(command)

    def __clear_static(self):
        self.TITLE_TRAY = []

    def __clear_section(self):
        self.SECTION_TRAY = []
    
    def __clear_buffer(self):
        self.BUFFER_TRAY = []

    def __out(self):
        self.BUFFER = ''.join(self.TITLE_TRAY) + ''.join(self.SECTION_TRAY) + ''.join(self.BUFFER_TRAY)
        print(self.BUFFER)
        for eachDelayedPrint in self.DELAYED_PRINTS:
            print(eachDelayedPrint)

    def __display(self, output):
        self.__clear()
        self.BUFFER = ''.join(self.TITLE_TRAY) + output
        print(self.BUFFER)

    def __print_b(self, *args):
        for e in args: 
            if isinstance(e, str): self.BUFFER_TRAY.append(f"{e}\n")

    def __clear(self):
        if system() == "Windows":
            os.system('cls')
        else:
            os.system('clear')

    def Input(self, message, Fore='', Back=''):
        value = input(f"{Fore}{Back} {message} {Style.RESET_ALL}")
        return value
       
    def safeOutput(self, *args, padding=False):
        '''
            This puts printable objects, variables in a DELAY_PRINT list
            and these get printed out whenever all other printing is finished
        '''
        for e in args:
            if padding: 
                if isinstance(e, str): e = " " + e # Any safeOutput that is a string add a padding to the left if noPadding is True
            self.DELAYED_PRINTS.append(e)
    
    def clearOutput(self, callBack=None, *args):
        # If some callback function was passed it should get executed here
        if callable(callBack): 
            if len(args) == 0: callBack()
            else: return callBack(args)
        self.DELAYED_PRINTS = []

    def dialog(self, message, options=('1', '2')):
        def displayDialog():
            self.__clear()
            dialogText = ''.join(self.TITLE_TRAY) + f"{Fore.YELLOW}{message}{Style.RESET_ALL}" + "\n" + f"{Fore.LIGHTGREEN_EX}[{options[0]}]{Style.RESET_ALL} --- {Fore.LIGHTRED_EX}[{options[1]}]{Style.RESET_ALL}"
            print(dialogText)
        while True:
            displayDialog()
            value = self.Input("?")
            if value == options[0]:
                break
            elif value == options[1]:
                break
            else: pass
        return value
    
    def form(self, mandatory=[], optional=[]):
        '''
            mandatory=[("Name", str, "Identifier or help")]
                                ^ Type
        '''     
        values = {}
        if mandatory != []:
            for each in mandatory:
                while True:
                    self.refresh()
                    inputValue = input(f"Please enter value for {each[0]} {each[2]} [Mandatory] :: ")
                    if isinstance(inputValue, each[1]):
                        if inputValue != "":
                            values[each[0]] = inputValue
                            break
            if optional != []:
                for each in optional:
                    inputValue = input(f"Please enter value for {each[0]} {each[2]} [Optional] :: ")
                    if isinstance(inputValue, each[1]):
                        try:
                            values[each[0]] = inputValue
                        except Exception:
                            values[each[0]] = inputValue
                    else:
                        values[each[0]] = None
        return values
        
    
    def fileExplorer(self, label="", text=[], extension="txt"):
        path = os.getcwd()
        target_file_path:str = ""
        def go_back(path_):
            if path_ == os.getcwd():
                return path_
            else:
                #self.safeOutput(path_, "".join(path_.split('/')[:-1]))
                return "/".join(path_.split('/')[:-1])
        def go_forward(path_, directory):
            if os.path.isdir((path_ + "/" +  directory)):
                return path_ + "/" + directory
        def is_dir(path_, directory):
            return os.path.isdir((path_ + "/" +  directory))
        def is_file(path_, file_):
            return os.path.isfile((path_ + "/" +  file_))
        while True:
            items_menu = []
            items = []
            for i, eachFileDir in enumerate(os.listdir(path)):
                if is_dir(path, eachFileDir) != True:
                    items_menu.append((str(i+1), "FILE  " + eachFileDir))
                    items.append(eachFileDir)
                else:
                    items_menu.append((str(i+1), "*DIR   " + eachFileDir))
                    items.append(eachFileDir)
            items_menu.append(("x", "Exit"))
            items_menu.append(("<", "Back"))
            self.section(["■ File Explorer ■\n", f"Selected File {target_file_path} allowed extension {extension}"], gaps=1, Fore_=Fore.LIGHTYELLOW_EX)
            choice = self.menu(items=items_menu, text=text)
            #self.safeOutput(choice)
            if choice == 'x':
                break
            elif choice == "<":
                path = go_back(path)
            else:
                selected = items[(int(choice)-1)]
                if is_dir(path, selected):
                    path = go_forward(path, selected)
                elif is_file(path, selected):
                    #self.safeOutput((path + "\\" + selected))
                    target_file_path = path + "\\" + selected
                    if target_file_path.endswith(extension): break
                    else: target_file_path = ""
        return target_file_path

    def refresh(self):
        if self.AUTO_WIPE_COUNT != 0:
            if self.WIPE_COUNT == self.AUTO_WIPE_COUNT: self.clearOutput(); self.WIPE_COUNT = 0 # After use presses 10 or 20 times without any input on a menu remove the previous output of a table or text
            self.WIPE_COUNT = self.WIPE_COUNT + 1
        self.__clear()
        self.__out() # Refresh and restore everything from our buffer

    def section(self, text:list, gaps=1, print_=False, Fore_=None, Back_=None):
        '''
            On different menus section information could be also displayed
            This method works the same way but it shows section information
            right below the title
        '''
        if Fore_ == None: Fore_ = Fore.WHITE
        if Back_ == None: Back_ = Back.BLACK

        self.__clear_section()
        for e in text: 
            if isinstance(e, str):
                gaps_ = ''.join(['\n' for each in range(0, gaps)])
                self.SECTION_TRAY.append(f"{Fore_}{Back_}{e}{gaps_}{Style.RESET_ALL}")
                if print_: print(f"{e}{gaps_}")

    def title(self, text:list, gaps=1, print_=False):
        '''
            This will set the title of the applicaton that will appear throughout the application
            unless this method is called and the title is changed then new title will appear
        '''
        self.__clear_static()
        for e in text: 
            if isinstance(e, str):
                gaps_ = ''.join(['\n' for each in range(0, gaps)])
                self.TITLE_TRAY.append(f"{e}{gaps_}")
                if print_: print(f"{e}{gaps_}")

    def showMenu(self, menu_identifer):
        '''
            This method allows us to call and pre-defined menus with an indentifier
        '''
        menu = self.MENUS[menu_identifer]

        '''
            Callbacks are rarely used with menus but very useful so flexibility is given
            whether or not they will be included with the menu defination the program will
            work
        '''
        try:
            on_load_callbacks = menu['on_load']
        except KeyError:
            on_load_callbacks = []

        try:
            on_exit_callbacks = menu['on_exit']
        except KeyError:
            on_exit_callbacks = []

        return self.menu(menu['items'], menu['text'], menu['gaps'], menu['print_'], on_load=on_load_callbacks, on_exit=on_exit_callbacks)

    
    def display(self, callback_or_str_or_list, *args):
        '''
            It will display the results of return from a callback with just title
            and no menu the user will be brought back to menu after pressing any
            key
        '''
        if callable(callback_or_str_or_list): 
            if len(args) != 0: self.__display(callback_or_str_or_list(args))
            else: self.__display(callback_or_str_or_list())
        if isinstance(callback_or_str_or_list, str):
            self.__display(callback_or_str_or_list + "\n\n")
        else:
            self.__display(str(callback_or_str_or_list) + "\n\n")
        
        input(f"{Fore.YELLOW}... Press any key to continue ...{Style.RESET_ALL}")
    
    
    def menu(self, items:list, text=[], gaps=1, print_=False, on_load=[], on_exit=[]):

        '''
            Provide menu items as tuples inside a list
            Gaps will allow you to set the gap between the title
            and sections below, print_ will immediately print items
            but it is not recommended, as they get printed whenever
            self.refresh is called
        '''

        for eachCallBack in on_load:
            if callable(eachCallBack): eachCallBack()

        self.__print_b(f"\n")
        for e in text: 
            if isinstance(e, str):
                gaps_ = ''.join(['\n' for each in range(0, gaps)])
                self.__print_b(f"{e}{gaps_}")
                if print_: print(f"{e}{gaps_}")

        validChoices = []
        for eachIndex, eachMenuItem in items:
            self.__print_b(f'{Fore.LIGHTGREEN_EX} ● [{eachIndex}]- {eachMenuItem} {Style.RESET_ALL}')
            if eachIndex != "": validChoices.append(eachIndex)
        while True:
            self.refresh()
            inputValue = input(f"{Fore.YELLOW} Please select :: ? {Style.RESET_ALL}")
            if inputValue in validChoices:
                break
            else:
                inputValue = None
        self.__clear_buffer()

        for eachCallBack in on_exit:
            if callable(eachCallBack): eachCallBack()
        return inputValue