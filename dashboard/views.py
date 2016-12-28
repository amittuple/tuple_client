# from django.shortcuts import render, HttpResponseRedirect
# from django.core.urlresolvers import reverse
# from team.models import master_table
# from django.conf import settings
#
# def dashboard(request):
#     print 'Start of Dashoard View'
#     if not request.user.is_authenticated:
#         return HttpResponseRedirect(reverse('login'))
#     master_object_list = []
#     if request.method == 'GET':
#         print 'Get Request'
#         try:
#             if request.session["master_list"]:
#                 x=request.session["master_list"]
#                 print x
#                 y=x[0]
#                 for y1 in y:
#                     obj=master_table.objects.get(cust_id=y1)
#                     master_object_list.append(obj)
#             x = master_object_list[:15]
#
#             del request.session['master_list']
#             return render(request, 'dashboard/dashboard-table.html', {'table': x})
#         except Exception as e:
#             print e
#             x = master_table.objects.all()[:30]
#             print 'len'
#             print len(x)
#             # adnan code
#             warning = False
#             if len(x) == 0:
#                 warning = True
#             return render(request, 'dashboard/dashboard.html', {
#                 'table':x,
#                 'warning': warning
#             })
#
# def index(request):
#     client_id = settings.CLIENT_ID
#     return render(request, 'dashboard/landing.html', {'client_id': client_id})

from django.shortcuts import render, HttpResponseRedirect
from django.core.urlresolvers import reverse
from team.models import master_table
def dashboard(request):
    print 'Start of Dashoard View'
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    master_object_list = []

    if request.method == 'GET':

        print 'Get Request'

    try:
        print 'post'
        if request.session["request_session"]:
            x = request.session["request_session"]
            for y1 in x:
                obj = master_table.objects.get(cust_id=y1)
                master_object_list.append(obj)

        x11 = master_object_list
        print "x11"
        print x11

        del request.session['request_session']

        if len(x11) == 0:
            warning = 'EMPTY'
        else:
            warning = False

        return render(request, 'dashboard/dashboard-table.html', {
            'table': x11,
            'warning': warning
        })

    except Exception as e:
        print e
        if e.message.__contains__('request_session'):
            x1 = master_table.objects.all()[:20]
            warning = False
        else:
            x1 = None
            warning = True

        if len(x1) == 0:
            warning = 'EMPTY'

        # warning = True/False/'ERROR'

        return render(request, 'dashboard/dashboard.html', {
            'table': x1,
            'warning': warning
        })

