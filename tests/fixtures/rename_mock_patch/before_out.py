from unittest import mock

class Klass:
    @mock.patch('foo')
    def func(self, patcher):
        foo()

