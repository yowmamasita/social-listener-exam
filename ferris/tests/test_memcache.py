from ferrisnose import AppEngineTest
from google.appengine.api import memcache
from ferris.core.memcache import cached, cached_by_args, none_sentinel_string


class MemcacheTest(AppEngineTest):

    def test_cached(self):
        mutators = [0, 0, 0]

        @cached('test-key')
        def test_cached():
            mutators[0] += 1
            return mutators[0]

        assert test_cached() == 1
        assert test_cached() == 1
        assert mutators[0] == 1
        assert memcache.get('test-key') == 1
        assert test_cached.uncached() == 2
        assert test_cached.cached() == 1

        test_cached.clear_cache()
        assert test_cached() == 3

        @cached('test-key-none')
        def test_cached_with_none():
            mutators[1] += 1
            return None

        assert test_cached_with_none() == None
        assert test_cached_with_none() == None
        assert mutators[1] == 1
        assert memcache.get('test-key-none') == none_sentinel_string


        @cached_by_args('arg-test')
        def args_test(num):
            mutators[2] += 1
            return num

        assert args_test(1) == 1
        assert args_test(1) == 1
        assert mutators[2] == 1
        assert memcache.get('arg-test:1::') == 1

        @cached_by_args('arg-method-test')
        def args_method_test(cls, num):
            mutators[2] += 1
            return num

        assert args_method_test(0, 4) == 4
        assert args_method_test(1, 4) == 4
        assert mutators[2] == 2
        assert memcache.get('arg-method-test:4::') == 4

