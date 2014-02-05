from ferrisnose import AppEngineWebTest
from ferris.core.controller import Controller, route
from ferris.components import cache


class Cachable(Controller):
    class Meta:
        components = (cache.Cache,)

    @route
    def public(self):
        self.components.cache('public')
        return 'public'

    @route
    def private(self):
        self.components.cache('private')
        return 'private'

    @route
    @cache.set_cache('public')
    def decorator(self):
        return 'decorator'


class TestEdgeCaching(AppEngineWebTest):
    def setUp(self):
        super(TestEdgeCaching, self).setUp()
        Cachable._build_routes(self.testapp.app.router)

    def test(self):
        r = self.testapp.get('/cachable/public')
        assert r.headers['Cache-Control'] == 'max-age=900, public'

        r = self.testapp.get('/cachable/private')
        assert r.headers['Cache-Control'] == 'max-age=900, private'

        r = self.testapp.get('/cachable/decorator')
        assert r.headers['Cache-Control'] == 'max-age=900, public'
