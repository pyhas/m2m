from netmiko import ConnectHandler
import elements
from datetime import date, datetime
from influxdb import InfluxDBClient
from rich import print
import time
from concurrent.futures import ThreadPoolExecutor

client = InfluxDBClient(host='172.21.164.231', port=8086, username='telegraf', password='telegraf', ssl=False)
client.switch_database('telegraf')

now = datetime.now()
measure = 'apn_statistics'
apn_stastics1 = []
apn_stastics5 = []


def getapnstats(elem):
    net_connect = ConnectHandler(
        device_type="ericsson_ipos",
        host=elem['ip'],
        username="report",
        password="Eric@2020",
    )
    for apn in elem['apns']:
        my_dict = {}
        tags = {}
        tags['apn_name'] = apn
        tags['epg'] = elem['hostname']
        command = f'epg pgw apn {apn} statistics'
        sfp = net_connect.send_command(command, use_ttp=True, ttp_template="ttp_template/statstics.ttp")
        for d in sfp[0]:
            down = 0
            up = 0
            try:
                fields = {}
                my_dict['measurement'] = measure
                my_dict['tags'] = tags
                for t in d['traffic']:
                    down = down + int(t['downlink'])
                    up = up + int(t['uplink'])
                fields['downlink'] = down
                fields['uplink'] = up
                my_dict['fields'] = fields
                apn_stastics1.append(my_dict)
            except (KeyError, TypeError):
                tags['apn_name'] = apn
                tags['epg'] = elem['hostname']
                my_dict['measurement'] = measure
                my_dict['tags'] = tags
                fields['downlink'] = 0
                fields['uplink'] = 0
                my_dict['fields'] = fields
                apn_stastics1.append(my_dict)

    net_connect.disconnect()
    return apn_stastics1


def getapnstats5(elem):
    net_connect = ConnectHandler(
        device_type="ericsson_ipos",
        host=elem['ip'],
        username="report",
        password="Eric@2020",
    )
    for apn in elem['apns']:
        my_dict = {}
        tags = {}
        tags['apn_name'] = apn
        tags['epg'] = elem['hostname']
        command = f'epg pgw apn {apn} statistics'
        sfp = net_connect.send_command(command, use_ttp=True, tp_template="ttp_template/statstics.ttp")
        for d in sfp[0]:
            down = 0
            up = 0
            try:
                fields = {}
                my_dict['measurement'] = measure
                my_dict['tags'] = tags
                for t in d['traffic']:
                    down = down + int(t['downlink'])
                    up = up + int(t['uplink'])
                fields['downlink'] = down
                fields['uplink'] = up
                my_dict['fields'] = fields
                apn_stastics5.append(my_dict)
            except (KeyError, TypeError):
                tags['apn_name'] = apn
                tags['epg'] = elem['hostname']
                my_dict['measurement'] = measure
                my_dict['tags'] = tags
                fields['downlink'] = 0
                fields['uplink'] = 0
                my_dict['fields'] = fields
                apn_stastics5.append(my_dict)

    net_connect.disconnect()
    return apn_stastics5


with ThreadPoolExecutor(max_workers=8) as executor:
    executor.map(getapnstats, [elem for elem in elements.elements])

time.sleep(300)

with ThreadPoolExecutor(max_workers=8) as executor:
    executor.map(getapnstats5, [elem for elem in elements.elements])

apn_stastics = []
for s in apn_stastics1:
    for d in apn_stastics5:
        my_dict = {}
        fields = {}
        if s['tags']['apn_name'] == d['tags']['apn_name'] and s['tags']['epg'] == d['tags']['epg']:
            my_dict['measurement'] = s['measurement']
            my_dict['tags'] = s['tags']
            fields['downlink'] = int(((d['fields']['downlink'] - s['fields']['downlink']) / 300) * 8)
            fields['uplink'] = int(((d['fields']['uplink'] - s['fields']['uplink']) / 300) * 8)
            my_dict['fields'] = fields
            apn_stastics.append(my_dict)

client.write_points(apn_stastics)
delta = datetime.now() - now
# print(apn_stastics1, apn_stastics5)
print(delta)

