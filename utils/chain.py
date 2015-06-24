'''
chain functions
analogous to haskell's '.'
'''

def chain(*methods):
    def concat(*args, **kw):
        res = methods[0](*args, **kw)
        for method in methods[1:]:
            res = method(res)
        return res

    return concat


# usage example
if __name__ == '__main__':
    add1 = lambda x : x + 1
    sub1 = lambda x : x - 1

    print(chain(add1, add1, sub1)(1))