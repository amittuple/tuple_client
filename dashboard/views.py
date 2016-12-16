from django.shortcuts import render, HttpResponseRedirect
from django.core.urlresolvers import reverse
from team.models import master_table
from django.conf import settings

def dashboard(request):
    print 'Start of Dashoard View'
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    master_object_list = []
    if request.method == 'GET':
        print 'Get Request'
        try:
            if request.session["master_list"]:
                x=request.session["master_list"]
                print x
                y=x[0]
                for y1 in y:
                    obj=master_table.objects.get(id=y1)
                    master_object_list.append(obj)
            x = master_object_list[:15]

            del request.session['master_list']
            return render(request, 'dashboard/dashboard-table.html', {'table': x})
        except Exception as e:
            print e
            print 'All'
            x = master_table.objects.all()[:30]
            # adnan code
            warning = False
            if len(x) == 0:
                warning = True
            return render(request, 'dashboard/dashboard.html', {
                'table':x,
                'warning': warning
            })

def index(request):
    client_id = settings.CLIENT_ID
    return render(request, 'dashboard/landing.html', {'client_id': client_id})
