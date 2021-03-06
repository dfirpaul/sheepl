

# #######################################################################
#
#  Task : RemoteDesktop Interaction
#
# #######################################################################


"""
 Creates the autoIT stub code to be passed into the master compile

 Takes a supplied text file for the Sheepl to type
 the master script will already define the typing speed as part of the master declarations

    ##############################################
        Add in Task Specific Notes Here
    ##############################################

 General Notes:
    The textwrap import is used to keep the AutoIT functions indented in code
    as this messes with the python code (back off OCD) when it's manually 
    appearing to hang outside of the class declarations and also stops code collapse in IDEs.
    So when creating code specific to the AutoIT functions just use tabs to indent insitu
    and the textwarp library will strip all leading tabs from the beginning of the AutoIT block.
    Also uses textwrap.indent() to add indentation to 'Send' commands in text_typing_block()

 Conventions:
    Use 'AutoIT' in code comments and class names and 'autoIT' when using as part of variable names

 Modes:
    Interactive Mode
        This uses the task module assign task requirements
        Add additional CMD functions using do_<argument>
        Once all the arguments are complete
        build the do_complete function out by passing the arguments
        as keywords to the staticmethod of the task object
        <TaskName>.create_autoIT_block(self.csh, 
                                        # add in other arguments
                                        # for object constructor
                                        # ---------------------> 
                                        parm1=self.parm1_value,
                                        parm2=self.parm3_value
                                        # ---------------------> 
                                        )
    Non-Interactive Profile
        This takes an input from the sheepl object
        and this creates a Profile() object. See profile.py
"""


__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"

import cmd
import sys
import random
import textwrap

from utils.base.base_cmd_class import BaseCMD
from utils.base.base_cmd_class import SubTaskCMD


# #######################################################################
#  Task CMD Class Module Loaded into Main Sheepl Console
# #######################################################################


class TaskConsole(BaseCMD):

    """
    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : complete_task()       > completes the task and resets trackers
        : check_task_started    > checks to see task status
        : self.subtask_supported = False
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(TaskConsole, self).__init__(csh, cl)


        # Override the defined task name
        self.taskname = 'RemoteDesktop'

        # check to see whether creating subtasks
        if csh.creating_subtasks:
            print(cl.blue("creating subtasks >>>>>>>>"))

        # Overrides Base Class Prompt Setup 
        self.baseprompt = cl.yellow('{} >: remotedesktop :> '.format(csh.name.lower()))
        self.prompt = self.baseprompt

        # creating my own 
        self.introduction = """
        ----------------------------------
        [!] RemoteDesktop Interaction.
        Type help or ? to list commands.
        ----------------------------------
        1: Start a new block using 'new'
        2: Assign subtasks using 'subtask'
        3: Complete the interaction using 'complete'
        """
        print(textwrap.dedent(self.introduction))

        # ----------------------------------- >
        #      Task Specific Variables
        # ----------------------------------- >

        # List to hold commands for current interaction for subtask
        self.task_func_names = []
        self.task_func_output = []

        # Tracker for credential assignment
        self.assigned_credentials = False

        # Configures Subtasking
        self.subtask_supported = True         


    # --------------------------------------------------->
    #   Task CMD Functions
    # --------------------------------------------------->


    def do_new(self, arg):
        """ 
        This command creates a new Word document
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        # Inverse check to see if task has already started
        # Booleans are set in parent method

        # method from parent class BaseCMD
        if self.check_task_started() == False:
            print("[!] Starting : 'RemoteDesktop_{}'".format(str(self.csh.counter.current())))
            # OCD Line break
            print()
            self.prompt = self.cl.blue("[*] RemoteDesktop_{}".format(str(self.csh.counter.current()))) + "\n" + self.baseprompt       


    def do_credentials(self, arg):
            """
            Enter the computer name
            """
            if self.taskstarted == False:
                print(self.cl.red("[!] <ERROR> You need to start a new RemoteDesktop Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
            
            else:
                if not self.assigned_credentials:
                    self.credential_input()
                else:
                    answer = self.ask_yes_no_question("[?] Overwrite stored credentials? {} {} :> ".format(
                                                        (self.cl.green("<yes>")), 
                                                        (self.cl.red("<no>"))
                                                        )
                                                    )

                    if answer == True:
                        self.credential_input()
                
                    print("[!] RemoteDesktop Details" )
                    print("[*] The target IP address is :   {}".format(self.cl.green(self.computer)))
                    print("[*] The Username is set to :     {}".format(self.cl.green(self.username)))
                    print("[*] The Pasword is set to :      {}".format(self.cl.green(self.password)))


    def credential_input(self):
            """
            Small Helper Function to request and store the credentials
            sets the assigned_credential Boolean switch to True
            """
            computer = input("[>] Enter the target IP address : ")
            self.computer = computer
            username = input("[>] Enter the username to connect : ")
            self.username = username
            password = input("[>] Enter the connection password : ")
            self.password = password
            self.assigned_credentials = True


    def do_show_credentials(self, arg):
        """
        Shows the currently configured credentials for a session
        """ 
        if self.assigned_credentials:
            print("[!] The following Remote Desktop configuration is in place")
            if self.computer:
                print("[*] The target IP address is :   {}".format(self.cl.green(self.computer)))
            else:
                print("[*] The target IP address is :   {}".format(self.cl.green("None")))
            if self.username:
                print("[*] The Username is set to :     {}".format(self.cl.green(self.username)))
            else:
                print("[*] The Username is set to :     {}".format(self.cl.green("None")))
            if self.password:
                print("[*] The Pasword is set to :      {}".format(self.cl.green(self.password)))
            else:
                print("[*] The Pasword is set to :      {}".format(self.cl.green("None")))
        else:
            print(self.cl.red("[!] There are currently no credentials assigned"))


    def do_assigned(self, arg):
        """ 
        Get the current list of assigned CMD commands
        """
        print(self.cl.green("[?] Currently Assigned Commands "))
        for command in self.csh.subtasks.keys():
            print("[>] {}".format(command))
 

    def do_complete(self, arg):
        """

        This command calls the constructor on the AutoITBlock
        with all the specific arguments
        >> Check the AutoIT constructor requirements

        setup create_internetexplorer for ease and clarity
        pass in unique contructor arguments for AutoITBlock

        """
        if self.assigned_credentials:
            # Call the static method in the task object
            RemoteDesktop.create_autoIT_block(self.csh, 
                                # add in other arguments
                                # for object constructor
                                # ---------------------> 
                                computer=self.computer,
                                username=self.username,
                                password=self.password,
                                subtasks=(self.csh.subtasks.items())
                                    # --------------------->
                                # ---------------------> 
                                )

            # now reset the tracking values and prompt
            self.complete_task()

        else:
            print(self.cl.red("[!] You need to assign credentials in order to complete this task"))



    # --------------------------------------------------->
    #   CMD Util Functions
    # --------------------------------------------------->


# #######################################################################
#  RemoteDesktop Class Definition
# #######################################################################


class RemoteDesktop:

    def __init__(self, csh, cl, **kwargs):
        """
        Initial object setup
        """
        self.__dict__.update(kwargs)
        
        self.csh = csh
        self.commands = []
        
        if csh.interactive == True:
            # create the task based sub console
            self.TaskConsole = TaskConsole(csh, cl)
            self.TaskConsole.cmdloop()               


    # --------------------------------------------------->
    #   End RemoteDesktop Constructor
    # --------------------------------------------------->


    # --------------------------------------------------->
    #   RemoteDesktop Static Method
    # --------------------------------------------------->

    """
    These are all the elements that get passed into the 
    @static method as keyword arguments
    Essentially, this is everything that needs to be passed
    to create the InternetExplorer object

    Parse the 'kwargs' dictionary for the arguments
    """

    @staticmethod
    def create_autoIT_block(csh, **kwargs):
        """
        Creates the AutoIT Script Block
        Note :
            Kwargs returns a dictionary
            do these values can be referenced
            by the keys directly

        This now creates an instance of the object with the correct
        counter tracker, and then appends as a task
        Note : add in additional constructor arguments as highlighted
            which get passed in from the 'kwargs' dictionary

        """

        csh.add_task('RemoteDesktop_' + str(csh.counter.current()),
                                RemoteDesktopAutoITBlock(
                                str(csh.counter.current()),
                                csh,
                                # add in other arguments
                                # for object constructor
                                # ---------------------> 
                                kwargs["computer"],
                                kwargs["username"],
                                kwargs["password"]
                                #kwargs["commands"]
                                #kwargs["task_name"],
                                #kwargs["task_output"]
                                # ---------------------> 
                                ).create()
                            )

    # --------------------------------------------------->
    #   End RemoteDesktop Static Method
    # --------------------------------------------------->


# #######################################################################
#  RemoteDesktop AutoIT Block Definition
# #######################################################################


class RemoteDesktopAutoITBlock(object):
    """
    Creates an AutoIT Code Block based on the current counter
    then returns this to Task Console which pushes this upto the Sheepl Object
    with a call to create.
    String returns are pushed through (textwarp.dedent) to strip off indent tabs

    Build out your constructor based on what the object takes
    """

    def __init__(self, counter, csh, computer, username, password):

        self.counter        = counter
        self.indent_space   = '    '
        self.csh            = csh
        self.computer       = computer
        self.username       = username
        self.password       = password
        #self.subtasks       = subtasks

        # for task_name, task_output in commands.items():
        #     print(task_name, task_output)
        #print(subtasks)


    def func_dec(self):
        """
        Initial Entrypoint Definition for AutoIT function
        when using textwrap.dedent you need to add in the backslash
        to the start of the multiline
        """

        function_declaration = """
        ; < --------------------------------------- >
        ;         RemoteDesktop Interaction        
        ; < --------------------------------------- >

        RemoteDesktop_{}()

        """.format(self.counter)

        return textwrap.dedent(function_declaration)


    def open_remotedesktop(self):
        """
        Creates the AutoIT Function Declaration Entry
        """

        """
        # Note a weird bug that the enter needs to be 
        # passed as format string argument as escaping
        # is ignored on a multiline for some reason
        # if it gets sent as an individual line as in text_typing_block()
        # >> typing_text += "Send('exit{ENTER}')"
        # everything works. Strange, Invoke-OCD, and then stop caring
        # and push it through the format string.

        # Note > Send('yourprogram{ENTER}')
        # Example : Send('powershell{ENTER}')
        """

        _open_remotedesktop = """

        Func RemoteDesktop_{}()

            ; Creates a RemoteDesktop Interaction

            Send("#r")
            ; Wait 10 seconds for the Run dialogue window to appear.
            WinWaitActive("Run", "", 10)
            ; note this needs to be escaped
            ; <PROGRAM EXECUTION>
            Send("mstsc{}")
            WinWaitActive("Remote Destop Connection", "", 10)
            ;SendKeepActive("[CLASS:OpusApp]") get the name of this class
            ; Send ALT 'o' to open the RDP options
            Send("!o")
            Sleep(2000)
            ;Send ALT 'c' to focus to computer
            Send("!c")
            Sleep(2000)

            ; Send RDP Connection Informaiton
            Send("{}{}")
            Sleep(2000)
            Send("{}{}")
            Sleep(2000)
            Send("{}{}")
            Sleep(2000)
            Send("!y")

            ; pins the RDP connection as focus
            WinWaitActive("[CLASS:TscShellContainerClass]")
            SendKeepActive("[CLASS:TscShellContainerClass]")

            ; sends key strokes to RDP session to focus Windows key
            Send("{}{}")

        """.format(self.counter, "{ENTER}",
                    self.computer, "{TAB}",
                    self.username, "{ENTER}",
                    self.password, "{ENTER}",
                    "{ALT}", "{HOME}"
        )

        return textwrap.dedent(_open_remotedesktop)   


    def text_typing_block(self):
        """
        Takes the Typing Text Input
        The bulk of Remote Desktop interactions
        are via subtasks 
        """
        typing_text = ''

        #for key, value in self.commands:
        for key in self.csh.subtasks.items():
            #print("The key is >> {}".format(key))
        
            typing_text += ("\n; ############################################\n")
            typing_text += ("; [!] Assigned Subtask Interaction >> " + str(key) + '\n')
            typing_text += (str(key) + "()" + '\n')
            typing_text += "; [>] Assigned subtask function\n"

        # for command in self.commands:
        #     # these are individual send commands so don't need to be wrapped in a block
        #     typing_text += 'Send("' + command + '{ENTER}")'
        #     command_delay = str(random.randint(2000, 20000))
        #     typing_text += 'sleep(" + command_delay + ")'

        # for task_name, task_output in self.commands.items():
        #     print(task_name, task_output)

        # # add in exit
        # typing_text += 'Send("exit{ENTER}")'
        # typing_text += "\n; Reset Focus"
        # typing_text += '\nSendKeepActive("")'


        return textwrap.indent(typing_text, self.indent_space * 2)


    def close_RemoteDesktop(self):
        """
        Closes the RemoteDesktop application function declaration
        """

        end_func = """

            Send("{CAPSLOCK}")
            ; Need a short sleep here for focus to restore properly.
	        Sleep(150)
            Send("{CAPSLOCK}")
            WinClose("[CLASS:TscShellContainerClass]")
            Sleep(50)
            ; probably need a check for the popup window based on visible text
            ControlClick("Remote Desktop Connection", "", "[Class:Button;Instance:1]")
            SendKeepActive("")

        EndFunc

        """

        return textwrap.dedent(end_func)


    def append_subtasks(self):
        """
        This gets all the subtasks values and get's appended to the returned text
        but outside of the main function declaration
        """

        typing_text = ''

        for key, value in self.csh.subtasks.items():
            #print("The key is >> {}".format(key))
        
            typing_text += ("\n; ############################################\n")
            typing_text += ("; [!] Assigned Subtask Interaction >> " + str(key) + '\n')
            typing_text += ("; [!] Parent : RemoteDesktop \n")

            typing_text += "\n; [>] Assigned subtask function\n"
            typing_text += str(value)
        
        return textwrap.dedent(typing_text)


    def create(self):
        """ 
        Grabs all the output from the respective functions and builds the AutoIT output
        """

        # Add in the constructor calls

        autoIT_script = (self.func_dec() +
                        self.open_remotedesktop() +
                        self.text_typing_block() +
                        self.close_RemoteDesktop() +
                        self.append_subtasks()
                        )

        # reset the subtasks option ready for next one
        self.csh.subtasks = {}

        # call completion on the task
        #self.csh.

        return autoIT_script

