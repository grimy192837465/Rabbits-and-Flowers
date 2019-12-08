"""
##################################################
PRNE Network Automation Integrated script
Created by: Lewis, Daiva, Adam, Myles and Daryl")
##################################################


Main Script for Program.
Contains user interface and calls other scripts as required



######################
WHEN CODE IS COMPLETED
######################

-Add import to your own individual task
-Change "funcName" in VALID_OPTS below to your function in individual script

###################################################
DELETE THIS COMMENT WHEN YOU PASTE INTO YOUR REPORT
###################################################

"""

from Telnet_to_Switch import demo_telnet_session
from SSH_Connect import demo_ssh_session
from Backup_Switch_Configs import backup_switch_configs
from Compare_Run_Start import compare_run_start
from Compare_Run_with_Local_File import compare_run_with_local_file
from Performance_Parameters import update_performance_metrics

# For Daryl
# from Configure_Loopback import configure_loopback

# For Adam
# from eigrp_test import eigrp_configuration


import getpass
from socket import inet_aton

VALID_OPTS = {
    "1.1": ["Unsecure Remote Connection", demo_telnet_session],
    "1.2": ["Secure Remote Connection", demo_ssh_session],
    "1.3": ["Backup Multiple Switch Configurations", backup_switch_configs],
    "2.1": ["Compare Running Configuration with Startup Configuration", compare_run_start],
    "2.2": ["Compare Running Configuration with Local File", compare_run_with_local_file],
    "3": ["Performance Parameters", update_performance_metrics],
    "4": ["Individual Task", "funcName"],
    "5": ["Individual Task", "eigrp_configuration"]

}

# For Daryl
# "4": ["Individual Task", configure_loopback]


def caller(func, *args, **kwargs):
    """
    Calls other functions
    :param func: Must be a function name with NO brackets '()' eg. caller(print, x, ...)
    :param args: All arguments to be passed to func
    :param kwargs: All named arguments to be passed to func eg "secret="
    :return: Whatever the function returns
    """
    if type(func) == str and func == "funcName":
        print("No function defined for option given")
    else:
        try:
            return func(*args, **kwargs)
        except TypeError:
            print("Cannot call this function!")
            return None
        except NameError:
            print("Cannot find function with this name!")
            return None


def display_options():
    global VALID_OPTS
    print("\n################################################\n!OPTIONS NEED REVISION!\n")
    for i in VALID_OPTS.keys():
        print(f"{i}: {VALID_OPTS[i][0]}")
    print("\n################################################\n")


def get_enable_pass():
    while True:
        enable_pass = getpass.getpass("Enter enable secret: ")
        if enable_pass != getpass.getpass("Confirm enable secret: "):
            print("Mismatch detected!")
            continue
        else:
            return enable_pass


def get_address():
    while True:
        address = input("Input IP Address for network device: ")
        try:
            inet_aton(address)
            return address
        except OSError:
            print("Invalid address entered:")
            continue


def yes_or_no(prompt=""):
    while True:
        decision = str(input(f"{prompt} [Y/n]: "))
        if decision[0].lower() == "y" or decision == "":
            return True
        elif decision[0].lower() == "n":
            return False
        else:
            print("Invalid input. Please try again")
            continue


def main():
    global VALID_OPTS
    """
    Main function for program
    This will show a menu that will create

    :return int: status code
    """

    # Print welcome msg
    print("################################################")
    print("PRNE Network Automation Integrated script v1.0")
    print("Created by: Lewis, Daiva, Adam, Myles and Daryl")
    print("###############################################\n")

    # Gets enable secret if its needed
    needs_en_secret = yes_or_no(prompt="Will you need an enable secret for this session?")
    enable_pass = get_enable_pass() if needs_en_secret else ""
    del needs_en_secret

    # Get SSH account info
    username = input("Input username for remote connection: ")
    while True:
        password = getpass.getpass("Input password for remote connection: ")
        if password != getpass.getpass("Confirming password: "):
            print("Passwords don't match!")
            continue
        else:
            break

    display_options()

    # Loop until a valid option is found or keyboard interrupt caught
    while True:
        try:
            option = input("Choose your option: ")
            if option not in VALID_OPTS.keys():
                print("Invalid option chosen")
                continue
            else:
                break
        except KeyboardInterrupt:
            print("\n\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print("Keyboard interrupt caught, exiting program")
            break

    # Run script specified by option


    return 0


# If this script was called directly (eg. from command-line or IDLE) and not by another script, run main() function
if __name__ == '__main__':
    if main() != 0:
        print("Program exit code signifies error during execution")

