#!/usr/bin/env python3
"""List working-tree changes as JSON without reading or modifying file contents."""

import argparse
import json
import os
import subprocess
import sys


def git(repo, *args):
    result = subprocess.run(
        ["git", "--no-optional-locks", "-C", repo, *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )
    return result.stdout


def paths(repo, *args):
    return [os.fsdecode(path) for path in git(repo, *args).split(b"\0") if path]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=".", help="Git worktree path (default: .)")
    args = parser.parse_args()

    try:
        # Git terminates this output with a newline; preserve any newline in the path.
        root = os.fsdecode(git(args.repo, "rev-parse", "--show-toplevel").removesuffix(b"\n"))
        diff_args = ("--name-only", "--no-renames", "--ignore-submodules=none", "-z")
        result = {
            "repository": root,
            "staged": paths(root, "diff", "--cached", *diff_args, "--"),
            "unstaged": paths(root, "diff", *diff_args, "--"),
            "untracked": paths(root, "ls-files", "--others", "--exclude-standard", "-z", "--"),
            "conflicted": paths(root, "diff", "--diff-filter=U", *diff_args, "--"),
        }
    except FileNotFoundError:
        print("Git executable not found.", file=sys.stderr)
        return 1
    except subprocess.CalledProcessError as error:
        print(os.fsdecode(error.stderr).rstrip(), file=sys.stderr)
        return 1

    print(json.dumps(result, ensure_ascii=True, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
