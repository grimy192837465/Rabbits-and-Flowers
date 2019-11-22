"""
TODO
interactive commands in sed commands functions
"""

import paramiko
import getpass
import sys

#start the ssh connection 
ssh_connection=paramiko.SSHClient()

def connect(ip_address, username, port=22):
    global ssh_connection
    try:
        password = getpass.getpass("What is the password of the user of which you would like to connect to?")
        #trusts all connections
        ssh_connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print("*****Connecting...*****")
        #gets the information neded to make the ssh connection
        ssh_connection.connect(hostname = ip_address, username = username,password = password, port = port)
        #if the connection information is wrong, catch the error and close the program
        
    except paramiko.AuthenticationException:
        print("*****Invalid details provided, please check the details and try again*****")
        sys.exit()
        
    except KeyboardInterrupt:
        print("\nSSH session closed")
        #exit program
        sys.exit()
            
    print("*****Connected!*****")
    return



def sendcommand(command, cmdin=None):
    global ssh_connection
    #stdin is used for commands requiring inputs
    #stdout gives the output of the command
    #stderr shows any errors
    stdin, stdout, stderr = ssh_connection.exec_command (command)
    stdin.write("{}\n".format(cmdin))
    return(stdout.read(), stderr.read())

def close():
    ssh_connection.close()


#For testing purposes only
if __name__ == '__main__':
    connect("127.0.0.1", "lewis")
    output = sendcommand("sudo ls")
    passw = getpass.getpass("sudo password")
    print(output)
    close()
    