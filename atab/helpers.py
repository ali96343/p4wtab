import sys, os, json, uuid, datetime

import sys


DATE_FORMAT =  "%d.%m.%Y %H:%M:%S"

def check_py_version():
    req_version = (3,9)
    cur_version = sys.version_info

    if cur_version < req_version:
         print ( "                                        warning! app tested with python 3.9" )

check_py_version()




def get_unique_name(orig_name, use_orig=True):
    prefix = "at_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S.%f_")
    uname = prefix + orig_name if use_orig else prefix + str(uuid.uuid4())
    return uname[:255] if len(uname) > 255 else uname


def data2file(data, fnm, mode="wb"):
    try:
        with open(fnm, mode) as f:
            f.write(data)
    except IOError:
        print(f"data2file: IOError, cannot write {fnm}")
        fnm = None
    return fnm


def file2data(fnm, mode="rb"):
    data = ""
    try:
        with open(fnm, "rb") as f:
            data = f.read()
    except IOError:
        print("file2data: IOError")
        data = f"Error file2data: File {r.orig_file_name} {file_path} does not appear to exist"
    return data


