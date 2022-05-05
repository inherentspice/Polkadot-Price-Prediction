import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split

class Utils:
    def test_classifiers(self, X, y):
        """This function requires an X (features)
        and a y (target), and returns a DataFrame with
        the names of classifiers, and their baseline score
        of predicting y given x.
        """
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        k_regressor = KNeighborsClassifier(random_state=42).fit(X_train, y_train)
        s_model = SVC(random_state=42).fit(X_train, y_train)
        classifier = DecisionTreeClassifier(random_state=42).fit(X_train, y_train)
        random_classifier = RandomForestClassifier(random_state=42).fit(X_train, y_train)
        ada = AdaBoostClassifier(random_state=42).fit(X_train, y_train)
        gradient = GradientBoostingClassifier(random_state=42).fit(X_train, y_train)
        scores = pd.DataFrame(columns=['scores'], index=['KNeighbors', 'Support Vector', 'Decision Tree',
                                                'Random Forest', 'Ada Boost', 'Gradient Boost'],
                      data=[k_regressor.score(X_test, y_test), s_model.score(X_test, y_test),
                           classifier.score(X_test, y_test), random_classifier.score(X_test, y_test),
                           ada.score(X_test, y_test), gradient.score(X_test, y_test)])
        return scores
