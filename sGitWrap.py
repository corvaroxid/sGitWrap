import os,sys,urllib2,subprocess,argparse

def main():
    
    commands=["extract",
              "clone"]

    parser = argparse.ArgumentParser()
    parser.add_argument("-k","--cmd", help="input commands {0}".format(commands))
    parser.add_argument("-u","--user", help="write gituser")
    parser.add_argument("-r","--rep", help="write repository")
    parser.add_argument("-f","--file", help="filename")
    parser.add_argument("-wG","--withWget", help="download with wget")


    args = parser.parse_args()
    
    if args.cmd == "clone" and args.user is None and args.rep is None:
        subprocess.call(["git","clone","https://github.com/corvaroxid/noStruct.git"])
    elif args.cmd == "clone" and args.user is not None and args.rep is not None:
        subprocess.call(["git","clone","https://github.com/{0}/{1}.git".format(args.user, args.rep)])
    elif args.cmd == "extract" and args.user is not None and args.rep is not None and args.withWget is not None:
        subprocess.call(["wget","https://github.com/{0}/{1}/raw/master/{2}".format(args.user, args.rep, args.withWget)])
    elif args.cmd == "extract" and args.user is not None and args.rep is not None and args.file is not None and args.withWget is None:
        downloadFile("https://github.com/{0}/{1}/raw/master/{2}".format(args.user, args.rep, args.file))
    else:
        print "no args"


def getPath(url, name=None, directory=None):    
    if directory==None: directory=os.curdir
    if not os.path.exists(directory): os.mkdir(directory)
    if name==None:
        path="%s%s%s" % (
            directory,
            os.sep,
            url.split("/")[-1])
    else:
        path="%s%s%s" % (
            directory,
            os.sep,
            name)
    return path

def downloadFile(url, newName=None, dir=None):
    newPath = getPath(url, newName, dir)
 
    if not os.path.exists(newPath):
        localLen = 0
    else:
        localLen = os.path.getsize(newPath)
 
    req = urllib2.Request(url)
    req.headers['Range'] = 'bytes='+str(localLen)+'-'
 
    print "Sending request..."
    remoteLen = 0
    try:
        res = urllib2.urlopen(url)
        remoteLen = int(res.info().getheader("Content-Length"))
    except urllib2.HTTPError, e:
        print e
        return
    except urllib2.URLError, e:
        print e
        return
 
    print "Received code:", res.getcode()
 
    print "Length: %d (%.02fM) [%s]" % (
        remoteLen,
        remoteLen/1024.0/1024.0,
        res.info().getheader("Content-Type"))
 
    print "Saving to: ", newPath
 
    if localLen == 0:
        localFile = open(newPath, "wb")
    elif localLen < remoteLen:
        localFile = open(newPath, "ab")
    elif localLen == remoteLen:
        print "File has downloaded already."
        return
 
    try:
        remoteFile = urllib2.urlopen(req)
    except urllib2.HTTPError, e:
        print e
        return
    except urllib2.URLError, e:
        print e
        return
 
    print "Downloading %s - %s (%s bytes) ..." % (remoteFile.url, newPath, remoteLen)
    if remoteLen != 0:
        remoteLen = float(remoteLen)
        bytesRead = float(localLen)
        for line in remoteFile:
            bytesRead += len(line)
            sys.stdout.write("\r%s: %.02f/%.02f kb (%d%%)" % (
                newPath,
                bytesRead/1024.0,
                remoteLen/1024.0,
                100*bytesRead/remoteLen))
            sys.stdout.flush()
            localFile.write(line)
    remoteFile.close()
    localFile.close()
    print "\nFile %s has been downloaded.\n" % newPath


if __name__ == "__main__":
    main()
