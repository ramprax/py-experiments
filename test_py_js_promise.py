from py_js_promise import JSPromise


def test_happy_promise_no_then():
    p = JSPromise.resolve('yay!')


def test_unhappy_promise_no_then():
    p = JSPromise.reject('oops!')


def test_happy_promise_then():
    p = JSPromise.resolve('cool! this will be printed.').then(print)


def test_unhappy_promise_then():
    p = JSPromise.reject('uh-oh! this will not be printed.').then(print)


def test_unhappy_promise_then_rej_handled():
    p = JSPromise.reject('error! but this will be handled(printed).').then(print, print)


def test_happy_promise_then_then():
    p = JSPromise.resolve('wow! chaining then-s is cool.').then(lambda x: x).then(print)


def test_unhappy_promise_then_then():
    p = JSPromise.reject('aargh! then-s cannot capture me.').then(lambda x: x).then(print)


def test_unhappy_promise_then_then_rej_handled():
    p = JSPromise.reject('nooo! 2nd then handles this.').then(lambda x: x).then(print, print)


def test_unhappy_promise_then_rej_handled_then_rej_handled():
    p = JSPromise.reject('err! both then-s handle this.').then(lambda x: x, lambda x: x).then(print, print)


def test_unhappy_promise_then_rej_handled_then():
    p = JSPromise.reject('bad! gets handled by 1st then').then(lambda x: x, lambda x: x).then(print)


def raiseException(sth):
    if isinstance(sth, Exception):
        raise Exception('Wrapped exception: '+str(sth)) from sth
    raise Exception(sth)


def test_unhappy_promise_then_rej_handled_then_raise():
    p = JSPromise.reject('grrr! gets handled and then wrapped in an exception').then(lambda x: x, lambda x: x).then(print, raiseException)


def test_unhappy_promise_then_rej_handled_then_catch():
    p = JSPromise.reject('rats! first then and caught').then(lambda x: x, lambda x: x).then(print).catch(lambda x: print('Caught:', x))


def test_unhappy_promise_then_then_catch():
    p = JSPromise.reject('egad! it takes catch to catch me').then(lambda x: x).then(print).catch(lambda x: print('Caught:', x))


def test_unhappy_promise_then_then_raise():
    p = JSPromise.reject('oh no! raises exception').then(lambda x: x).then(print, raiseException)


def test_unhappy_promise_then_then_raise_catch():
    p = JSPromise.reject('hmm.. exception caught').then(lambda x: x).then(print, raiseException).catch(lambda x: print('Caught:', x))


def test_unhappy_promise_finally():
    p = JSPromise.reject('blaah! never caught! finally called').Finally(lambda: print('Clean clean!'))


def test_unhappy_promise_then_rej_handled_finally():
    p = JSPromise.reject('oooh! handled by then! finally called').then(print, print).Finally(lambda: print('Clean clean!'))


def test_happy_promise_finally():
    p = JSPromise.resolve('yay! finally called').Finally(lambda: print('Clean clean!'))


def test_happy_promise_then_finally():
    p = JSPromise.resolve('yay! finally called after handling by then').then(print).Finally(lambda: print('Clean clean!'))


def promise_not_none(x):
    def not_none_test(res, rej):
        if x is None:
            return rej(x)
        return res(x)

    return JSPromise(not_none_test)


def test_promise_not_none():
    p1 = promise_not_none(None).then(print)
    p2 = promise_not_none(None).then(print, print)
    p3 = promise_not_none(None).then(print).catch(print)

    p4 = promise_not_none('promise').then(print)
    p5 = promise_not_none('promise').then(print, print)
    p6 = promise_not_none('promise').then(print).catch(print)


def main():
    test_happy_promise_no_then()
    test_unhappy_promise_no_then()
    test_happy_promise_then()
    test_unhappy_promise_then()
    test_unhappy_promise_then_rej_handled()
    test_happy_promise_then_then()
    test_unhappy_promise_then_then()
    test_unhappy_promise_then_then_rej_handled()
    test_unhappy_promise_then_rej_handled_then_rej_handled()
    test_unhappy_promise_then_rej_handled_then()
    test_unhappy_promise_then_rej_handled_then_raise()
    test_unhappy_promise_then_rej_handled_then_catch()
    test_unhappy_promise_then_then_catch()
    test_unhappy_promise_then_then_raise()
    test_unhappy_promise_then_then_raise_catch()
    test_unhappy_promise_finally()
    test_unhappy_promise_then_rej_handled_finally()
    test_happy_promise_finally()
    test_happy_promise_then_finally()

    test_promise_not_none()

    input('<ENTER> to exit')


if __name__ == '__main__':
    main()

