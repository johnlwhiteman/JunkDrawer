#!/usr/bin/env python3
import json
import os
import pprint
import shutil
import sys
import time

class Msg:

    LABEL = "MSG"

    @staticmethod
    def abort(msg, abortFlag=False):
        Msg.raw("[{0}][Abort]: {1}".format(Msg.LABEL, msg), isErrorFlag=True)
        if abortFlag:
            sys.exit(1)

    @staticmethod
    def error(msg):
        Msg.raw("[{0}][Error]: {1}".format(Msg.LABEL, msg), isErrorFlag=True)

    @staticmethod
    def exe(cmd):
        Msg.raw("[{0}][Exe]: {1}".format(Msg.LABEL, msg), isErrorFlag=False)

    @staticmethod
    def flush():
        sys.stdout.flush()
        sys.stderr.flush()

    @staticmethod
    def pretty(msg):
        pprint.pprint(msg)
        Msg.flush()

    @staticmethod
    def raw(msg, isErrorFlag=False):
        if isErrorFlag:
            sys.stderr.write("{0}\n".format(msg))
            sys.stderr.flush()
        else:
            sys.stdout.write("{0}\n".format(msg))
            sys.stdout.flush()

    @staticmethod
    def show(msg):
        Msg.raw("[{0}]: {1}".format(Msg.LABEL, msg), isErrorFlag=False)


class DateTime:

    @staticmethod
    def convertEpochToTimestamp(epoch):
        return time.strftime("%Y-%m-%dT%H:%M:%S+0000", time.localtime(epoch))

    @staticmethod
    def convertTimestampToEpoch(timestamp):
        return int(time.mktime(time.strptime(timestamp, "%Y-%m-%dT%H:%M:%S+0000")))

    @staticmethod
    def getEpoch():
        return int(time.time())

    @staticmethod
    def getTimestamp():
        return DateTime.convertEpochToTimestamp(DateTime.getEpoch())


class Dir:

    @staticmethod
    def delete(path):
        if Dir.exists(path):
            shutil.rmtree(path)

    @staticmethod
    def expandPath(path):
        return os.path.expanduser(path)

    @staticmethod
    def exists(path):
        return os.path.isdir(path)

    @staticmethod
    def make(path):
        if not Dir.exists(path):
            os.makedirs(path, exist_ok=True)


class File:

    @staticmethod
    def copy(srcPath, tgtPath):
        try:
            shutil.copyfile(srcPath, tgtPath)
        except IOError as e:
            Msg.abort("Can't copy log file: {0} to {1}\n{2}".format(srcPath, tgtPath, e), True)

    @staticmethod
    def delete(path):
        if not os.path.isfile(path):
            return
        os.unlink(path)

    @staticmethod
    def exists(path):
        return os.path.isfile(path)

    @staticmethod
    def expandPath(path):
        return os.path.expanduser(path)

    @staticmethod
    def find(name):
        paths = []
        if File.exist(name):
            paths.append("{0}/{1}".format(File.getCanonicalPath(os.getcwd()), name))
        for directory in os.environ["PATH"].split(os.pathsep):
            path = "{0}/{1}".format(File.getCanonicalPath(directory), name)
            if File.exists(path):
                paths.append(path)
        if len(paths) < 1:
            return None
        return sorted(list(set(paths)))

    @staticmethod
    def getAbsPath(path):
        return File.getCanonicalPath(os.path.abspath(path))

    @staticmethod
    def getBasename(path):
        return os.path.basename(path)

    @staticmethod
    def getCanonicalPath(path):
        return path.replace('\\', '/')

    @staticmethod
    def getDirectory(path):
        return File.getCanonicalPath(os.path.abspath(os.path.join(path, os.pardir)))

    @staticmethod
    def getExtension(path):
        return os.path.splitext(path)[1].strip().replace(".", "")

    @staticmethod
    def getFileSizeAsBytes(path):
        return os.path.getsize(path)

    @staticmethod
    def getName(path):
        return File.getCanonicalPath(os.path.basename(os.path.splitext(path)[0]))

    @staticmethod
    def getModifiedTimeAsEpoch(path):
        return int(os.path.getmtime(path))

    @staticmethod
    def read(path, asJsonFlag=False, asBytes=False):
        content = None
        try:
            with open(path, "r",  encoding="utf-8") as fd:
                if asJsonFlag:
                    content = json.load(fd)
                else:
                    content = fd.read()
        except IOError as e:
            Msg.abort("Can't read file: {0}\n{1}".format(path, e), True)
        return content

    @staticmethod
    def write(path, content, asJsonFlag=False, asBytesFlag=False):
        try:
            Dir.make(File.getDirectory(path))
            mode = "w"
            if abBytesFlag:
                mode = "wb"
            with open(path, mode, encoding="utf-8") as fd:
                if asJsonFlag:
                    json.dump(content, fd, indent=4, sort_keys=True)
                else:
                    fd.write(content)
        except IOError as e:
            Msg.abort("Can't write file: {0}\n{1}".format(path, e), True)


class Stopwatch(object):

    def __init__(self):
        self.__startSecs = 0
        self.__stopSecs = 0

    def elapsed(self):
        return self.__stopSecs - self.__startSecs

    def reset(self):
        self.__startSecs = 0
        self.__stopSecs = 0

    def start(self):
        self.reset()
        self.__startSecs = DateTime.getEpoch()

    def stop(self):
        self.__stopSecs = DateTime.getEpoch()

