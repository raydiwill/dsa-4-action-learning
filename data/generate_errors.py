import pandas as pd
import numpy as np

# Load your dataset (replace 'your_data.csv' with the path to your dataset)
df = pd.read_csv('Test.csv')

# Sample 1000 records from the dataset
sampled_dfs = [df.sample(n=1000, replace=False) for _ in range(10)]


def introduce_errors(dataframe):
    # Identifying numerical and categorical columns
    numerical_cols = (dataframe.select_dtypes(include=['number'])
                      .columns.tolist())
    categorical_cols = ['user_id']

    # Randomly change some numerical values to be less than 0
    for col in numerical_cols:
        indices_to_change = np.random.choice(dataframe.index,
                                             size=int(len(dataframe) * 0.1),
                                             replace=False)
        dataframe.loc[indices_to_change, col] *= -1

    # Randomly delete some 'user_id' values
    user_id_indices_to_delete = np.random.choice(dataframe.index,
                                                 size=int(len(dataframe) * 0.1),
                                                 replace=False)
    dataframe.loc[user_id_indices_to_delete, 'user_id'] = None


for i, sdf in enumerate(sampled_dfs):
    introduce_errors(sdf)
    sdf.to_csv(f'../data/default/customers_file_{i+1}.csv', index=False)
