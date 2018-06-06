from click.testing import CliRunner

from agiletoolkit.commands import start
from agiletoolkit.repo import RepoManager
from agiletoolkit.test import gitrepo
from agiletoolkit.api import GithubException


def mocked(*a, **kw):
    print('mocked')


def test_main():
    runner = CliRunner()
    result = runner.invoke(start)
    assert result.exit_code == 0
    assert result.output.startswith('Usage:')
    #
    result = runner.invoke(start, '--config', 'tests/cfg1.json')
    assert result.exit_code == 2
    assert result.output.startswith('Usage:')


def test_repo(mocker):
    with gitrepo('deploy'):
        m = RepoManager()
        m.validate_version = mocker.Mock(return_value=True)
        assert m.can_release()

    with gitrepo('deploy'):
        m = RepoManager()
        m.validate_version = mocker.Mock(side_effect=GithubException('test'))
        assert m.can_release() is False
