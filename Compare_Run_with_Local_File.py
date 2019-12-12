import getpass
from SSH_Connect import SSH


def get_object(ip_address, username, port=22):
    try:
        password = getpass.getpass(
            "What is the password of the user of which you would like to connect to?"
        )
        # calls the SSH class from SSH_Connect file to gather the necessary details
        return SSH(
            ip_address=ip_address, username=username, password=password, port=port
        )

    except KeyboardInterrupt:
        print("\nSSH session closed")
        # exit program
        sys.exit()


# creates file called sh_run.txt of which sh run command output is written to
def writerunningconfig(text):
    file = open("sh_run.txt", "w")
    file.write(text)
    file.close()

    
# printTF is printTrueFalse
def sendcommand(ssh, command, printTF):
    # stdin is used for commands requiring inputs
    # stdout gives the output of the command
    # stderr shows any errors
    output = ssh.send_command(command)
    # if printTF is true then writerunningconfiguration definition is called
    if printTF == True:
        writerunningconfig(output)
    # print(output)
    # stdin.write("{}\n".format)
    return output


# local file called test.txt is opened and read
def localFile():
    file = open("test.txt", "r")
    lines = file.readlines()
    # dictionary list is created for newconfig
    newconfig = []
    for x in lines:
        newconfig.append(x)
    # print (newconfig)
    return newconfig


# routerConfig=sh_run.txt and grabbedOutput=test.txt
def compare(routerConfig, grabbedOutput):
    print("starting Comparison")
    to_compare = routerConfig.splitlines(True)
    # i is test.txt and j is sh_run.txt, they're set to 0 as in line 0 of each file
    i = 0
    j = 0
    while i < len(to_compare) and j < len(grabbedOutput):
        # != means not equal to so that the below code in the block runs only if a difference occurs.
        if to_compare[i] != grabbedOutput[j]:
            # prints what is set such as Difference detected. Line...and then grabs i which test.txt and outputs the line number as a string
            # no need to decode string with utf-8 as netmiko decodes bytes to string unlike paramiko
            print(
                "Difference detected. Line "
                + str(i)
                + " in router config: "
                + to_compare[i]
                + "\nfile configuration: "
                + grabbedOutput[j]
            )
        # += 1 representing going line by line 1 at a time checking for a difference
        i += 1
        j += 1
    # will only print below print statement f i (test.txt) and j (sh_run.txt) are not identical files line by line
    if i != j:
        print("Files unequal")

# grabs the necessary information as is configured by user in main script
def compare_run_with_local_file(host, username, password, secret=""):
    ssh = SSH(host, username, password, secret=secret)
    # creates ssh session and connects
    ssh.connect()
    # runs sh run command on the connected device
    output = sendcommand(ssh, "sh run", True)
    # localfile is saved as grabbedOutput variable
    grabbedOutput = localFile()
    # output=sh run command output and is saved to output variable, compare is a defined function run above
    compare(output, grabbedOutput)
    ssh.close()


if __name__ == "__main__":
    # ip and username set here if user wanted to run script locally from file and not main script
    ssh = get_object("192.168.1.1", "admin")
    ssh.connect()
    # netmiko handles errors so output, errors changed to just output, also cmdin=none and any reference of it has disappeared in netmiko
    output = sendcommand(ssh, "sh run", True)
    grabbedOutput = localFile()
    compare(output, grabbedOutput)
    ssh.close()
