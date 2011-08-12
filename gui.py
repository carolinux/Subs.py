#!/usr/bin/env python

__author__="zorbash"
__contact__="zorbash@hotmail.com"
__date__ ="$Aug 10, 2011 8:59:46 PM$"


import gtk
import datetime
import subs # our module





class Subfixer:


        def destroy(self, window):
                gtk.main_quit()

        def __init__(self):
                self.window = gtk.Window()
                self.choose = gtk.Button("Choose srt file")
                
                self.apply = gtk.Button("Apply")

                #self.hbox = gtk.HBox()
                self.vbox = gtk.VBox()
                self.text = gtk.Entry()

                self.vbox.pack_start(self.choose)
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


        


        def process_file(self):
            start_of_write= self.f.tell()
            line=self.f.readline()
            
            while  (line!=""):
                #print line 
                if self.sf.is_time_line(line):#only parse lines with time values in them
                    self.sf.add_time(line,self.add_time,start_of_write)
                start_of_write= self.f.tell()
                line=self.f.readline()

            self.f.close()
            print "Finished converting your file"

        def apply_clicked(self, btn):
                #self.browser.open(self.text.get_text())
                self.add_time = int(self.text.get_text()) #IS THIS AN INT OR NOT? 
                print self.add_time
                self.process_file()

        def choose_clicked(self, btn):
                
                chooser_dialog = gtk.FileChooserDialog("Open .srt file", btn.get_toplevel(), gtk.FILE_CHOOSER_ACTION_OPEN)
                chooser_dialog.add_button(gtk.STOCK_CANCEL, 0)
                chooser_dialog.add_button(gtk.STOCK_OPEN, 1)
                chooser_dialog.set_default_response(1)

                if chooser_dialog.run() == 1:
                    print chooser_dialog.get_filename()
                    filepath = chooser_dialog.get_filename() #IS THIS A SRT FILE? (EXTENSION CHECK)
                    self.f = open(filepath, 'r+')
                    self.sf = srt_file(self.f)
                    chooser_dialog.destroy()
                #if chooser_dialog.run() == 0:
                 #   chooser_dialog.destroy()


if __name__ == "__main__":
        subfixer = Subfixer()
        gtk.main()
