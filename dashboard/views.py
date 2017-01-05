# # from django.shortcuts import render, HttpResponseRedirect
# # from django.core.urlresolvers import reverse
# # from team.models import master_table
# # from django.conf import settings
# #
# # def dashboard(request):
# #     print 'Start of Dashoard View'
# #     if not request.user.is_authenticated:
# #         return HttpResponseRedirect(reverse('login'))
# #     master_object_list = []
# #     if request.method == 'GET':
# #         print 'Get Request'
# #         try:
# #             if request.session["master_list"]:
# #                 x=request.session["master_list"]
# #                 print x
# #                 y=x[0]
# #                 for y1 in y:
# #                     obj=master_table.objects.get(cust_id=y1)
# #                     master_object_list.append(obj)
# #             x = master_object_list[:15]
# #
# #             del request.session['master_list']
# #             return render(request, 'dashboard/dashboard-table.html', {'table': x})
# #         except Exception as e:
# #             print e
# #             x = master_table.objects.all()[:30]
# #             print 'len'
# #             print len(x)
# #             # adnan code
# #             warning = False
# #             if len(x) == 0:
# #                 warning = True
# #             return render(request, 'dashboard/dashboard.html', {
# #                 'table':x,
# #                 'warning': warning
# #             })
# #
# # def index(request):
# #     client_id = settings.CLIENT_ID
# #     return render(request, 'dashboard/landing.html', {'client_id': client_id})
#
#
#
# from django.shortcuts import render, HttpResponseRedirect
# from django.core.urlresolvers import reverse
# from team.models import master_table, Personal
#
#
# def dashboard(request):
#     print 'Start of Dashoard View'
#     if not request.user.is_authenticated:
#         return HttpResponseRedirect(reverse('login'))
#     master_object_list = []
#
#     try:
#         print 'post'
#         x = request.session["request_session"]
#     except Exception as e:
#         print e
#         if e.message.__contains__('request_session'):
#             x1 = master_table.objects.all()[:20]
#             print x1[0].percent_cltv
#             warning = False
#         else:
#             x1 = None
#             warning = True
#
#         if len(x1) == 0:
#             warning = 'EMPTY'
#
#         # warning = True/False/'ERROR'
#
#         return render(request, 'dashboard/dashboard.html', {
#             'table': x1,
#             'warning': warning
#         })
#
#     for y1 in x:
#         obj = None
#         try:
#             obj = master_table.objects.get(cust_id=y1)
#         except Exception as e:
#             print e
#             if e.message.__contains__('more than one'):
#                 obj = master_table.objects.filter(cust_id=y1)[0]
#         master_object_list.append(obj)
#
#     x11 = master_object_list
#     print "x11"
#     print x11
#
#     del request.session['request_session']
#
#     if len(x11) == 0:
#         warning = 'EMPTY'
#     else:
#         warning = False
#
#     return render(request, 'dashboard/dashboard-table.html', {
#         'table': x11,
#         'warning': warning
#     })
#
#
#

from django.shortcuts import render, HttpResponseRedirect
from django.core.urlresolvers import reverse

from team.function_input import name_firstname_lastname
from team.models import master_table

def dashboard(request):
    print 'Start of Dashoard View'
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    master_object_list = []
    try:
        print 'post'
        x = request.session["request_session"]
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
        yone_name = []
        for yone in x1:

            yone_name.append(yone.cust_id)
        print yone_name
        print 'yone_name'
        ylast = name_firstname_lastname(yone_name)
        print ylast
        print 'ylast'
        i = 0
        for xone in x1:
            xone.name = ylast[i]
            i = i + 1
        return render(request, 'dashboard/dashboard.html', {
            'table': x1,
            'warning': warning
        })

    for y1 in x:
        obj = None
        try:
            obj = master_table.objects.get(cust_id=y1)
        except Exception as e:
            print e
            if e.message.__contains__('more than one'):
                obj = master_table.objects.filter(cust_id=y1)[0]
        master_object_list.append(obj)

    x11 = master_object_list
    try:
        list_name = request.session['request_name']
        i = 0
        for xone in x11:
            xone.name = list_name[i]
            i = i + 1

        del request.session['request_name']
        del request.session['request_session']

        if len(x11) == 0:
            warning = 'EMPTY'
        else:
            warning = False
    except Exception as e:
        print e
        warning = True
        if e.message.__contains__('request_name') or e.message.__contains__('request_session'):
            yone_name = []
            x1 = master_table.objects.all()
            if len(x1) !=0:
                x1 = master_table.objects.all()[:20]
                for yone in x1:
                    yone_name.append(yone.cust_id)
                ylast = name_firstname_lastname(yone_name)
                i = 0
                for xone in x1:
                    xone.name = ylast[i]
                    i = i + 1

                warning = False
            else:
                x1 = None
                warning = 'EMPTY'
        else:
            x1 = None
            warning = True
        return render(request, 'dashboard/dashboard.html', {
            'table': x1,
            'warning': warning
        })


    return render(request, 'dashboard/dashboard-table.html', {
        'table': x11,
        'warning': warning
    })