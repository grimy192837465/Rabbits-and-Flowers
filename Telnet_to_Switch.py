import paramiko
import threading
import netmiko


class SSH:
    def __init__(self, ip_address, username, password, secret="", port=22):

        # Create a dictionary representing the device
        self._device = {
            "device_type": "cisco_ios",
            "host": ip_address,
            "username": username,
            "password": password,
            "port": port,  # optional, defaults to 22
            "secret": secret,  # optional, defaults to ''
        }
        self._remote_connection = netmiko.ConnectHandler(**self._device)

    def send_command(self, command):
        return self._remote_connection.send_command(command)

    def send_configuration(self, from_file=False, configuration=None):
        if from_file:
            if type(configuration) is not str:
                print(
                    "Please specify a string name of a file with configuration commands in"
                )
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
        self._remote_connection.disconnect()


if __name__ == "__main__":
    test = SSH("192.168.1.1", "admin", "admin", secret="admin")
    test.send_command("sh ip int brie")
    test.send_command("conf t")
    test.send_command("no ip domain-lookup")
    test.close()
