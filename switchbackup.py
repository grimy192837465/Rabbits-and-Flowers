from SSH_Connect1 import SSH
#import SSH_Connect as paramiko


#Login details
username = 'admin'
password = 'cisco'

#Switch1 IP address and login authentication
switch = SSH('192.168.0.1', username, password)

#Connecting to the switch
switch.connect()

#Writing the startup-configs on the file
file1 = open('switch1.txt', 'w')
#switch.send_command ('en', 'cisco')
output, errors = switch.send_command ('show start')

#Writes the output in string
file1.write(str(output))
file1.close() # Close and save file1
switch.close() #Close switch connection

#Switch2 IP address and login authentication
switch = SSH('192.168.0.2', username, password)

#Connecting to the switch
switch.connect()

#Writing the startup-configs on the file
file2 = open('switch2.txt', 'w')
#switch.send_command ('en', 'cisco')
output, errors = switch.send_command ('show start')

#Writes the output in string  
file2.write(str(output))
file2.close()# Close and save file2
switch.close() #Close switch connection
 
