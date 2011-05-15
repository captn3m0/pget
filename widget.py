#!/usr/bin/python
import pygtk, gtk
pygtk.require('2.0')
import pyaxel

def print_callback(widget=None, data=None):
	w=pyaxel.Download("http://download918.mediafire.com/v432nne0s3pg/yvq5ehijdjj/VB.NET+Black+Book.chm")
	w.start()
def main():
	win = gtk.Window(gtk.WINDOW_TOPLEVEL)
	win.connect("delete_event", lambda wid, we: gtk.main_quit())
	vbox = gtk.VBox(True, 2)
	win.add(vbox)
	# Add widget code here
	print_button = gtk.Button("Print Text")
	print_button.connect("clicked", print_callback)
	vbox.pack_start(print_button, True, True, 2)
	win.show_all()

if __name__ == "__main__":
	main()
	gtk.main()
