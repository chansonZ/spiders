""" A bunch of utilitiy classes and functions. """


def counted(function):
    def wrapper(*args, **kwargs):
        wrapper.called += 1
        return function(*args, **kwargs)
    wrapper.called = 0
    wrapper.__name__ = function.__name__
    return wrapper


class UrlBuilder:
    # See http://stackoverflow.com/questions/1590219/url-builder-for-python

    def __init__(self, domain, path='', params=''):
        self.domain = domain
        self.path = path
        self.params = params

    def with_path(self, path):
        self.path = path
        return self

    def with_params(self, params):
        self.params = params
        return self

    def __str__(self):
        return 'http://' + self.domain + '/' + self.path + '?' + self.params

    def build(self):
        return self.__str__()


if __name__ == '__main__':
    u = UrlBuilder('www.example.com')
    print u.with_path('bobloblaw')
    print u.with_params('lawyer=yes')
    print u.with_path('elvis').with_params('theking=true')