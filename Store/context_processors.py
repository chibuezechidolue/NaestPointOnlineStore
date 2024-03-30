from .models import Collection,Advertisement
from User.forms import NewsLetterForm
form=NewsLetterForm()

def nav_bar(request):
    return {'collections': Collection.objects.all(),
            "nav_advert":Advertisement.objects.get(advert_location="Nav_advert"),
            "newsletterform":form
            }

