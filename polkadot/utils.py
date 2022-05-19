import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import RobustScaler
from sklearn.impute import SimpleImputer

class Utils:
    def test_classifiers(self, X, y):
        """This function requires an X (features)
        and a y (target), and returns a DataFrame with
        the names of classifiers, and their baseline score
        of predicting y given x.
        """

        # split data, impute missing values, scale data for models
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
        imp_simple = SimpleImputer()
        imp_simple.fit(X_train)
        X_train_impute = imp_simple.transform(X_train)
        scaler = RobustScaler().fit(X_train_impute)
        X_train_scaled = scaler.transform(X_train_impute)

        # instantiate different classifiers
        k_regressor = KNeighborsClassifier()
        s_model = SVC()
        classifier = DecisionTreeClassifier()
        random_classifier = RandomForestClassifier()
        ada = AdaBoostClassifier()
        gradient = GradientBoostingClassifier()

        # calculate the cross validation score for each model
        score_k = cross_val_score(k_regressor, X_train_scaled, y_train, cv=5)
        score_s = cross_val_score(s_model, X_train_scaled, y_train, cv=5)
        score_c = cross_val_score(classifier, X_train_scaled, y_train, cv=5)
        score_rc = cross_val_score(random_classifier, X_train_scaled, y_train, cv=5)
        score_a = cross_val_score(ada, X_train_scaled, y_train, cv=5)
        score_g = cross_val_score(gradient, X_train_scaled, y_train, cv=5)

        # create a DataFrame that contains the name and score of each model
        scores = pd.DataFrame(columns=['scores'], index=['KNeighbors', 'Support Vector', 'Decision Tree',
                                                'Random Forest', 'Ada Boost', 'Gradient Boost'],
                      data=[score_k.mean(), score_s.mean(), score_c.mean(), score_rc.mean(),
                           score_a.mean(), score_g.mean()])
        return scores
