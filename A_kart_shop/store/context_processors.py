from .models import Category

def categories_context_processor(request):
    return {
        'Categories': Category.objects.all()
    }