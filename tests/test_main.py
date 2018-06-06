from click.testing import CliRunner

from agiletoolkit.commands import start


def mocked(*a, **kw):
    print('mocked')


def test_aws():
    runner = CliRunner()
    result = runner.invoke(start)
    assert result.exit_code == 0
    assert result.output.startswith('Usage:')
    #
    result = runner.invoke(start, '--config', 'tests/cfg1.json')
    assert result.exit_code == 2
    assert result.output.startswith('Usage:')
