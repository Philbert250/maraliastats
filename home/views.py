from io import BytesIO

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.template.loader import get_template
from django.db.models import Sum

from .models import*
import pandas as pd
from xhtml2pdf import pisa

from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from datetime import datetime

# Create your views here.

# Create your views here.
def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Invalid Username or Password')
            return redirect('signing')
    else:
        return render(request, 'signin.html')

def logout_user(request):
    auth.logout(request)
    return redirect('signing')

def welcome(request):
    selectcase = CaseData.objects.all()
    casesum = CaseData.objects.aggregate(Sum('value'))
    seversum = SevereData.objects.aggregate(Sum('value'))
    deathsum = DeathData.objects.aggregate(Sum('value'))
    contextdata = {
        'cases': selectcase,
        'sumcase': casesum,
        'sumsever': seversum,
        'sumdeath': deathsum
    }
    return render(request,'index.html', context=contextdata)

def generaldata(request):
    qs = GeneralData.objects.all().values()
    generaldata = qs.to_timeseries(index='year',
                          pivot_columns='casename',
                          values='value',
                          storage='long')
    contextdata = {
        'general' : generaldata.to_html(classes='table table-bordered', table_id="dataTable")
    }
    return render(request,'general.html', context=contextdata)

def allcase(request):
    selectcase = CaseData.objects.all()
    contextdata = {
        'cases': selectcase
    }
    return render(request,'allcase.html', context=contextdata)

def delcase(request,id):
    select =CaseData.objects.all().order_by('id')
    deletedata =CaseData.objects.get(id=id)
    try:
        updatenew = GeneralData.objects.get(year=deletedata.year, casename='cases', value=deletedata.value).delete()
        deleteinfos = CaseData.objects.get(id=id).delete()
        return render(request, 'allcase.html', {'delmsg': 'data has been deleted', 'cases': select})
    except:
        return render(request,'allcase.html',{'delmsg':'Failed has been deleted','cases':select})

    return render(request,'allcase.html',{'delmsg':'data has been deleted','cases':select})

def updatecase(request,id):
    select = CaseData.objects.all().order_by('id')
    update = CaseData.objects.get(id=id)
    updatenew = GeneralData.objects.get(year=update.year, casename='cases', value=update.value)
    if request.method=='POST':
        update.year =request.POST['year']
        update.value =request.POST['value']
        updatenew.year = request.POST['year']
        updatenew.value =request.POST['value']
        try:
            update.save()
            updatenew.save()
            return render(request,'allcase.html',{'messag':'Update successefull','cases':select,'update':update})
        except:
            return render(request,'updatecase.html',{'messag':'fail do update','data':select,'update':update})

    return render(request,'updatecase.html',{'messag':'data has been deleted','data':select,'update':update})

def severecase(request):
    selectcase = SevereData.objects.all()
    contextdata = {
        'cases': selectcase
    }
    return render(request,'allsevere.html', context=contextdata)

def delsevere(request,id):
    select =SevereData.objects.all().order_by('id')
    deletedata =SevereData.objects.get(id=id)
    try:
        updatenew = GeneralData.objects.get(year=deletedata.year, casename='severe', value=deletedata.value).delete()
        deleteinfos =SevereData.objects.get(id=id).delete()
        return render(request, 'allsevere.html', {'delmsg': 'data has been deleted', 'cases': select})
    except:
        return render(request,'allsevere.html',{'delmsg':'Failed has been deleted','cases':select})
    return render(request,'allsevere.html',{'delmsg':'data has been deleted','cases':select})

def updatesevere(request,id):
    select = SevereData.objects.all().order_by('id')
    update = SevereData.objects.get(id=id)
    updatenew = GeneralData.objects.get(year=update.year, casename='severe', value=update.value)
    if request.method=='POST':
        update.year =request.POST['year']
        update.value =request.POST['value']
        updatenew.year = request.POST['year']
        updatenew.value =request.POST['value']
        try:
            update.save()
            updatenew.save()
            return render(request,'allsevere.html',{'messag':'Update successefull','cases':select,'update':update})
        except:
            return render(request,'updatesevere.html',{'messag':'fail do update','data':select,'update':update})

    return render(request,'updatesevere.html',{'messag':'data has been deleted','data':select,'update':update})

def deathcase(request):
    selectcase = DeathData.objects.all()
    contextdata = {
        'cases': selectcase
    }
    return render(request,'alldeath.html', context=contextdata)

def deldeath(request,id):
    select =DeathData.objects.all().order_by('id')
    deletedata =DeathData.objects.get(id=id)
    try:
        updatenew = GeneralData.objects.get(year=deletedata.year, casename='death', value=deletedata.value).delete()
        deleteinfos =DeathData.objects.get(id=id).delete()
        return render(request, 'alldeath.html', {'delmsg': 'data has been deleted', 'cases': select})
    except:
        return render(request,'alldeath.html',{'delmsg':'Failed has been deleted','cases':select})
    return render(request,'alldeath.html',{'delmsg':'data has been deleted','cases':select})

def updatedeath(request,id):
    select = DeathData.objects.all().order_by('id')
    update = DeathData.objects.get(id=id)
    updatenew = GeneralData.objects.get(year=update.year, casename='death', value=update.value)
    if request.method=='POST':
        update.year =request.POST['year']
        update.value =request.POST['value']
        updatenew.year = request.POST['year']
        updatenew.value =request.POST['value']
        try:
            update.save()
            updatenew.save()
            return render(request,'alldeath.html',{'messag':'Update successefull','cases':select,'update':update})
        except:
            return render(request,'updatedeath.html',{'messag':'fail do update','data':select,'update':update})

    return render(request,'updatedeath.html',{'messag':'data has been deleted','data':select,'update':update})

def upgradecase(request):
    if request.method =='POST':
        casename = request.POST['casename']
        year = request.POST['year']
        value = request.POST['value']
        insert = CaseData(year=year, value=value)
        inserttwo = GeneralData(year=year, casename=casename, value=value)
        try:
            insert.save()
            inserttwo.save()
            return render(request,'upgradecase.html',{'message':'Data has been inserted successful'})
        except:
            return render(request,'upgradecase.html',{'messagefailed':'fail to insert'})
    return render(request,'upgradecase.html')

def upgradesevere(request):
    if request.method =='POST':
        casename = request.POST['casename']
        year = request.POST['year']
        value = request.POST['value']
        insert = SevereData(year=year, value=value)
        inserttwo = GeneralData(year=year, casename=casename, value=value)
        try:
            insert.save()
            inserttwo.save()
            return render(request,'upgradesevere.html',{'message':'Severe Data has been inserted successful'})
        except:
            return render(request,'upgradesevere.html',{'messagefailed':'fail to insert'})
    return render(request,'upgradesevere.html')

def upgradedeath(request):
    if request.method =='POST':
        casename = request.POST['casename']
        year = request.POST['year']
        value = request.POST['value']
        insert = DeathData(year=year, value=value)
        inserttwo = GeneralData(year=year, casename=casename, value=value)
        try:
            insert.save()
            inserttwo.save()
            return render(request,'upgradedeath.html',{'message':'Death Data has been inserted successful'})
        except:
            return render(request,'upgradedeath.html',{'messagefailed':'fail to insert'})
    return render(request,'upgradedeath.html')

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("utf-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

def reportpdf(request):
    template = get_template('reportpdf.html')
    selectcase = CaseData.objects.all()
    selectdeathcase = DeathData.objects.all()
    selectseverecase = SevereData.objects.all()
    qs = GeneralData.objects.all().values()
    ts = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    generaldata = qs.to_timeseries(index='year',
                                   pivot_columns='casename',
                                   values='value',
                                   storage='long')
    contextdata = {
        'cases': selectcase,
        'severecase': selectseverecase,
        'deathcase': selectdeathcase,
        'timesp': ts,
        'general': generaldata.to_html(classes='table table-bordered', )
    }
    html = template.render(contextdata)
    pdf = render_to_pdf('reportpdf.html',contextdata)
    return HttpResponse(pdf, content_type='application/pdf')