import sys
import gnome.ui 
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
		
	#Initialization routine
	def __init__( self ):
		self.commonFolders = gtk.ListStore(str) #Pre load a list of used folders here
		self.wTree = gtk.glade.XML( "gwget3.glade" )#Load the glade file
		#Show the main window
		self.wTree.get_widget("main_window").show()
		#Connect all signals
		self.wTree.signal_autoconnect(self)
		
	#Start a new download and add it to the queue
	def on_ok_button_clicked(self,*args):
		self.url = self.new_dlg.get_widget("url_entry").get_text()		#get the url to download
		self.saveTo = self.combo.get_active()							#the folder where to save the file
		self.new_dlg.get_widget("new_window").destroy()					#destroy the new_download window
		
	def on_main_window_destroy(self,*args):
		sys.exit(0)
		
p=Pget()
gtk.main()
