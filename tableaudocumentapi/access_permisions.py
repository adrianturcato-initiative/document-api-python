import pandas as pd
from collections import OrderedDict

class GroupPermissions(object):
    def __init__(self,name: str, advertisers: list):
        self._name = name
        self._advertisers = advertisers

    @property
    def name(self):
        return self._name

    @property
    def advertisers(self):
        return self._advertisers

class AccessPermissions(object):
    def __init__(self,user_filter_group = None, csv_file_contents = None):
        self._group_permissions = []
        self._csv_table = csv_file_contents

        if user_filter_group:
            self._prepare_permissions_from_group(user_filter_group)
        elif csv_file_contents:
            pass

    @property
    def group_permissions(self):
        return self._group_permissions

    def _strip_group_name(self,name):
        return name.replace("ISMEMBEROF('local\\",'').replace("')",'')

    def _strip_advertiser_name(self,name):
        return name[1:-1]

    def _prepare_permissions_from_group(self,filter_group):
        filterXML = filter_group.groupXML
        groupfiltersXML = filterXML.findall('.//groupfilter')
        for gfXML in groupfiltersXML:
            expression = gfXML.get('expression', None)
            if expression and "ISMEMBEROF" in expression:
                group_name = self._strip_group_name(expression)
                advertisersXML = gfXML.findall('.//groupfilter')
                advertiser_names = []
                for aXML in advertisersXML:
                    member = aXML.get('member',None)
                    if member:
                        advertiser_name = self._strip_advertiser_name(member)
                        advertiser_names.append(advertiser_name)

                self._group_permissions.append(GroupPermissions(group_name,advertiser_names))

    def get_permissions_table_CSV(self):
        if self._csv_table:
            return self._csv_table
        else:
            indices = dict()

            for g in self._group_permissions:
                series_indices = g.advertisers

                for a in series_indices:
                    if a not in indices:
                        indices[a] = len(indices)

            print(indices)
            for g in self._group_permissions:
                series_name = g.name
                series_indices = g.advertisers
                series_values = [0]*25

                for a in series_indices:
                    sseries_values[indices[a]] = 1


                print(series_values)







