# UCODE_NETWORKING
UCODE DEVOPS NETWORK CHALANGE

# Before working on project
To use code provided you need to install some packages and [Python 3](https://www.python.org/downloads/)

## Package Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install packages
```bash
pip install ansible
pip install napalm
pip install tabulate
pip install flask
pip install virl2_client
```

Install [Cisco ios configuration module for Ansible](https://docs.ansible.com/ansible/latest/collections/cisco/ios/ios_config_module.html)
```bash
ansible-galaxy collection install cisco.ios
```
## Script Usage

All *.sh scripts must be excutable or can be run as:
```bash
sh some_script.sh
```
Or directly
```bash
./some_script.sh
```
## Cisco Lab on DEVNET
To test solution you need to register on [Cisco DEVNET PORTAL](https://devnetsandbox.cisco.com/)
Then you need to reserv lab [Cisco Modeling Labs Enterprise](https://devnetsandbox.cisco.com/RM/Diagram/Index/45100600-b413-4471-b28e-b014eb824555?diagramType=Topology).

In ten minutes you should get link on your email to connect with Cisco ANYConnect software.

Make shure that you are connected to lab and can ping devices from lab 10.10.20.175-10.10.20.178

## Scripts runtime
When you are lonching scripts it will create host file and yml playbook for ansible. Then execute that playbook with ansible.

All info will be seen in console while executing. After script finishes it removes all files.

Scripts will work only for [Cisco Modeling Labs Enterprise](https://devnetsandbox.cisco.com/RM/Diagram/Index/45100600-b413-4471-b28e-b014eb824555?diagramType=Topology) and it is hardocded. But you may change IPs and device model in .py files.

Be avare that script changes system var and it may lead to security issues
```bash
export ANSIBLE_HOST_KEY_CHECKING=False
```

# Advanced section

To implement advanced part you need [Flask framework](https://flask.palletsprojects.com/en/2.0.x/)
It may be installed via [pip](https://pip.pypa.io/en/stable/). Refer to package installation.

## Flask runtime

Before starting advanced.py make shure that you connected to [Cisco Modeling Labs Enterprise](https://devnetsandbox.cisco.com/RM/Diagram/Index/45100600-b413-4471-b28e-b014eb824555?diagramType=Topology) via Any connect.
First page allow to connect to the lab, all setings are predefined but may be changed as needed.

### Info page

On info page you can see all device available in the lab.
Some options are not available for all host. But sholud work for switches and routers
<img width="1436" alt="Screenshot 2021-10-24 в 23 03 02" src="https://user-images.githubusercontent.com/4414979/138610813-b6b0ca54-3053-45f9-a22a-aa73a02be6ec.png">

### Config command page

Devices are predefind from [Cisco Modeling Labs Enterprise](https://devnetsandbox.cisco.com/RM/Diagram/Index/45100600-b413-4471-b28e-b014eb824555?diagramType=Topology) and can be changed in code.
<img width="1430" alt="image" src="https://user-images.githubusercontent.com/4414979/138610841-e388c523-09d2-428b-95ff-ba10cdd63075.png">

Basic URL for command page is [config commands](http://127.0.0.1:5000/send_conf). Therea are predefind commands and you can excute your own command choosing "Custom command"
<img width="1434" alt="Screenshot 2021-10-24 в 23 05 36" src="https://user-images.githubusercontent.com/4414979/138610887-86bde8ff-a76a-4f1c-a7ca-2c26473f45f3.png">

### Config command page

Devices are predefind from [Cisco Modeling Labs Enterprise](https://devnetsandbox.cisco.com/RM/Diagram/Index/45100600-b413-4471-b28e-b014eb824555?diagramType=Topology) and can be changed in code.

Basic URL for command page is [enable commands](http://127.0.0.1:5000/send_cmd)
<img width="1429" alt="Screenshot 2021-10-24 в 23 06 34" src="https://user-images.githubusercontent.com/4414979/138610957-03315450-67a1-4e72-af00-411316a71cdb.png">

## Contributing
Pull requests are welcome. And all are welcome to discuss what you would like to change.

## License
No licence. You can use the code as you want.
