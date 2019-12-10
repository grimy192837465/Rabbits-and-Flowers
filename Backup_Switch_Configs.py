from SSH_Connect import SSH
from socket import inet_aton


def get_address(switch_number):
    while True:
        address = input("Input IP Address for switch {}: ".format(switch_number))
        try:
            inet_aton(address)
            return address
        except OSError:
            print("Invalid address entered:")
            continue


def backup_switch_configs(switch1_address, username, password, secret=""):

    # Get the amount of switches to be backed up
    while True:
        try:
            num_switches = int(input("Input the amount of switches you are backing up: "))
            if num_switches < 1:
                print("Invalid amount")
                continue
            else:
                break
        except TypeError:
            print("Enter a number..")
            continue

    # Backup switch 1 configuration
    # Switch1 IP address and login authentication
    switch = SSH(switch1_address, username, password, secret=secret)

    # Connecting to the switch
    switch.connect()

    # Get the startup-configs and open the file
    file1 = open("switch1.txt", "w")
    output = switch.send_command("show start")

    # Writes the output as string
    file1.write(str(output))
    file1.close()  # Close and save file1
    switch.close()  # Close switch connection

    for i in range(1, num_switches):
        # Switch IP address and login authentication
        switch = SSH(get_address(f"{i+1}"), username, password, secret=secret)

        # Connecting to the switch
        switch.connect()

        # Get the startup-configs and open the file
        file = open("switch{}.txt".format(i+1), "w")
        output = switch.send_command("show start")

        # Writes the output as string
        file.write(str(output))
        file.close()  # Close and save file2
        switch.close()  # Close switch connection


if __name__ == "__main__":
    # Login details
    username = "admin"
    password = "cisco"
    backup_switch_configs("192.168.0.1", username, password)
