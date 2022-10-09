import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import datetime

def cal_age(date):
    today = date.today()
    work_exp = today.year - date.year - ((today.month, today.day) < (date.month, date.day))
    return work_exp

df = pd.read_csv('data-devclub.csv')
figure, axis = plt.subplots(2, 2)
data = [len(df[df['GENDER']==0]), len(df[df['GENDER']==1])]
axis[0, 0].pie(data, labels = ["Male", "Female"])
axis[0, 0].set_title("Gender")

region = df['REGION'].value_counts().rename_axis('region').reset_index(name='counts')
axis[0, 1].pie(region['counts'], labels=region['region'])
axis[0, 1].set_title("Region")

df['WORK_EXP'] = df.apply(lambda x: cal_age(datetime.strptime(x['HIRED'], '%d-%m-%Y').date()), axis=1)
axis[1, 0].barh(df['FIRSTNAME'], df['WORK_EXP'], color ='maroon')
axis[1, 0].invert_yaxis()
axis[1, 0].set_xlabel('Years')
axis[1, 0].set_title('Work Experience')

df_gender_count = df.groupby(["GENDER", "POSITION"]).size().reset_index()
df_male = df_gender_count[df_gender_count['GENDER'] == 0]
df_female = df_gender_count[df_gender_count['GENDER'] == 1]
ind = np.arange(3)
width = 0.35
p1 = axis[1, 1].bar(ind, tuple(df_male[0].values), width)
p2 = axis[1, 1].bar(ind, tuple(df_female[0].values), width, bottom = tuple(df_male[0].values))
axis[1, 1].set_ylabel('Contribution')
axis[1, 1].set_title('Contribution by the teams')
axis[1, 1].set_xticks(ind)
axis[1, 1].set_xticklabels(['Airhostess', 'Pilot', 'Steward'])
axis[1, 1].legend((p1[0], p2[0]), ('Male', 'Female'))
plt.show()
