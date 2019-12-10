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
import getpass
from socket import inet_aton
from Telnet_to_Switch import demo_telnet_session
from SSH_Connect import demo_ssh_session
from Backup_Switch_Configs import backup_switch_configs
from Compare_Run_Start import compare_run_start
from Compare_Run_with_Local_File import compare_run_with_local_file
from Performance_Parameters import update_performance_metrics

# For Daryl
from Configure_Address import configure_address

# For Adam
from eigrp_test import eigrp_configuration


OPTIONS = {
    "1.1": {
        "description": "Unsecure Remote Connection",
        "function": demo_telnet_session,
        },
    "1.2": {
        "description": "Secure Remote Connection",
        "function": demo_ssh_session,
        },
    "1.3": {
        "description":"Backup Multiple Switch Configurations",
        "function": backup_switch_configs
        },
    "2.1": {
        "description": "Compare Running Configuration with Startup Configuration",
        "function": compare_run_start
        },
    "2.2": {"description": "Compare Running Configuration with Local File",
            "function": compare_run_with_local_file
            },
    "3": {"description": "Performance Parameters",
          "function": update_performance_metrics,
            },
    "4": {"description": "Individual Task - Daryl",
          "function": configure_address
          },
    "5": {"description": "Individual Task - Adam",
          "function": eigrp_configuration
          }
}

VALID_OPTS = OPTIONS.keys()


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
        except TypeError as e:
            print(f"Cannot call this function!\n{e}")
            return None
        except NameError as e:
            print(f"Cannot find function with this name!\n{e}")
            return None


def display_options():
    global VALID_OPTS
    global OPTIONS
    print("\n################################################\n")
    for i in VALID_OPTS:
        print(f"{i}: {OPTIONS[i]['description']}")
    print("\n################################################\n")


def get_enable_pass():
    while True:
        enable_pass = getpass.getpass("Enter enable secret: ")
        if enable_pass != getpass.getpass("Confirm enable secret: "):
            print("Mismatch detected!")
            continue
        else:
            return enable_pass


def get_address(prompt="Input IP Address for network device: "):
    while True:
        address = input(prompt)
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
    global OPTIONS
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

    try:
        # Gets enable secret if its needed
        needs_en_secret = yes_or_no(prompt="Will you need an enable secret for this session?")
        enable_pass = get_enable_pass() if needs_en_secret else ""
        del needs_en_secret

        # Get account info for remote connections
        username = input("Input username for remote connection: ")
        while True:
            password = getpass.getpass("Input password for remote connection: ")
            if password != getpass.getpass("Confirming password: "):
                print("Passwords don't match!")
                continue
            else:
                break

        # Get Network Device Address
        device_address = get_address()

        display_options()
        # Loop until a valid option is found or keyboard interrupt caught
        while True:
            option = input("Choose your option: ")
            if option not in VALID_OPTS:
                print("Invalid option chosen")
                continue
            else:
                break

        # Run script specified by option
        if option == "1.1":
            output = caller(OPTIONS[option]['function'], device_address. username, password)
        elif option == "4":
            output = caller(
                OPTIONS[option]['function'],
                device_address,
                username,
                password,
                get_address(prompt="Input Address to be configured: "),
                get_address(prompt="Input Subnet Mask to be configured"),  # Needs revisiting
                secret=enable_pass
            )
        else:
            output = caller(OPTIONS[option]['function'], device_address, username, password, secret=enable_pass)
            print(output)

        return 0

    except KeyboardInterrupt:
        print("\n\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("Keyboard interrupt caught, exiting program")
        return 0

    except Exception as e:
        print("\n\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print(f"An Exception Occured\n{e}")
        return 1


# If this script was called directly (eg. from command-line or IDLE) and not by another script, run main() function
if __name__ == '__main__':
    main()
