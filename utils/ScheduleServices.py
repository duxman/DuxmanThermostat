import uuid
import datetime


class Task(object):
    Id = "{12345678-1234-5678-1234-567812345678}"
    Day = 0
    HourFrom = "0000" # Hour Minute withoutseparator
    HourTo =    "2359"# Hour Minute withoutseparator
    Objetive = 21 # Objetive value
    Manual = False

    def __init__(self, day,hourfrom,hourto,obj,manual=False,id=None):

        if(id == None ):
            Id = str( uuid.uuid1() )

        self.Day =day
        self.HourFrom = hourfrom
        self.HourTo = hourto
        self.Objetive = obj
        self.Manual = manual

class WeekSchedule(object):

    WeekDays = [[] for x in range(7) ]
    Tasks = dict()
    ManualTask = None

    def RegenerateTask(self):
        for t in self.Task:
            self.WeekDays[t.Day].append(t)

    def AddTask(self,task):
        if( task.Manual == True ):
            self.ManualTask = task
        else:
            self.Tasks.update({task.Id,task})
            self.RegenerateTask()

    def DeleteTask(self, id):
        if( ( self.ManualTask != None ) & (self.ManualTask.Id == id) ):
            self.ManualTask = None
        else:
            self.Tasks.pop(id)
            self.RegenerateTask()

    def CheckTime(self, hfrom, hto):
        # Comprobamos la hora
        now = datetime.strftime("%H%M")
        # representacion de fecha y hora
        return_value = False
        if ((now >= hfrom) & (now < hto)):
            return True
        return False

    def ClockTask(self):
        today = datetime.datetime.today().weekday()
        daytask = self.WeekDays[today]
        for t in daytask:
            value =self.CheckTime(t.HourFrom, t.HourTo)
            if( value == True ):
                return True, t.Objetive
        return False

    def CheckManualTask(self,actual):
        if(self.ManualTask != None):
            if( self.CheckTime( self.ManualTask.HourFrom, self.ManualTask.HourTo) ):
                if ( actual < self.ManualTask.Objetive ) :
                    return True
                else:
                    return False
            else:
                self.ManualTask = None
        return False


    def ClockTaskTemp(self,actual):
        if( self.CheckManualTask( actual ) == True ):
            return "ON"
        start,objetive = self.ClockTask()
        if( ( start == True ) & (actual < objetive) ):
            return "ON"
        return "OFF"

