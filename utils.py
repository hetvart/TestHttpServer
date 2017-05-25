import sys


def test_print(context, *args):
    sys.stdout.flush()
    print('%s' % context, *args)
    sys.stdout.flush()
