from django.contrib.auth.models import User
user = User.objects.get(username='adkhn999')
print user
