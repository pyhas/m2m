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
measure = 'apn_statistics_test'
apn_stastics = []


def getapnstats(elem):
    net_connect = ConnectHandler(
        device_type="ericsson_ipos",
        host=elem['ip'],
        username="report",
        password="Eric@2020",
    )
    for apn in elem['apns']:
        try:
            my_dict = {}
            tags = {}
            tags['apn_name'] = apn
            tags['epg'] = elem['hostname']
            command = f'epg pgw apn {apn} statistics'
            sfp = net_connect.send_command(command, use_ttp=True, ttp_template="/home/system/scripts/m2m/ttp_template/test_statstics.ttp")
            for d in sfp[0]:
                fields = {}
                my_dict['measurement'] = measure
                my_dict['tags'] = tags
                for t in d['traffic']:
                    try:
                        fields['downlink'] = int(t['downlink'])
                    except:
                        pass
                    try:
                        fields['uplink'] = int(t['uplink'])
                    except:
                        pass
                fields['pdp'] = int(d['pdp']['pdp_active'])
                fields['pdn'] = int(d['pdp']['pdn'])
                fields['ue'] = int(d['pdp']['ue_count'])
                fields['gx-ccr-termination-failed'] = 0
                fields['gx-ccr-update-failed'] = 0
                fields['gx-ccr-initial-failed'] = 0
                fields['gy-ccr-termination-failed'] = 0
                fields['gy-ccr-update-failed'] = 0
                fields['gy-ccr-initial-failed'] = 0
                try:
                    for x in d['gx']:
                        fields['gx-ccr-termination-failed'] += int(x['ccr-termination-failed'])
                        fields['gx-ccr-update-failed'] += int(x['ccr-update-failed'])
                        fields['gx-ccr-initial-failed'] += int(x['ccr-initial-failed'])
                except:
                    pass
                try:
                    for y in d['gy']:
                        fields['gy-ccr-termination-failed'] += int(y['ccr-termination-failed'])
                        fields['gy-ccr-update-failed'] += int(y['ccr-update-failed'])
                        fields['gy-ccr-initial-failed'] += int(y['ccr-initial-failed'])
                except:
                    pass
                my_dict['fields'] = fields
                apn_stastics.append(my_dict)
        except Exception as xx:
            pass
    net_connect.disconnect()

with ThreadPoolExecutor(max_workers=8) as executor:
    executor.map(getapnstats, [elem for elem in elements.elements])

client.write_points(apn_stastics)


delta = datetime.now() - now
print(apn_stastics)
