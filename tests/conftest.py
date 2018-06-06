from unittest import mock
from contextlib import contextmanager

from agiletoolkit import utils


@contextmanager
def gitrepo(branch, pr=False, tag=None):

    original_gitrepo = utils.gitrepo

    def mocker(root=None):
        data = original_gitrepo(root)
        data['branch'] = branch
        data['pr'] = pr
        data['tag'] = tag
        return data

    with mock.patch('agiletoolkit.utils.gitrepo', side_effect=mocker) as m:
        yield m
