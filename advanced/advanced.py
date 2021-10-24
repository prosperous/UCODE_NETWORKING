from flask import Flask, render_template, request, flash
from virl2_client import ClientLibrary
from netmiko import ConnectHandler
import napalm, urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__)
app.config['SECRET_KEY'] = '751a4afb2044a72d88532679d10e0f15'

@app.route("/")
def index():
    return render_template('index.html')


menu = [{"name": "Enable command", "url": "/send_cmd"}, {"name": "Config Command", "url": "/send_conf"}, {"name": "Get Device info", "url": "/"}]
lab_nodes = dict()
lab_title = ""

def connect_to_lab(url,login,password):

    client = ClientLibrary(url, login, password, ssl_verify=False)
    client.is_system_ready(wait=True)

    lab_list = client.get_lab_list()
    lab = client.join_existing_lab(lab_list[0])
    global lab_title
    lab_title = lab.title
    for node_in_lab in lab.nodes():
        node = dict()
        node['name'] = node_in_lab.label
        node['status'] = node_in_lab.state
        node['config'] =  node_in_lab.config.split('\n')
        # print(node['config'])
        lab_nodes[node_in_lab.label] = node


@app.route("/actions")
def actions():
    return render_template('actions.html', menu = menu)

@app.route("/connect",methods=["POST", "GET"])
def connect_to_virl():
    if request.method == 'GET':
        node_title = request.args.get('node')
        show = request.args.get('show')
        flash("")
        devices_table = []
        devices_table_int = []
        mac_table = []

        if show == "config":
            try:
                config = lab_nodes[node_title]['config']
                flash(config, category='config')
            except Exception as err:
                flash(str(err))
                return render_template('error.html', error=err)


        if show == "info":
            try:
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
                        'node': 'dist-rtr01'
                    },
                    {
                        'device_type': 'cisco_ios',
                        'host': '10.10.20.176',
                        'type': 'ios',
                        'username': 'cisco',
                        'password': 'cisco',
                        'secret': 'cisco',
                        'port': 22,
                        'node': 'dist-rtr02'
                    },
                    {
                        'device_type': 'cisco_ios',
                        'host': '10.10.20.177',
                        'type': 'nxos',
                        'username': 'cisco',
                        'password': 'cisco',
                        'secret': 'cisco',
                        'port': 22,
                        'node': 'dist-sw01'
                    },
                    {
                        'device_type': 'cisco_ios',
                        'host': '10.10.20.178',
                        'type': 'nxos',
                        'username': 'cisco',
                        'password': 'cisco',
                        'secret': 'cisco',
                        'port': 22,
                        'node': 'dist-sw02'
                    }]

                urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

                devices_table = [["hostname", "vendor", "model", "OS version", "uptime", "serial_number", "hardware"]]
                # devices_table_int = [["hostname", "interface", "ip"]]

                network_devices = []
                for device in devices:
                    if device['node'] == node_title:
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
                    flash("Connecting to {} ...".format(device.hostname))
                    device.open()

                    flash("Getting device info")
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

                    flash("Getting device interfaces")
                    int_ip = device.get_interfaces_ip()
                    for interface, settings in int_ip.items():
                        hostname = device_facts["hostname"]
                        for ip, prefix in settings['ipv4'].items():
                            address = f'{ip}/{prefix["prefix_length"]}'
                            devices_table_int.append([hostname, interface, address])
                    flash("Done.",category="info")
                    device.close()

                    print(devices_table)
                    print(devices_table_int)

                # return render_template('connected.html', menu=menu, lab_title=lab_title, lab_nodes=lab_nodes)
            except Exception as err:
                print(err)
                return render_template('error.html', error=err)

        if show == "mac":
            try:
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
                        'node': 'dist-rtr01'
                    },
                    {
                        'device_type': 'cisco_ios',
                        'host': '10.10.20.176',
                        'type': 'ios',
                        'username': 'cisco',
                        'password': 'cisco',
                        'secret': 'cisco',
                        'port': 22,
                        'node': 'dist-rtr02'
                    },
                    {
                        'device_type': 'cisco_ios',
                        'host': '10.10.20.177',
                        'type': 'nxos',
                        'username': 'cisco',
                        'password': 'cisco',
                        'secret': 'cisco',
                        'port': 22,
                        'node': 'dist-sw01'
                    },
                    {
                        'device_type': 'cisco_ios',
                        'host': '10.10.20.178',
                        'type': 'nxos',
                        'username': 'cisco',
                        'password': 'cisco',
                        'secret': 'cisco',
                        'port': 22,
                        'node': 'dist-sw02'
                    }]

                urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

                network_devices = []
                for device in devices:
                    if device['node'] == node_title:
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
                    flash("Connecting to {} ...".format(device.hostname))
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
                    flash("Done",category='mac')
            except Exception as err:
                print(err)
                return render_template('error.html', error=err)


        return render_template('connected.html', menu=menu, lab_title=lab_title, lab_nodes=lab_nodes, info = devices_table, int_ip = devices_table_int,mac = mac_table)

    if request.method == 'POST':
        try:
            url = request.form['url']
            login = request.form['login']
            password = request.form['password']

            connect_to_lab(url,login,password)

            return render_template('connected.html', menu = menu, lab_title = lab_title, lab_nodes = lab_nodes)
        except Exception as err:
            print(err)
            return render_template('error.html', error = err)


@app.route("/conf",methods=["GET"])
def show_config():
    if request.method == 'GET':
        node_title = request.args.get('node')
        show = request.args.get('show')
        if show == "config":
            try:
                config = lab_nodes[node_title]['config']
                return render_template('show_cfg.html', node_title=node_title, config=config, menu=menu)
            except Exception as err:
                print(err)
                return render_template('error.html', error=err)
        if show == "info":
            try:
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

                urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

                devices_table = [["hostname", "vendor", "model", "OS version", "uptime", "serial_number", "hardware"]]
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
                            address = f'{ip}/{prefix["prefix_length"]}'
                            devices_table_int.append([hostname, interface, address])
                    print("Done.")
                    device.close()

                return render_template('info.html', node_title=node_title, menu=menu)
            except Exception as err:
                print(err)
                return render_template('error.html', error=err)

    else:
        return render_template('error.html', error="Method not allowed")

# @app.route("/info",methods=["GET"])
# def show_config():
#     if request.method == 'GET':
#         node_title = request.args.get('node')
#         show = request.args.get('info')
#         if show == "info":
#             try:
#                 config = lab_nodes[node_title]['config']
#                 return render_template('show_cfg.html', node_title=node_title, config=config, menu=menu)
#             except Exception as err:
#                 print(err)
#                 return render_template('error.html', error=err)
#
#     else:
#         return render_template('error.html', error="Method not allowed")

@app.route("/send_conf",methods=["GET","POST"])
def perform_conf_command():
    if request.method == 'POST':
        command = request.form['action']
        hostname_cmd = request.form['hostname']

        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        devices = [
            {
                'device_type': 'cisco_ios',
                'host': '10.10.20.175',
                'type': 'ios',
                'username': 'cisco',
                'password': 'cisco',
                'secret': 'cisco',
                'port': 22,
                'hostname': 'dist-rtr01',
            },
            {
                'device_type': 'cisco_ios',
                'host': '10.10.20.176',
                'type': 'ios',
                'username': 'cisco',
                'password': 'cisco',
                'secret': 'cisco',
                'port': 22,
                'hostname': 'dist-rtr02',
            },
            {
                'device_type': 'cisco_ios',
                'host': '10.10.20.177',
                'type': 'nxos',
                'username': 'cisco',
                'password': 'cisco',
                'secret': 'cisco',
                'port': 22,
                'hostname': 'dist-sw01',
            },
            {
                'device_type': 'cisco_ios',
                'host': '10.10.20.178',
                'type': 'nxos',
                'username': 'cisco',
                'password': 'cisco',
                'secret': 'cisco',
                'port': 22,
                'hostname': 'dist-sw02',
            }]


        if command == 'interface':
            int_type = request.form['int_type']
            int_num = request.form['int_num']
            for device in devices:
                if device['hostname'] == hostname_cmd:
                    if device['type'] == "nxos":
                        save_cmd = "copy running-config startup-config"
                    else:
                        save_cmd = "write"
                    device.pop('hostname')
                    device.pop('type')
                    if int_type == "loopback":
                        int_cmd = [f"interface loopback {int_num}", f"description Loopback {int_num}"]
                    else:
                        int_cmd = ["interface null0", "ip unreachable"]
                    ssh = ConnectHandler(**device)
                    ssh.enable()
                    result = ssh.send_config_set(int_cmd)
                    ssh.send_command(save_cmd)
                    formated_result = result.split('\n')
                    flash(formated_result)
        elif command == 'vlan':
            vlan_id = request.form['vlan_id']
            vlan_name = request.form['vlan_name']
            for device in devices:
                if device['hostname'] == hostname_cmd:
                    if device['type'] == "nxos":
                        save_cmd = "copy running-config startup-config"
                    else:
                        save_cmd = "write"
                    device.pop('hostname')
                    device.pop('type')
                    ssh = ConnectHandler(**device)
                    ssh.enable()
                    result = ssh.send_config_set([f"vlan {vlan_id}", f"name {vlan_name}"])
                    ssh.send_command(save_cmd)
                    formated_result = result.split('\n')
                    flash(formated_result)
        elif command == 'snmp':
            snmp = request.form['snmp_str']
            for device in devices:
                if device['hostname'] == hostname_cmd:
                    if device['type'] == "nxos":
                        save_cmd = "copy running-config startup-config"
                    else:
                        save_cmd = "write"
                    device.pop('hostname')
                    device.pop('type')
                    ssh = ConnectHandler(**device)
                    ssh.enable()
                    result = ssh.send_config_set([f"snmp-server community {snmp} ro"])
                    ssh.send_command(save_cmd)
                    formated_result = result.split('\n')
                    flash(formated_result)
        elif command == 'log':
            log_ip = request.form['log-ip']
            for device in devices:
                if device['hostname'] == hostname_cmd:
                    if device['type'] == "nxos":
                        save_cmd = "copy running-config startup-config"
                    else:
                        save_cmd = "write"
                    if device['type'] == 'nxos':
                        commands = ["logging server 192.168.90.23",
                                    "logging module 3",
                                    "logging level aaa 2",
                                    "logging timestamp milliseconds"]
                    else:
                        commands = ["logging host 192.168.90.23",
                                    "logging trap 2",
                                    "logging on"]
                    device.pop('hostname')
                    device.pop('type')
                    ssh = ConnectHandler(**device)
                    ssh.enable()
                    result = ssh.send_config_set(commands)
                    ssh.send_command(save_cmd)
                    formated_result = result.split('\n')
                    flash(formated_result)
        elif command == 'ntp':
            ntp = request.form['ntp']
            for device in devices:
                if device['hostname'] == hostname_cmd:
                    if device['type'] == "nxos":
                        save_cmd = "copy running-config startup-config"
                    else:
                        save_cmd = "write"
                    device.pop('hostname')
                    device.pop('type')
                    ssh = ConnectHandler(**device)
                    ssh.enable()
                    result = ssh.send_config_set([f"ntp server {ntp}"])
                    ssh.send_command(save_cmd)
                    formated_result = result.split('\n')
                    flash(formated_result)
        elif command == 'custom':
            for device in devices:
                cmd = request.form['custom_cmd']
                if device['hostname'] == hostname_cmd:
                    if device['type'] == "nxos":
                        save_cmd = "copy running-config startup-config"
                    else:
                        save_cmd = "write"
                    device.pop('hostname')
                    device.pop('type')
                    ssh = ConnectHandler(**device)
                    ssh.enable()
                    result = ssh.send_config_set([f"{cmd}"])
                    ssh.send_command(save_cmd)
                    formated_result = result.split('\n')
                    flash(formated_result)
        print(request.form)
        # try:
        #     url = request.form['url']
        #     login = request.form['login']
        #     password = request.form['password']
        #
        #     connect_to_lab(url,login,password)
        #
        #     return render_template('connected.html', menu = menu, lab_title = lab_title, lab_nodes = lab_nodes)
        # except Exception as err:
        #     print(err)
        #     return render_template('error.html', error = err)

    return render_template('send_conf_command.html',menu = menu)

@app.route("/send_cmd",methods=["GET","POST"])
def perform_command():
    if request.method == 'POST':
        hostname_cmd = request.form['hostname']
        print(request.form)
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        devices = [
            {
                'device_type': 'cisco_ios',
                'host': '10.10.20.175',
                'type': 'ios',
                'username': 'cisco',
                'password': 'cisco',
                'secret': 'cisco',
                'port': 22,
                'hostname': 'dist-rtr01',
            },
            {
                'device_type': 'cisco_ios',
                'host': '10.10.20.176',
                'type': 'ios',
                'username': 'cisco',
                'password': 'cisco',
                'secret': 'cisco',
                'port': 22,
                'hostname': 'dist-rtr02',
            },
            {
                'device_type': 'cisco_ios',
                'host': '10.10.20.177',
                'type': 'nxos',
                'username': 'cisco',
                'password': 'cisco',
                'secret': 'cisco',
                'port': 22,
                'hostname': 'dist-sw01',
            },
            {
                'device_type': 'cisco_ios',
                'host': '10.10.20.178',
                'type': 'nxos',
                'username': 'cisco',
                'password': 'cisco',
                'secret': 'cisco',
                'port': 22,
                'hostname': 'dist-sw02',
            }]
        try:
            custom_cmd = request.form['custom_cmd']
            for device in devices:
                if device['hostname'] == hostname_cmd:
                    device.pop('hostname')
                    device.pop('type')
                    ssh = ConnectHandler(**device)
                    ssh.enable()
                    result = ssh.send_command(custom_cmd)
                    formated_result = result.split('\n')
                    flash(formated_result)
        except Exception as err:
            print(err)
            return render_template('error.html', error=err)

    return render_template('send_command.html',menu = menu)



if __name__ == "__main__":
    app.run(debug=True)