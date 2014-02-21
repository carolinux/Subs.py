#!/usr/bin/env python

__author__="carolinux, zorbash"
__contact__="carolinegr@gmail.com, zorbash@hotmail.com"
__date__ ="$Aug 16, 2011 8:59:46 PM$"


import gtk
import subs   # mai modzul
import shutil # for copying files
import os

# make UI prettier & easier to use. Usability ftw!
# fix the indentation. I prefer all tabs.
# fix naming to be more readable. Moar descriptive function names etc.
# check for too much time added (trivial)
# make a backup of the file just in case, and delete it if all goes well (trivial)

class Subfixer:

	is_file_selected = False
	alert_window = None
	factory = subs.subtitle_file_factory()

        def destroy_alert(self,window):
		self.alert_window.destroy()
 
        def quit(self, event_source):
                try:
			self.subtitle_file.cleanup()
		except:
			pass
                gtk.main_quit()

        def __init__(self):
                self.window = gtk.Window()
                self.choose = gtk.Button("Choose file")
                
                self.apply = gtk.Button("Apply")

                #self.hbox = gtk.HBox()
		self.label = gtk.Label("Enter time shift in milliseconds (can take negative values)")
                self.vbox = gtk.VBox()
                self.text = gtk.Entry()
		self.file_text = gtk.Label("File selected: None")
                self.vbox.pack_start(self.choose)
		self.vbox.pack_start(self.file_text)
		self.vbox.pack_start(self.label)
		
                self.vbox.pack_start(self.text)
                self.vbox.pack_start(self.apply)
                #self.vbox.pack_start(self.hbox)
                
                self.window.set_size_request(400, 300)
                self.window.set_title("SubsFixer")
                self.window.connect("destroy", self.quit)
                self.choose.connect("clicked", self.choose_clicked)
                self.apply.connect("clicked", self.apply_clicked)
                self.window.add(self.vbox)
                #self.window.add(self.text)
                #self.window.add(self.go)
                self.window.show_all()


        def show_alert(self, alert_text): 
		self.alert_window = gtk.Dialog("Message",None, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT)
		self.alert_window.vbox.add(gtk.Label(alert_text))
		btn = gtk.Button("OK")
		self.alert_window.vbox.add(btn)
		btn.connect("clicked", self.destroy_alert) 
		self.alert_window.set_size_request(200, 100)
		self.alert_window.move(100,200)
		self.alert_window.show_all()
		


        def process_file(self):
	   
	    try:  
            	self.subtitle_file = self.factory.create(self.filepath,self.extension) 
	    except:
		self.show_alert("Problem opening file")
		return
 	    #create temp backup of file
	    backup = self.basename+"-backup."+self.extension
	    shutil.copyfile(self.filepath,backup) 
	    print "Created backup  at {}".format(backup)
            
	    try:
	    	self.subtitle_file.process(self.add_time)
	    except: 
		self.show_alert("Problem parsing file")
		self.subtitle_file.cleanup()
		return	
          
	    #delete backup
            print "Finished converting your file"
	    self.show_alert("File converted successfully")

        def apply_clicked(self, btn):

		try:
                	self.add_time = int(self.text.get_text())

		except:
                	self.show_alert("Please enter a valid integer")
			self.text.set_text("")
                        return

		if self.is_file_selected == False:
			self.show_alert("Please select a file first")
			return

                self.process_file()


        def choose_clicked(self, btn):
                
		self.is_file_selected = False
		self.extension =""
		self.file_text.set_text("File selected: None")
                chooser_dialog = gtk.FileChooserDialog("Open file", btn.get_toplevel(), gtk.FILE_CHOOSER_ACTION_OPEN)
                chooser_dialog.add_button(gtk.STOCK_CANCEL, 0)
                chooser_dialog.add_button(gtk.STOCK_OPEN, 1)
                chooser_dialog.set_default_response(1)

                if chooser_dialog.run() == 1:
		    
                    #print chooser_dialog.get_filename()
                    self.filepath = chooser_dialog.get_filename() 
                    chooser_dialog.destroy()

		    try:
		    	self.basename, self.extension = os.path.splitext(self.filepath)
			self.extension = self.extension[1:]
			print  self.extension
		    except:
                    	self.show_alert("Invalid file")            #case for .aaa? meh
			return

		    if self.extension not in self.factory.supported_extensions: # woot, this is super readable
			self.show_alert("Not a valid subtitle file")
			return
 
		    self.is_file_selected = True
	   	    self.file_text.set_text("File selected:"+self.filepath)
		    print "FILE SELECTED"
                else: #no bugs nao :)
             	    chooser_dialog.destroy()


if __name__ == "__main__":
        subfixer = Subfixer()
        gtk.main()
