export ANSIBLE_HOST_KEY_CHECKING=False
echo [lab-router] > hosts
echo 10.10.20.17[5:6] >> hosts
echo [lab-sw] >> hosts
echo 10.10.20.17[7:8] >> hosts
echo [all:vars] >> hosts
echo ansible_user=cisco >> hosts
echo ansible_ssh_pass=cisco >> hosts
echo ansible_network_os=ios >> hosts
echo ansible_connection=network_cli >> hosts
echo "Host file Created"
echo --- > config.yml
echo "- hosts: lab-sw" >> config.yml
echo "  gather_facts: false" >> config.yml
echo "  tasks:" >> config.yml
echo "    - name: Configure logging for switches" >> config.yml
echo "      ios_config:" >> config.yml
echo "        lines:" >> config.yml
echo "          - logging server 192.168.90.23" >> config.yml
echo "          - logging module 3" >> config.yml
echo "          - logging level aaa 2" >> config.yml
echo "          - logging timestamp milliseconds" >> config.yml
echo "          - logging source-interface Loopback0" >> config.yml
echo "        save_when: modified" >> config.yml
echo "- hosts: lab-router" >> config.yml
echo "  gather_facts: false" >> config.yml
echo "  tasks:" >> config.yml
echo "    - name: Configure logging for router" >> config.yml
echo "      ios_config:" >> config.yml
echo "        lines:" >> config.yml
echo "          - logging host 192.168.90.23" >> config.yml
echo "          - logging trap 2" >> config.yml
echo "          - logging on" >> config.yml
echo "        save_when: modified" >> config.yml
echo "Playbook cretaed"
ansible-playbook config.yml -i hosts
echo "Ansible tasks Done"
rm hosts
rm config.yml
echo "Temp Files removed"
