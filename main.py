#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Rafael Corsi @ insper.edu.br
# 2021

import argparse
import yaml
import os
import git

# https://stackoverflow.com/questions/19687394/python-script-to-determine-if-a-directory-is-a-git-repository
def is_git_repo(path):
    try:
        _ = git.Repo(path).git_dir
        return True
    except git.exc.InvalidGitRepositoryError:
        return False


def ghIssueCreeate(issue):
#    import pdb; pdb.set_trace()
    title = '\'{}\''.format(issue['Title'])
    body = '\'{}\''.format(issue['Body'])
    command = 'gh issue create -t {} -b {}'.format(title,body)
    #if :
    #    command = command + " -m {}".format(milestone)
    os.system(command)


def ghissueCreateBulk(issues, reposPath):
    os.chdir(reposPath)
    for repo in os.listdir():
        os.chdir(repo)
        print('repo: {}'.format(repo))
        for k, v in issues.items():
            print('   - criando issue: {}'.format(k))
            ghIssueCreeate(v)
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
    parser.add_argument('--issues', default=None,  type=str, help='Issues (yml)')
    parser.add_argument('--repos', default=None,  type=str, help='Repositorios (yml)')

    parser.add_argument('--repos_dir', default='repos',  type=str, help='Pasta com os repositorios')
    parser.add_argument('--repos_update', default=False, action='store_true', help='Atualiza/Clona repositorios')

    args = parser.parse_args()

    with open(args.issues, 'r') as file:
        issues = yaml.load(file, Loader=yaml.FullLoader)

    if(args.repos is not None):
        with open(args.repos, 'r') as file:
            repos = yaml.load(file, Loader=yaml.FullLoader)

    if args.repos_update:
        print('Atualizando/Clonando repositorios')
        initRepo(repos, args.repos_dir)

    ghissueCreateBulk(issues, args.repos_dir)
