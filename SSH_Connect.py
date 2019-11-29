"""
Implements a basic API for use with netmiko also allows paramiko SSH connections (depreciated)
Allows you to instantiate a ssh connection to a remote host using paramiko and send commands
Sends stdout back to the caller


NOTE: No need to enter enable password - its handled by paramiko
"""

import paramiko
import netmiko
import sys


class SSH:
    def __init__(self, ip_address, username, password, device_type="cisco_ios", secret='', port=22):
        # Create a dictionary representing the networking device
        self._device = {
            "device_type": device_type,
            "host": ip_address,
            "username": username,
            "password": password,
            "port": port,
            "secret": secret,
        }
        self._remote_connection = None

    def connect(self):
        # Let netmiko setup a SSH connection to the networking device described above
        print("Attempting to connect to remote device")
        self._remote_connection = netmiko.ConnectHandler(**self._device)
        print("Connected")

    def send_command(self, command):
        if command == "enable":
            self._remote_connection.enable()
            return
        # Send output of SSH command to caller
        return self._remote_connection.send_command(command)

    def send_configuration(self, from_file=False, configuration=None):
        """
        Used to send batch configuration to networking device
        HINT: Good for doing some similar configuration over and over..

        :param from_file: Boolean to indicate whether to read config from specified file
        :param configuration: String representing a file or a list containing commands to execute
        :return: Returns the output from the commands
        """
        if from_file:
            if type(configuration) is not str:
                print("Please specify a string name of a file with configuration commands in")
                return None
            else:
                with open(configuration, "r") as file:
                    return self._remote_connection.send_config_from_file(file)
        else:
            if type(configuration) is not list:
                print("Please pass configuration file as a list if not using a file")
                return None
            else:
                return self._remote_connection.send_config_set(configuration)

    def close(self):
        # Closes the connection
        self._remote_connection.disconnect()


class ParamikoSSH:
    """
    Previous SSH connection method. Session is wiped after 1 command executes
    """
    def __init__(self, ip_address, username, password, port=22):
        self._connection = paramiko.SSHClient()
        self._address = ip_address
        self._username = username
        self._password = password
        self._port = port

    def connect(self):
        try:
            # Automatically add unknown hosts to known hosts
            self._connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            print("*****Connecting...*****")
            # Connect to remote host
            self._connection.connect(
                hostname=self._address,
                username=self._username,
                password=self._password,
                port=self._port
            )
            print("Connected")
            return 0

        except paramiko.AuthenticationException:
            # Executed if authentication errors occur
            print("Authentication exception occured please check your details and try again.")
            # Below line commented out and changed with return statement to allow caller to control exception
            # to allow retries
            # sys.exit()
            # Non zero return codes signify error
            return 1

    def send_command(self, command, cmd_input=None):
        # stdin is used for commands requiring inputs
        # stdout gives the output of the command
        # stderr shows any errors
        stdin, stdout, stderr = self._connection.exec_command(command)
        stdin.write("{}\n".format(cmd_input))
        return stdout.read(), stderr.read()

    def close(self):
        print("Closing SSH Connection")
        self._connection.close()


# For testing purposes only
if __name__ == '__main__':
    # Opening SSH connection to example network device
    # Secret is enable password
    test = SSH("192.168.1.1", "admin", "admin", secret="admin")
    test.connect()
    test.send_command("enable")
    test.send_command("sh ip int brie")
    test.send_command("conf t")
    test.send_command("no ip domain-lookup")
    # Closing the connection
    test.close()
