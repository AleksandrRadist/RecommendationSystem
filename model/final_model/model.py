import psycopg2
import pandas.io.sql as sqlio
from data_processing import data_processing
from latent_factor_model_with_svd import latent_factor_model_with_svd
import warnings

warnings.filterwarnings('ignore')


def model():
    def calc_precision(column):
        return (
            data_true
                .apply(
                lambda row: len(set(row['true_test']).intersection(row[column])) / min(len(row['true_test']) + 0.001,
                                                                                       top_k),
                axis=1
            )
        ).mean()

    def calc_recall(column):
        return (
            data_true
                .apply(
                lambda row: len(set(row['true_test']).intersection(row[column])) / min(len(row[column]) + 0.001, top_k),
                axis=1
            )
        ).mean()

    def calc_fscore_precision(column):
        beta = 0.5
        precision = calc_precision(column)
        recall = calc_recall(column)
        fscore_precision = ((1 + beta ** 2) * precision * recall) / (beta ** 2 * precision + recall)
        return fscore_precision

    # top k рекомендаций
    top_k = 1

    # соединение с базой данных PostgreSQL
    db_connect = psycopg2.connect(
        host='127.0.0.1',
        port='5432',
        database='reccomendation_system',
        user='aleks',
        password='qweasd'
    )

    # cursor = db_connect.cursor()

    select_clients_data = 'SELECT * FROM analytics_client'
    select_categories_data = 'SELECT * FROM analytics_category'
    select_transactions_data = 'SELECT * FROM analytics_transaction'

    # cursor.execute(select_transactions_data)
    # transaction_data = cursor.fetchall()
    clients_data = sqlio.read_sql_query(select_clients_data, db_connect)
    categories_data = sqlio.read_sql_query(select_categories_data, db_connect)
    transaction_data = sqlio.read_sql_query(select_transactions_data, db_connect)

    # модуль предобработки данных
    data_matrix, data_true = data_processing(clients_data, categories_data, transaction_data)

    # модуль обучения модели и предсказания рекомендаций
    predictions, data_true = latent_factor_model_with_svd(data_matrix, data_true, top_k)

    # оценка модели по метрике качества F-score@1
    fscore = calc_fscore_precision("prediction_svd")

    db_connect = None

model()

