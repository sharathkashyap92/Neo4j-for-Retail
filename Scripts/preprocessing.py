import pandas as pd
import numpy as np

df_purchaseHistory = pd.read_csv('purchase_history.csv')
df_itemToid = pd.read_csv('item_to_id.csv')

# getting the number of items
df_purchaseHistory['n_items'] = df_purchaseHistory['id'].apply(lambda x: len(x.split(',')))

# getting the sum of items purchased per user
df_totalPurchasesByCustomer = df_purchaseHistory[['user_id', 'n_items']].groupby('user_id').sum()

#  sorting and displaying
df_totalPurchasesByCustomer.sort_values('n_items', ascending = False).head()

# flattening the orders column into (customer, item) tuples to simplify grouping
df_flattened = pd.DataFrame(columns = ['user_id', 'id'])
count = 0
for i in df_purchaseHistory.iterrows():
    u_id = i[1][0]
    for j in i[1][1].split(','):
        df_temp = pd.DataFrame([[u_id, j]], columns = ['user_id', 'id'])
        df_flattened = df_flattened.append(df_temp)
    count += 1
    print(count)

df_flattened.to_csv('flattened.csv', index = False)

# adding a ones column to simplify summation
df_flattened['count'] = np.ones(df_flattened.shape[0])

# grouping by and getting the customers who ordered each products the most
df_flattened = df_flattened.groupby(['id', 'user_id']).sum()
df_tr = df_flattened.reset_index()

# merging
df_tr['id'] = df_tr['id'].astype(int)
df_trp = pd.merge(df_tr, df_itemToid, left_on = 'id', right_on = 'Item_id', how = 'left')

df_trp['count'] = df_trp['count'].astype(np.number)
df_trp = df_trp.drop(['id', 'Item_id'], axis = 1)
df_trp = df_trp.groupby(['Item_name', 'user_id']).sum().reset_index()

# exporting
df_trp.to_csv('agg.csv', index = False)
pd.DataFrame(df_trp.Item_name.unique(), columns = ['item']).to_csv('item.csv', index = False)
pd.DataFrame(df_trp.user_id.unique(), columns = ['user']).to_csv('user.csv', index = False)