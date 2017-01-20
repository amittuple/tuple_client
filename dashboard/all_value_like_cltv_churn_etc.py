from team.models import MasterTable

def cltv_all_max(self):
    i=0
    for x in MasterTable.objects.all():
        cltv_all_value=i+x.cltv
    return cltv_all_value
def churn_all_max(self):
    i=0
    for x in MasterTable.objects.all():
        cltv_all_value=i+x.churn
    return cltv_all_value
def churn_all_max(self):
    i=0
    for x in MasterTable.objects.all():
        cltv_all_value=i+x.churn
    return cltv_all_value