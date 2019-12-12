from SSH_Connect import SSH
from socket import inet_aton


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


def get_address(prompt="Input IP Address: "):
    while True:
        address = input(prompt)
        try:
            inet_aton(address)
            return address
        except OSError:
            print("Invalid address entered:")
            continue


def configure_address(device_address, username, password, secret=""):
    """
    :param device_address: Router Address
    :param username: Administrator Username
    :param password: Administrator Password - Recommended to be passed in via getpass
    :param enable_pass: Enable password
    :return: Status Code
    """
    remote_device = SSH(device_address, username, password, secret=secret)
    remote_device.connect()

    # Get List of Interface to Configure
    int_brief = remote_device.send_command("sh ip int brief").split("\n")
    interfaces = [line.split()[0] for line in int_brief]
    interfaces.append("Loopback1")
    del int_brief

    print("Possible interfaces:")
    for i in interfaces:
        print(i)

    while True:
        print("NOTE: When selecting an interface, please type out fully, shortened notation not supported yet..")
        interface = input("Please choose an interface to configure address on: ")
        if interface in interfaces:
            break
        else:
            print("Invalid interface.")
            continue

    new_address = get_address(prompt=f"Enter new address for {interface}: ")
    netmask = get_address(prompt=f"Enter new subnet mask for {interface}: ")

    # Create configuration list to send to router
    configuration = [
        f"int {interface}",
        f"ip address {new_address} {netmask}",
        "description Configured Remotely using Python",
    ]
    remote_device.send_command("enable")
    remote_device.send_configuration(configuration=configuration)


# For testing purposes only
if __name__ == "__main__":
    configure_address("192.168.1.1", "admin", "cisco", "192.168.4.5")
