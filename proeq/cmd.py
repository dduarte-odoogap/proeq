#!/usr/bin/env python
import paramiko
import click
import os
import yaml
import glob
import subprocess, imp

def ssh_in(host, port, user, content):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.load_system_host_keys()
    ssh.connect(host, username=user, port=port)
    for line in iter(content.splitlines()):
        stdin, stdout, stderr = ssh.exec_command(line)
        for out in stdout:
            click.echo(out)


def fabric_in(fab_command, base_path):
    out = subprocess.check_output('cd %s && fab %s' % (base_path, fab_command), shell=True)
    click.echo(out)


def shell_in(content):
    for line in iter(content.splitlines()):
        out = subprocess.check_output(line, shell=True)
        click.echo(out)


def lxc_in(container_name, content):
    for line in iter(content.splitlines()):
        command = "lxc exec {container_name} -- {line}".format(
            container_name=container_name,
            line=line
        )
        out = subprocess.check_output(command, shell=True)
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
    """ProEQ is a tool made for making developers life easier based on that you already have
    scripts built in bash. This tool allows you to store all info about your projects, as well
    as collecting and listing your scripts.
    """
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


@click.command('src-list', short_help='List all scripts')
@click.pass_obj
def list_src(repo):
    for scripts in list(filter(lambda d: 'manifest' in d.keys(), repo.src)):
        click.secho(scripts['manifest']['id'], fg='red')


@click.command('src-exec', short_help='Executes script')
@click.option('--script-id', '-n', default=False, help='Executes script', required=True)
@click.pass_obj
def exec_src(repo, script_id):
    """Execute Script command will run custom scripts stored in the user folder
    defaults to (~/.proeq/scripts) declared with the manifest.yml file.
    """
    script_ids = [f['manifest'].get('id') for f in list(filter(lambda d: 'manifest' in d.keys(), repo.src))]
    if script_id not in script_ids:
        raise click.BadParameter("This script-id does not exist!")
    for man in repo.src:
        if man['manifest'].get('id') == script_id:
            script_list0 = man['manifest'].get('scripts')
            environment = man['manifest'].get('environment')
            base_path = man['manifest'].get('full-path')
    # Sort by order key
    script_list0 = sorted(script_list0, key=lambda k: k['order'])
    script_list = list(filter(lambda d: d.get('active'), script_list0))
    for scr in script_list:
        click.secho("Script order %s" % scr.get('order'), fg='red')
        if scr.get('ssh-server'):
            host = scr['ssh-server'].get('host')
            user = scr['ssh-server'].get('user')
            port = scr['ssh-server'].get('port')

        script_type = scr.get('type')
        container_name = scr.get('container')
        fab_command = scr.get('command')

        content = scr.get('file')
        if content:
            with open(os.path.join(base_path, content)) as f:
                content = f.read()
                parsed_content = content.format(**environment)

        if script_type == 'ssh':
            ssh_in(host, port, user, parsed_content)
        elif script_type == 'shell':
            shell_in(parsed_content)
        elif script_type == 'lxc':
            lxc_in(container_name, parsed_content)
        elif script_type == 'fabric':
            fabric_in(fab_command, base_path)

cli.add_command(list_all)
cli.add_command(list_src)
cli.add_command(exec_src)

if __name__ == '__main__':
    cli()

