from pyramid.view import view_config
from pyramid.renderers import render_to_response

@view_config(route_name='home', renderer='mako')
def home(request):
    return render_to_response(
            'templates/home.mako',
            {},
            request=request
    )