from asyncio import gather

import click

from ..api import GithubApi
from ..utils import wait, CommandError


@click.command()
@click.pass_context
def labels(ctx):
    """Crate or update labels in github
    """
    config = ctx.obj['agile']
    repos = config.get('repositories')
    labels = config.get('labels')
    if not isinstance(repos, list):
        raise CommandError(
            'You need to specify the "repos" list in the config'
        )
    if not isinstance(labels, dict):
        raise CommandError(
            'You need to specify the "labels" dictionary in the config'
        )
    wait(_labels(repos, labels))


async def _labels(repos, labels):
    git = GithubApi()
    for repo in repos:
        repo = git.repo(repo)
        requests = []
        for name, color in labels.items():
            requests.append(_repo_label(repo, name, color))
        await gather(*requests)


async def _repo_label(repo, label, color):
    if await repo.label(label, color):
        click.echo('Created label "%s" @ %s' % (label, repo))
    else:
        click.echo('Updated label "%s" @ %s' % (label, repo))
