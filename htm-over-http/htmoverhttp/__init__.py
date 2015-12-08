from pyramid.config import Configurator

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('create', '/create/{predicted_field}')
    config.add_route('reset', '/reset/{guid}')
    config.add_route('run','/run/{guid}')
    config.scan()
    return config.make_wsgi_app()
