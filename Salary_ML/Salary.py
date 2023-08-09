import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report


# importing data

df = pd.read_csv('Car details v3.csv')

# Cleaning data


df.dropna(inplace=True)
df.drop(['name', 'seller_type', 'mileage', 'max_power', 'torque','seats'], axis='columns', inplace=True)


# # Label encoding for year
#
# year_lb = pd.DataFrame(df.year)
#
# # Label encoding for km_driven
#
# km = pd.DataFrame(df.km_driven)
#

# Label encoding for fuel

label = LabelEncoder()

fuel_lb = pd.DataFrame(label.fit_transform(df.fuel), columns=['fuel'])

# Label encoding for transmission

transmission_lb = pd.DataFrame(label.fit_transform(df.transmission), columns=['transmission'])

# Label encoding for owner

owner_lb = pd.DataFrame(label.fit_transform(df.owner), columns=['owner'])

# Label encoding for engine

engine_lb = pd.DataFrame(label.fit_transform(df.engine), columns=['engine'])

# Dropping useless data

df.drop(columns=['owner', 'transmission', 'engine', 'fuel'], inplace=True)

# Joining datasets

new_df = df.join([fuel_lb, transmission_lb, owner_lb, engine_lb])
new_df.dropna(inplace=True)
new_df.reset_index(drop=True, inplace=True)
price = new_df['selling_price'] * 0.012872
new_df.drop(['selling_price', 'engine'], axis='columns', inplace=True)

# Creating a model

x = new_df
y = price


X_train, X_test, Y_train, Y_test = train_test_split(x, y, test_size=0.2, random_state=3)

model = DecisionTreeClassifier()
model.fit(X_train, Y_train)

predictions = model.predict(X_test)
accuracy = accuracy_score(y_true=Y_test, y_pred=predictions)
print(accuracy)
print(classification_report(y_true=Y_test, y_pred=predictions))
print(model.score(X_train, X_test))
