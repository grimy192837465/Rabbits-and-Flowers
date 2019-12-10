from SSH_Connect import SSH


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


def configure_address(device_address, username, password, new_address, netmask, enable_pass=""):
    """
    :param device_address: Router Address
    :param username: Administrator Username
    :param password: Administrator Password - Recommended to be passed in via getpass
    :param new_address: Address for the configured interface
    :param netmask: Subnet mask for the configured interface
    :param enable_pass: Enable password
    :return: Status Code
    """
    remote_device = SSH(device_address, username, password, secret=enable_pass)
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
    configure_address(
        "192.168.1.1", "admin", "cisco", "192.168.4.5", "255.255.255.0", enable_pass="cisco"
    )
