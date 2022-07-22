from netmiko import ConnectHandler
import elements
from rich import print
from concurrent.futures import ThreadPoolExecutor
import json

new_elements = []


def getapnlist(elem):
    net_connect = ConnectHandler(
        device_type="ericsson_ipos",
        host=elem['ip'],
        username="report",
        password="Eric@2020",
    )
    com = 'show running-config | include apn'
    command = net_connect.send_command(com, use_ttp=True, ttp_template="ttp_template\\apn_list.ttp")
    my_dict = {}
    my_dict['hostname'] = elem['hostname']
    my_dict['ip'] = elem['ip']
    apn_list = []
    chunked_list = []
    for result in command[0]:
        for apn in result['apns']:
            apn_list.append(apn['apn'])
        
        chunk_size = 25
        for i in range(0, len(apn_list), chunk_size):
            chunked_list.append(apn_list[i:i+chunk_size])
        for ls in chunked_list:
            my_dict = {}
            my_dict['hostname'] = elem['hostname']
            my_dict['ip'] = elem['ip']
            my_dict['apns'] = ls
            print(my_dict)
            new_elements.append(my_dict)


with ThreadPoolExecutor(max_workers=8) as executor:
    executor.map(getapnlist, [elem for elem in elements.elements])

with open("elements.json", "w") as final:
   json.dump(new_elements, final, indent=2)
# final = json.dumps(new_elements, indent=2)
# print(final)