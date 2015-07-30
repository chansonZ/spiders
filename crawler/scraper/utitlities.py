""" A bunch of utilitiy classes and functions. """

def counted(function):
    def wrapper(*args, **kwargs):
        wrapper.called += 1
        return function(*args, **kwargs)
    wrapper.called = 0
    wrapper.__name__ = function.__name__
    return wrapper


class UrlBuilder:
    # Inspired by http://stackoverflow.com/questions/1590219/url-builder-for-python

    def __init__(self, domain, path='', params={}):
        self.domain = domain
        self.path = path
        self.params = params

    def with_path(self, path):
        self.path = path
        return self

    def with_params(self, params):
        self.params.update(params)
        return self

    @property
    def slash(self):
        return '/' if self.path else ''

    @property
    def question_mark(self):
        return '?' if self.params else ''

    @property
    def query(self):
        if not self.params:
            return ''

        q = []
        for k, v in self.params.items():
            q.append(str(k) + '=' + str(v))
        return '&'.join(q)

    def __str__(self):
        return 'http://' + self.domain + self.slash + self.path + self.question_mark + self.query

    def build(self):
        return self.__str__()

    def clear(self):
        self.path = ''
        self.params = {}
        return self


if __name__ == '__main__':
    u = UrlBuilder('www.example.com')
    print u.with_path('blablabla')
    print u.with_params({'a': 1})
    print u.with_path('elvis').with_params({'bar': 'foo'})
    print u.clear()