
from django.contrib.auth.models import User

user = User.objects.get(username='test')
user.set_password('test123')
user.save()