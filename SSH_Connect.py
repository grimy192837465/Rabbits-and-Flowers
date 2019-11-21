import paramiko
import time
import sys

try:
    #ip address of what is being connected to
    ip_address = raw_input("What is the ip address of which you would like to connect to?")
except KeyboardInterrupt:
    print("\nSSH session closed")
    #exit program
    sys.exit()
    
try:
    #username of the user that will be logging into on the instance
    username = raw_input("What is the user of which you would like to login as?")
except KeyboardInterrupt:
    print("\nSSH session closed")
    sys.exit()

#password of the user that will be logging into on the instance
password = raw_input("What is the password of the user of which you would like to connect to?")
    
#port that is used connect to the instance
port = 22
try:
    #start the ssh connection with paramiko
    ssh_connection=paramiko.SSHClient()
    #trusts all connections
    ssh_connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    #gets the information neded to make the ssh connection
    ssh_connection.connect(hostname = ip_address, username = username,password = password, port = port)
#if the connection information is wrong, catch the error and close the program
except paramiko.AuthenticationException:
    print("*****Invalid details provided, please check the details and try again*****")
    sys.exit()

print("*****Connecting...*****")
#wait for 3 seconds
time.sleep(3)
print("*****Connected!*****")
#wait for 1 second
time.sleep(1)

#Asks the user what command they would like to run
try:
    #loop to allow multiple commands to be done without restarting the script
    while True:
        command = raw_input("What command would you like to run?")
        #stdin is used for commands requiring inputs
        #stdout gives the output of the command
        #stderr shows any errors
        stdin, stdout, stderr = ssh_connection.exec_command (command)
        print(stdout.read())
#if the user ends the script with a keyboard interupt, catch the error and close the program with a print statement
except KeyboardInterrupt:
    print("\n*****SSH session closed*****")
    #close the ssh connection
    ssh_connection.close()