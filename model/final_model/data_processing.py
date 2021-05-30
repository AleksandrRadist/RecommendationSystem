import pandas as pd
import numpy as np
from datetime import date


def data_processing(clients, categories, transactions):
    # clients preprocessing
    clients.id = clients.id.astype('str')
    clients = clients.rename(columns={'id': 'client_id'})
    clients.birthdate = pd.to_datetime(clients.birthdate, format='%Y-%m-%d')
    clients.registration_date = pd.to_datetime(clients.registration_date, format='%Y-%m-%d')
    mean = clients.loc[clients['income'].isnull() != True, 'income'].mean()
    clients.loc[clients['income'].isnull() == True, 'income'] = mean
    clients.loc[clients['credit'].isnull() == True, 'credit'] = 0
    clients.credit = clients.credit.astype('int')
    clients.loc[clients['deposit'].isnull() == True, 'deposit'] = 0
    clients.deposit = clients.deposit.astype('int')

    # categories processing
    categories.id = categories.id.astype('str')
    categories['mcc_code'] = categories['mcc_code'].fillna('no_code')
    categories['mcc_code'] = categories['mcc_code'].astype('str')
    categories = categories.rename(columns={'id': 'product_category'})

    # transactions processing
    transactions.rename(columns={'Unnamed: 0': 'id'}, inplace=True)
    transactions.product_category = transactions.product_category.astype('str')
    transactions.client_id = transactions.client_id.astype('str')
    transactions.id = transactions.id.astype('str')
    transactions.date = pd.to_datetime(transactions.date, format='%Y-%m-%d %H:%M:%S').dt.date
    transactions = transactions.query('transaction_type != "Positive"')
    transactions = transactions.query('product_category != "28"')
    transactions = transactions.query('product_category != "29"')
    transactions.reset_index(inplace=True, drop=True)
    transactions.loc[transactions.product_company.isnull() == True, 'product_company'] = 'no_company'
    transactions_part = transactions[['client_id', 'product_category', 'date']]

    # data processing
    data = transactions_part.groupby(['client_id', 'product_category'], as_index=False) \
        .agg({'date': 'count'}) \
        .rename(columns={'date': 'purchase_count'})
    users_interactions = data \
        .groupby('client_id', as_index=False) \
        .agg({'product_category': 'count'}) \
        .rename(columns={'product_category': 'unique_categories'})
    users_with_enough_interactions = users_interactions.query('unique_categories > 4')['client_id']
    data = data.loc[np.in1d(data.client_id,
                            users_with_enough_interactions)]
    data = data.assign(purchase_normalize=(data.purchase_count - data.purchase_count.min()) / (
            data.purchase_count.max() - data.purchase_count.min()))
    data.drop(columns=['purchase_count'], inplace=True)
    transactions_last_date = transactions_part \
        .groupby(['client_id', 'product_category'], as_index=False) \
        .date \
        .last()
    data = data \
        .merge(transactions_last_date, on=['client_id', 'product_category']) \
        .rename(columns={'date': 'last_date'})
    split_date = date(2020, 12, 30)
    print(data['last_date'] < split_date)
    data_train = data.query('last_date < @split_date').copy()
    data_test = data.query('last_date >= @split_date').copy()
    data_true = (
        data_train
            .groupby('client_id')['product_category'].agg(lambda x: list(x))
            .reset_index()
            .rename(columns={'product_category': 'true_train'})
            .set_index('client_id')
    )
    data_true['true_test'] = (
        data_test
            .groupby('client_id')['product_category'].agg(lambda x: list(x))
    )
    data_true.loc[pd.isnull(data_true.true_test), 'true_test'] = [
        list() for x in range(len(data_true.loc[pd.isnull(data_true.true_test), 'true_test']))]

    # data processing for collaborative filtering (latent factor model + singular value decomposition
    data_matrix = pd.pivot_table(data, index='client_id', columns='product_category', values='purchase_normalize',
                                 fill_value=0)

    return data_matrix
