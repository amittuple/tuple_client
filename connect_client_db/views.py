from django.shortcuts import render, HttpResponseRedirect, HttpResponse, get_object_or_404
from .forms import ClientDbForm
from . import models
from django.core.urlresolvers import reverse
import psycopg2

def client_has_db_config():
    try:
        return models.ClientDbModel.objects.all()[0]
    except Exception as e:
        print e
        return None

def result(request):
    return render(request, 'connect_client_db/result.html', {})


def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    else:
        user = request.user
    client_db_settings = client_has_db_config()
    if request.method == 'GET':
        if client_db_settings is not None:
            form = ClientDbForm(instance=client_db_settings)
        else:
            form = ClientDbForm()
    if request.method == 'POST':
        form = ClientDbForm(request.POST)
        if not form.is_valid():
            return HttpResponse('Incomplete or Invalid Form')
        else:
            database_name = form.cleaned_data['database_name']
            usern = form.cleaned_data['usern']
            passw = form.cleaned_data['passw']
            host = form.cleaned_data['host']
            port = form.cleaned_data['port']
            database_type = form.cleaned_data['database_type']
            print database_type
            if database_type == 'PostgreSQL':
                try:
                    # Connect Database To Confirm Database Exists
                    conn = psycopg2.connect(
                        database=database_name,
                        user=usern,
                        password=passw,
                        host=host,
                        port=port,
                        sslmode='require'
                    )
                    cur = conn.cursor()
                    if cur is not None:
                        if client_db_settings is not None:
                            print 'Client has already Database Connection Config'
                            print 'Update New Settings'
                            clientObj = models.ClientDbModel.objects.all()[0]
                            clientObj.database_name = database_name
                            clientObj.usern = usern
                            clientObj.passw = passw
                            clientObj.host = host
                            clientObj.port = port
                            clientObj.database_type = database_type
                            clientObj.save()
                        else:
                            clientObj = models.ClientDbModel()
                            clientObj.client = user
                            clientObj.database_name = database_name
                            clientObj.usern = usern
                            clientObj.passw = passw
                            clientObj.host = host
                            clientObj.port = port
                            clientObj.database_type = database_type
                            clientObj.save()
                        print "Successfully Connected"
                        conn.close()
                        cur.close()
                        return HttpResponseRedirect(reverse('connection_successfull'))
                    else:
                        print 'Connection Failed'
                except Exception as e:
                    if e.message.__contains__('UNIQUE constraint failed'):
                        print 'Database Connection Details Already Exists'
                    elif e.message.__contains__('NOT NULL constraint'):
                        print 'Key Value Missing'
                    print e
                    print "Error In Connection"
            else:
                # Other Type Of Database
                pass

    return render(request, 'connect_client_db/form.html', {
        'form': form
    })

def failed(request):
    return render(request, 'connect_client_db/failed.html', {})

def connected(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    return render(request, 'connect_client_db/connected.html', {})
