from netmiko import ConnectHandler
import napalm, urllib3
from tabulate import tabulate

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

driver_ios = napalm.get_network_driver("ios")
driver_nxos = napalm.get_network_driver("nxos_ssh")

devices = [
    {
        'device_type': 'cisco_ios',
        'host': '10.10.20.175',
        'username': 'cisco',
        'password': 'cisco',
        'secret': 'cisco',
        'port': 22,
    },
    {
        'device_type': 'cisco_ios',
        'host': '10.10.20.176',
        'username': 'cisco',
        'password': 'cisco',
        'secret': 'cisco',
        'port': 22,
    },
    {
        'device_type': 'cisco_nxos',
        'host': '10.10.20.177',
        'username': 'cisco',
        'password': 'cisco',
        'secret': 'cisco',
        'port': 22,
    },
    {
        'device_type': 'cisco_nxos',
        'host': '10.10.20.178',
        'username': 'cisco',
        'password': 'cisco',
        'secret': 'cisco',
        'port': 22,
    }]



for device in devices:
    try:
        ssh = ConnectHandler(**device)
        ssh.enable()
        if device['device_type'] == 'cisco_ios':
            print(f'Creating Null interface on {device["host"]}...')
            print(f'{ssh.send_config_set(["interface null0", "ip unreachable"])}')
            print('-----------------------------------------------------------------------------\n')

        print(f'Creating loopback on {device["host"]}...')
        # print('-----------------------------------------------------------------------------\n')
        print(f'{ssh.send_config_set(["interface loopback 7", "description Loopback 7"])}')
        print('-----------------------------------------------------------------------------')
    except Exception as err:
        print(f"Can not connect to device {device['host']}")
        print(err)