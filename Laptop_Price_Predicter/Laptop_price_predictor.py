import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LinearRegression
from sklearn import linear_model

df = pd.read_csv("laptops.csv", encoding="ISO-8859-1") # Utf -8

listColumns = df.columns.to_list()
listColumns = listColumns[1:]
df = df[listColumns]
price = df["Price_euros"]*1.07

# dropping useless data

df.drop(['Price_euros'],axis = 'columns', inplace=True)
df.drop(['Product'],axis = 'columns', inplace=True)
df.drop(['TypeName'],axis = 'columns', inplace=True)
df.drop(['Inches'],axis = 'columns', inplace=True)
df.drop(['Weight'],axis = 'columns', inplace=True)
df.drop(['Gpu'],axis = 'columns', inplace=True)

# simplification of long data

cpu = df.Cpu
for x in range(0,len(cpu)):

    if 'Celeron' in cpu.iloc[x]:
         cpu.iloc[x] = 'Celeron';
    elif 'Core M' in cpu.iloc[x]:
         cpu.iloc[x] = 'Core M';
    elif 'Pentium' in cpu.iloc[x]:
         cpu.iloc[x] = 'Pentium';
    elif 'i3' in cpu.iloc[x]:
         cpu.iloc[x] = 'i3';
    elif 'i5' in cpu.iloc[x]:
         cpu.iloc[x] = 'i5';
    elif 'i7' in cpu.iloc[x]:
         cpu.iloc[x] = 'i7';
    elif 'i9' in cpu.iloc[x]:
         cpu.iloc[x] = 'i9';
    elif 'AMD A6' in cpu.iloc[x]:
         cpu.iloc[x] = 'AMD A6';
    elif 'AMD A9' in cpu.iloc[x]:
         cpu.iloc[x] = 'AMD A9';
    elif 'AMD A10' in cpu.iloc[x]:
         cpu.iloc[x] = 'AMD A10';


# encoding data


# get_dummies encoding

dummies_company = pd.get_dummies(df.Company)
dummies_screenResolution = pd.get_dummies(df.ScreenResolution)
dummies_cpu = pd.get_dummies(cpu)
dummies_opSys = pd.get_dummies(df.OpSys)

# label encoding

ram = df.Ram
for x in range(0,len(ram)):
    if ram.iloc[x] == '2GB':
         ram.iloc[x] = 0;
    elif ram.iloc[x] == '4GB':
         ram.iloc[x] = 1;
    elif ram.iloc[x] == '6GB':
         ram.iloc[x] = 2;
    elif ram.iloc[x] == '8GB':
         ram.iloc[x] = 3;
    elif ram.iloc[x] == '12GB':
         ram.iloc[x] = 4;
    elif ram.iloc[x] == '16GB':
         ram.iloc[x] = 5;
    elif ram.iloc[x] == '24GB':
         ram.iloc[x] = 6;
    elif ram.iloc[x] == '32GB':
         ram.iloc[x] = 7;
    elif ram.iloc[x] == '64GB':
         ram.iloc[x] = 8;




label = LabelEncoder()
label_memory = pd.DataFrame()
label_memory['Memory'] = label.fit_transform(df.Memory)


# dropping after encoding

df.drop(['Company'],axis = 'columns', inplace=True)
df.drop(['ScreenResolution'],axis = 'columns', inplace=True)
df.drop(['Ram'], axis='columns', inplace=True)
df.drop(['Cpu'], axis='columns', inplace=True)
df.drop(['Memory'], axis='columns', inplace=True)
df.drop(['OpSys'], axis='columns', inplace=True)

# joining data

new_df = df.join([dummies_company, dummies_screenResolution, ram, dummies_cpu, dummies_opSys])


# dropping some data to fit model
new_df.drop(['Acer','Celeron','1366x768', 'No OS'], axis='columns', inplace=True)


# creating a model

reg = linear_model.LinearRegression()
reg.fit(new_df, price)
print(reg.score(new_df, price))

