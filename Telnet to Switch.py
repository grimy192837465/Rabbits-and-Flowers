#Telnet to switch author @ Myles

#The libraries I have imported:
import telnetlib
import getpass
import sys

#LOGIN FOR TELNET
Host = "IP Address"
User = input("Enter Username for Login")
secret = getpass.getpass()

#STARTS A TELNET SESSION

tele = telnetlib.Telnet(Host)

tele.read_until("User: ")
tele.write(User + "\n" )

#CONFIGURING THE DEVICE

if secret:
    tele.read_until("Secret: ")
    tele.write(secret + "\n")
    tele.write("enable\n")
    tele.write("conf t\n")
    
    tele.write("end\n")
    tele.write("exit\n")
        
print (tele.read_all)

