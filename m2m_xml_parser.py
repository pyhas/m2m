import xmltodict, json

with open("xmlfiles/A20220113.0945+0300-1000+0300_BISCex-EPG01.xml") as xml_file:
    data_dict = xmltodict.parse(xml_file.read())

xml_file.close()
# for d in data_dict["measCollecFile"]['measData']["measInfo"]:
# #     # if d["@measInfoId"] == "pgw-traffic-gngp-apn":
#         print(d)
    # for a in d:
    #     # if a == 'ggsn-uplink-traffic-info':
    #         print(a)
        # print(d["measValue"])
# print(data_dict["measCollecFile"]['measData']["measInfo"])
# json_data = json.dumps(data_dict, indent=2)
# with open("data.json", "w") as json_file:
#     json_file.write(json_data)
# for d in json_data["measCollecFile"]:
#     print(d)
# print(json_data["measCollecFile"]['measData']["measInfo"])
# print(json_data)
f = open('data.json')
json_data = json.load(f)
for d in json_data["measCollecFile"]['measData']["measInfo"]:
    # for a in d:
    #     print(a)
    if d["@measInfoId"] == "pgw-apn-rating-group":
        for a in d["measValue"]:
            print(f'apn-name {a["@measObjLdn"]}')
            # print(a)
            for r in a['r']:
                if r['@p'] == "1":
                    print(f' uplink-bytes = {r["#text"]}')
                else:
                    print(f' downlink-bytes = {r["#text"]}')
        # print(d["measValue"])
    # print(d["@measInfoId"])
