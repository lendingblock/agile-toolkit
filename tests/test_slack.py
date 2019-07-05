from unittest import mock
from agiletoolkit.test import gitrepo
from agiletoolkit.repo import RepoManager


def test_message():
    with gitrepo('slack'):
        m = RepoManager()
        with mock.patch('click.secho') as p:
            m.message('test')
            assert p.called
