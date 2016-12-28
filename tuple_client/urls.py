"""tuple_client URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
# from .views import fildb
# from .views import filpro

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'', include('login.urls')),
    url(r'', include('mapper.urls')),
    url(r'', include('database_management.urls')),
    url(r'^connect-client-db/', include('connect_client_db.urls')),
    url(r'^connect-client-db/', include('connect_client_db.urls')),
    url(r'^dashboard/', include('dashboard.urls')),
    url(r'', include('banana_py.urls')),
    url(r'^bananas/ripe/', include('build_mailchimp.urls')),
    url(r'^build-mailchimp/complete/', include('build_mailchimp.urls')),
    url(r'^am/', include('team.urls')),
    url(r'^slack/', include("slack_bot.urls")),
    # url(r'^fill/',fildb),
    # url(r'^filled/',filpro),
]
