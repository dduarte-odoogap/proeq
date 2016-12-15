#!/usr/bin/env python
import paramiko
import click
import os
import yaml
import glob


def ssh_in(host, port, user, content):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.load_system_host_keys()
    ssh.connect(host, username=user, port=port)
    for line in iter(content.splitlines()):
        stdin, stdout, stderr = ssh.exec_command(line)
        for out in stdout:
            click.echo(out)


class Proeq(object):

    def __init__(self, home=None):
        self.home = os.path.expanduser(home or '.')
        proj = []
        for ymlFile in self.list_project_files():
            docs = yaml.load(open(os.path.join(self.home, ymlFile)))
            if 'id' not in docs['project'].keys():
                docs['project'].update({'id': ymlFile.split('/')[-2]})
            proj.append(docs)
        self.proj = proj

        src = []
        for ymlFile in self.list_script_files():
            full_path = os.path.join(self.home, ymlFile)
            docs = yaml.load(open(full_path))
            docs['manifest'].update({'full-path': full_path[:-12]})
            if 'id' not in docs['manifest'].keys():
                docs['manifest'].update({'id': ymlFile.split('/')[-2]})
            src.append(docs)

        self.src = src

    def list_project_files(self):
        rv = []
        for filename in glob.glob(self.home + '/projects/**/project.yml'):
            if filename.endswith('.yml'):
                rv.append(filename)
        return rv

    def list_script_files(self):
        rv = []
        for filename in glob.glob(self.home + '/scripts/**/manifest.yml'):
            if filename.endswith('.yml'):
                rv.append(filename)
        return rv


@click.group()
@click.option('--proeq-home', envvar='PROEQ_HOME', default='~/.proeq', help='Project repo home')
@click.pass_context
def cli(ctx, proeq_home):
    ctx.obj = Proeq(proeq_home)


@click.command('list', short_help='List all projects')
@click.option('--all', default=False, is_flag=True)
@click.pass_obj
def list_all(repo, all):
    for project in list(filter(lambda d: 'project' in d.keys(), repo.proj)):
        click.secho(project['project']['id'], fg='red')
        if all:
            click.secho('\t' + project['project']['name'], fg='green')
            ssh_servers = project['project'].get('ssh-server', False)
            for server in ssh_servers:
                click.echo('\t' + "SSH-SERVER {name} --> ssh -p {port} {user}@{host}".format(
                    name=server.get('name', ''),
                    port=server.get('port', ''),
                    user=server.get('user', ''),
                    host=server.get('host', '')))

            click.echo('\t' + project['project'].get('comments', ''))


@click.command('list-src', short_help='List all scripts')
@click.pass_obj
def list_src(repo):
    for scripts in list(filter(lambda d: 'manifest' in d.keys(), repo.src)):
        script_list = scripts['manifest'].get('scripts', False)
        click.secho(scripts['manifest']['id'], fg='red')


@click.command('exec-src', short_help='Executes script')
@click.option('--script-id', '-n', default=False, help='Executes script', required=True)
@click.pass_obj
def exec_src(repo, script_id):
    script_ids = [f['manifest'].get('id') for f in list(filter(lambda d: 'manifest' in d.keys(), repo.src))]
    if script_id not in script_ids:
        raise click.BadParameter("This script-id does not exist!")
    for man in repo.src:
        if man['manifest'].get('id') == script_id:
            script_list0 = man['manifest'].get('scripts')
            base_path = man['manifest'].get('full-path')
    # Sort by order key
    script_list = sorted(script_list0, key=lambda k: k['order'])
    for scr in script_list:
        click.secho("Script order %s" % scr.get('order'), fg='red')
        host = scr['ssh-server'].get('host')
        user = scr['ssh-server'].get('user')
        port = scr['ssh-server'].get('port')
        with open(os.path.join(base_path, scr.get('file'))) as f:
            content = f.read()
        ssh_in(host, port, user, content)


cli.add_command(list_all)
cli.add_command(list_src)
cli.add_command(exec_src)

if __name__ == '__main__':
    cli()

