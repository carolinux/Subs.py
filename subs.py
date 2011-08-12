import datetime

#i wonder if abstract methods are possibul, im a c++ person!!
# is self.blah really necessary? :S
# null /xception handling...

class SubtitleFile:

    def __init__(self,fileptr):
        self.file=fileptr
    
class SrtFile(SubtitleFile):
    
    separator="-->"
    def isTimeLine(self,line):
        array = line.split()
        if(len(array)==3 and array[1]==self.separator):
           return True
        return False
    
    def addTime(self,line,add_time,writePos):
        array=line.split()
        start_time= self.parseTimeFromString(array[0]);
        start_time = start_time + datetime.timedelta(milliseconds= add_time)
        end_time= self.parseTimeFromString(array[2]);
        end_time = end_time + datetime.timedelta(milliseconds= add_time)
        self.formatTime(end_time)
        self.file.seek(writePos,0)
        self.file.write(self.formatTime(start_time)+" "+self.separator+" "+self.formatTime(end_time)+"\n")
        
    def parseTimeFromString(self,timestring): #format: hh:mm:ss,mmm

        array1= timestring.split(":") #what if wrong format?
        hours = int(array1[0])
        minutes=int(array1[1])
        array2 = array1[2].split(",")
        seconds = int(array2[0])
        milliseconds= int(array2[1])
        return datetime.datetime(1,1,1,hours,minutes,seconds, milliseconds * 1000)

    def formatTime(self,dt_object):
        return str(dt_object.hour).zfill(2) +":"+str(dt_object.minute).zfill(2)+":"+str(dt_object.second).zfill(2)+","+str(int(dt_object.microsecond/1000)).zfill(3)
     
#read user input
filepath = input('Enter the path of the srt file: ')
add_time = input('Enter time to add in milliseconds (negative values for substraction: ')
#catch excepshuns
f = open(filepath, 'r+')
sf = SrtFile(f) #can add support for other subtitle files
add_time = int(add_time) #milliseconds 
#parse the file line by line
start_of_write= f.tell()
line=f.readline()

while  (line!=""):
    if sf.isTimeLine(line):#only parse lines with time values in them
       sf.addTime(line,add_time,start_of_write)
    start_of_write= f.tell()
    line=f.readline()
    
f.close()
print "Finished converting your file"
exit()
