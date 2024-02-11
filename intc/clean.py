# Copyright the author(s) of intc.
import os
import shutil


def rm_dirs(dirpath):
    if os.path.exists(dirpath) and os.path.isdir(dirpath):
        shutil.rmtree(dirpath)


if __name__ == "__main__":
    rm_dirs("./build")
    rm_dirs("./intc.egg-info")
    rm_dirs("./logs")
    rm_dirs("./dist")
