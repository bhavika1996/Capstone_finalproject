from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,HttpResponse
from django.shortcuts import render
import pandas as pd
import csv
import requests
import json

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


# ageGroups = {}
#
# ageGroups[1] = "0 to 19 Years"
# ageGroups[2] = "20 to 29 Years"
# ageGroups[3] = "30 to 39 Years"
# ageGroups[4] = "40 to 49 Years"
#
# ageGroups[5] = "50 to 59 Years"
# ageGroups[6] = "60 to 69 Years"
# ageGroups[7] = "70 to 79 Years"
# ageGroups[8] = "80 to 89 Years"
#
# ageMortality = []
#
# for ageGroup in ageGroups:
#     positiveCount = df[(df["Age group"] == ageGroup)]["Age group"].count()
#     deathCount = df[(df["Age group"] == ageGroup) & (df["Death"] == 1)]["Age group"].count()
#     ageMortality.append(round((deathCount / positiveCount) * 100, 2))
#     print(ageGroups[ageGroup], "Mortality", round((deathCount / positiveCount) * 100, 2), "%")

regions = {}

regions[1] = "Alantic"
regions[2] = "Quebec"
regions[3] = "Ontario & Nunavat"
regions[4] = "Prairies"
regions[5] = "British Columbia"

regionMortality = []

for region in regions:
    print()
    positiveCount = df[(df["Region"] == region)]["Region"].count()
    print(regions[region], "Total Cases :", positiveCount)
    deathCount = df[(df["Region"] == region) & (df["Death"] == 1)]["Region"].count()
    regionMortality.append(round((deathCount / positiveCount) * 100, 2))
    print("Mortality", round((deathCount / positiveCount) * 100, 2), "%")

json_regionMortality = json.dumps(regionMortality)

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
        'region_mortality': json_regionMortality,

    }

    return render(request, "upload.html", context)

def file(request):
    return render(request, "file.html")