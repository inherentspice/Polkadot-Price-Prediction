import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import RobustScaler

class Utils:
    def test_classifiers(self, X, y):
        """This function requires an X (features)
        and a y (target), and returns a DataFrame with
        the names of classifiers, and their baseline score
        of predicting y given x.
        """
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
        X_train, X_val, y_train, y_val = train_test_split(X_train, y_train,
                                                          test_size=0.25, random_state=42)
        scaler = RobustScaler().fit(X_train)
        X_train_scaled = scaler.transform(X_train)
        X_val_scaled = scaler.transform(X_val)
        X_test_scaled = scaler.transform(X_test)
        k_regressor = KNeighborsClassifier().fit(X_train_scaled, y_train)
        s_model = SVC().fit(X_train_scaled, y_train)
        classifier = DecisionTreeClassifier().fit(X_train_scaled, y_train)
        random_classifier = RandomForestClassifier().fit(X_train_scaled, y_train)
        ada = AdaBoostClassifier().fit(X_train_scaled, y_train)
        gradient = GradientBoostingClassifier().fit(X_train_scaled, y_train)
        scores = pd.DataFrame(columns=['scores'], index=['KNeighbors', 'Support Vector', 'Decision Tree',
                                                'Random Forest', 'Ada Boost', 'Gradient Boost'],
                      data=[k_regressor.score(X_val_scaled, y_val), s_model.score(X_val_scaled, y_val),
                           classifier.score(X_val_scaled, y_val), random_classifier.score(X_val_scaled, y_val),
                           ada.score(X_val_scaled, y_val), gradient.score(X_val_scaled, y_val)])
        return scores
