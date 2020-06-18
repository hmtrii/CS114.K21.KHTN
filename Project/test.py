import pandas as pd

file = pd.read_json("crawler/player20.json")
# a = file['info']
# print(a[0:3])
team = []
ovr = []
for info in file['info']:
    team.append(info['raw team'])
    ovr.append(info['rating'])




# print(file['info'][0]['raw team'])
data = {'name': file['name'], 'team': team, 'ovr': ovr}
df = pd.DataFrame(data = data)
print(df.head())