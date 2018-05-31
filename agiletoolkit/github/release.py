import click

from ..utils import command, niceJson
from ..repo import RepoManager
from ..aws.dockertools import docker_repo


@click.command()
@click.pass_context
@click.option(
    '--yes', is_flag=True,
    help='Commit changes to github', default=False)
@click.option(
    '--docker-url', is_flag=True,
    help='Add docker repository url to the release body', default=False)
def release(ctx, yes, docker_url):
    """Create a new release in github
    """
    with command():
        m = RepoManager(ctx.obj['agile'])
        branch = m.info['branch']
        if m.can_release('stage'):
            version = m.validate_version()
            name = 'v%s' % version
            body = ['Release %s from agilelib' % name]
            if docker_url:
                url = f'{docker_repo(m)}:{m.version()}'
                body.append('Docker repository %s' % url)
            api = m.github_repo()
            data = dict(
                tag_name=name,
                target_commitish=branch,
                name=name,
                body='\n\n'.join(body),
                draft=False,
                prerelease=False
            )
            if yes:
                data = m.wait(api.releases.create(data=data))
                m.message('Successfully created a new Github release')
            click.echo(niceJson(data))
        else:
            click.echo('skipped')
