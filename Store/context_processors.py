from .models import Collection,Advertisement
from User.forms import NewsLetterForm
from Cart.models import Cart,CartItems, SavedItems
import uuid





form=NewsLetterForm()
def nav_bar(request):
    user=request.user
    if user.is_authenticated:
        try:
            cart = Cart.objects.get(user=user,paid=False)
        except:
            cart={"num_of_item":0}
        usr_saved_items= SavedItems.objects.filter(user=request.user)
    else:
        usr_saved_items=[]
        try:
            session=request.session['session_id']
        except:
            request.session['session_id']=str(uuid.uuid4)
            session=request.session.get('session_id')
        finally:
            try:
                cart = Cart.objects.get(session_id=session,paid=False)
            except:
                cart={"num_of_item":0}
    return {'collections': Collection.objects.all(),
            "nav_advert":Advertisement.objects.get(advert_location="Nav_advert"),
            "newsletterform":form,"cart":cart,"saved_items":usr_saved_items
            }

