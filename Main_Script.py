"""

Created a potential outline for program
Feel free to change or discuss what I have done here

"""
import getpass
from socket import inet_aton

VALID_OPTS = {
    "1.1": ["Unsecure Remote Connection", "funcName"],
    "1.2": ["Secure Remote Connection", "funcName"],
    "1.3": ["Backup Multiple Switch Configurations", "funcName"],
    "2.1": ["Compare Running Configuration with Startup Configuration", "funcName"],
    "2.2": ["Compare Running Configuration with Local File", "funcName"],
    "3": ["Performance Parameters", "funcName"],
    "4": ["Individual Task", "funcName"]
}


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

