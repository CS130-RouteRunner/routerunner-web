#!/usr/bin/env python
import argparse
import os
import sys
from subprocess import Popen

APPENGINE_NAME = 'route-runner-130'
MODULES = ['app.yaml']


def get_parser():
    parser = argparse.ArgumentParser(
        description='Deploys to Google App Engine')
    return parser


def main():
    return deploy()


def deploy():
    cmd = ['appcfg.py']
    cmd.extend(['-A', APPENGINE_NAME])
    update_cmd = cmd[:] + ['update'] + MODULES
    out = sys.stdout
    outerr = sys.stderr
    p = Popen(update_cmd, stdout=out, stderr=outerr)
    p.communicate()
    ret = p.returncode
    return ret


if __name__ == '__main__':
    main()
