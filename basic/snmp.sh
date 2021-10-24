export ANSIBLE_HOST_KEY_CHECKING=False
echo [lab] > hosts
echo 10.10.20.17[5:8] >> hosts
echo [all:vars] >> hosts
echo ansible_user=cisco >> hosts
echo ansible_ssh_pass=cisco >> hosts
echo ansible_network_os=ios >> hosts
echo ansible_connection=network_cli >> hosts
echo "Host file Created"
echo --- > config.yml
echo "- hosts: lab" >> config.yml
echo "  gather_facts: false" >> config.yml
echo "  tasks:" >> config.yml
echo "    - name: Update SNMP" >> config.yml
echo "      ios_config:" >> config.yml
echo "        lines:" >> config.yml
echo "          - snmp-server community TEST-CS-Ansible rw" >> config.yml
echo "        save_when: modified" >> config.yml
echo "Playbook cretaed"
ansible-playbook config.yml -i hosts
echo "Ansible tasks Done"
rm hosts
rm config.yml
echo "Temp Files removed"
