from django.shortcuts import render
from patch.forms import ConForm
from hindi_summarizer import views as hs
from english_summarizer import views as es

def Organiser(request):
    dict={}
    if request.method == 'POST':
        form = ConForm(request.POST)
        if form.is_valid():
            lin=form.cleaned_data['link']
            l=hs.main(lin)
            dict["form"]=form
            dict["inp"]=l[1]
            if l[0]!=0:
                dict["sum"]=l[0]
            else:
                #just an error message for safety if there was some problem like wrong link given etc.
                dict["sum"]="Sorry for the inconvenience check you link our backend does not support articles with bad encoding patterns please try with articles from other websites or try copy pasting text instead of giving the link"
            print(l)
        return render(request,'page.html',{"dict":dict})
    else:
        form=ConForm()
        dict["form"]=form
        return render(request,'page.html',{'dict':dict})

def TempView(request):
    return render(request,'index.html')

def EngOrganiser(request):
    dict={}
    if request.method == 'POST':
        form = ConForm(request.POST)
        if form.is_valid():
            lin=form.cleaned_data['link']
            l=es.main(lin)
            dict["sum"]=l[0]
            dict["form"]=form
            dict["inp"]=l[1]
            print(l)
        return render(request,'page.html',{"dict":dict})
    else:
        form=ConForm()
        dict["form"]=form
        return render(request,'page.html',{'dict':dict})
