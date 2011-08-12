import datetime

class subtitle_file:

    def __init__(self,fileptr):
        self.file=fileptr

class srt_file(subtitle_file):

    separator = "-->"

    def is_time_line(self,line):
        array = line.split()
        if(len(array)==3 and array[1]==self.separator):
            return True
        return False

    def add_time(self,line,add_time,writePos):
        array=line.split()
        start_time= self.parse_time_from_string(array[0]);
        start_time = start_time + datetime.timedelta(milliseconds= add_time)
        end_time= self.parse_time_from_string(array[2]);
        end_time = end_time + datetime.timedelta(milliseconds= add_time)
        self.format_time(end_time)
        self.file.seek(writePos,0)
        self.file.write(self.format_time(start_time)+" "+self.separator+" "+self.format_time(end_time)+"\n")

    def parse_time_from_string(self,timestring): #format: hh:mm:ss,mmm

        array1= timestring.split(":") #what if wrong format?
        hours = int(array1[0])
        minutes=int(array1[1])
        array2 = array1[2].split(",")
        seconds = int(array2[0])
        milliseconds= int(array2[1])
        return datetime.datetime(1,1,1,hours,minutes,seconds, milliseconds * 1000)

    def format_time(self,dt_object):
        return str(dt_object.hour).zfill(2) +":"+str(dt_object.minute).zfill(2)+":"+str(dt_object.second).zfill(2)+","+str(int(dt_object.microsecond/1000)).zfill(3)
     

