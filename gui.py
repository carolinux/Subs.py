#!/usr/bin/env python

__author__="carolinux, zorbash"
__contact__="carolinegr@gmail.com, zorbash@hotmail.com"
__date__ ="$Aug 10, 2011 8:59:46 PM$"


import gtk
import datetime
import subs # our modzul

#make prettier in general - WHERE BE DOCUMENTATION? FFS.
#show teh file selected...
#opshun to choose another fiel

class Subfixer:

	is_file_selected = False
	supported_extensions = {"srt"}

        def destroy(self, window):
                gtk.main_quit()

        def __init__(self):
                self.window = gtk.Window()
                self.choose = gtk.Button("Choose srt file")
                
                self.apply = gtk.Button("Apply")

                #self.hbox = gtk.HBox()
		self.label = gtk.Label("Enter time shift in milliseconds (can take negative values)")
                self.vbox = gtk.VBox()
                self.text = gtk.Entry()

                self.vbox.pack_start(self.choose)
		self.vbox.pack_start(self.label)
                self.vbox.pack_start(self.text)
                self.vbox.pack_start(self.apply)
                #self.vbox.pack_start(self.hbox)
                
                self.window.set_size_request(400, 300)
                self.window.set_title("SubsFixer")
                self.window.connect("destroy", self.destroy)
                self.choose.connect("clicked", self.choose_clicked)
                self.apply.connect("clicked", self.apply_clicked)
                self.window.add(self.vbox)
                #self.window.add(self.text)
                #self.window.add(self.go)
                self.window.show_all()


        def show_alert(self, alert_text): #den ehei alert class? meh
		alert_window = gtk.Window()
		alert_window.add(gtk.Label(alert_text))
		alert_window.set_size_request(400, 300)
		#alert_window.connect("destroy", alert_window.main_quit())
		alert_window.show_all()
		


        def process_file(self):

	    if self.is_file_selected == False:
		self.show_alert("Please select a file first")
		return

            start_of_write= self.f.tell()
            line=self.f.readline()
            
            while  (line!=""):
                if self.sf.is_time_line(line):                           #only parse lines with time values in them
			try:
                    		self.sf.add_time(line,self.add_time,start_of_write)  #make dis throw an excepshun
			except:
				self.show_alert("Problem parsing file")
				return

                start_of_write= self.f.tell()
                line=self.f.readline()

            self.f.close()
            print "Finished converting your file"

        def apply_clicked(self, btn):

		try:
                	self.add_time = int(self.text.get_text()) #IS THIS AN INT OR NOT? 

		except:
                	self.show_alert("Please enter a valid integer")
			self.text.set_text("")
                        return

                self.process_file()


        def choose_clicked(self, btn):
                
                chooser_dialog = gtk.FileChooserDialog("Open .srt file", btn.get_toplevel(), gtk.FILE_CHOOSER_ACTION_OPEN)
                chooser_dialog.add_button(gtk.STOCK_CANCEL, 0)
                chooser_dialog.add_button(gtk.STOCK_OPEN, 1)
                chooser_dialog.set_default_response(1)

                if chooser_dialog.run() == 1:
		    
                    print chooser_dialog.get_filename()
                    filepath = chooser_dialog.get_filename() #IS THIS A SRT FILE? (EXTENSION CHECK)
                    chooser_dialog.destroy()

		    try:
		    	extension = filepath.split(".")[len(filepath.split("."))-1] # \m/
			#print  extension
		    except:
                    	self.show_alert("Invalid file")            #case for .aaa? meh
			return

		    if extension not in self.supported_extensions: # woot, this is super readable
			self.show_alert("Not a valid subtitle file")
			return
 
		    self.is_file_selected = True
                    self.f = open(filepath, 'r+')
                    self.sf = subs.srt_file(self.f) #will implement extenshun chooser, liek a factory class or sumfin
                else: #no bugs nao
             	    chooser_dialog.destroy()


if __name__ == "__main__":
        subfixer = Subfixer()
        gtk.main()
