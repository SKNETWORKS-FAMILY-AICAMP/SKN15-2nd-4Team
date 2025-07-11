import pandas as pd
import os

def make_data5():
    root = "./mydata"  # 상대 경로 (t4_app 기준 ../mydata 아님)

    # CSV 파일 읽기
    orders = pd.read_csv(os.path.join(root, "orders.csv"))
    order_products__prior = pd.read_csv(os.path.join(root, "order_products__prior.csv"))
    products = pd.read_csv(os.path.join(root, "products.csv"))
    departments = pd.read_csv(os.path.join(root, "departments.csv"))
    aisles = pd.read_csv(os.path.join(root, "aisles.csv"))

    # 불필요한 열 제거 (메모리 최적화)
    products_slim = products[['product_id', 'product_name', 'aisle_id', 'department_id']]
    departments_slim = departments[['department_id', 'department']]
    aisles_slim = aisles[['aisle_id', 'aisle']]
    orders_slim = orders[['order_id', 'user_id', 'order_number', 'eval_set', 'days_since_prior_order']]

    # prior 데이터만 필터링
    prior_orders = orders_slim[orders_slim['eval_set'] == 'prior']

    # 병합
    data1 = pd.merge(order_products__prior, prior_orders, on='order_id', how='right')
    data2 = pd.merge(data1, products_slim, on='product_id', how='left')
    data3 = pd.merge(data2, departments_slim, on='department_id', how='left')
    data4 = pd.merge(data3, aisles_slim, on='aisle_id', how='left')

    # NaN 처리
    data4['days_since_prior_order'] = data4['days_since_prior_order'].fillna(-1)

    return data4

# ['department', 'product_id', 'user_id', 'order_number', 'days_since_prior_order']
def make_data_for_check():
    root = "./mydata"  # 상대 경로 (t4_app 기준 ../mydata 아님)

    # CSV 파일 읽기
    orders = pd.read_csv(os.path.join(root, "orders.csv"))
    order_products__prior = pd.read_csv(os.path.join(root, "order_products__prior.csv"))
    products = pd.read_csv(os.path.join(root, "products.csv"))
    departments = pd.read_csv(os.path.join(root, "departments.csv"))
    aisles = pd.read_csv(os.path.join(root, "aisles.csv"))

    # 불필요한 열 제거 (메모리 최적화)
    order_products__prior = order_products__prior[['order_id','product_id']]
    products = products[['product_id', 'product_name', 'aisle_id', 'department_id']]
    departments = departments[['department_id', 'department']]
    aisles = aisles[['aisle_id', 'aisle']]
    orders = orders[orders['eval_set'] == 'prior']
    orders = orders[['order_id','user_id','order_number','days_since_prior_order']]


    # 병합
    data = pd.merge(products, aisles, on='aisle_id', how='left')
    data = pd.merge(data, departments, on='department_id', how='left')
    data = pd.merge(order_products__prior, data, on='product_id', how='left')
    data = pd.merge(orders, data, on='order_id', how='left')

    # NaN 처리 (0으로 표시시 주문간격이 짧은 사람과 첫 주문과 구분이 안되므로 -1로 설정)
    data['days_since_prior_order'] = data['days_since_prior_order'].fillna(-1)

    return data[['department', 'product_id', 'user_id', 'order_number', 'days_since_prior_order']]
