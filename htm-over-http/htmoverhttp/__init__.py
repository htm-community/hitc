from pyramid.config import Configurator


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('pyramid_mako')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('model_create', '/models')
    config.add_route('models', '/models/{guid}')
    config.add_route('reset', '/models/reset/{guid}')
    config.add_route('run', '/models/run/{guid}')
    config.add_route('home', '/')
    config.scan()
    return config.make_wsgi_app()
