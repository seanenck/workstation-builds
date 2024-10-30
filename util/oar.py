#!/usr/bin/env python3
import argparse
import os
import typing
import shutil
import subprocess

_DIR_TAR = "tar"
_DIR_FS = "fs"
_FILE_ARG = "--file"

def _untar(src: str, dst: str) -> None:
    subprocess.run(["tar", "xf", src, "-C", dst])


def _import(args: argparse.Namespace) -> None:
    os.mkdir(args.dst)
    for d in [_DIR_TAR, _DIR_FS]:
        os.mkdir(os.path.join(args.dst, d))
    dest = os.path.join(args.dst, _DIR_TAR)
    fs = os.path.join(args.dst, _DIR_FS)
    _untar(args.src, dest)
    for root, dirs, files in os.walk(os.path.join(dest, "blobs")):
        for file in files:
            f = os.path.join(root, file)
            out = subprocess.check_output(["file", f])
            res = out.decode("utf-8").strip()
            if ": POSIX tar archive" in res:
                _untar(f, fs)
                continue
            if ": JSON text data" in res:
                continue
            raise Exception("unknown data: {}".format(res))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("src", help="source file")
    parser.add_argument("dst", help="working directory")
    args = parser.parse_args()
    if os.path.exists(args.dst):
        raise Exception("{} already exists".format(args.dst))
    try:
        _import(args)
    except Exception as e:
        if os.path.exists(args.dst):
            shutil.rmtree(args.dst)
        raise

if __name__ == "__main__":
    main()
