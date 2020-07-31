from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from main_app.models import *
from csv import reader
from io import StringIO
from .utils import *
from datetime import datetime

# Create your views here.
def main(request):

    if(request.method == 'POST'):
        in_data = request.POST.copy()
        data_out = None
        data_group = None
        if(in_data['type']=='student'):
            data_out = generateTable_student(in_data)
            st_gr_dict = {'sy1':'นิสิตปี1','sy2':'นิสิตปี2','sy3':'นิสิตปี3','sy4':'นิสิตปี4','grad':'นิสิตบัณฑิต'}
            st_ty_dict = {'all':'','normal':'ภาคปกติ','special':'ภาคพิเศษ','iup':'IUP'}
            data_group = st_gr_dict[in_data['year']] + ' ' +st_ty_dict[in_data['group']]
        elif(in_data['type']=='teacher'):
            data_out = generateTable_teacher(in_data)
            data_group = 'อาจารย์ '+lecturer.objects.get(lecturer_id = in_data['group']).__str__()
        elif(in_data['type']=='subject'):
            data_out = generateTable_subject(in_data) 
            data_group = 'วิชา '+sub_list.objects.get(sub_id = in_data['group']).__str__()
        elif(in_data['type']=='room'):
            data_out = generateTable_room(in_data)
            data_group =  'ห้อง '+in_data['group']
        table_data = gentableData(data_out,in_data['type'],in_data['group'])
        day_count,day_count_list = genDayCount(table_data)
        table_data_clear = clearDash(table_data)
        time_list = ['','8.00-9.00','9.00-10.00','10.00-11.00','11.00-12.00','12.00-13.00',
                    '13.00-14.00','14.00-15.00','15.00-16.00','16.00-17.00','17.00-18.00'
                    ,'18.00-19.00','19.00-20.00','20.00-21.00']
        return render(request,'table.html',{"data":data_out,"table_data":table_data_clear,"day_data":day_count
                        ,"day_data_list":day_count_list,"mode":in_data['type'],"group":data_group})
    
    
    sem = semester.objects.all()
    sem = sem[::-1]
    lec_qr = lecturer.objects.order_by('lecturer_name')
    lec = []
    for lc in lec_qr:
        if lc.__str__() == "" or lc.__str__() ==' ' or len(lc.__str__().split(',')) > 1:
            continue
        else :
            lec.append(lc)
    subject = {}
    for s in sem:
        sub_temp = list(set(sub_sec.objects.filter(semester=s).values_list('sub_id__sub_code','sub_id__sub_name','sub_id')))
        sub_temp = sorted(sub_temp)
        sub_temp = [list(i) for i in sub_temp]
        subject[s.__str__()] = sub_temp
        #subject = sub_list.objects.all()
    room_qr = sorted(room_db.objects.values_list('room_id',flat=True))
    room = []
    #print(subject)
    for rm in room_qr:
        if rm == "" or rm ==' ' or len(rm.split(',')) > 1:
            continue
        else :
            room.append(rm)
    data = {"semester":sem,"teacher":lec,"subject":subject,"room":room}
    return render(request,'main.html',data)



def add_file(request):

    if request.method == 'POST' and request.FILES['file']:
        in_data = request.POST.copy()
        year = in_data.get('year')
        term = in_data.get('term')
        sub_sec.objects.filter(semester__year=year,semester__term=term).delete()
        sem_id = checkSem(term,year)
        csv_file = request.FILES['file']
        file_data = csv_file.read().decode("utf-8")	
        file_data = StringIO(file_data)
        file_data = reader(file_data)
        file_data = list(file_data)
        file_data = file_data[1:]
        #Check Empty in col 1-4 every row
        for i,data in enumerate(file_data):
            if(data[0]==''):
                for j in range(4):
                    file_data[i][j] = file_data[i-1][j]
            sub_code = data[0]
            sub_year = data[1]
            sub_name = data[2]
            sub_cr = data[3]
            section = data[4]
            sub_dt = data[5]
            if len(sub_dt.split(',')) >= 2:
                #Case multiple day/time
                multi_dt = sub_dt.split(',')
                dt_day,dt_time = timeSplit(multi_dt[0])
                if multi_dt[1][0] == " ":
                    multi_dt[1] = multi_dt[1][1:]
                dt_day2,dt_time2 = timeSplit(multi_dt[1])
            else :
                dt_day,dt_time = timeSplit(sub_dt)
                dt_day2,dt_time2 = "-","-"

            sec_room = data[6]
            student_type = data[7].split('(')[0]
            try:
                sec_amount = data[7].split('(')[1].split(')')[0]
            except :
                sec_amount = '999'
            teacher_name = data[8]
            teacher_id = data[9]
            sub_id = checkSub_list(sub_code = sub_code,sub_name=sub_name,sub_cr=sub_cr,sub_year=sub_year)
            checkTeacher(teacher_id=teacher_id,teacher_name=teacher_name)
            dt_id = checkClass_dt(dt_day=dt_day,dt_time=dt_time,dt_day2=dt_day2,dt_time2=dt_time2)
            checkSec_room(sec_room)
            checkSub_sec(sub_id,dt_id,teacher_id,sem_id,str(section),sec_room,sec_amount,student_type)
        newdate = update_date()
        newdate.date_str = datetime.now().strftime("%B %d %Y")
        newdate.save()

        return render(request,'addfile.html',{"success":"yes"})

                

    
    return render(request,'addfile.html')

def conflict(request):
    if(request.method == 'POST'):
        data_sem = request.POST.copy()['sem']
        lec_qr = lecturer.objects.order_by('lecturer_name')
        lec = []
        for lc in lec_qr:
            if lc.__str__() == "" or lc.__str__() ==' ' or len(lc.__str__().split(',')) > 1:
                continue
            else :
                lec.append(lc)
            room_qr = sorted(set(sub_sec.objects.values_list('sec_room',flat=True)))
        room = []
        for rm in room_qr:
            if rm.__str__() == "" or rm.__str__() ==' ' or len(rm.__str__().split(',')) > 1:
                continue
            else :
                room.append(rm)
        con_lec = checkConflict_teacher(lec,data_sem)
        con_room = checkConflict_room(room,data_sem)
        sem = semester.objects.all()
        return render(request,'conflict.html',{"semester":sem,"con_lec":con_lec,"con_room":con_room})
    
    sem = semester.objects.all()
    return render(request,'conflict.html',{"semester":sem})

def summary(request):
    lec_qr = lecturer.objects.order_by('lecturer_name')
    lec = []
    for lc in lec_qr:
        if lc.__str__() == "" or lc.__str__() ==' ' or len(lc.__str__().split(',')) > 1:
            continue
        else :
            lec.append(lc)
    
    if(request.method == 'POST'):
        in_data = request.POST.copy()
        out_data,mode,out_lec = generateSummaryData(in_data,lec)
        if mode == 0:
            table_data = clearDash(gentableData(out_data,"teacher",in_data['group']))
            table_data = sorted(table_data, key = lambda i:(i['code'],i['sec']))
            length_data = len(table_data)
        elif mode == 1:
            table_data = []
            length_data = []
            lec_sort = []
            for sub_data in out_data:
                temp_data = clearDash(gentableData(sub_data,"teacher",in_data['group']))
                #print(temp_data)
                temp_data = sorted(temp_data, key = lambda i:(i['code'],i['sec']))
                if(len(temp_data) != 0):
                    table_data.append(temp_data)
                    length_data.append(len(temp_data))
        return render(request,'summary.html',{"teacher" : lec,"data":table_data,"mode":mode,"length_data":length_data,"table_lec":out_lec,"prev_data":dict(in_data)})
    
    
    return render(request,'summary.html',{"teacher" : lec})

def advance(request):
    sem = semester.objects.all()
    if(request.method == 'POST'):
        in_data = request.POST.copy()
        out_data = roomCheck(in_days=in_data['day'],in_time=in_data['time'],room_amount=in_data['st_amount'],sem_str=in_data['sem'])
        return render(request,'advance.html',{"semester":sem,"info_data":in_data,"data":out_data,"prev_data":dict(in_data)})
        

    
    return render(request,'advance.html',{"semester":sem})