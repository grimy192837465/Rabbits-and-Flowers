# Telnet to switch author @ Myles
# The libraries I have imported:
import telnetlib
import getpass


def demo_telnet_session(host, user, telnet_secret):
    # STARTS A TELNET SESSION
    tele = telnetlib.Telnet(host)

    tele.read_until("User: ")
    tele.write(user + "\n")

    # CONFIGURING THE DEVICE
    if telnet_secret:
        tele.read_until("Secret: ")
        tele.write(telnet_secret + "\n")
        tele.write("enable\n")
        tele.write("conf t\n")

        tele.write("end\n")
        tele.write("exit\n")

    print(tele.read_all)


if __name__ == '__main__':
    # LOGIN FOR TELNET
    Host = "192.168.1.2"
    User = input("Enter Username for Login: ")
    secret = getpass.getpass("Telnet Password: ")
    demo_telnet_session(Host, User, secret)

