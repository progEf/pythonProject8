import pandas as pd
import os
import glob
  
  
path = './files/'
csv_files = glob.glob(os.path.join(path, "*.xlsx"))
  

for f in csv_files:

    df = pd.read_excel(f)

    df = df.drop_duplicates(subset=['Ссылка на профиль продавца'])

    # print('File Name:', f.split("/")[2])

    # print(df.to_string())

    # print(f'./corrected_files/{f.split("/")[2]}')

    df.to_excel('./corrected_files/{}'.format(f.split("\\")[1]), index=False)


path = './corrected_files/'
data = []
csv_files = glob.glob(os.path.join(path, "*.xlsx"))

df = pd.DataFrame()

for f in csv_files:

    data = pd.read_excel(f)

    df = df.append(data)

    print(df.to_string())

df.to_excel(f'./total.xlsx', index=False)