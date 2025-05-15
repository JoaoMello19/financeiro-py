import numpy as np
import pandas as pd

from xgboost import XGBClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, RobustScaler
from sklearn.neural_network import MLPClassifier
from sklearn.feature_selection import VarianceThreshold


def filter_features(df, target_col='Next Raised', corr_threshold=0.9, top_n=15, random_state=42):
    # Separa features e target
    X = df.drop(columns=[target_col])
    y = df[target_col]

    # 1. Remove colunas com baixa variância
    var_sel = VarianceThreshold(threshold=0.01)
    X_var = pd.DataFrame(
        var_sel.fit_transform(X),
        columns=X.columns[var_sel.get_support()]
    )
    descartadas_variancia = list(X.columns[~var_sel.get_support()])

    # 2. Remove colunas com alta correlação
    corr_matrix = X_var.corr().abs()
    upper = corr_matrix.where(
        np.triu(np.ones(corr_matrix.shape), k=1).astype(bool)
    )
    to_drop_corr = [column for column in upper.columns if any(upper[column] > corr_threshold)]
    X_corr = X_var.drop(columns=to_drop_corr)
    
    # 3. Random Forest para seleção de variáveis importantes
    rf = RandomForestClassifier(random_state=random_state)
    rf.fit(X_corr, y)
    importances = pd.Series(rf.feature_importances_, index=X_corr.columns)
    top_features = importances.sort_values(ascending=False).head(top_n).index

    # Dados finais
    df_reduzido = df[top_features.tolist() + [target_col]]
    lista_descartadas = descartadas_variancia + to_drop_corr

    return df_reduzido, lista_descartadas



def preprocess(data):
    # Colunas candidatas para padronização com Z-Score
    standard_columns = [
        'Open', 'High', 'Low', 'Close', 'MM_7', 'MM_15',
        'Lag_1', 'Lag_2', 'Lag_3', 'Lag_4', 'Lag_5'
    ]
    # Colunas candidatas para padronização robusta
    robust_columns = ['Volume', '% Change', 'Delta_7', 'Delta_15', 'Delta_MM']

    # Filtra apenas as colunas que realmente estão no DataFrame
    standard_columns = [col for col in standard_columns if col in data.columns]
    robust_columns = [col for col in robust_columns if col in data.columns]

    # Aplica os scalers se houver colunas válidas
    if standard_columns:
        standard_scaler = StandardScaler()
        data[standard_columns] = standard_scaler.fit_transform(data[standard_columns])

    if robust_columns:
        robust_scaler = RobustScaler()
        data[robust_columns] = robust_scaler.fit_transform(data[robust_columns])

    return data


def train_test_split(data, test_size=0.2):
    target = 'Next Raised'
    X, y = data.drop(columns=target), data[target]

    split_idx = int(len(data) * (1 - test_size))
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

def do_default_model(model, X_train, X_test, y_train, y_test):
    """
    Função para treinar e avaliar um modelo da forma genérica
    """
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    return evaluate_model(y_test, y_pred)


def do_random_forest(X_train, X_test, y_train, y_test):
    model = RandomForestClassifier(class_weight='balanced', random_state=42)
    return do_default_model(model, X_train, X_test, y_train, y_test)


def do_xgboost(X_train, X_test, y_train, y_test):
    model = XGBClassifier(scale_pos_weight=1, eval_metric='logloss', random_state=42)
    return do_default_model(model, X_train, X_test, y_train, y_test)


def do_svm(X_train, X_test, y_train, y_test):
    model = SVC(class_weight='balanced', probability=False, random_state=42)
    return do_default_model(model, X_train, X_test, y_train, y_test)


def do_mlp(X_train, X_test, y_train, y_test):
    model = MLPClassifier(hidden_layer_sizes=(100,), max_iter=5000, random_state=42, early_stopping=True)
    return do_default_model(model, X_train, X_test, y_train, y_test)
