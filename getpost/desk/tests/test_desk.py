from nose import with_setup
from nose.tools import eq_

from tests.test_getpost import app, setup_func, teardown_func


@with_setup(setup=setup_func, teardown=teardown_func)
def test_wizard_index():
    test_app = app.test_client()
    rv = test_app.get('/students/')
    rv_string = rv.data.decode('utf-8')
    eq_(
        rv_string,
        '<h1>Welcome to the Student Search Page.</h1>',
        'Response string not identical'
    )
