#!/usr/bin/env python

__author__="carolinux, zorbash"
__contact__="carolinegr@gmail.com, zorbash@hotmail.com"
__date__ ="$Aug 10, 2011 8:59:46 PM$"


import gtk
import subs # our modzul
import shutil # for copying files

#make prettier in general # HAO?
#show teh file selected... DONE
#opshun to choose another fiel, well, sure they can.. NOT NECESARY
#make a backup of the file just in case, and delete it if all goes well :)  hhmm.. why evan delete?
#factory class for different subtitle types.. or sumfin --> whee extenshuns

class Subfixer:

	is_file_selected = False
	supported_extensions = ("srt")
	alert_window = None

        def destroy_alert(self,window):
		self.alert_window.destroy()
 
        def quit(self, event_source):
                try:
			self.f.close()
		except:
			pass
                gtk.main_quit()

        def __init__(self):
                self.window = gtk.Window()
                self.choose = gtk.Button("Choose srt file")
                
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


        def show_alert(self, alert_text): #den ehei alert class? meh
		self.alert_window = gtk.Dialog("Message",None, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT)
		self.alert_window.vbox.add(gtk.Label(alert_text))
		btn = gtk.Button("OK")
		self.alert_window.vbox.add(btn)
		btn.connect("clicked", self.destroy_alert) 
		self.alert_window.set_size_request(200, 100)
		self.alert_window.move(100,200)
		self.alert_window.show_all()
		


        def process_file(self):

	    if self.is_file_selected == False:
		self.show_alert("Please select a file first")
		return

	    #create temp backup of file
            shutil.copyfile(self.filepath,"backup.srt")
	    self.f = open(self.filepath, 'r+')
            self.sf = subs.srt_file(self.f) #will implement extenshun chooser, liek a factory class or sumfin

            start_of_write= self.f.tell()
            line=self.f.readline()
            
            while  (line!=""):
                if self.sf.is_time_line(line):                           #only parse lines with time values in them
			try:
                    		self.sf.add_time(line,self.add_time,start_of_write)  #make dis throw an excepshun
			except:
				self.show_alert("Problem parsing file.") 
				return

                start_of_write= self.f.tell()
                line=self.f.readline()

            self.f.close()
	    #delete backup
            print "Finished converting your file"
	    self.show_alert("File converted successfully")

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
		    
                    #print chooser_dialog.get_filename()
                    self.filepath = chooser_dialog.get_filename() 
                    chooser_dialog.destroy()

		    try:
		    	extension = self.filepath.split(".")[len(self.filepath.split("."))-1] # \m/
			#print  extension
		    except:
                    	self.show_alert("Invalid file")            #case for .aaa? meh
			return

		    if extension not in self.supported_extensions: # woot, this is super readable
			self.show_alert("Not a valid subtitle file")
			return
 
		    self.is_file_selected = True
	   	    self.file_text.set_text("File selected:"+self.filepath)
		   
                else: #no bugs nao :)
             	    chooser_dialog.destroy()


if __name__ == "__main__":
        subfixer = Subfixer()
        gtk.main()
