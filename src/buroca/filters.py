FILTERS = {}
register = (lambda f: FILTERS.setdefault(f.__name__, f))


@register
def cronogram(phases, type, year, month):
    if type in ('md', 'markdown'):
        pass
    else:
        raise NotImplementedError
