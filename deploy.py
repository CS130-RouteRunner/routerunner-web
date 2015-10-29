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
    parser.add_argument('-V', '--version', default=None,
                        help='set version to deploy')
    return parser


def main():
    parser = get_parser()
    args = parser.parse_args()
    return deploy(args)


def deploy(args):
    cmd = ['appcfg.py']
    cmd.extend(['-A', APPENGINE_NAME])
    # Deploy to a version of the instance, e.g.
    # version-dot-APPENGINE_NAME.appspot.com"
    if args.version:
        cmd += ['--version', args.version]
    update_cmd = cmd[:] + ['update'] + MODULES
    out = sys.stdout
    outerr = sys.stderr
    p = Popen(update_cmd, stdout=out, stderr=outerr)
    p.communicate()
    ret = p.returncode
    return ret


if __name__ == '__main__':
    main()
