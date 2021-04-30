from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage

# Create your views here.
from django.shortcuts import render,HttpResponse
from django.shortcuts import render
import pandas as pd
import csv
import requests
import json

import io
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

data = pd.read_csv('./home/COVID19.csv')
count = data['Death'].count()
df = pd.DataFrame(data)

################# Regression ##########################################
df_x = df[["Region", 'Gender', 'Age group', "Occupation"]]
df_y = df['Death']

train_x, unseen_test_x, train_y, unseen_test_y = train_test_split(df_x, df_y, test_size=0.05, random_state=42)
train_x, test_x, train_y, test_y = train_test_split(train_x, train_y, test_size=0.25, random_state=42)

reg = LinearRegression().fit(train_x, train_y)
reg.score(train_x, train_y)
reg.score(test_x, test_y)
reg.score(unseen_test_x, unseen_test_y)

#######################################################################

totalPositive = len(data)
totalDeath = df[df["Death"] == 1]["Death"].count()
totalMortality = round((totalDeath / totalPositive) * 100, 2)

#Male Mortality
def maleData(data = pd.read_csv('./home/COVID19.csv')):
    df = pd.DataFrame(data)
    malePositive = df[df["Gender"] == 1]["Gender"].count()
    maleDeath = df[(df["Gender"] == 1) & (df["Death"] == 1)]["Gender"].count()
    malemortality = round((maleDeath / malePositive) * 100,2)

    return malemortality

#Female Mortality
def femaleData(data = pd.read_csv('./home/COVID19.csv')):
    df = pd.DataFrame(data)
    femalePositive = df[df["Gender"] == 2]["Gender"].count()
    femaleDeath = df[(df["Gender"] == 2) & (df["Death"] == 1)]["Gender"].count()
    femalemortality = round((femaleDeath / femalePositive) * 100,2)

    return femalemortality
    

#Age Group Mortality
def ageGroupData(data = pd.read_csv('./home/COVID19.csv')):
    df = pd.DataFrame(data)
    ageGroups = {}
    ageGroups[1] = "0 to 19 Years"
    ageGroups[2] = "20 to 29 Years"
    ageGroups[3] = "30 to 39 Years"
    ageGroups[4] = "40 to 49 Years"
    ageGroups[5] = "50 to 59 Years"
    ageGroups[6] = "60 to 69 Years"
    ageGroups[7] = "70 to 79 Years"
    ageGroups[8] = "80 to 89 Years"

    ageMortality = []

    for ageGroup in ageGroups:
        positiveCount = df[(df["Age group"] == ageGroup)]["Age group"].count()
        deathCount = df[(df["Age group"] == ageGroup) & (df["Death"] == 1)]["Age group"].count()
        ageMortality.append(round((deathCount / positiveCount) * 100, 2))    

    json_ageMortality = json.dumps(ageMortality)
    return json_ageMortality


#Region Mortality
def regionData(data = pd.read_csv('./home/COVID19.csv')):
    df = pd.DataFrame(data)
    regions = {}
    regions[1] = "Alantic"
    regions[2] = "Quebec"
    regions[3] = "Ontario & Nunavat"
    regions[4] = "Prairies"
    regions[5] = "British Columbia"

    regionMortality = []

    for region in regions:
        positiveCount = df[(df["Region"] == region)]["Region"].count()    
        deathCount = df[(df["Region"] == region) & (df["Death"] == 1)]["Region"].count()
        regionMortality.append(round((deathCount / positiveCount) * 100, 2))    

    json_regionMortality = json.dumps(regionMortality)

    return json_regionMortality


#Occupation Mortality
def occupationData(data = pd.read_csv('./home/COVID19.csv')):
    df = pd.DataFrame(data)
    occupations = {}
    occupations[1] = "Health care worker"
    occupations[2] = "School or daycare worker/attendee"
    occupations[3] = "Long term care resident"
    occupations[4] = "Other"
    occupationMortality = []

    for occupation in occupations:
        positiveCount = df[(df["Occupation"] == occupation)]["Occupation"].count()
        deathCount = df[(df["Occupation"] == occupation) & (df["Death"] == 1)]["Occupation"].count()
        occupationMortality.append(round((deathCount / positiveCount) * 100, 2))

    json_occupationMortality = json.dumps(occupationMortality)
    return json_occupationMortality


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
    malemortality = maleData()
    femalemortality = femaleData()
    json_regionMortality = regionData()
    json_ageMortality = ageGroupData()
    json_occupationMortality = occupationData()
    
    context = {
        'male_mortality': malemortality,
        'female_mortality': femalemortality,
        'region_mortality': json_regionMortality,
        'age_mortality': json_ageMortality,
        'occupation_mortality': json_occupationMortality        
    }

    return render(request, "upload.html", context)

def download_csv_template(request):

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="covid-template.csv"'

    writer = csv.writer(response)
    writer.writerow(["Case identifier number", "Region", "Episode week", "Episode week group", "Episode year", 'Gender', 'Age group', "Occupation",
                    "Asymptomatic",	'Onset week of symptoms', "Onset year of symptoms",	"Hospital status", "Recovered",	"Recovery week", "Recovery year", "Death", "Transmission"])
    return response

def file(request):

    download_url = "http://" + request.get_host() + "/download_csv_template"
    context = {

        "url": download_url
    }

    return render(request, "file.html", context)

def predict(request):

    return render(request, "predict.html")

def predict_post(request):
    
    age = float(request.GET.get("age", 0))
    region = float(request.GET.get("region", 0))
    occupation = float(request.GET.get("occupation", 0))
    gender = float(request.GET    .get("gender", 0))

    # age = float(request.POST.get("age_group", 0))
    # region = float(request.POST.get("region", 0))
    # occupation = float(request.POST.get("occupation", 0))
    # gender = float(request.POST.get("gender", 0))

    prediction = (reg.coef_[0] * region) + (reg.coef_[1] * gender) + (reg.coef_[2] * age) + (reg.coef_[3] * occupation) + reg.intercept_

    msg = ''
    if(abs(int(prediction)) == 2):
        msg = 'Risk factor for given demographics is less.'
    elif(abs(int(prediction)) == 1):
        msg = "Risk factor for given demographics is high."
    else:
        msg = "No Pridictable data is available for given demographic."

    pred = abs(int(prediction))
    
    context = {
        "prediction": pred,
        "msg": msg
    }

    return HttpResponse(json.dumps(context), content_type="application/json")

def uplaod_csv(request):

    msg = ""
    try:
        csv_file = request.FILES["csv_file"]

        if not csv_file.name.endswith('.csv'):
            context ={
                msg: "Upload a valid file"
            }
            return render(request, "csv_upload_review.html", context)
        
        #data_set = io.StringIO(csv_file.read().decode('UTF-8'))

        #data = pd.read_csv(data_set,  delimiter=',', low_memory=False)

        df = pd.concat((chunk for chunk in pd.read_csv(csv_file,  delimiter=',', chunksize=10**4)), ignore_index=True)

        #data = pd.DataFrame(data).dropna()

        # msg = data["Death"].count()
        # df = pd.DataFrame(data)

        malemortality = maleData(data)
        femalemortality = femaleData(data)
        json_regionMortality = regionData(data)
        json_ageMortality = ageGroupData(data)
        json_occupationMortality = occupationData(data)

        context = {            
            'male_mortality': malemortality,
            'female_mortality': femalemortality,
            'region_mortality': json_regionMortality,
            'age_mortality': json_ageMortality,
            'occupation_mortality': json_occupationMortality                        
        }
        return render(request, "csv_upload_review.html", context) 

    except Exception as e:
        context = {
            msg: "Error"
        }
        print(e)
        return render(request, "csv_upload_review.html", context)
