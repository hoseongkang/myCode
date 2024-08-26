import pyodbc 
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter

server = '130.1.22.33,2433'
database = 'PowerBI'
username = 'sa'
password = '@sygrpa22!'

conn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+password)

cursor = conn.cursor()

cursor.execute('SELECT [구매확정일],[배송상태],[주문자연락처],[오더번호],[이름] FROM naverstore_main')

rows = cursor.fetchall()

dataset = []

for row in rows:
    purchase_date, delivery_status, customer_phone, order_number, str_name = row
    if delivery_status == 'DELIVERY_COMPLETION' and purchase_date is not None:
        dataset.append({
            '구매확정일': purchase_date,
            '배송상태': delivery_status,
            '주문자연락처': customer_phone,
            '오더번호': order_number,
            '이름': str_name
        })

conn.close()

dataset = pd.DataFrame(dataset)
order_counts = Counter(dataset.groupby('이름')['오더번호'].nunique())
dataset = dataset.drop_duplicates(subset='오더번호')

dataset['구매확정일'] = pd.to_datetime(dataset['구매확정일']).dt.to_period('D').dt.to_timestamp()

end_date = datetime.now()
start_date = end_date - timedelta(days=90)

# Identifying customers who made at least two purchases before the last 90 days
previous_customers = {}
for i in range(len(dataset)):
    purchase_date = dataset.iloc[i, 0]
    if purchase_date < start_date:
        customer_name = dataset.iloc[i, 4]
        if customer_name in previous_customers:
            previous_customers[customer_name] += 1
        else:
            previous_customers[customer_name] = 1

repeat_previous_customers = {customer for customer, count in previous_customers.items() if count >= 5}

recent_customers = set()
for i in range(len(dataset)):
    purchase_date = dataset.iloc[i, 0]
    if start_date <= purchase_date <= end_date:
        customer_name = dataset.iloc[i, 4]
        recent_customers.add(customer_name)

non_repeat_customers = repeat_previous_customers - recent_customers

data = []
for customer in non_repeat_customers:
    data.append([customer, 1])
# print(data)

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

fig, ax = plt.subplots(1, 1)
# data = [["김봉수"], ["문서영"], ["김성민"]]
column_labels = ["재구매 이탈 고객", "구매횟수"]
df = pd.DataFrame(data, columns=column_labels)
table = ax.table(
    cellText=df.values,
    colLabels=df.columns,
    # rowLabels=["A", "B", "C"],
    colColours=["yellow"] * 2,
    loc="center",
    cellLoc='center',
    colLoc='center',
    rowLoc='right',
    colWidths=[0.5,0.4]
)
table.auto_set_font_size(False)
ax.axis("off")
plt.rcParams["figure.figsize"] = (5,5)
plt.show()