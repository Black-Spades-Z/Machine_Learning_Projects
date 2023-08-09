import pandas as pd
import pickle
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
from sklearn import  linear_model


df = pd.read_csv("Melbourne_housing_extra_data.csv")


new_df = df.drop(["Address", "SellerG", "Date", "Distance", "Postcode", "Car", "Landsize", "BuildingArea", "YearBuilt", "Lattitude", "Longtitude", "Propertycount", "CouncilArea"], axis='columns')

price = new_df["Price"].mean()


new_df["Price"].fillna(price, inplace=True)
new_df.dropna(inplace=True)
new_df.reset_index(drop=True, inplace=True)


cols = new_df.columns.tolist()
cols = cols[0:2] + cols[4:-1] + cols[2:4]
new_df = new_df[cols]

target = new_df["Price"]
inputs = new_df.drop("Price", axis='columns')



for col in new_df.columns:
    print(col, end=" ")
print('\n', new_df.index)

label = LabelEncoder()
# le_suburb = label.fit_transform(["Suburb"])
# le_suburb = le_suburb.reshape(len(le_suburb), 1)
#

# oh_suburb = OneHotEncoder(sparse=False)
# oh_suburb = oh_suburb.fit_transform(le_suburb).to_array()

# column_set = ColumnTransformer([('encoder', OneHotEncoder(), [0])], remainder='passthrough')
# oneHot_data = np.array(column_set.fit_transform(new_df["Suburb"]), dtype=np.str)

# inputs["Suburb_n"] = oh_suburb
inputs["Rooms_n"] = label.fit_transform(inputs["Rooms"])
inputs["Bedroom2_n"] = label.fit_transform(inputs["Bedroom2"])
inputs["Bathroom_n"] = label.fit_transform(inputs["Bathroom"])
inputs["Type_n"] = label.fit_transform(inputs["Type"])
inputs["Method_n"] = label.fit_transform(inputs["Method"])

inputs_n = inputs.drop(["Suburb", "Rooms", "Method", "Bedroom2", "Bathroom", "Type"], axis='columns')

reg = linear_model.LinearRegression()
reg.fit(inputs_n, target)

rooms = int(input("Input rooms : "))
bedrooms = int(input("Input bedrooms : "))
bathrooms = int(input("Input bathrooms : "))
type = int(input("Input type : "))
method = int(input("Input method : "))

prices = reg.predict([[rooms, bedrooms, bathrooms, type, method]])
prices = float(prices)
round(prices, 4)

print(reg.score(inputs_n, target))
print("Price is : " , prices)

