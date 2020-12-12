import foo

import foo.bar

import foo

class Klass:
    def func(self):
        import foo
        foo.bar.method()
        foo.call()
