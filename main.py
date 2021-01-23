#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Rafael Corsi @ insper.edu.br
# 2021

import argparse
import yaml
import json
import os
import git
import pipes
import tempfile
import subprocess

# https://stackoverflow.com/questions/19687394/python-script-to-determine-if-a-directory-is-a-git-repository
def is_git_repo(path):
    try:
        _ = git.Repo(path).git_dir
        return True
    except git.exc.InvalidGitRepositoryError:
        return False


# TODO: precisa criar o alias antes, tirar isso
# gh alias set createMilestone 'api --method POST repos/:owner/:repo/milestones --input'
def ghMilestoneCreate(milestone):
    p = pipes.Template()
    p.append('gh createMilestone')
    p.debug(True)

    # Pass some text through the pipeline,
    # saving the output to a temporary file.
    t = tempfile.NamedTemporaryFile(mode='r')
    f = p.open(t.name, 'w')
    try:
        f.write(j)
    finally:
        f.close()

    # Rewind and read the text written
    # to the temporary file
    t.seek(0)
    print(t.read())
    t.close()

    j = json.dumps(milestone)
    command = 'gh createMilestone \'{}\''.format(j)
    print(command)
    os.system(command)


def ghMilestoneCreateBulk(milestone, reposPath):
    os.chdir(reposPath)
    for repo in os.listdir():
        if is_git_repo(repo):
            os.chdir(repo)
            print('repo: {}'.format(repo))
            for m in milestone:
                ghMilestoneCreate(milestone[m])
        os.chdir('..')
    os.chdir('..')


def ghIssueList():
    command = 'issue list -s all'
    print()
    out = subprocess.check_output('gh {}'.format(command), shell=True).decode('utf-8')
    return(out)


def ghIssueExist(issueList, issue):
    if issueList.find(issue['Title']) > 0:
        return True
    return False


def ghIssueCreeate(issue):
    title = '\'{}\''.format(issue['Title'])
    body = '\'{}\''.format(issue['Body'])
    command = 'gh issue create -t {} -b {}'.format(title,body)
    #if :
    #    command = command + " -m {}".format(milestone)
    os.system(command)


def ghIssueCreateBulk(issues, reposPath):
    os.chdir(reposPath)
    for repo in os.listdir():
        if is_git_repo(repo):
            os.chdir(repo)
            print('repo: {}'.format(repo))
            issueList = ghIssueList()
            for k, v in issues.items():
                if ghIssueExist(issueList, v) is False:
                    print('   - criando issue: {}'.format(v['Title']))
                    ghIssueCreeate(v)
                else:
                    print('   - issue já existia: {}'.format(v['Title']))
            os.chdir('..')
    os.chdir('..')


def initRepo(repoList, reposPath):
    for repo in repoList:
        print('Clonando: {}'.format(repo))
        try:
            git.Git(reposPath).clone(repo)
        except:
            pass


if __name__ == '__main__':
    argparse.ArgumentParser()
    parser = argparse.ArgumentParser(prog='Automatic issue create on github - CLI')
    parser.add_argument('--config', default=None,  type=str, help='Issues (yml)')
    parser.add_argument('--issues', default=False, action='store_true', help='Cria os issues')
    parser.add_argument('--milestone', default=False, action='store_true', help='Cria os milestones')

    parser.add_argument('--repos', default=None,  type=str, help='Repositorios (yml)')
    parser.add_argument('--repos_dir', default='repos',  type=str, help='Pasta com os repositorios')
    parser.add_argument('--repos_update', default=False, action='store_true', help='Atualiza/Clona repositorios')

    args = parser.parse_args()

    if(args.config is not None):
        with open(args.config, 'r') as file:
            config = yaml.load(file, Loader=yaml.FullLoader)

    if(args.repos is not None):
        with open(args.repos, 'r') as file:
            repos = yaml.load(file, Loader=yaml.FullLoader)

    if args.repos_update:
        print('Atualizando/Clonando repositorios')
        initRepo(repos, args.repos_dir)

    if args.milestone:
        print('Criando milestones')
        ghMilestoneCreateBulk(config['milestone'], args.repos_dir)

    if args.issues:
        print('Criando issues')
        ghIssueCreateBulk(config['issues'], args.repos_dir)
