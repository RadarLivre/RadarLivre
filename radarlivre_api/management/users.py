from django.contrib.auth.models import User


def createUsers():
    superuser = User.objects.get(username="felipe")

    if not superuser:
        superuser = User(username="felipe", password="felipe11235813", email="felipe76857685@gmail.com")
        superuser.save()

    else:
        print(superuser)
