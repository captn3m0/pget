#! /usr/bin/python
#Axel Test
import pyaxel
import threading
import time

#p = pyaxel.download("http://download918.mediafire.com/v432nne0s3pg/yvq5ehijdjj/VB.NET+Black+Book.chm")
#Stats : pyaxel vs axel
#real 11.717	user 0.124	sys 0.180	pcpu 2.59 pyaxel
#real 12.716	user 0.036	sys 0.220	pcpu 2.01   axel

class DownloadWorker(threading.Thread):
	def set_url(self,url):
		self.url = url
		return self
	def set_options(self,options):
		self.options = options
		return self
	def complete_callback(self):
		#Function is called when download is completed
		print 'Download Complete'
	def run(self):
		self.worker = pyaxel
		self.worker.download(self.url,self.options,self.complete_callback)
	def progress(self):
		return self.worker.progress
	def complete(self):
		return self.worker.complete
	def quit(self):
		self.worker.quit()


w=DownloadWorker().set_url("http://download918.mediafire.com/v432nne0s3pg/yvq5ehijdjj/VB.NET+Black+Book.chm").set_options(None)
w.start()
