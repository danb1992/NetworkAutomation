from netmiko import ConnectHandler
import netmiko.exceptions
from getpass import getpass


# Login Info

username = input("Username: ")
password = getpass("Password: ",echo_char="*")

devices = [

    # S1-2960X Details
    {
        "ip": "192.168.0.27",
        "device_type": "cisco_ios",
        "username": username,
        "password": password,
        "port": 22,
    },
    # R1-11006G Details
    {
        "ip": "192.168.0.223",
        "device_type": "cisco_ios",
        "username": username,
        "password": password,
        "port": 22,
    },
    # R2-4331 Details
    {
        "ip": "192.168.0.166",
        "device_type": "cisco_ios",
        "username": username,
        "password": password,
        "port": 22,
    },
]

for device in devices:

    try:
        connection = ConnectHandler(**device)

        output = connection.send_command("show ip interface brief | exclude unassigned",strip_command=False)
        print(output)

        print("\n")
        connection.disconnect()

    # NetmikoTimeoutException = Device unreachable

    except netmiko.exceptions.NetmikoTimeoutException:
        print(f"\nERROR: Connection Timeout for {device["ip"]}.")
        print("""Possible causes...
            1. Incorrect hostname or IP
            2. Wrong TCP port
            3. Firewall blocking access
            """)

    # NetmikoAuthenticationException = Authentication failed
    
    except netmiko.exceptions.NetmikoAuthenticationException:
        print(f"\nERROR: Authentication Failure on {device["ip"]}.")
        print("""Possible causes...
            1. Invalid Username and/or Password
            2. Incorrect SSH key file
            3. Connecting to wrong device
            """)
    
    # ReadTimeout = Expected command prompt is not detected
    
    except netmiko.exceptions.ReadTimeout:
        print(f"\nERROR: Read Timeout on {device["ip"]}.")
        print("""Possible causes...
            1. Missing/Incorrect 'enable' password
            2. Small timeout value
            3. Unexpected device prompt
            """)
    
    # SSHException = Generic SSH error
    
    except netmiko.exceptions.SSHException:
        print(f"\nERROR: General SSH error when connecting to {device["ip"]}.")
        print(""" Possible causes...
            1. Unsupported cipher
            2. Incompatible SSH key exchange algorithm
            3. Corrupted SSH session
            """)

    # Catch-all exception check, which outputs the error as a string
    
    except Exception as e:
        print(f"\nERROR: Undefined error occurred on {device["ip"]}: ", str(e))
