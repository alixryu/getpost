from nose import with_setup
from nose.tools import eq_
from firelands.firelands import app


def setup_func():
    "set up pre-test configurations"
    app.config['TESTING'] = True


def teardown_func():
    "tear down pre-test configurations"
    app.config['TESTING'] = False


@with_setup(setup=setup_func, teardown=teardown_func)
def test_index():
    test_app = app.test_client()
    rv = test_app.get('/')
    rv_string = rv.data.decode('utf-8')
    eq_(
        rv_string,
        '<h1>What the brangan.</h1>',
        'Response string not identical'
    )
