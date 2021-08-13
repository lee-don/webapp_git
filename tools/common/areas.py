import json


class province:
    def __init__(self,name):
        self.citys = {}
        self.name = name
class city:
    def __init__(self,name):
        self.districts = []
        self.name = name

file = 'area-full.json'
class cn_provinces:
    def __init__(self):
        with open(file, 'r', encoding='utf8')as fp:
            self.json_data = json.load(fp)
        self.provinces = {}
        for shengdata in self.json_data:
            prov = province(shengdata['name'])
            self.provinces[shengdata['name']] = prov
            if 'children' in shengdata.keys():
                for citydata in shengdata['children']:
                    ct =city(citydata['name'])
                    prov.citys[ct.name] = ct
                    if 'children' in citydata.keys():
                        for districtdata in citydata['children']:
                            ct.districts.append(districtdata['name'])

    def get_province(self,name):
        return self.provinces[name]

    def get_city(self,name):
        for prov in self.provinces.values():
            if name in prov.citys.keys():
                return prov.citys[name]



if __name__ == '__main__':
    cn = cn_provinces()
    prov = cn.get_province('四川省').citys
    print(prov)

    print(cn.get_city('雅安市').districts)

