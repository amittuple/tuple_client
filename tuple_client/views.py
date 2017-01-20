from django.http import HttpResponse
from random import randint
from team.models import MasterTable
from team.models import PersonalTable
def fildb(request):
    l=['a','b','c','d','e','f']
    for x in PersonalTable.objects.all():
        print x
        c=MasterTable()
        c.churn=randint(0,99)
        c.cltv=randint(1,100000)
        c.engagement=l[randint(0,5)]
        c.value=l[randint(0,5)]
        c.profile=l[randint(0,5)]
        c.high_converter=randint(0,99)
        c.personal=x
        c.save()
    return HttpResponse('success')

def filpro(request):
    m=['singapore','india','america','japan','rusia','australia']
    email=['amit@tuple.tech','adnan@tuple.tech','vishal@tuple.tech','neha@tuple.tech','anmol@tuple.tech','dipali@tuple.tech','anish@tuple.tech','santosh@tuple.tech']
    n=['amit','santosh','adnan','vikas','dipali','anmol','vishal','neha']
    o=['M','F']

    for x in range(1000):
        d=PersonalTable()
        d.country=m[randint(0,5)]
        d.name=n[randint(0,7)]
        d.gender=o[randint(0,1)]
        d.age=randint(1,99)
        d.email_id=email[randint(0,7)]
        d.save()
    return HttpResponse('profile successfully save')