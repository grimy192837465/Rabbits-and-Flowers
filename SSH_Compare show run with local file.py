import getpass
from SSH_Connect import SSH


def get_object(ip_address, username, port=22):
    try:
        password = getpass.getpass("What is the password of the user of which you would like to connect to?")
        return SSH(ip_address = ip_address, username = username, password = password, port = port)

    except KeyboardInterrupt:
        print("\nSSH session closed")
        #exit program
        sys.exit()


def writerunningconfig(text):
    file = open('sh_run.txt', 'w')
    file.write (text)
    file.close()


def sendcommand(ssh, command, printTF):
    #stdin is used for commands requiring inputs
    #stdout gives the output of the command
    #stderr shows any errors
    output = ssh.send_command(command)
    if printTF == True:
        writerunningconfig (output)
    #print(output)
    #stdin.write("{}\n".format)
    return output


def localFile():
    file = open('test.txt', 'r')
    lines = file.readlines()
    newconfig = []
    for x in lines:
        newconfig.append(x)
    #print (newconfig)
    return newconfig


def compare(routerConfig, grabbedOutput):
    print ("starting Comparison")
    to_compare = routerConfig.splitlines(True)
    i = 0
    j = 0
    while i< len(to_compare) and j<len(grabbedOutput):
        if to_compare[i] != grabbedOutput[j]:
            print("Diffence detected. Line " + str(i) + " in router config: " + to_compare[i] + "\nfile configuration: "+ grabbedOutput[j])
        i += 1
        j += 1
    if i != j:
        print("Files unequal")


if __name__ == '__main__':
    ssh = get_object('192.168.1.1', 'admin')
    ssh.connect()
    output = sendcommand(ssh, "sh run", True)
    grabbedOutput = localFile()
    compare (output, grabbedOutput)
    ssh.close()
