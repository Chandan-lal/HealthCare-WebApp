import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import pickle
from sklearn import metrics

df = pd.read_csv(r"best_one_1.csv")

X = df.drop(["Disease"], axis = 1)
Y = df["Disease"]
X = X.apply(LabelEncoder().fit_transform)

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.1, random_state = 1)

model = RandomForestClassifier(n_estimators=100)
model = model.fit(X_train, Y_train)

y_pred = model.predict(X_test)

print("Accuracy:",metrics.accuracy_score(Y_test, y_pred))

pickle.dump(model, open('model_chandan.pkl', 'wb'))

