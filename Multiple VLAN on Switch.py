#uses file 'deivces' which can be found on this commit too
from SSH_Connect import SSH

switches_list = []

file = open("devices", "r")
for line in file:
    switch_info_list = line.strip().split(',')
    #test what is being read
#    print(switch_info_list[0], switch_info_list[1], switch_info_list[2])
    test = SSH(switch_info_list[0], switch_info_list[1], switch_info_list[2])
    test.connect()

    #passwords to be run on each device connected to
    output, errors = test.send_command("en", "PASSWORD")
    output, errors = test.send_command("vlan 10")
    output, errors = test.send_command("name Finance")
    output, errors = test.send_command("vlan 20")
    output, errors = test.send_command("name IT")
    output, errors = test.send_command("vlan 30")
    output, errors = test.send_command("name Sales")
    output, errors = test.send_command("exit")

    #print any errors
    print(output,errors)
    #close ssh session
    test.close()    
        
#close the file
file.close()
