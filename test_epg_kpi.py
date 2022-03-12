from netmiko import ConnectHandler
import elements
from datetime import date, datetime
from influxdb import InfluxDBClient
from rich import print
import time
from concurrent.futures import ThreadPoolExecutor

now = datetime.now()

client = InfluxDBClient(host='172.21.164.231', port=8086, username='telegraf', password='telegraf', ssl=False)
client.switch_database('telegraf')

epg_stats = []
def getapnstats(elem):
    net_connect = ConnectHandler(
        device_type="ericsson_ipos",
        host=elem['ip'],
        username="report",
        password="Eric@2020",
    )
    command = 'epg node kpi'
    sfp = net_connect.send_command(command, use_ttp=True, ttp_template="/home/system/scripts/m2m/ttp_template/test_epg_kpi.ttp")
    my_dict = {}
    fields = {}
    tags = {}
    for d in sfp[0]:
        my_dict['measurement'] = 'epg_statistics_test'
        tags['epg'] = elem['hostname']	
        fields['GgsnPdpContexts'] = int(d['kpi']['GgsnPdpContexts'])
        fields['PgwBearers'] = int(d['kpi']['PgwBearers'])
        fields['GgsnCreatePdpCtxFR'] = float(d['kpi']['GgsnCreatePdpCtxFR'].strip('%'))
        fields['GgsnUpdatePdpCtxFR'] = float(d['kpi']['GgsnUpdatePdpCtxFR'].strip('%'))
        fields['PgwS5CreateSessionFR'] = float(d['kpi']['PgwS5CreateSessionFR'].strip('%'))
        fields['PgwS5ModifyBearerFR'] = float(d['kpi']['PgwS5ModifyBearerFR'].strip('%'))
        fields['PgwGgsnDlThroughput'] = float(d['kpi']['PgwGgsnDlThroughput'])
        fields['PgwGgsnUlThroughput'] = float(d['kpi']['PgwGgsnUlThroughput'])
        fields['SgwSubscribers'] = int(d['kpi']['SgwSubscribers'])
        fields['SgwConnectedSubscribers'] = int(d['kpi']['SgwConnectedSubscribers'])
        fields['SgwPdnConnections'] = int(d['kpi']['SgwPdnConnections'])
        fields['SgwBearers'] = int(d['kpi']['SgwBearers'])
        fields['SgwS4S11CreateSessionFR'] = float(d['kpi']['SgwS4S11CreateSessionFR'].strip('%'))
        fields['SgwS4S11ModifyBearerFR'] = float(d['kpi']['SgwS4S11ModifyBearerFR'].strip('%'))
        fields['SgwS4S11DlDataNotificationFR'] = float(d['kpi']['SgwS4S11DlDataNotificationFR'].strip('%'))
        fields['SgwDlThroughputS1uS4S12'] = float(d['kpi']['SgwDlThroughputS1uS4S12'])
        fields['SgwUlThroughputS5S8'] = float(d['kpi']['SgwUlThroughputS5S8'])
        my_dict['fields'] = fields
        my_dict['tags'] = tags
        epg_stats.append(my_dict)
        for cpu in d['cpu']:
            my_cpu = {}
            tags_cpu = {}
            fields_cpu = {}
            my_cpu['measurement'] = 'epg_statistics_test'
            tags_cpu['board'] = cpu['board']
            fields_cpu['cpu'] = int(cpu['cpu'].split('%')[0])
            tags_cpu['epg'] = elem['hostname']
            my_cpu['tags'] = tags_cpu
            my_cpu['fields'] = fields_cpu
            epg_stats.append(my_cpu)
    net_connect.disconnect()


with ThreadPoolExecutor(max_workers=8) as executor:
    executor.map(getapnstats, [elem for elem in elements.elements])

client.write_points(epg_stats)
delta = datetime.now() - now

print(epg_stats)
print(delta)
