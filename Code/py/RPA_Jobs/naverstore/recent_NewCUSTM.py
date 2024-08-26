import pyodbc 
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import pandas as pd

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
        # formatted_purchase_date = datetime.strptime(str(purchase_date).split()[0], '%Y-%m-%d %H:%M:%S').strftime('%Y-%m')
        dataset.append({
            '구매확정일': purchase_date,
            '배송상태': delivery_status,
            '주문자연락처': customer_phone,
            '오더번호': order_number,
            '이름': str_name
        })

conn.close()

dataset = pd.DataFrame(dataset)
dataset = dataset.drop_duplicates(subset='오더번호')

dataset['구매확정일'] = pd.to_datetime(dataset['구매확정일']).dt.to_period('D').dt.to_timestamp()

end_date = datetime.now()
start_date = end_date - timedelta(days=90)

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

recent_customers = {}

for i in range(len(dataset)):
    purchase_date = dataset.iloc[i, 0]
    if start_date <= purchase_date <= end_date:
        customer_phone = dataset.iloc[i, 4]
        recent_customers[customer_phone] = recent_customers.get(customer_phone, 0) + 1

prev_customers = set()
for i in range(len(dataset)):
    purchase_date = dataset.iloc[i, 0]
    if purchase_date < start_date:
        prev_customers.add(dataset.iloc[i, 4])

repeat_customers = {customer: count for customer, count in recent_customers.items() if customer not in prev_customers and count >= 2}
top_15_customers = dict(sorted(repeat_customers.items(), key=lambda x: x[1], reverse=True)[:15])

plt.bar(range(len(top_15_customers)), top_15_customers.values(), align='center')
plt.xticks(range(len(top_15_customers)), list(top_15_customers.keys()), rotation=45, fontsize=13, ha='right')
# plt.xlabel('주문고객', fontsize=20)
plt.ylabel('결제 건', fontsize=20)
plt.tight_layout()
# plt.title('최근 60일간 재구매 고객')
plt.show()