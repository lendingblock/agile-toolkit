import json
from unittest.mock import patch

from click.testing import CliRunner

from agiletoolkit import __version__
from agiletoolkit.commands import start
from agiletoolkit.utils import gitrepo


def test_git():
    runner = CliRunner()
    result = runner.invoke(start, ['git'])
    assert result.exit_code == 0
    assert result.output.startswith('Usage:')


def test_git_validate(gitrepo):
    runner = CliRunner()

    gitrepo['branch'] = 'deploy'
    result = runner.invoke(start, ['git', 'validate'])
    assert result.exit_code == 0
    assert result.output.strip() == __version__


def test_git_info():
    runner = CliRunner()
    result = runner.invoke(start, ['git', 'info'])
    assert result.exit_code == 0
    data = json.loads(result.output.strip())
    assert 'branch' in data


def test_git_remote():
    runner = CliRunner()
    result = runner.invoke(start, ['git', 'remote'])
    assert result.exit_code == 0
    assert result.output.strip() == 'lendingblock/platform'


def __test_git_release():
    runner = CliRunner()

    def _gitrepo(root=None):
        data = gitrepo(root)
        data['branch'] = 'deploy'
        data['pr'] = False
        return data

    with patch('agilelib.utils.gitrepo', side_effect=_gitrepo) as mock:
        result = runner.invoke(start, ['git', 'release', '--docker-url'])
        assert result.exit_code == 0
        assert mock.called
        data = json.loads(result.output.strip())
        assert data['name'] == 'v%s' % __version__
        body = data['body'].split('\n')
        assert body[-1].endswith('amazonaws.com/platform:%s' % __version__)


def test_git_release_skipped():
    runner = CliRunner()

    def _gitrepo(root=None):
        data = gitrepo(root)
        data['branch'] = 'master'
        return data

    with patch('agilelib.utils.gitrepo', side_effect=_gitrepo) as mock:
        result = runner.invoke(start, ['git', 'release', '--docker-url'])
        assert result.exit_code == 0
        assert mock.called
        assert result.output.strip() == 'skipped'


def test_labels_error():
    runner = CliRunner()
    result = runner.invoke(start, [
        '--config', 'tests/cfg1.json', 'git', 'labels'
    ])
    assert result.exit_code == 1
    assert result.output == (
        'Error: You need to specify the "repos" list in the config\n'
    )
    result = runner.invoke(start, [
        '--config', 'tests/cfg2.json', 'git', 'labels'
    ])
    assert result.exit_code == 1
    assert result.output == (
        'Error: You need to specify the "labels" dictionary in the config\n'
    )


def __test_git_labels():
    runner = CliRunner()
    result = runner.invoke(start, ['labels'])
    assert result.exit_code == 0
    assert result.output.startswith('Usage:')
