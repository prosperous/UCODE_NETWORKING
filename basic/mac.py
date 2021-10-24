import napalm, urllib3

from tabulate import tabulate

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

driver_ios = napalm.get_network_driver("ios")
driver_nxos = napalm.get_network_driver("nxos_ssh")

devices = [
    {
        'device_type': 'cisco_ios',
        'host': '10.10.20.175',
        'type': 'ios',
        'username': 'cisco',
        'password': 'cisco',
        'secret': 'cisco',
        'port': 22,
    },
    {
        'device_type': 'cisco_ios',
        'host': '10.10.20.176',
        'type': 'ios',
        'username': 'cisco',
        'password': 'cisco',
        'secret': 'cisco',
        'port': 22,
    },
    {
        'device_type': 'cisco_ios',
        'host': '10.10.20.177',
        'type': 'nxos',
        'username': 'cisco',
        'password': 'cisco',
        'secret': 'cisco',
        'port': 22,
    },
    {
        'device_type': 'cisco_ios',
        'host': '10.10.20.178',
        'type': 'nxos',
        'username': 'cisco',
        'password': 'cisco',
        'secret': 'cisco',
        'port': 22,
    }]

network_devices = []
for device in devices:
    if device['type'] == "ios":
        network_devices.append(
            driver_ios(
                hostname=device['host'],
                username=device['username'],
                password=device['password']
            )
        )
    elif device['type'] == "nxos":
        network_devices.append(
            driver_nxos(
                hostname=device['host'],
                username=device['username'],
                password=device['password']
            )
        )

mac_table = [["hostname","interface", "mac", "vlan","static", "active"]]

for device in network_devices:
    try:
        print("Connecting to {} ...".format(device.hostname))
        device.open()
        device_hostname = device.get_facts()['hostname']
        table_mac = device.get_mac_address_table()

        for element in table_mac:
            mac_table.append([device_hostname,
                              element["interface"],
                              element["mac"],
                              element['vlan'],
                              element["static"],
                              element["active"]
                                  ])
        device.close()
        print("Done")
    except Exception as err:
        print(f"Can not connect to device {device_hostname}")
        print(err)

print(tabulate(mac_table, headers="firstrow"))
