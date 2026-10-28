import napalm
from pprint import pprint
from getpass import getpass


# 'ios' = Cisco IOS

driver = napalm.get_network_driver("ios")

# Device Object

device = driver(hostname="192.168.0.166",
                username=input("Username: "),
                password=getpass("Password: ",echo_char="*"),
                )

# Establish connection

device.open()

# Implement NAPALM methods (pprint = formats output to be more readable)
# 'get_facts()' returns essential device data in a dictonary format, such as hostname, serial number, and interfaces

print("\nPrinting results of 'get_facts()' method, using pprint for formatting...")
print("-" * 63)
pprint(device.get_facts())

# Assign device facts dictionary to 'device_facts' variable
# Print each key-value pair within the dictionary by calling the key, instead of calling the method each time

device_facts = device.get_facts()

print("\nPrinting key-value pairs of 'get_facts()' method...")
print("-" * 61)
print("fqdn:", device_facts["fqdn"])
print("hostname:", device_facts["hostname"])
print("model:", device_facts["model"])
print("os_version:", device_facts["os_version"]) # Value is a long string containing more details, along with the version
print("serial_number:", device_facts["serial_number"])
print("uptime:", device_facts["uptime"]) # Value is a float, in seconds
print("vendor:", device_facts["vendor"])

# Interfaces are part of the 'get_facts()' output, but is stored as a list
# Using a for loop makes the list even more readable

print("interface_list:")
for interface in device_facts["interface_list"]:
    print(f" - {interface}")

# Close connection

device.close()