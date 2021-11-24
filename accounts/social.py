from functools import wraps

from django.shortcuts import render


def partial(func):
    @wraps(func)
    def wrapper(strategy, pipeline_index, *args, **kwargs):
        out = func(strategy=strategy, pipeline_index=pipeline_index,
                    *args, **kwargs) or {}
        if not isinstance(out, dict):
            values = strategy.partial_to_session(pipeline_index, *args, **kwargs)
            strategy.session_set('partial_pipeline', values)
        return out
    return wrapper


@partial
def optional_user_data(backend, details, response, request, user, is_new=False, *args, **kwargs):
    if social_core.backends == 'google' and is_new:
        data = backend.strategy.request_data()
        if data.get('nickname' and 'country') is None:
            return render('signup_option.html', {'google_details': details })
        else:
            return {'nickname': data.get('nickname'),'country':data.get('country')}


def save_profile(backend, user, response, is_new, *args, **kwargs):
    if backend.name == 'google' and is_new:
        data = backend.strategy.request_data()

        profile = user.profile
        profile.nickname = data.get('nickname', '')
        profile.country = data.get('country', '')
        profile.email = response.get('email', '')
        profile.save()
