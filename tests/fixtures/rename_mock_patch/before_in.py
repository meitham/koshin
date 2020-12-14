from unittest import mock
import another

class Klass:
    @mock.patch('foo')
    def func(self, patcher):
        foo()

    @patch('foo')
    def func(self, patcher):
        foo()

patch('test')

# patch(another)
