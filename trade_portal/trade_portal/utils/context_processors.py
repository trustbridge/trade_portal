from constance import config
from django.conf import settings


def settings_context(_request):
    if _request.user.is_authenticated:
        # for authenticated users
        # we return the org stored in the session
        # or first available otherwise
        current_org = _request.user.get_current_org(_request.session)
    else:
        current_org = None

    return {
        "ICL_APP_COUNTRY": settings.ICL_APP_COUNTRY,
        "BID_NAME": settings.BID_NAME,
        "BRANDING_TITLE": config.BRANDING_TITLE,
        "current_org": current_org,
        "IS_CONNECTED_TO_IGL": bool(config.IGL_CHANNELS_CONFIGURED.strip())  # True if there is at least one channel
    }
