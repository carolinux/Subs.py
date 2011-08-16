#!/usr/bin/env python

__author__="carolinux"
__contact__="carolinegr@gmail.com"
__date__ ="$Aug 16, 2011 8:59:46 PM$"

import datetime
import re

class InvalidFormatException(Exception):
    def __init__(self, value):
       self.value = value
    def __str__(self):
       return repr(self.value)

class NegativeTimeException(Exception):
    def __init__(self, value):
       self.value = value
    def __str__(self):
       return repr(self.value)


class subtitle_file_factory: #halp, i'm trapped

     supported_extensions = ("srt","ssa","ass")
     def __init__(self):
	pass

     def create(self,filepath,extension):
	try:	
		if extension=="srt":
			return srt_file(filepath)
		if extension=="ssa" or extension =="ass" :
			return ssa_file(filepath)
		return None
	except:
		raise Exception("Problem opening file")


class subtitle_file: 

    def __init__(self,filepath):
	try:
        	self.file= open(filepath, 'r+')
	except:
		raise Exception("Problem opening file")

    def process(self,add_time):
       start_of_write= self.file.tell()
       line=self.file.readline()
            
       while line!="":
                if self.is_time_line(line):                           #only parse lines with time values in them
			try:
                    		self.add_time(line,add_time,start_of_write)  #make dis throw an excepshun
			except:
				raise InvalidFormatException("Problem parsing file")
				return

        	start_of_write= self.file.tell()
       	 	line=self.file.readline()
       self.file.close()

    def cleanup(self):
       self.file.close()

class ssa_file(subtitle_file):

#[Events]
#Format: Marked, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
#Dialogue: Marked=0,0:01:31.53,0:01:33.80,Default,NTP,0000,0000,0000,!Effect,Te lo debo una vez ms.t


    def is_time_line(self,line):
	
    	if re.match('Dialogue:',line) is not None: #ssa/ass files can also have Sound:,Movie:,Command:, Picture: events some of which ignore the end time though
		return True
	
	return False

    def format_time(self,dt_object):
        return str(dt_object.hour).zfill(1) +":"+str(dt_object.minute).zfill(2)+":"+str(dt_object.second).zfill(2)+"."+str(int(dt_object.microsecond/10000)).zfill(2)


    def add_time(self,line,add_time,writePos):

	try:
		
		times= re.findall('[0-9][:][0-6][0-9]:[0-6][0-9][.][0-9][0-9]',line)
		start_time= self.parse_time_from_string(times[0]);
		start_time = start_time + datetime.timedelta(milliseconds= add_time)
		line1= line.replace(times[0],self.format_time(start_time))
		end_time= self.parse_time_from_string(times[1]);
		end_time = end_time + datetime.timedelta(milliseconds= add_time)
		line2= line1.replace(str(times[1]),self.format_time(end_time))

	except:
		
		raise InvalidFormatException("File is not a valid .ssa file")
		return

	
        self.file.seek(writePos,0)
        self.file.write(line2)

    def parse_time_from_string(self,timestring): #format:0:01:31.53

	try:
		array1= timestring.split(":") 
		hours = int(array1[0])
		minutes=int(array1[1])
		array2 = array1[2].split(".")
		seconds = int(array2[0])
		milliseconds= int(array2[1]) * 10 #hey

	except:
		raise InvalidFormatException("File is not a valid .ssa file")
		return

        return datetime.datetime(1,1,1,hours,minutes,seconds, milliseconds * 1000)


class srt_file(subtitle_file):

    separator = "-->"

    def is_time_line(self,line):
        array = line.split()
        if(len(array)==3 and array[1]==self.separator):
            return True
        return False

    

    def add_time(self,line,add_time,writePos):

	try:
		array=line.split()
		start_time= self.parse_time_from_string(array[0]);
		start_time = start_time + datetime.timedelta(milliseconds= add_time)
		end_time= self.parse_time_from_string(array[2]);
		end_time = end_time + datetime.timedelta(milliseconds= add_time)

	except:
		#print "timedelta :("
		raise InvalidFormatException("File is not a valid .srt file")
		return

        self.file.seek(writePos,0)
        self.file.write(self.format_time(start_time)+" "+self.separator+" "+self.format_time(end_time)+"\n")

    def parse_time_from_string(self,timestring): #format: hh:mm:ss,mmm

	try:
		array1= timestring.split(":") #what if wrong format?
		hours = int(array1[0])
		minutes=int(array1[1])
		array2 = array1[2].split(",")
		seconds = int(array2[0])
		milliseconds= int(array2[1])
	except:
		#print "parsing err0r"
		raise InvalidFormatException("File is not a valid .srt file")
		return

        return datetime.datetime(1,1,1,hours,minutes,seconds, milliseconds * 1000)

    def format_time(self,dt_object):
        return str(dt_object.hour).zfill(2) +":"+str(dt_object.minute).zfill(2)+":"+str(dt_object.second).zfill(2)+","+str(int(dt_object.microsecond/1000)).zfill(3)
     

