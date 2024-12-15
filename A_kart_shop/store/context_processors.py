from .models import Category,SubCategory

def categories_context_processor(request):
    return {
        'Categories': Category.objects.all()
    }
    
def sub_categories_context_processor(request):
    return{
        'sub_categories': SubCategory.objects.all()
    }
    
    
from orders.models import Cart

def cart_context(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).count()
        return {'cart': cart}
    return {'cart': None}