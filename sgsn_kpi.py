from netmiko import ConnectHandler
import test_elements
from datetime import date, datetime
from influxdb import InfluxDBClient
from rich import print
import time
from concurrent.futures import ThreadPoolExecutor

now = datetime.now()

client = InfluxDBClient(host='172.21.164.231', port=8086, username='telegraf', password='telegraf', ssl=False)
client.switch_database('telegraf')

sgsn_stats = []
def sgsnstatus(elem):
    net_connect = ConnectHandler(
        device_type="ericsson_ipos",
        host=elem['ip'],
        username="report",
        password="Eric@2020",
    )
    command = 'pdc_kpi.pl -l'
    kpis = net_connect.send_command(command) #, use_ttp=True, ttp_template="/home/system/scripts/m2m/ttp_template/sgsn_kpi.ttp")
    print(kpis)
    for kpi in kpis[0]:
        try:
            my_dict = {}
            fields = {}
            tags = {}
            tags['sgsn'] = elem['hostname']
            my_dict['measurement'] = 'sgsn_statistics'
            fields['sau_catm'] = int(kpi['sau_catm'])
            fields['sau_nb'] = int(kpi['sau_nb'])
            fields['sub_lte'] = int(kpi['sub_lte'])
            fields['sau_sgs_lte'] = int(kpi['sau_sgs_lte'])
            fields['sau_s102_lte'] = int(kpi['sau_s102_lte'])
            fields['sau_nr_lte'] = int(kpi['sau_nr_lte'])
            fields['sau_lte'] = int(kpi['sau_lte'])
            fields['active_pdn_lte'] = int(kpi['active_pdn_lte'])
            fields['active_bearer_lte'] = int(kpi['active_bearer_lte'])
            fields['sds_wcdma'] = int(kpi['sds_wcdma'])
            fields['sau_wcdma'] = int(kpi['sau_wcdma'])
            fields['pdp_wcdma'] = int(kpi['pdp_wcdma'])
            fields['sds_gsm'] = int(kpi['sds_gsm'])
            fields['sau_gsm'] = int(kpi['sau_gsm'])
            fields['pdp_gsm'] = int(kpi['pdp_gsm'])
            fields['uplink_mbps_s11u'] = float(kpi['uplink_mbps_s11u'])
            fields['uplink_kpps_s11u'] = float(kpi['uplink_kpps_s11u'])
            fields['uplink_avg_s11u'] = float(kpi['uplink_avg_s11u'])
            fields['downlink_mbps_s11u'] = float(kpi['downlink_mbps_s11u'])
            fields['downlink_kpps_s11u'] = float(kpi['downlink_kpps_s11u'])
            fields['downlink_avg_s11u'] = float(kpi['downlink_avg_s11u'])
            fields['uplink_mbps_s4'] = float(kpi['uplink_mbps_s4'])
            fields['uplink_kpps_s4'] = float(kpi['uplink_kpps_s4'])
            fields['uplink_avg_s4'] = float(kpi['uplink_avg_s4'])
            fields['downlink_mbps_s4'] = float(kpi['downlink_mbps_s4'])
            fields['downlink_kpps_s4'] = float(kpi['downlink_kpps_s4'])
            fields['downlink_avg_s4'] = float(kpi['downlink_avg_s4'])
            fields['uplink_mbps_gn'] = float(kpi['uplink_mbps_gn'])
            fields['uplink_kpps_gn'] = float(kpi['uplink_kpps_gn'])
            fields['uplink_avg_gn'] = float(kpi['uplink_avg_gn'])
            fields['downlink_mbps_gn'] = float(kpi['downlink_mbps_gn'])
            fields['downlink_kpps_gn'] = float(kpi['downlink_kpps_gn'])
            fields['downlink_avg_gn'] = float(kpi['downlink_avg_gn'])
            fields['uplink_mbps_iu'] = float(kpi['uplink_mbps_iu'])
            fields['uplink_kpps_iu'] = float(kpi['uplink_kpps_iu'])
            fields['uplink_avg_iu'] = float(kpi['uplink_avg_iu'])
            fields['downlink_mbps_iu'] = float(kpi['downlink_mbps_iu'])
            fields['downlink_kpps_iu'] = float(kpi['downlink_kpps_iu'])
            fields['downlink_avg_iu'] = float(kpi['downlink_avg_iu'])
            fields['uplink_mbps_gb'] = float(kpi['uplink_mbps_gb'])
            fields['uplink_kpps_gb'] = float(kpi['uplink_kpps_gb'])
            fields['uplink_avg_gb'] = float(kpi['uplink_avg_gb'])
            fields['downlink_mbps_gb'] = float(kpi['downlink_mbps_gb'])
            fields['downlink_kpps_gb'] = float(kpi['downlink_kpps_gb'])
            fields['downlink_avg_gb'] = float(kpi['downlink_avg_gb'])
            fields['x2_handover_catm'] = float(kpi['x2_handover_catm'].strip('%'))
            fields['s1_handover_catm'] = float(kpi['s1_handover_catm'].strip('%'))
            fields['paging_sms_catm'] = float(kpi['paging_sms_catm'].strip('%'))
            fields['paging_catm'] = float(kpi['paging_catm'].strip('%'))
            fields['intra_mme_tau_catm'] = float(kpi['intra_mme_tau_catm'].strip('%'))
            fields['inter_mme_tau_catm'] = float(kpi['inter_mme_tau_catm'].strip('%'))
            fields['attach_catm'] = float(kpi['attach_catm'].strip('%'))
            fields['t6a_mt_data_request'] = float(kpi['t6a_mt_data_request'].strip('%'))
            fields['t6a_mo_data_request'] = float(kpi['t6a_mo_data_request'].strip('%'))
            fields['paging_sms_nb'] = float(kpi['paging_sms_nb'].strip('%'))
            fields['paging_nb'] = float(kpi['paging_nb'].strip('%'))
            fields['intra_mme_tau_nb'] = float(kpi['intra_mme_tau_nb'].strip('%'))
            fields['inter_mme_tau_nb'] = float(kpi['inter_mme_tau_nb'].strip('%'))
            fields['enb_cp_relocation_nb'] = float(kpi['enb_cp_relocation_nb'].strip('%'))
            fields['default_bearer_nonip_scef_act'] = float(kpi['default_bearer_nonip_scef_act'].strip('%'))
            fields['default_bearer_nonip_act_nb'] = float(kpi['default_bearer_nonip_act_nb'].strip('%'))
            fields['control_plane_service_request'] = float(kpi['control_plane_service_request'].strip('%'))
            fields['attach_nb'] = float(kpi['attach_nb'].strip('%'))
            fields['x2_handover_lte'] = float(kpi['x2_handover_lte'].strip('%'))
            fields['srvcc_w_lte'] = float(kpi['srvcc_w_lte'].strip('%'))
            fields['srvcc_g_lte'] = float(kpi['srvcc_g_lte'].strip('%'))
            fields['service_request_lte'] = float(kpi['service_request_lte'].strip('%'))
            fields['s1_handover_lte'] = float(kpi['s1_handover_lte'].strip('%'))
            fields['paging_sms_lte'] = float(kpi['paging_sms_lte'].strip('%'))
            fields['paging_lte'] = float(kpi['paging_lte'].strip('%'))
            fields['location_update_lte'] = float(kpi['location_update_lte'].strip('%'))
            fields['irat_ho_mme_target_lte'] = float(kpi['irat_ho_mme_target_lte'].strip('%'))
            fields['irat_ho_mme_source_lte'] = float(kpi['irat_ho_mme_source_lte'].strip('%'))
            fields['intra_mme_tau_lte'] = float(kpi['intra_mme_tau_lte'].strip('%'))
            fields['intra_isc_tau_lte'] = float(kpi['intra_isc_tau_lte'].strip('%'))
            fields['intra_5gs_to_eps_n26_tau_lte'] = float(kpi['intra_5gs_to_eps_n26_tau_lte'].strip('%'))
            fields['inter_mme_tau_lte'] = float(kpi['inter_mme_tau_lte'].strip('%'))
            fields['inter_isc_tau_lte'] = float(kpi['inter_isc_tau_lte'].strip('%'))
            fields['inter_5gs_to_eps_n26_tau_lte'] = float(kpi['inter_5gs_to_eps_n26_tau_lte'].strip('%'))
            fields['gbr_bearer_activation_lte'] = float(kpi['gbr_bearer_activation_lte'].strip('%'))
            fields['fivegs_to_eps_n26_handover_kpi_lte'] = float(kpi['fivegs_to_eps_n26_handover_kpi_lte'].strip('%'))
            fields['csfb_wg_lte'] = float(kpi['csfb_wg_lte'].strip('%'))
            fields['csfb_1xrtt_lte'] = float(kpi['csfb_1xrtt_lte'].strip('%'))
            fields['bearer_establishment_lte'] = float(kpi['bearer_establishment_lte'].strip('%'))
            fields['attach_lte'] = float(kpi['attach_lte'].strip('%'))
            fields['service_request_wcdma'] = float(kpi['service_request_wcdma'].strip('%'))
            fields['rab_establishment_wcdma'] = float(kpi['rab_establishment_wcdma'].strip('%'))
            fields['pdp_cut_off_wcdma'] = float(kpi['pdp_cut_off_wcdma'].strip('%'))
            fields['pdp_activation_wcdma'] = float(kpi['pdp_activation_wcdma'].strip('%'))
            fields['paging_wcdma'] = float(kpi['paging_wcdma'].strip('%'))
            fields['israu_wcdma'] = float(kpi['israu_wcdma'].strip('%'))
            fields['intra_rau_wcdma'] = float(kpi['intra_rau_wcdma'].strip('%'))
            fields['attach_wcdma'] = float(kpi['attach_wcdma'].strip('%'))
            fields['pdp_cut_off_gsm'] = float(kpi['pdp_cut_off_gsm'].strip('%'))
            fields['pdp_activation_gsm'] = float(kpi['pdp_activation_gsm'].strip('%'))
            fields['paging_gsm'] = float(kpi['paging_gsm'].strip('%'))
            fields['israu_gsm'] = float(kpi['israu_gsm'].strip('%'))
            fields['intra_rau_gsm'] = float(kpi['intra_rau_gsm'].strip('%'))
            fields['attach_gsm'] = float(kpi['attach_gsm'].strip('%'))
            my_dict['fields'] = fields
            my_dict['tags'] = tags
            sgsn_stats.append(my_dict)
        except Exception as xx:
            print(xx)
            pass
    net_connect.disconnect()


with ThreadPoolExecutor(max_workers=8) as executor:
    executor.map(sgsnstatus, [elem for elem in test_elements.sgsn])

client.write_points(sgsn_stats)
print(sgsn_stats)
