from main_app.models import update_date

def sendUpdateDate(request):
    try :
        list(update_date.objects.all())[-1].date_str
        return {'lastDate' : list(update_date.objects.all())[-1].date_str}
    except :
        return {'lastDate' : '-'}
