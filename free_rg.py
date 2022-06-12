from netmiko import ConnectHandler
import elements_rg
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
        try:
            my_dict = {}
            tags = {}
            tags['apn_name'] = apn
            tags['epg'] = elem['hostname']
            command = f'epg pgw apn {apn} statistics'
            sfp = net_connect.send_command(command, use_ttp=True, ttp_template="/home/system/scripts/m2m/ttp_template/free_rg.ttp")
            print(sfp)
            # for d in sfp[0]:
            #     down = 0
            #     up = 0
            #     try:
            #         fields = {}
            #         my_dict['measurement'] = measure
            #         my_dict['tags'] = tags
            #         for t in d['traffic']:
            #             down = down + int(t['downlink'])
            #             up = up + int(t['uplink'])
            #         fields['downlink'] = down
            #         fields['uplink'] = up
            #         fields['pdp'] = d['pdp']['pdp_active']
            #         fields['pdn'] = d['pdp']['pdn']
            #         fields['ue'] = d['pdp']['ue_count']
            #         my_dict['fields'] = fields
            #         apn_stastics1.append(my_dict)
                # except Exception as xx: #(KeyError, TypeError):
                #     print(xx)
                    # tags['apn_name'] = apn
                    # tags['epg'] = elem['hostname']
                    # my_dict['measurement'] = measure
                    # my_dict['tags'] = tags
                    # fields['downlink'] = 0
                    # fields['uplink'] = 0
                    # fields['pdp'] = d['pdp']['pdp_active']
                    # fields['pdn'] = d['pdp']['pdn']
                    # fields['ue'] = d['pdp']['ue_count']
                    # my_dict['fields'] = fields
                    # apn_stastics1.append(my_dict)
        except Exception as xx:
            pass
    net_connect.disconnect()


with ThreadPoolExecutor(max_workers=8) as executor:
    executor.map(getapnstats, [elem for elem in elements_rg.elements])