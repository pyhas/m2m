from netmiko import ConnectHandler
import elements_rg
from influxdb import InfluxDBClient
from rich import print
from concurrent.futures import ThreadPoolExecutor

client = InfluxDBClient(host='172.21.164.231', port=8086, username='telegraf', password='telegraf', ssl=False)
client.switch_database('telegraf')

measure = 'free_rg'
freerg_stat = []
rgs = [16, 341, 358, 359, 930, 959, 975, 985, 995, 1000]

def getapnstats(elem):
    net_connect = ConnectHandler(
        device_type="ericsson_ipos",
        host=elem['ip'],
        username="report",
        password="Eric@2020",
    )
    for apn in elem['apns']:
        try:
            command = f'epg pgw apn {apn} statistics'
            sfp = net_connect.send_command(command, use_ttp=True, ttp_template="ttp_template/free_rg.ttp")
            for d in sfp[0]:
                try:
                    for t in d['traffic']:
                        for rg in rgs:
                            if rg == int(t['rg']):
                                fields = {}
                                tags = {}
                                my_dict = {}
                                my_dict['measurement'] = measure
                                tags['apn'] = apn
                                tags['epg'] = elem['hostname']
                                tags['rg'] = t['rg']
                                fields['downlink'] = int(t['downlink'])
                                fields['uplink'] = int(t['uplink'])
                                my_dict['fields'] = fields
                                my_dict['tags'] = tags
                                freerg_stat.append(my_dict)                                

                except Exception as xx:
                    print(xx)
        except Exception as xx:
            pass
    net_connect.disconnect()


with ThreadPoolExecutor(max_workers=8) as executor:
    executor.map(getapnstats, [elem for elem in elements_rg.elements])

client.write_points(freerg_stat)
print(freerg_stat)