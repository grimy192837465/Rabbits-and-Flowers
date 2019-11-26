# Whoever said this is the easier of the options to pick...you're full of shit lol

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

def writerunningconfig(text):
    file = open('sh_run.txt', 'w')
    for x in text:
        file.write (x + '\n')
    file.close()

def sendcommand(command, printTF, cmdin=None):
    global ssh_connection
    #stdin is used for commands requiring inputs
    #stdout gives the output of the command
    #stderr shows any errors
    stdin, stdout, stderr = ssh_connection.exec_command (command)
    list = stdout.readlines()
    output = [line.rstrip() for line in list] # Above two lines get rid of white space allowing more readable text file
    for x in output:
        print(x)
    if printTF == True:
        writerunningconfig (output)
    #print(output)
    #stdin.write("{}\n".format(cmdin))
    return(output)

def close():
    ssh_connection.close()

def localFile():
    file = open('test.txt', 'r')
    lines = file.readlines()
    newconfig = []
    for x in lines:
        newconfig.append(x.rstrip())
    #print (newconfig)
    return newconfig

def compare(routerConfig, grabbedOutput):
    print ("starting Comparison")
    line = 0
    for x in routerConfig:
        if routerConfig[line] != grabbedOutput[line]:
            print("Diffence detected. Line " + str(line) + " in router config: " + routerConfig[line] + "\nfile configuration: "+ grabbedOutput[line])
        line += 1

#For testing purposes only
if __name__ == '__main__':
    connect("192.168.1.1", "admin")
    routerConfig = sendcommand("sh run" , True)
    close()
    grabbedOutput = localFile()
    compare(routerConfig, grabbedOutput)
    #print (routerConfig)
    #print ('\n')
    #print('\n')
    #print (grabbedOutput)
