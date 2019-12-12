"""
Implements a basic API for use with netmiko also allows paramiko SSH connections (depreciated)
Allows you to instantiate a ssh connection to a remote host using paramiko and send commands
Sends stdout back to the caller


NOTE: No need to enter enable password - its handled by netmiko
"""

import netmiko


class SSH:
    def __init__(
        self,
        ip_address,
        username,
        password,
        device_type="cisco_ios",
        secret="",
        port=22,
    ):
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
                print(
                    "Please specify a string name of a file with configuration commands in"
                )
                return None
            else:
                return self._remote_connection.send_config_from_file(configuration)
        else:
            if type(configuration) is not list:
                print("Please pass configuration file as a list if not using a file")
                return None
            else:
                return self._remote_connection.send_config_set(configuration)

    def close(self):
        # Closes the connection
        self._remote_connection.disconnect()


def demo_ssh_session(ip_address, username, password, secret=""):
    # Opening SSH connection to example network device
    # Secret is enable password
    remote_device = SSH(ip_address, username, password, secret=secret)
    remote_device.connect()
    remote_device.send_command("sh ip int brie")

    # Closing the connection
    remote_device.close()


# For testing purposes only
if __name__ == "__main__":
    # Opening SSH connection to example network device
    # Secret is enable password
    demo = SSH("192.168.1.1", "admin", "admin", secret="admin")
    demo.connect()
    demo.send_command("sh ip int brie")
    demo.send_command("conf t")
    demo.send_command("no ip domain-lookup")
    # Closing the connection
    demo.close()
