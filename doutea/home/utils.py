# coding=utf8


def beautify_price(price):
    '''
    >>> beautify_price(12.50)
    '12.5'
    >>> beautify_price(12)
    '12'
    '''

    return ('%f' % price).rstrip('0').rstrip('.')


if __name__ == "__main__":
    import doctest
    doctest.testmod()
