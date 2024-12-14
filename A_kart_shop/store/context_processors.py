from .models import Category,SubCategory

def categories_context_processor(request):
    return {
        'Categories': Category.objects.all()
    }
    
def sub_categories_context_processor(request):
    return{
        'sub_categories': SubCategory.objects.all()
    }