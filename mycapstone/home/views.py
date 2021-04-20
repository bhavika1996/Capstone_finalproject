from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,HttpResponse
from django.shortcuts import render
import pandas as pd
import csv
import requests

data = pd.read_csv('./home/COVID19.csv')
count = data['Death'].count()
df = pd.DataFrame(data)

totalPositive = len(data)
totalDeath = df[df["Death"] == 1]["Death"].count()
totalMortality = round((totalDeath / totalPositive) * 100, 2)

malePositive = df[df["Gender"] == 1]["Gender"].count()
maleDeath = df[(df["Gender"] == 1) & (df["Death"] == 1)]["Gender"].count()
malemortality = round((maleDeath / malePositive) * 100,2)


femalePositive = df[df["Gender"] == 2]["Gender"].count()
femaleDeath = df[(df["Gender"] == 2) & (df["Death"] == 1)]["Gender"].count()
femalemortality = round((femaleDeath / femalePositive) * 100,2)

gendermortality = 100-(femalemortality+malemortality)

totalDeath = maleDeath + femaleDeath
totalPositive = malePositive + femalePositive

# Create your views here.
def home(request):
    response = requests.get('https://api.covid19tracker.ca/summary')
    coviddata= response.json()
    context = {
        'current_cases':coviddata['data'][0]['total_cases'],
        'fatalities':coviddata['data'][0]['total_fatalities'],
        'hospitalized':coviddata['data'][0]['total_hospitalizations'],
        'critical':coviddata['data'][0]['total_criticals'],
        'recoveries':coviddata['data'][0]['total_recoveries'],
        'vaccinated':coviddata['data'][0]['total_vaccinated'],
    }
    return render(request, 'home.html', context)

def upload(request):
    context = {
        'loaded_data': count,
        'male_death': malemortality,
        'female_death':femalemortality,
        'totalDeath': totalMortality,
        'gender_death':gendermortality,
        'male_positive':malePositive,
        'female_positive':femalePositive,
        'total_positive': totalPositive,
    }

    return render(request, "upload.html", context)

def file(request):
    return render(request, "file.html")