import napalm, urllib3

from tabulate import tabulate

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def main():
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

    devices_table = [["hostname", "vendor", "model","OS version", "uptime", "serial_number","hardware"]]
    devices_table_int = [["hostname", "interface", "ip"]]

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

    for device in network_devices:
        try:
            print("Connecting to {} ...".format(device.hostname))
            device.open()

            print("Getting device info")
            device_facts = device.get_facts()

            hardware = "Not Defined"
            commands = ['show ver']
            result = device.cli(commands)['show ver'].split("\n")
            for row in result:
                if row.find('of memory') != -1:
                    hardware = row

            devices_table.append([device_facts["hostname"],
                                  device_facts["vendor"],
                                  device_facts["model"],
                                  device_facts['os_version'],
                                  device_facts["uptime"],
                                  device_facts["serial_number"],
                                  hardware
                                  ])

            print("Getting device interfaces")
            int_ip = device.get_interfaces_ip()
            for interface, settings in int_ip.items():
                hostname = device_facts["hostname"]
                for ip, prefix in settings['ipv4'].items():
                    address  = f'{ip}/{prefix["prefix_length"]}'
                    devices_table_int.append([hostname,interface,address])
            print("Done.")
            device.close()
        except Exception as err:
            print(f'Can not connect to device {device_facts["hostname"]}')
            print(err)

    print(tabulate(devices_table, headers="firstrow"))
    print()
    print(tabulate(devices_table_int, headers="firstrow"))


if __name__ == '__main__':
    main()
