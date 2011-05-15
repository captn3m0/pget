#! /usr/bin/python
#Axel Test
import pyaxel
import threading
import time
import sys

#p = pyaxel.download("http://download918.mediafire.com/v432nne0s3pg/yvq5ehijdjj/VB.NET+Black+Book.chm")
#Stats : pyaxel vs axel
#real 11.717	user 0.124	sys 0.180	pcpu 2.59 pyaxel
#real 12.716	user 0.036	sys 0.220	pcpu 2.01   axel

w=pyaxel.Download("http://download918.mediafire.com/v432nne0s3pg/yvq5ehijdjj/VB.NET+Black+Book.chm")
w.start()
#w2=pyaxel.Download("http://www.greenteapress.com/thinkpython/thinkpython.pdf")
#w2.start()
