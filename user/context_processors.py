from .forms import LoginForm
from designer_shop.models import Shop


def include_login_form(request):
    form = LoginForm()
    return {'login_form': form}

def get_user_shop(request):
    if(hasattr(request.user, 'is_seller') and request.user.is_seller):
        shop = Shop.objects.get(user=request.user)
        return {
            'shopUrl' : shop.slug,
            'shopName': shop.name
        }
    else:
        return {}