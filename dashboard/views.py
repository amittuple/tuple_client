from django.shortcuts import render, HttpResponseRedirect
from django.core.urlresolvers import reverse
import plotly.plotly as py
import plotly

from dashboard.cltv_value import graph_value, graph_cltv, graph_engagement, graph_profile
from team.function_input import name_firstname_lastname
from team.models import MasterTable
import plotly.graph_objs as go
from plotly.offline import plot
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
           x1 = MasterTable.objects.all()[:30]

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

       ylast = name_firstname_lastname(yone_name)

       i = 0
       for xone in x1:
           xone.name = ylast[i]
           i = i + 1


       fig22 = graph_cltv()
       fig23 = graph_value()
       return render(request, 'dashboard/dashboard.html', {
           'table_9': x1,
           'warning': warning,
           'ploty_cltv':fig22,
           'ploty_value':fig23,

       })

   for y1 in x:
       obj = None
       try:
           obj = MasterTable.objects.get(cust_id=y1)
       except Exception as e:
           print e
           if e.message.__contains__('more than one'):
               obj = MasterTable.objects.filter(cust_id=y1)[0]
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
           x1 = MasterTable.objects.all()
           if len(x1) !=0:
               x1 = MasterTable.objects.all()[:20]
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

       fig22 = graph_cltv()
       fig23 = graph_value()
       return render(request, 'dashboard/dashboard.html', {
           'table_9': x1,
           'warning': warning,
           'ploty_cltv':fig22,
           'ploty_value':fig23,

       })

   fig22=graph_cltv()
   fig23=graph_value()
   fig24=graph_engagement()
   fig25=graph_profile()
   return render(request, 'dashboard/dashboard-table.html', {
       'table_9': x11,
       'warning': warning,
       'ploty_cltv':fig22,
        'ploty_value':fig23,
        'ploty_engagement':fig24,
       'ploty_profile':fig25

   })