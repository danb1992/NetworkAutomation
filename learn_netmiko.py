from netmiko import ConnectHandler
from getpass import getpass


"""
Netmiko Boilerplate
"""

device = {
    "device_type": "cisco_ios",
    "ip": "192.168.0.26",
    "username": input("Enter username: "),
    "password": getpass("Enter password: ",echo_char="*"), # 'echo_char' shows visible '*' as characters are inputted
    "secret": getpass("Enter enable secret: ",echo_char="*"), # Not needed if login account is priv 15
    "port": 22,
    "session_log": "session_log.txt" # Appends device output to this log file
}

connection = ConnectHandler(**device)

"""
Enter Priv EXEC Mode
"""

connection.enable()

"""
Send 'show' commands:

Methods used:
# 'strip_command()' method can show/hide CLI command in terminal (True=invisible [default], False=visible)
# 'find_prompt()' method shows hostname prompt in terminal

"""

print("\n") # Provides some spacing between login info and the command output
ip_intfs = connection.send_command("show ip interface brief | exclude unassigned",strip_command=False)
print(connection.find_prompt(),ip_intfs) # This combo emulates native IOS CLI line

"""
Saves configuration ('write mem')
"""

connection.save_config()

"""
Gracefully closes SSH connection
"""

connection.disconnect()