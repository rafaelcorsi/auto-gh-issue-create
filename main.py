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
import tempfile
import subprocess


# TODO: precisa criar o alias antes, tirar isso
# gh alias set createMilestone 'api --method POST repos/:owner/:repo/milestones --input'
def ghMilestoneCreate(milestone):
    body = {'title':milestone, 'state':'open', 'due_on': '2021-06-16T23:00:01Z'}
    with tempfile.NamedTemporaryFile() as tf:
        j = json.dumps(body)
        tf.write(bytes(j, encoding = 'utf-8'))
        tf.flush()
        command = 'gh api --method POST repos/rafaelcorsi/test/milestones --input {}'.format(tf.name)
    #out = subprocess.check_output(command, shell=True).decode('utf-8')
        print(command)
        import pdb; pdb.set_trace()
    #print(out)


def ghMilestoneCreateBulk(milestone, repos):
    for repo in repos:
        print('repo: {}'.format(repo))
        for m in milestone:
            ghMilestoneCreate(milestone[m])


def ghIssueList(repo):
    command = 'issue list -s all -R {}'.format(repo)
    out = subprocess.check_output('gh {}'.format(command), shell=True).decode('utf-8')
    return(out)


def ghIssueExist(issueList, issue):
    if issueList.find(issue['Title']) > 0:
        return True
    return False


def ghIssueCreeate(issue, repo):
    title = '\'{}\''.format(issue['Title'])
    body = '\'{}\''.format(issue['Body'])
    command = 'gh issue create -t {} -b {} -R {}'.format(title, body, repo)
    #if :
    #    command = command + " -m {}".format(milestone)
    os.system(command)


def ghIssueCreateBulk(issues, repos):
    for repo in repos:
        print(repo)
        issueList = ghIssueList(repo)
        for k, v in issues.items():
            if ghIssueExist(issueList, v) is False:
                print('\t- criando issue: {}'.format(v['Title']))
                ghIssueCreeate(v, repo)
            else:
                print('\t- issue já existia: {}'.format(v['Title']))


if __name__ == '__main__':
    argparse.ArgumentParser()
    parser = argparse.ArgumentParser(prog='Automatic issue create on github - CLI')
    parser.add_argument('--config', default=None,  type=str, help='Issues (yml)')
    parser.add_argument('--repos', default=None,  type=str, help='Repositorios (yml)')
    parser.add_argument('--issues', default=False, action='store_true', help='Cria os issues')
    parser.add_argument('--milestone', default=False, action='store_true', help='Cria os milestones')

    args = parser.parse_args()

    #ghMilestoneCreate('aaaaa')

    if(args.config is not None):
        with open(args.config, 'r') as file:
            config = yaml.load(file, Loader=yaml.FullLoader)

    if(args.repos is not None):
        with open(args.repos, 'r') as file:
            repos = yaml.load(file, Loader=yaml.FullLoader)

    if args.milestone:
        print('Criando milestones')
        ghMilestoneCreateBulk(config['milestone'], repos)

    if args.issues:
        print('Criando issues')
        ghIssueCreateBulk(config['issues'], repos)
