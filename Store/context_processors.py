from .models import Collection,Advertisement


def nav_bar(request):
    return {'collections': Collection.objects.all(),
            "nav_advert":Advertisement.objects.get(advert_location="Nav_advert"),
            }

