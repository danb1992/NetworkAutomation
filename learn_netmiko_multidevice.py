from netmiko import ConnectHandler
from getpass import getpass


device_list = [
    "192.168.0.27", # S1-2960
    "192.168.0.223", # R1-11006G
    "192.168.0.166", # R2-4331
]

login_info = {
    "username": input("Username: "),
    "password": getpass("Password: "),
}

for device in device_list:

    connection = ConnectHandler(
        ip = device,
        device_type = "cisco_ios",
        username = login_info["username"],
        password = login_info["password"],
        port = 22
    )

    print("\nPrinting IP Interfaces...")
    output = connection.send_command("show ip int br | exc unassigned",strip_command=False)
    print(connection.find_prompt(),output)

    print("\nClosing connection...")
    connection.disconnect()