import json

from click.testing import CliRunner

from agiletoolkit import __version__
from agiletoolkit.commands import start
from agiletoolkit.test import gitrepo


def test_git():
    runner = CliRunner()
    result = runner.invoke(start, ['git'])
    assert result.exit_code == 0
    assert result.output.startswith('Usage:')


def test_git_validate():
    runner = CliRunner()

    with gitrepo('deploy'):
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
    assert result.output.strip() == 'lendingblock/agile-toolkit'


def __test_git_release():
    runner = CliRunner()

    with gitrepo('deploy') as mock:
        result = runner.invoke(start, ['git', 'release'])
        assert result.exit_code == 0
        assert mock.called
        data = json.loads(result.output.strip())
        assert data['name'] == 'v%s' % __version__


def test_git_release_skipped():
    runner = CliRunner()

    with gitrepo('master') as mock:
        result = runner.invoke(start, ['git', 'release'])
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


def test_git_labels():
    runner = CliRunner()
    result = runner.invoke(start, ['labels'])
    assert result.exit_code == 0
    assert result.output.startswith('Usage:')
