"""
Implements a basic API for use with paramiko
Allows you to instantiate a ssh connection to a remote host using paramiko and send commands
Sends stdout and stderr back to the caller
"""

import paramiko
import sys


class SSH:
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
        return (stdout.read(), stderr.read())

    def close(self):
        print("Closing SSH Connection")
        self._connection.close()


# For testing purposes only
if __name__ == '__main__':
    # Opening SSH connection to example network device
    test = SSH("192.168.1.1", "adminAccount", "superSecretPassword")
    test.connect()
    output, errors = test.send_command("en", "cisco")
    output, errors = test.send_command("sh ip int brie")
    print(output, errors)

    # Closing the connection
    test.close()
    # del test
