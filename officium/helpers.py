
def get_app_profile(request):
    return getattr(request, 'OFFICIUM_MIDDLEWARE_PROFILE')

def get_app_themes(request):
    return getattr(request, 'OFFICIUM_MIDDLEWARE_THEMES')
