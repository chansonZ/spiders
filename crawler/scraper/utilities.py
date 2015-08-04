""" A bunch of utilitiy classes and functions. """


def count_me(function):
    def wrapper(*args, **kwargs):
        wrapper.called += 1
        return function(*args, **kwargs)
    wrapper.called = 0
    wrapper.__name__ = function.__name__
    return wrapper


# UrlObject is inspired by http://stackoverflow.com/questions/1590219/url-builder-for-python

class Url:
    def __init__(self, domain, path=None, params=None):
        self.domain = domain
        self.path = path
        self.params = params

    def with_path(self, path):
        self.path = path
        return self

    def with_params(self, params):
        if not self.params:
            self.params = params
        else:
            self.params.update(params)
        return self

    @property
    def _slash(self):
        return '/' if self.path else ''

    @property
    def _question_mark(self):
        return '?' if self.params else ''

    @property
    def _query(self):
        if not self.params:
            return ''
        else:
            query = []
            for key, value in self.params.items():
                query.append(str(key) + '=' + str(value))
        return '&'.join(query)

    def __str__(self):
        return 'http://' + self.domain + self._slash + self.path + self._question_mark + self._query

    def build(self):
        return self.__str__()

    def clear(self):
        self.path = ''
        self.params = {}
        return self


if __name__ == '__main__':
    u = Url('www.example.com')
    print u.with_path('blablabla')
    print u.with_params({'a': 1})
    print u.with_path('elvis').with_params({'bar': 'foo'})
    print u.clear()