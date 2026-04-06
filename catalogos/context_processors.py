from .views import es_admin

def admin_context(request):
    return {'es_admin': es_admin(request.user) if request.user.is_authenticated else False}