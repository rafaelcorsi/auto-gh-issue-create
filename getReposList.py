#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Rafael Corsi @ insper.edu.br
# 2021
#
# Precisa ter o github cli instalado
# exemplo: python3 getReposList.py --name 21a-emb-proj1
#

import argparse
import yaml
import os
import subprocess


class getReposList():
    def __init__(self, org, name, wfile):
        self.org = org
        self.name = name
        self.wfile = wfile
        self.GH_LIMIT = 300
        self.rawList = self.get()
        self.list =  self.search()
        self.save()

    def get(self):
        command = 'gh repo list {} --limit {}'.format(self.org, self.GH_LIMIT)
        raw = subprocess.check_output(command, shell=True).decode('utf-8')
        return(raw.splitlines())

    def search(self):
        l = []
        for n in self.rawList:
            url = n.split()[0]
            if url.find(self.name) > 0:
                l.append(url)
        return(l)

    def save(self):
        with open(self.wfile, 'a') as f:
            y = yaml.dump(self.list, explicit_start=True, default_flow_style=False)
            print(y)
            f.write(y)


if __name__ == '__main__':
    argparse.ArgumentParser()
    parser = argparse.ArgumentParser(prog='Download repos url created from github classroom')
    parser.add_argument('--name', default=None, type=str, help='Base repo name.')
    parser.add_argument('--save', default='repo-url.yml',  type=str, help='Save to .yml)')
    parser.add_argument('--org', default='insper-classroom', type=str, help='Organization name.')

    args = parser.parse_args()

    r = getReposList(args.org, args.name, args.save)
