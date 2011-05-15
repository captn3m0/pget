#!/usr/bin/python

import sys
import urllib2
import re
import getopt
import threading

##########################################################################
def process_input(argv):
    """
    Processes all the input suplied by the user. Returns a list with the 
    urls to download and the number of threads to use.
    """

    numThreads = 5      # default number of threads
    try:
        opts, args = getopt.getopt(argv, "hn:", ["help", "threads="])
    except getopt.GetoptError:
        usage("ppd.py: unknown argumment")
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage("ppd.py: multithread download manager")
            sys.exit()
        elif opt in ("-n", "--threads"):
            numThreads = arg

    if (not args):      # no url at all...
        usage("ppd.py: missing url")
        sys.exit(1)

    url_list = []
    for url in args:
        s_url = re.compile(r'^(http://.*)\[(\d+)-(\d+)\](.*)')
        if (s_url.search(url)): # if it's a range url, expands it.
            spawn_list = UrlExpander(url)
            url_list.extend(spawn_list.list)
        else:
            url_list.append(url)

    return url_list, int(numThreads)

##########################################################################
def usage(header):
    """ Prints the help message. Returns nothing. """

    print header
    print """
Usage: ppd.py [OPTON]... [URL]...

Options index:
    -h,         --help          Shows this help menu.
    -n n,       --threads=n     Spawns n working threads.

URL format:
    ppd.py handles standart url forms. It also supports range style urls.

Example:
    ppd.py http://www.somesite.com/index.html 
    ppd.py http://www.somesite.com/pictures/pic[1-10].jpg
    ppd.py http://www.somesite.com/pictures/pic[01-10].jpg (padding support)
    """

#############################################################################
class UrlExpander:
    """
    This class expands a "range url" to a list containing urls.
    """

    def __generateList__(self):
        """
        Generates a list with all the urls.
        """
        list_urls = []
        min = int(self.min)
        pad = len(self.min)
        max = int(self.max)
        for num in range(min, max + 1):
            num_str = str(num)
            num_str = num_str.zfill(pad)
            list_urls.append(self.prefix + num_str + self.suffix)
        return list_urls

    def __init__(self, url):
        """ Dismember the url range a generates the list. """
        s_url= re.compile(r'^(http://.*)\[(\d+)-(\d+)\](.*)')
        try: # get all the necessary info to make an url
            self.prefix, self.min, \
                    self.max, self.suffix = s_url.search(url).groups()
        except AttributeError:
            usage("ppd.py: URL format error.")
            sys.exit(2)
        self.list = self.__generateList__()

#############################################################################
class GetFile(threading.Thread):
    """ GetFile is a thread that downloads a remote file.  """ 
        
    def __init__(self, url, queue):
        """ Receives a url to download and a queue (semphore) to wait. """

        threading.Thread.__init__(self)
        self.url = url
        self.queue = queue

    def __getFiles__(self):
        """ Downloads a the url. """

        self.queue.acquire()
        request = urllib2.Request(self.url)
        try:
            handle = urllib2.urlopen(request)
        except IOError: # 400+ error
            print "It seems to be a problem with ", self.url
        except ValueError:      # url error
            print "Bad format:", self.url
        else:
            fileRE = re.compile(r'.*\/([^/]*)$')
            try:        # get the file name
                fileName = fileRE.search(self.url).groups()
            except AttributeError:
                usage("ppd.py: URL format error.")
                sys.exit(2)
            data = handle.read()
            arq = open(fileName[0], 'w')
            arq.write(data)
            arq.close()
            print "Download completed:", fileName[0]
        self.queue.release()

    def run(self):
        self.__getFiles__()

##########################################
def download(urls, numThreads):
    """ Sets up a queue and start the download process. """

    downQueue = threading.Semaphore(numThreads) # the download queue

    # start all threads
    downloadThreads = []
    for url in urls:
        down = GetFile(url, downQueue)
        downloadThreads.append(down)
        down.start()

    # join them
    for thread in downloadThreads:
        thread.join

############### main ###################
urls, numThreads = process_input(sys.argv[1:])
download(urls, numThreads)

