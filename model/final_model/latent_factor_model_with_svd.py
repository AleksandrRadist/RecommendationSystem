import pandas as pd
import numpy as np
from scipy.linalg import svd


def latent_factor_model_with_svd(data_matrix, data_true, top_k):
    U, sigma, V = svd(data_matrix)

    Sigma = np.zeros((200, 27))
    Sigma[:27, :27] = np.diag(sigma)

    new_data_matrix = U.dot(Sigma).dot(V)

    K = 25
    sigma[K:] = 0
    Sigma = np.zeros((200, 27))
    Sigma[:27, :27] = np.diag(sigma)

    new_data_matrix = U.dot(Sigma).dot(V)

    new_data_matrix = pd.DataFrame(new_data_matrix, index=data_matrix.index, columns=data_matrix.columns)

    predictions = []
    for client_id in data_true.index:
        prediction = (
            new_data_matrix
                .loc[client_id]
                .sort_values(ascending=False)
                .index.values
        )

        predictions.append(
            list(prediction)[:top_k])

    data_true['prediction_svd'] = predictions

    return predictions, data_true
