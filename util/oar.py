#!/usr/bin/env python3
import argparse
import os
import typing
import shutil
import subprocess
import json

_DIR_TAR = "tar"
_DIR_FS = "fs"
_FILE_ARG = "--file"
_LS = "ls"
_UNPACK = "unpack"
_INFO = "info"
_UNTAR = "xf"
_MODES = [_LS, _UNPACK, _INFO]


def _untar(src: str, dst: str, args: str) -> None:
    subprocess.run(["tar", args, src, "-C", dst])


def _cat(file: str) -> None:
    print("file: {}".format(file))
    with open(file, "r") as f:
        print(json.dumps(json.loads(f.read()), indent=2))
    print("")


def _import(args: argparse.Namespace) -> None:
    os.mkdir(args.dst)
    for d in [_DIR_TAR, _DIR_FS]:
        os.mkdir(os.path.join(args.dst, d))
    dest = os.path.join(args.dst, _DIR_TAR)
    fs = os.path.join(args.dst, _DIR_FS)
    _untar(args.src, dest, _UNTAR)
    is_info = args.mode == _INFO
    if is_info:
        for file in ["index.json", "oci-layout"]:
            _cat(os.path.join(dest, file))
    data = []
    info = []
    for root, dirs, files in os.walk(os.path.join(dest, "blobs")):
        for file in files:
            f = os.path.join(root, file)
            out = subprocess.check_output(["file", f])
            res = out.decode("utf-8").strip()
            if ": POSIX tar archive" in res:
                data.append(f)
                continue
            if ": JSON text data" in res:
                info.append(f)
                continue
            raise Exception("unknown data: {}".format(res))
    if is_info:
        for item in info:
            _cat(item)
        return
    untar = _UNTAR
    if args.mode == _LS:
        untar = "tf"
    for d in data:
        _untar(d, fs, untar)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("src", help="source file")
    parser.add_argument("dst", help="working directory")
    parser.add_argument("--mode", default=_UNPACK, help="operating mode: {}".format(",".join(_MODES)))
    args = parser.parse_args()
    if args.mode not in _MODES:
        raise Exception("unknown mode: {}", args.mode)
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
