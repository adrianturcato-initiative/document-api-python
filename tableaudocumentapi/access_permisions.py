import pandas as pd
from xml.etree.ElementTree import tostring
import xml.dom.minidom

class GroupPermissions(object):
    def __init__(self,name: str, advertiser_names: list):
        self._name = name
        self._advertisers = advertiser_names


    @property
    def name(self):
        return self._name


    @property
    def advertisers(self):
        return self._advertisers


class AccessPermissions(object):
    def __init__(self,user_filter_group = None, csv_file_contents:str = None):
        self._group_permissions = []
        self._csv_table = csv_file_contents

        if user_filter_group:
            self._prepare_permissions_from_group(user_filter_group)
        elif csv_file_contents:
            self._prepare_permissions_from_csv(csv_file_contents)


    @property
    def group_permissions(self):
        return self._group_permissions


    def _strip_group_name(self,name):
        stripped = name.replace("ISMEMBEROF('local\\", '').replace("')", '')
        return stripped


    def _strip_advertiser_name(self,name):
        stripped = name.replace('"', '')
        return stripped


    def _prepare_permissions_from_group(self,filter_group):
        filterXML = filter_group.groupXML
        groupfiltersXML = filterXML.findall('.//groupfilter')
        for gfXML in groupfiltersXML:
            expression = gfXML.get('expression', None)
            if expression and "ISMEMBEROF" in expression:
                group_name = self._strip_group_name(expression)
                advertisersXML = gfXML.findall('.//groupfilter')
                advertiser_names = []
                #print(group_name)
                for aXML in advertisersXML:
                    member = aXML.get('member',None)
                    if member:
                        # xml_string = tostring(aXML)
                        # print(xml.dom.minidom.parseString(xml_string).toprettyxml())
                        advertiser_name = self._strip_advertiser_name(member)
                        advertiser_names.append(advertiser_name)
                # print(advertiser_names)
                self._group_permissions.append(GroupPermissions(group_name,advertiser_names))


    def _prepare_permissions_from_csv(self,csv_file_contents:str):
        lines = [l.split(',') for l in csv_file_contents.split('\n')]
        zipped = list(zip(*lines))
        advertiser_names = zipped[0]
        groups = zipped[1:]
        self._group_permissions = []
        for g in groups:
            group_advertisers = [advertiser_names[index] for index, ad in enumerate(g) if ad == '1']
            self._group_permissions.append(GroupPermissions(g[0],group_advertisers))


    def get_permissions_table_CSV(self):
        if self._csv_table:
            return self._csv_table
        else:
            indices = dict()
            df = pd.DataFrame()

            for g in self._group_permissions:
                series_indices = g.advertisers

                for a in series_indices:
                    if a not in indices:
                        indices[a] = len(indices)

            for g in self._group_permissions:
                series_name = g.name
                series_indices = g.advertisers
                series_values = [0]*len(indices)

                for a in series_indices:
                    series_values[indices[a]] = 1

                df[series_name] = series_values

            df['advertisers'] = list(indices.keys())
            df = df.set_index('advertisers')
            csv = df.to_csv()
            return csv