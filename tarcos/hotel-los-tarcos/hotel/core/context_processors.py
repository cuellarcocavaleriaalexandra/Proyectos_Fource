from django.conf import settings

def global_vars(request):
    return {
       'GOOGLE_ANALYTICS_KEY': getattr(settings, 'GOOGLE_ANALYTICS_KEY', None),
    }
