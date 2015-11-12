from nose import with_setup
from nose.tools import eq_

from firelands import app
from firelands.tests.test_firelands import setup_func, teardown_func


@with_setup(setup=setup_func, teardown=teardown_func)
def test_lobby_index():
    test_app = app.test_client()
    rv = test_app.get('/lobby/')
    rv_string = rv.data.decode('utf-8')
    eq_(
        rv_string,
        '<h1>Welcome to the Firelands lobby.</h1>',
        'Response string not identical'
    )
