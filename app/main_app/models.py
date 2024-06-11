from django.db import models

# Create your models here.

class update_date(models.Model):
    date_id = models.AutoField(auto_created=True, primary_key=True, name='ID')
    date_str = models.CharField(max_length=255)
    
    def __str__(self):
        return self.date_str
class room_db(models.Model):
    room_id = models.CharField(max_length=255,primary_key=True)
    room_amount = models.IntegerField()
    
    def __str__(self):
        return self.room_id+'('+str(self.room_amount)+')'

class sub_list(models.Model):
    #ids = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    sub_id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    sub_code = models.CharField(max_length=255)
    sub_name = models.CharField(max_length=255)
    sub_credit = models.CharField(max_length=10)
    sub_year = models.CharField(max_length=255)
    
    def __str__(self):
        return self.sub_code+'('+str(self.sub_credit)+') ' +self.sub_name+' -'+self.sub_year

class class_dt(models.Model):
    #dt_id = models.IntegerField()
    dt_day = models.CharField(max_length=255)
    dt_time = models.CharField(max_length=255)
    dt_day2 = models.CharField(max_length=255)
    dt_time2 = models.CharField(max_length=255)

    def __str__(self):
        if self.dt_day2 != '-' and self.dt_time2 != '-':
            return str(self.dt_day)+'  '+str(self.dt_time) +","+str(self.dt_day2)+'  '+str(self.dt_time2)
        else:
            return  str(self.dt_day)+'  '+str(self.dt_time)

class lecturer(models.Model):
    lecturer_id = models.CharField(max_length=255, primary_key=True)
    lecturer_name = models.CharField(max_length=255)

    def __str__(self):
        return self.lecturer_name+' '+self.lecturer_id

class semester(models.Model):
    first = 1
    second = 2
    summer = 3
    term_choice = [(1,'First'),(2,'Second'),(3,'Summer')]
    year = models.IntegerField()
    term = models.IntegerField(choices=term_choice)
    def __str__(self):
        ret_str = "ภาค"
        term_map = {1:'ต้น',2:'ปลาย',3:'ฤดูร้อน'}
        ret_str = ret_str + term_map[self.term] + '/' + str(self.year)
        return ret_str
        #return str(self.term)+'/'+str(self.year)

class sub_sec(models.Model):
    sub_id = models.ForeignKey(sub_list,on_delete=models.CASCADE)
    semester = models.ForeignKey(semester,on_delete=models.CASCADE)
    section = models.CharField(max_length=255)
    sec_group = models.CharField(choices=[('normal','ปก'),('special','เป'),('iup','IUP')],max_length=10)
    dt_id = models.ForeignKey(class_dt,on_delete=models.CASCADE)
    sec_room = models.ForeignKey(room_db,on_delete=models.CASCADE)
    sec_amount = models.IntegerField()
    sec_student_type = models.CharField(max_length=255)
    lecturer = models.ForeignKey(lecturer,on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.sub_id) + ' sec' + self.section +'   :'+str(self.semester)

    