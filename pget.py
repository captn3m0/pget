#! /usr/bin/python
import threading
from time import time
import sys
import gnome.ui
import config
import pyaxel
gnome.init("pget", "0.1")
try:  
	import pygtk  
	pygtk.require("2.0")  
except:  
	pass  
try:  
	import gtk  
	import gtk.glade  
	import gobject
except:  
	print("GTK Not Availible")
	sys.exit(1)

class Pget:
	downloadList = gtk.ListStore(str,str,str,str,str,str)
	workers = []
	#Initialization routine
	def __init__( self ):
		gtk.timeout_add(500, self.my_timer) # call every half a sec
		self.commonFolders = gtk.ListStore(str) #Pre load a list of used folders here
		self.wTree = gtk.glade.XML( "gwget3.glade" )#Load the glade file
		#Show the main window
		self.wTree.get_widget("main_window").show()
		#Connect all signals
		self.wTree.signal_autoconnect(self)
		
	#Browses for a folder location where to save the file
	def on_new_browse_save_in_button_clicked(self,widget):
		#Create a folder chooser dialogue
		self.chooser = gtk.FileChooserDialog(title="Where to download?",action=gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER,
                                  buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN,gtk.RESPONSE_OK))	
		#Run the folder chooser
		response = self.chooser.run()
		if response == gtk.RESPONSE_OK:
			self.new_dlg.get_widget("save_in_comboboxentry").set_active_iter(self.commonFolders.append([self.chooser.get_filename()]))
		#destroy once the work is done
		self.chooser.destroy()

	#Close the add download window
	def on_cancel_button_clicked(self,widget):
		self.new_dlg.get_widget("new_window").destroy()

	#Show the add new download ui and add it to download list
	def on_button_new_clicked(self,*args):
		#Our new form
		self.new_dlg = gtk.glade.XML("newdownload.glade")
		# get the clipboard
		clipboard = gtk.clipboard_get()
		# read the clipboard text data.
		text = clipboard.wait_for_text()
		if len(text) > 0 and text[0:4] == 'http':
			self.new_dlg.get_widget("url_entry").set_text(text)
		#Connect the signals
		self.new_dlg.signal_autoconnect(self)
		#Combobox
		self.combo = self.new_dlg.get_widget("save_in_comboboxentry")	#init
		self.combo.set_model(self.commonFolders)							#set model
		self.combo.set_text_column(0)									#Singe column
		#show the window
		self.new_dlg.get_widget("new_window").show()
	def my_timer(self):
		#print '======= NoW', len(self.workers),'========='
		#print '___________________'
		sys.stdout.flush()
		if len(self.workers):
			for worker in self.workers[:]:
				if(worker.complete == True):		#remove the worker if download is complete
					print 'something got completed'
					self.workers.remove(worker)
		return True

	#Start a new download and add it to the queue
	def on_ok_button_clicked(self,*args):
		url = self.new_dlg.get_widget("url_entry").get_text()		#get the url to download
		saveTo = self.combo.get_active()							#the folder where to save the file
		options = config.Pconfig()	#default options
		if saveTo > -1 :		#if user choose a folder
			options.output_folder = self.combo.get_model()[saveTo][0]
		self.combo.destroy()
		self.combo = None
		self.new_dlg.get_widget("new_window").hide()
		self.new_dlg.get_widget("new_window").destroy()					#destroy the new_download window
		#Start download job in a new thread
		#print 'd2'
		w = pyaxel.Download(url,options,self.download_finished_callback)					#Create an instance of the thread
		#print 'd3'
		self.workers.append(w)					#Append the worker to our list
		#print 'd4'
		w.start()								#Start the thread		
		print 'd-is w started ?'
		sys.stdout.flush()
	def download_finished_callback(self):
		print 'dl complete'
	def on_main_window_destroy(self,*args):
		for worker in self.workers:
			worker.quit()
		sys.exit(0)

p=Pget()
gtk.main()
