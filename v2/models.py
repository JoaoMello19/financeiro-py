from sklearn.preprocessing import StandardScaler, RobustScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from xgboost import XGBClassifier

def preprocess(data):
    # Padronização com Z-Score
    standard_columns = ['Open', 'High', 'Low', 'Close', 'MM_7', 'MM_15']
    standard_scaler = StandardScaler()
    data[standard_columns] = standard_scaler.fit_transform(data[standard_columns])

    # Padronização robusta para colunas com outliers
    robust_columns = ['Volume', '% Change', 'Delta_7', 'Delta_15', 'Delta_MM']
    robust_scaler = RobustScaler()
    data[robust_columns] = robust_scaler.fit_transform(data[robust_columns])

    return data


def train_test_split(data, test_size=0.2):
    split_idx = int(len(data) * (1 - test_size))
    features = [
        'Open', 'High', 'Low', 'Close', 'MM_7', 'MM_15', 'Volume', '% Change', 'Delta_7',
        'Delta_15', 'Delta_MM', 'Raised'
    ]
    target = 'Next Raised'

    X, y = data[features], data[target]

    X_train, X_test = X[:split_idx], X[split_idx:]
    y_train, y_test = y[:split_idx], y[split_idx:]
    
    return X_train, X_test, y_train, y_test


def evaluate_model(y_test, y_pred):
    return {
        'Accuracy': accuracy_score(y_test, y_pred),
        'Precision': precision_score(y_test, y_pred),
        'Recall': recall_score(y_test, y_pred),
        'F1 Score': f1_score(y_test, y_pred),
        'Confusion Matrix': confusion_matrix(y_test, y_pred).tolist()
    }


def do_random_forest(X_train, X_test, y_train, y_test):
    model = RandomForestClassifier(class_weight='balanced', random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    return evaluate_model(y_test, y_pred)


def do_xgboost(X_train, X_test, y_train, y_test):
    model = XGBClassifier(scale_pos_weight=1, eval_metric='logloss', random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    return evaluate_model(y_test, y_pred)


def do_svm(X_train, X_test, y_train, y_test):
    model = SVC(class_weight='balanced', probability=False, random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    return evaluate_model(y_test, y_pred)


def do_mlp(X_train, X_test, y_train, y_test):
    model = MLPClassifier(hidden_layer_sizes=(100,), max_iter=5000, random_state=42, early_stopping=True)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    return evaluate_model(y_test, y_pred)
