"""Resolve exact PR merge data without executing PR code or relaxing parent checks."""
import argparse
import json
import re
import subprocess


def checked_sha(value):
    if not isinstance(value,str) or not re.fullmatch(r'[a-f0-9]{40}',value):
        raise ValueError('Expected a full commit identity')
    return value


def resolve(number,base,head,fetch_reference,read_pull,read_parents,read_trees=None):
    if type(number)is not int or number<=0:raise ValueError('Expected a positive PR number')
    checked_sha(base);checked_sha(head)
    merge_ref=True
    try:
        revision=fetch_reference(f'refs/pull/{number}/merge')
    except subprocess.CalledProcessError:
        merge_ref=False
        # A ready-for-review event can start after GitHub removed the merge ref.
        # Only the same PR's verified completed merge is an admissible fallback.
        pull=read_pull(number)
        if (pull.get('number')!=number or pull.get('state')!='closed' or pull.get('merged') is not True
                or pull.get('head',{}).get('sha')!=head or pull.get('base',{}).get('sha')!=base):
            raise ValueError('Merge ref unavailable; no completed merge with the exact event identity')
        revision=fetch_reference(checked_sha(pull.get('merge_commit_sha')))
        if revision!=pull['merge_commit_sha']:raise ValueError('Fetched merge differs from API identity')
        if fetch_reference(f'refs/pull/{number}/head')!=head:raise ValueError('Fetched head differs from the exact event identity')
    checked_sha(revision)
    parents=read_parents(revision)
    if merge_ref:
        if parents!=[base,head]:raise ValueError('Merge parents differ from the exact event base/head')
    elif parents==[base,head]:
        pass
    elif parents==[base] and read_trees is not None:
        if read_trees(revision)!=read_trees(head):
            raise ValueError('Fallback merge tree differs from the exact event head')
    else:
        raise ValueError('Merge parents differ from the exact event base/head')
    return revision


def git(*args):
    return subprocess.run(['git',*args],check=True,capture_output=True,text=True).stdout.strip()


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--pr',type=int,required=True);p.add_argument('--base',required=True);p.add_argument('--head',required=True);a=p.parse_args()
    import os
    repo=os.environ.get('GITHUB_REPOSITORY','')
    if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+',repo):raise SystemExit('Invalid repository identity')
    def fetch(ref):
        git('fetch','--no-tags','--depth=2','origin',ref)
        return git('rev-parse','FETCH_HEAD')
    def pull(number):
        return json.loads(subprocess.run(['gh','api',f'repos/{repo}/pulls/{number}'],check=True,capture_output=True,text=True).stdout)
    try:
        print(resolve(
            a.pr,a.base,a.head,fetch,pull,
            lambda rev:git('show','-s','--format=%P',rev).split(),
            lambda rev:git('show','-s','--format=%T',rev).strip(),
        ))
    except (ValueError,subprocess.CalledProcessError,json.JSONDecodeError):
        # Do not echo authenticated subprocess output or API payloads.
        raise SystemExit('Cannot verify an exact merge revision; review gate remains closed') from None


if __name__=='__main__':main()
