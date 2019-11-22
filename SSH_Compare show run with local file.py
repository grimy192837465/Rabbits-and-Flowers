# First proper stab at comparing the show run command with a local file but if the code here is correct then the output of the command should be saved to a file and compared with a local file once SSH'd into the router

import paramiko
import diffios

# Paramiko code to SSH into router and get output of show run command and save output to file
host = '192.168.1.66'
user = 'cisco'
secret = 'cisco'
port = 22

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) #Set policy to use when connecting to servers without a known host key
ssh.connect(hostname=host, username=user, password=secret, port=port)
ssh.exec_command('terminal length 0')
stdin, stdout, stderr = ssh.exec_command('show run')
list = stdout.readlines()
output = [line.rstrip() for line in list] # Above two lines get rid of white space allowing more readable text file
#print (''.join(output))
file = open('sh_run.txt', 'w')
file.write('\n'.join(output))
file.close()

# diffios code meant to compare cisco ios files and output differences between them
output = "sh_run.txt"
local_file = "sh_run_local.txt"

# We initialise a diffios Compare() object with our two files.
diff = diffios.Compare(output, local_file)
# From this Compare object we can see the differences between our
# configurations using the delta() method.
print(diff.delta())
--- output
+++ local_file