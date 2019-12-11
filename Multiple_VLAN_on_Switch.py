from SSH_Connect import SSH
from socket import inet_aton


def get_address(prompt="Input IP Address for network device: "):
    while True:
        address = input(prompt)
        try:
            inet_aton(address)
            return address
        except OSError:
            print("Invalid address entered:")
            continue


# function that can be called to configure the vlans on switches
def configure_switch_vlan(ip_address, username, password, secret=""):
    # Infinite loop until correct number of switches entered
    while True:
        try:
            num_switches = int(input("Input the amount of switches you want to configure: "))
            if num_switches < 1:
                print("Please enter a value greater than 1")
                continue
            else:
                break
        except TypeError:
            print("Please enter a number")
            continue

    # creates the ssh connection and saves it to a variable
    vlan_config = SSH(ip_address, username, password, secret=secret)
    # connects to the device
    vlan_config.connect()

    vlan_config.send_configuration(from_file=True, configuration="Multi_switch_conf")

    for i in range(1, num_switches):
        vlan_config = SSH(get_address(), username, password, secret=secret)
        # connects to the device
        vlan_config.connect()

        vlan_config.send_configuration(from_file=True, configuration="Multi_switch_conf")

    return "Everything has been completed successfully!"


# test function
if __name__ == "__main__":
    configure_switch_vlan("192.168.0.1", "admin", "cisco")
    configure_switch_vlan("192.168.0.2", "admin", "cisco")
