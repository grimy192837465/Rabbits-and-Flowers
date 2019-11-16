import paramiko
import telnetlib
import fabric
from getpass import getpass
#import urmum


class RemoteConnection:
    def __init__(self, address, port, type="ssh"):
        self.address = address
        self.port = port
        self.connection = None
        # Some validation for type
        if not type.lower() == "telnet" or type.lower() == "ssh":
            print("Unrecognized type entered.. defaulting to SSH")
            self.type = "ssh"
        else:
            self.type = type

    def connect(self):
        if self.type == "telnet":
            print(f"Opening Telnet connection to ({self.address}, {self.port})")
            # Do some telnet stuff
        else:
            print(f"Opening SSH connection to ({self.address}, {self.port})")
            # Do some ssh stuff
        self.connection = "Not there yet"

    def send_command(self, command=None):
        pass
