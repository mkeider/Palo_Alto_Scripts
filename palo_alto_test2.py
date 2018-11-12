from getpass import getpass
import netmiko
import sys
import json


def get_input(prompt=''):
    try:
        line = input(prompt)
    except NameError:
        line = input(prompt)
    return line

def get_credentials():
    username = get_input('Enter Username: ')
    password = None
    while not password:
        password = getpass()
    return username, password

username, password = get_credentials()



#Device ssh timeout and ssh authentication error handleing
netmiko_exceptions = (netmiko.ssh_exception.NetMikoTimeoutException,netmiko.ssh_exception.NetMikoAuthenticationException)

ssh_results = {'Successful':[], 'Failed':[]}

system = []

#opens json formatted device file for Palo Alto devices to be examined
with open('device_paloalto_panos.json') as dev_file:
    devices = json.load(dev_file)




for device in devices:
    device['username'] = username
    device['password'] = password
    try:
        print('~' * 79)
        print('Connecting to device', device['ip'])
        connection = netmiko.ConnectHandler(**device)
        system.append(connection.find_prompt())
        output = connection.send_command("show clock")

        for item in output:
            system.append(item)
        system.append('\n')

        connection.disconnect()
        ssh_results['Successful'].append(device['ip'])

    except netmiko_exceptions as e:
        print('Failed to', device, e)
        ssh_results['Failed'].append('.'.join((device['ip'], str(e))))


system_str = ''.join(system)
print(type(system_str))

#ssh connection results to json file
print(json.dumps(ssh_results, indent=2))
with open('palo_alto_clock_ssh_results.json','w') as results_file:
    json.dump(ssh_results, results_file, indent=2)

#Data output to txt file
with open('palo_alto_clock.txt', 'w') as f:
    f.write(system_str)

