#%%
import pandas as pd
import os

name_list=[]
root = "../mydata"
# 1. 여러 CSV 파일을 globals로 불러오기
for filename in os.listdir(root):
    name = filename.split(".")[0]
    globals()[name] = pd.read_csv(os.path.join(root, filename))
    name_list.append(name)

# 2. 전처리 함수 정의
def make_data5():
    data  = globals()[name_list[2]][globals()[name_list[2]]['eval_set'] == 'prior']
    data1 = pd.merge(order_products__prior, data, on='order_id', how='right')
    data2 = pd.merge(data1, products, on='product_id', how='left')
    data3 = pd.merge(data2, departments, on='department_id', how='left')
    data4 = pd.merge(data3, aisles, on='aisle_id', how='left')
    return data4
# %%
