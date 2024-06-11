from main_app.models import *
from django.db.models import Q
from itertools import combinations
import csv

term_table_rev = {'ภาคต้น':1,'ภาคปลาย':2,'ภาคฤดูร้อน':3}

def checkSem(term,year):
    if (int(term),int(year)) in semester.objects.values_list('term','year'):
        return semester.objects.filter(term=term,year=year).values_list('id',flat=True)[0]
    else :
        newsem = semester()
        newsem.term = int(term)
        newsem.year = int(year)
        newsem.save()
        return newsem.id

def checkTeacher(teacher_id,teacher_name):
    if (str(teacher_id) in lecturer.objects.values_list('lecturer_id',flat=True)):
        return 
    else :
        newlec = lecturer()
        newlec.lecturer_id = str(teacher_id)
        newlec.lecturer_name = str(teacher_name)
        newlec.save()
        return 

def checkClass_dt(dt_day,dt_time,dt_day2,dt_time2):
    check_dt = (str(dt_day),str(dt_time),str(dt_day2),str(dt_time2)) in class_dt.objects.values_list('dt_day','dt_time','dt_day2','dt_time2')
    if (check_dt):
        return class_dt.objects.filter(dt_day=dt_day,dt_time=dt_time).values_list('id',flat=True)[0]
    else :
        newdt = class_dt()
        newdt.dt_day = str(dt_day)
        newdt.dt_time = str(dt_time)
        newdt.dt_day2 = str(dt_day2)
        newdt.dt_time2 = str(dt_time2)
        newdt.save()
    return newdt.id

def checkSub_list(sub_code,sub_name,sub_cr,sub_year):
    check_sub = (str(sub_code),str(sub_year)) in sub_list.objects.values_list('sub_code','sub_year')
    if (check_sub):
        cur_sub = sub_list.objects.get(sub_code=sub_code,sub_year=sub_year)
        if(cur_sub.sub_name == str(sub_name) and cur_sub.sub_code == str(sub_code) and cur_sub.sub_credit == str(sub_cr) and cur_sub.sub_year == str(sub_year)):
            return cur_sub.sub_id
        else :
            cur_sub.sub_code = str(sub_code)
            cur_sub.sub_name = str(sub_name)
            cur_sub.sub_credit = str(sub_cr)
            cur_sub.sub_year = str(sub_year)
            cur_sub.save()
            return cur_sub.sub_id

    else: 
        newsub_list = sub_list()
        newsub_list.sub_code = str(sub_code)
        newsub_list.sub_name = str(sub_name)
        newsub_list.sub_credit = str(sub_cr)
        newsub_list.sub_year = str(sub_year)
        newsub_list.save()
    return newsub_list.sub_id

def checkSec_room(sec_room):
    if sec_room in room_db.objects.values_list('room_id',flat=True):
        return 
    else :
        newroom = room_db()
        newroom.room_id = sec_room
        newroom.room_amount = 0
        newroom.save()

def checkSub_sec(sub_id,dt_id,lecturer_id,sem_id,sub_section,sec_room,sec_amount,student_type):
    check_subsec = (sub_id,sub_section,sem_id) in sub_sec.objects.values_list('sub_id','section','semester')
    if check_subsec:
        cur_subsec = sub_sec.objects.get(sub_id=sub_id,section=sub_section,semester=sem_id)
        cur_subsec.sec_amount = sec_amount
        cur_subsec.sub_id = sub_list.objects.get(sub_id=sub_id)
        cur_subsec.semester = semester.objects.get(id=sem_id)
        cur_subsec.dt_id = class_dt.objects.get(id=dt_id)
        cur_subsec.lecturer = lecturer.objects.get(lecturer_id = lecturer_id)
        cur_subsec.section = sub_section
        cur_subsec.sec_room = room_db.objects.get(room_id = sec_room)
        cur_subsec.sec_student_type = student_type
        if len(sub_section) < 3:
            secGroup = 'normal'
        elif sub_section[0] =='2':
            secGroup = 'special'
        elif sub_section[0] == '4':
            secGroup = 'iup'
        cur_subsec.sec_group = secGroup
        cur_subsec.save()
        return
    else :
        newsec = sub_sec( sub_id = sub_list.objects.get(sub_id=sub_id) )
        newsec.semester = semester.objects.get(id=sem_id)
        newsec.dt_id = class_dt.objects.get(id=dt_id)
        newsec.lecturer = lecturer.objects.get(lecturer_id = lecturer_id)
        newsec.section = sub_section
        newsec.sec_room = room_db.objects.get(room_id = sec_room)
        newsec.sec_amount = sec_amount
        newsec.sec_student_type = student_type
        if len(sub_section) < 3:
            secGroup = 'normal'
        elif sub_section[0] =='2':
            secGroup = 'special'
        elif sub_section[0] == '4':
            secGroup = 'iup'
        newsec.sec_group = secGroup
        newsec.save()
        
    return

def generateTable_student(in_data):
    sem = in_data['sem']
    term,year = sem.split('/')
    term = term_table_rev[term]
    sem_id = semester.objects.filter(term=term,year=year).values_list('id',flat=True)[0]
    student_dict = {'sy1':['E05-1','E26-1',',1'],'sy2':['E05-2','E26-2',',2'],
                    'sy3':['E05-3','E26-3',',3'],'sy4':['E05-4','E26-4',',4'],'grad':'XE06'}
    student_type = student_dict[in_data['year']]
    qu_id =[]
    if(student_type == 'XE06'):
        for query in sub_sec.objects.values():
            if query['sec_student_type'].find(student_type) != -1:
                qu_id.append(query['id'])
        data = sub_sec.objects.filter(id__in=qu_id,semester=sem_id).values()
    else :
        for query in sub_sec.objects.values():
            if query['sec_student_type'].find(student_type[0]) != -1 or query['sec_student_type'].find(student_type[1]) != -1 or query['sec_student_type'].find(student_type[2]) != -1:
                qu_id.append(query['id'])
        if in_data['group'] == 'all':
            data = sub_sec.objects.filter(id__in=qu_id,semester=sem_id).values()
        else :
            data = sub_sec.objects.filter(id__in=qu_id,sec_group=in_data['group'],semester=sem_id).values()

    return data

def generateTable_teacher(in_data):
    sem = in_data['sem']
    term,year = sem.split('/')
    term = term_table_rev[term]
    sem_id = semester.objects.filter(term=term,year=year).values_list('id',flat=True)[0]
    data = sub_sec.objects.filter(lecturer__lecturer_id__contains=in_data['group'],semester=sem_id).values()
    return data

def generateTable_subject(in_data):
    sem = in_data['sem']
    term,year = sem.split('/')
    term = term_table_rev[term]
    sem_id = semester.objects.filter(term=term,year=year).values_list('id',flat=True)[0]
    data = sub_sec.objects.filter(sub_id=in_data['group'],semester=sem_id).values()
    return data
def generateTable_room(in_data):
    sem = in_data['sem']
    term,year = sem.split('/')
    term = term_table_rev[term]
    sem_id = semester.objects.filter(term=term,year=year).values_list('id',flat=True)[0]
    data = sub_sec.objects.filter(sec_room__room_id__contains=in_data['group'],semester=sem_id).values()
    return data


def gentableData(in_data,data_mode,data_group):
        out_data = []
        for data in in_data:
            data_dt = class_dt.objects.filter(id=data['dt_id_id']).values()[0]
            data_day = data_dt['dt_day']
            data_time = data_dt['dt_time']
            data_day2 = data_dt['dt_day2']
            data_time2 = data_dt['dt_time2']
            data_sec = data['section']
            data_subCode = sub_list.objects.filter(sub_id=data['sub_id_id']).values()[0]['sub_code']
            data_subName = sub_list.objects.filter(sub_id=data['sub_id_id']).values()[0]['sub_name']
            data_credit = sub_list.objects.filter(sub_id=data['sub_id_id']).values()[0]['sub_credit']
            data_sem = semester.objects.get(id=data['semester_id']).term
            data_sem_dict = {1:"ต้น",2:"ปลาย",3:"ฤดูร้อน"}
            data_sem_word = data_sem_dict[data_sem]
            data_lecturer = lecturer.objects.filter(lecturer_id=data['lecturer_id']).values()[0]['lecturer_name']
            if( len(data['sec_room_id'].split(','))>= 2 ):
                #case mutiple room
                data_room = data['sec_room_id'].split(',')[0]
                data_room2 = data['sec_room_id'].split(',')[1]
                if data_room2[0] == " ":
                    data_room2 = data_room2[1:]
            else:
                data_room = data['sec_room_id']
                data_room2 = "-"
            if(data_mode == 'room') :
                if data_room.find(data_group) == -1:
                    data_room = data_room2
                    data_room2 = '-'
                    if len(data_day.split(' '))>1:
                        data_day = data_day.split(' ')[0]
                elif data_room2.find(data_group) == -1 and data_room2 != '-':
                    data_room2 = '-'
                    data_day2 = '-'
                    data_time2 = '-'
                    if len(data_day.split(' '))>1:
                        data_day = data_day.split(' ')[1]
                
            out_data.append({'day':data_day,'time':data_time,'day2':data_day2,'time2':data_time2,'sec':data_sec,
                            'code':data_subCode,'name':data_subName,'lecturer':data_lecturer,'room':data_room,
                            'room2':data_room2,'amount':data['sec_amount'],'student_type':data['sec_student_type'],
                            'credit':data_credit,'term':data_sem_word})
        return out_data

def genDayCount(in_data):
    Mon = []
    Tue = []
    Wed = []
    Thr = []
    Fri = []
    for data in in_data:
        if(data['room2'] != "-" and (data['day2'] != "-" or data['time2'] != "-")):
            #multiple room ,multiple dt
            isFirst = True
            day_data = data['day']
            day_data2 = data['day2']
            if day_data.find('M') != -1 or day_data2.find('M') != -1:
                if(isFirst == False):
                    data['room']=data['room2']
                    data['day']=data['day2']
                    data['time']=data['time2']
                Mon.append(data.copy())
                isFirst=False
            if day_data.find('Tu') != -1 or day_data2.find('Tu') != -1:
                if(isFirst == False):
                    data['room']=data['room2']
                    data['day']=data['day2']
                    data['time']=data['time2']
                Tue.append(data.copy())
                isFirst=False
            if day_data.find('W') != -1 or day_data2.find('W') != -1:
                if(isFirst == False):
                    data['room']=data['room2']
                    data['day']=data['day2']
                    data['time']=data['time2']
                Wed.append(data.copy())
                isFirst=False
            if day_data.find('Th') != -1 or day_data2.find('Th') != -1:
                if(isFirst == False):
                    data['room']=data['room2']
                    data['day']=data['day2']
                    data['time']=data['time2']
                Thr.append(data.copy())
                isFirst=False
            if day_data.find('F') != -1 or day_data2.find('F') != -1:
                if(isFirst == False):
                    data['room']=data['room2']
                    data['day']=data['day2']
                    data['time']=data['time2']
                Fri.append(data.copy())
                isFirst=False

        elif(data['room2'] != "-" and (data['day2'] == "-" or data['time2'] == "-")):
            #multiple room,same dt
            isFirst = True
            day_data = data['day']
            if day_data.find('M') != -1:
                if(isFirst == False):
                    data['room']=data['room2']
                Mon.append(data.copy())
                isFirst=False
            if day_data.find('Tu') != -1:
                if(isFirst == False):
                    data['room']=data['room2']
                Tue.append(data.copy())
                isFirst=False
            if day_data.find('W') != -1:
                if(isFirst == False):
                    data['room']=data['room2']
                Wed.append(data.copy())
                isFirst=False
            if day_data.find('Th') != -1:
                if(isFirst == False):
                    data['room']=data['room2']
                Thr.append(data.copy())
                isFirst=False
            if day_data.find('F') != -1:
                if(isFirst == False):
                    data['room']=data['room2']
                Fri.append(data.copy())
                isFirst=False

        elif(data['room2'] == "-" and (data['day2'] != "-" or data['time2'] != "-")):
            #same room multiple dt
            isFirst = True
            day_data = data['day']
            day_data2 = data['day2']
            if day_data.find('M') != -1 or day_data2.find('M') != -1:
                if(isFirst == False):
                    data['day']=data['day2']
                    data['time']=data['time2']
                Mon.append(data.copy())
                isFirst=False
            if day_data.find('Tu') != -1 or day_data2.find('Tu') != -1:
                if(isFirst == False):
                    data['day']=data['day2']
                    data['time']=data['time2']
                Tue.append(data.copy())
                isFirst=False
            if day_data.find('W') != -1 or day_data2.find('W') != -1:
                if(isFirst == False):
                    data['day']=data['day2']
                    data['time']=data['time2']
                Wed.append(data.copy())
                isFirst=False
            if day_data.find('Th') != -1 or day_data2.find('Th') != -1:
                if(isFirst == False):
                    data['day']=data['day2']
                    data['time']=data['time2']
                Thr.append(data.copy())
                isFirst=False
            if day_data.find('F') != -1 or day_data2.find('F') != -1:
                if(isFirst == False):
                    data['day']=data['day2']
                    data['time']=data['time2']
                Fri.append(data.copy())
                isFirst=False

        else :
            day_data = data['day']
            if day_data.find('M') != -1:
                Mon.append(data)
            if day_data.find('Tu') != -1:
                Tue.append(data)
            if day_data.find('W') != -1:
                Wed.append(data)
            if day_data.find('Th') != -1:
                Thr.append(data)
            if day_data.find('F') != -1:
                Fri.append(data)
    return {'mon':Mon,'tue':Tue,'wed':Wed,'thr':Thr,'fri':Fri},list((Mon,Tue,Wed,Thr,Fri))
        
def timeSplit(sub_dt):
    sub_dt_split = sub_dt.split(' ')
    if len(sub_dt_split) == 1 : #case ติดต่อผู้สอน
        dt_day = sub_dt
        dt_time = sub_dt
    elif len(sub_dt_split) == 2: #1 day
        dt_day = sub_dt_split[0]
        dt_time = sub_dt_split[1]
    else :
        lastCheck = -1
        while( sub_dt_split[lastCheck]== '' ):
            lastCheck -= 1
        dt_day = (' ').join(sub_dt_split[:lastCheck])
        dt_time = sub_dt_split[lastCheck]
    return dt_day,dt_time

def clearDash(in_data):
    for data in in_data:
        if(data['room2'] == '-'):
            data['room2'] = ''
        if(data['day2'] == '-'):
            data['day2'] = ''
        if(data['time2'] == '-'):
            data['time2'] = ''
        if(data['day'] == data['time']):
            data['time'] = " "
            #data['room'] = data['day']
    return in_data

def checkConflict_teacher(lec_qr,data_sem):
    confCase = []
    term,year = data_sem.split('/')
    term = term_table_rev[term]
    sem_id = semester.objects.filter(term=term,year=year).values_list('id',flat=True)[0]
    for sub_lec in lec_qr:
        data_lec = sub_sec.objects.filter(lecturer__lecturer_id__contains=sub_lec.lecturer_id,semester=sem_id).values()
        if (checkConflict(data_lec,sub_lec.lecturer_name,"teacher")) :
            confCase.append(sub_lec.__str__())
    return confCase

def checkConflict_room(room_qr,data_sem):
    confCase = []
    term,year = data_sem.split('/')
    term = term_table_rev[term]
    sem_id = semester.objects.filter(term=term,year=year).values_list('id',flat=True)[0]
    for sub_room in room_qr:
        data_room = sub_sec.objects.filter(sec_room__room_id__contains=sub_room,semester=sem_id).values()
        if (checkConflict(data_room,sub_room,"room")) :
            confCase.append(sub_room)
    return confCase

def checkConflict(in_data,data_name,data_mode):
    _,data_day = genDayCount( gentableData(in_data,data_mode,data_name ))
    for data in data_day:
        times = []
        if(len(data) > 1):
            for sub_data in data:
                try :
                    time_sp = [float(i) for i in sub_data['time'].split('-') ]
                    times.append(time_sp)
                except :
                    continue
        times_comb = list(combinations(times,2))
        for (u0,u1),(l0,l1) in times_comb:
            if((u0==l0 and u1==l1) or (u0>l0 and u0<l1) or (u1>l0 and u1<l1) or (u0==l0 and u0<l1) or (u1>l0 and u1==l1) or (u0<l0 and u1>l1) or (u0>l0 and u1<l1)):
                return True

    return False

def add_room(csvPath):
    with open(csvPath, encoding="utf-8") as csvfile:
        csvreader = csv.reader(csvfile, delimiter=",")
        for i,data in enumerate(csvreader):
            if i==0 :
                continue
            newroom = room_db()
            newroom.room_id = data[0]
            newroom.room_amount = data[1]
            newroom.save()
#add_room('/Users/layyer/Work/Other/room.csv')

def generateSummaryData(in_data,lecs):
    mode = 0
    try:
        out_lec = lecturer.objects.get(lecturer_id = in_data["lecturer"]).lecturer_name
    except:
        out_lec = []
    if(in_data['term']== "all"):
        if(in_data['lecturer']=='all'):
            mode =1 
            out_lec = []
            if(in_data["group"]=='all'):
                #all all
                data_temp = sub_sec.objects.filter(semester__year=in_data["year"])
                data = []
                for lec in lecs:
                    q_data = data_temp.filter(lecturer__lecturer_id__contains = lec.lecturer_id).values()
                    data.append(q_data)
                    if not (list(q_data) == []):
                        out_lec.append(lec.lecturer_name)
            else:
                #term,lec all
                data_temp = sub_sec.objects.filter(semester__year=in_data["year"],sec_group=in_data['group'])
                data = []
                for lec in lecs:
                    q_data = data_temp.filter(lecturer__lecturer_id__contains = lec.lecturer_id).values()
                    data.append(q_data)
                    if not (list(q_data) == []):
                        out_lec.append(lec.lecturer_name)
        else:
            if(in_data["group"]=='all'):
                #term,group all
                data = sub_sec.objects.filter(semester__year=in_data["year"],lecturer__lecturer_id__contains=in_data['lecturer']).values()
            else:
                #term all
                data = sub_sec.objects.filter(semester__year=in_data["year"],lecturer__lecturer_id__contains=in_data['lecturer'],sec_group=in_data['group']).values()

    else :
        if(in_data['lecturer']=='all'):
            mode =1 
            out_lec = []
            if(in_data["group"]=='all'):
                #lec,group all
                data_temp = sub_sec.objects.filter(semester__year=in_data["year"],semester__term=in_data["term"])
                data = []
                for lec in lecs:
                    q_data = data_temp.filter(lecturer__lecturer_id__contains = lec.lecturer_id).values()
                    data.append(q_data)
                    if not (list(q_data) == []):
                        out_lec.append(lec.lecturer_name)
            else:
                #lec all
                data_temp = sub_sec.objects.filter(semester__year=in_data["year"],semester__term=in_data["term"],sec_group=in_data['group'])
                data = []
                for lec in lecs:
                    q_data = data_temp.filter(lecturer__lecturer_id__contains = lec.lecturer_id).values()
                    data.append(q_data)
                    if not (list(q_data) == []):
                        out_lec.append(lec.lecturer_name)
        else:
            if(in_data["group"]=='all'):
                #group all
                data = sub_sec.objects.filter(semester__year=in_data["year"],semester__term=in_data["term"],lecturer__lecturer_id__contains=in_data['lecturer']).values()

            else:
                #no all
                data = sub_sec.objects.filter(semester__year=in_data["year"],semester__term=in_data["term"],lecturer__lecturer_id__contains=in_data['lecturer'],sec_group=in_data['group']).values()
    return data,mode,out_lec


def roomCheck(in_days,in_time,room_amount,sem_str):
    term,year = sem_str.split('/')
    term = term_table_rev[term]
    sem_id = semester.objects.filter(term=term,year=year).values_list('id',flat=True)[0]
    room_query = room_db.objects.filter(room_amount__gte = room_amount)
    days = in_days.split(' ')
    day_con = Q()
    for day in days:
        day_con |= Q(dt_day__contains=day)

    dt_query = class_dt.objects.filter(day_con)
    data = sub_sec.objects.filter(dt_id__in = dt_query, sec_room__in = room_query, semester_id = sem_id)
    (u0,u1) = [float(i) for i in in_time.split('-')]
    room_list = []
    for sub_data in data :
        try:
            (l0,l1) = [float(i) for i in sub_data.dt_id.dt_time.split('-') ]
            print(sub_data.sub_id.sub_name,(l0,l1))
            if((u0==l0 and u1==l1) or (u0>l0 and u0<l1) or (u1>l0 and u1<l1) or (u0==l0 and u0<l1) or (u1>l0 and u1==l1) or (u0<l0 and u1>l1) or (u0>l0 and u1<l1)):
                room_list.append(sub_data.sec_room.room_id)
        except :
            continue
    room_all = set(room_query.values_list('room_id',flat=True))
    room_list = set(room_list)
    return sorted(list(room_all.difference(room_list)))

