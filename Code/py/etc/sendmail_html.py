import smtplib, re
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from ldap3 import Server, Connection, ALL, ALL_ATTRIBUTES, SUBTREE

def create_html_table(data):
    html = """<style>
                table {border-collapse: collapse; width: 95%; font-family: 'Yu Gothic', sans-serif;}
                th, td {border: 1px solid #ddd; text-align: left; padding: 5px;}
                th {background-color: #f2f2f2;}
              </style>
              <font face="Yu Gothic";>
              <body class="text-center">
              <h4>법인카드 미처리 사용 내역으로<br>
              전자전표 시스템에서 빠른 처리 부탁드립니다.</h4>
              <table style="font-size:10pt;">
                <tr>
                <th>사업장</th>
                <th>카드번호</th>
                <th>승인번호</th>
                <th>승인일자</th>
                <th>취소일자</th>
                <th>승인시간</th>
                <th>가맹점명</th>
                <th>공급가액</th>
                <th>부가세</th>
                <th>총금액</th>
                </tr>"""
    for emp, details in data.items():
        for _, content in details['contents'].items():
            html += f"<tr><td>{content['사업장']}</td><td>{content['카드번호']}</td><td>{content['승인번호']}</td><td>{content['승인일자']}</td><td>{content['취소일자']}</td><td>{content['승인시간']}</td><td>{content['가맹점명']}</td><td>{content['공급가액']}</td><td>{content['부가세']}</td><td>{content['총금액']}</td></tr>"
    html += """</table></body>"""
    return html



def send_email(receiver_email, html_content, strName, bChkemp):
    sender_email = "SYC719691@samyang.com"
    
    message = MIMEMultipart("alternative")
    if bChkemp == "Y":
        message["Subject"] = "[전송불가] 법인카드 미품의 내역 안내_" + strName
    else:
        message["Subject"] = "법인카드 미품의 내역 안내_" + strName

    message["From"] = "RPA_BOT_39[삼양데이타시스템 Digital Lab]"
    message["To"] = receiver_email
    
    part = MIMEText(html_content, "html")
    message.attach(part)
    
    with smtplib.SMTP("symail.samyang.com", 25) as server:

        server.sendmail(sender_email, receiver_email, message.as_string())

def send(data):
    # 사번 살아있는지 확인하는 절차
    ldap_server = Server("ldap://*****:389")
    ldap_conn = Connection(ldap_server, 'sy\\SYC223351', '*****', auto_bind=True)
    ldap_conn.bind()

    base_dn = 'DC=sy,DC=com'

    for emp, details in data.items():
        html_content = create_html_table({emp: details})
        pattern = re.compile(r'(SYC|syc)([0-9]\w+)')
        result = re.match(pattern, details['mail'])
        search_filter = '(&(objectClass=user)(sAMAccountName='+ result.group() + '))'  #syc219417 이건 514
        attributes = ['mail','displayName','sAMAccountName','userAccountControl','givenName']
        ldap_conn.search(search_base=base_dn, search_filter=search_filter, search_scope=SUBTREE, attributes=attributes)
        pattern = re.compile(r'\[.*?\]')
        for entry in ldap_conn.entries:
            user_account_control  = entry.userAccountControl.value
            strName = re.sub(pattern, '', str(entry.givenName))
            if user_account_control & 2:
                bChkemp = "Y"  # 퇴사자인 경우 Y
            else:
                bChkemp = "N"
        if bChkemp == "N":
            receiver_mail = str(entry.mail)
        else:
            receiver_mail = "hoseng.kang@samyang.com"

        # send_email(receiver_mail, html_content)
        send_email("hoseng.kang@samyang.com", html_content, strName, bChkemp)

data = {
    "emp1": {
        "mail": "syc219417@samyang.com",
        "contents": {
                "1": {"사업장":"testmail1","카드번호":"4518444503742535","승인번호":"749820","승인일자":"2024-02-29","취소일자":"","승인시간":"","가맹점명":"커피숍","공급가액":"120000","부가세":"17800","총금액":"19600"},
                "2": {"사업장":"321321","카드번호":"4518444503742535","승인번호":"749820","승인일자":"2024-02-29","취소일자":"","승인시간":"","가맹점명":"커피숍","공급가액":"120000","부가세":"17800","총금액":"19600"}
        }
    },
    "emp2": {
        "mail": "SYC223007@samyang.com",
        "contents": {
                    "1": {"사업장":"testmail2","카드번호":"4518444503742535","승인번호":"749820","승인일자":"2024-02-29","취소일자":"","승인시간":"","가맹점명":"커피숍","공급가액":"120000","부가세":"17800","총금액":"19600"},
                    "2": {"사업장":"321321","카드번호":"4518444503742535","승인번호":"749820","승인일자":"2024-02-29","취소일자":"","승인시간":"","가맹점명":"커피숍","공급가액":"120000","부가세":"17800","총금액":"19600"}
                }
            },
    "emp3": {
        "mail": "SYC219295@samyang.com",
        "contents": {
                    "1": {"사업장":"testmail3","카드번호":"4518444503742535","승인번호":"749820","승인일자":"2024-02-29","취소일자":"","승인시간":"","가맹점명":"커피숍","공급가액":"120000","부가세":"17800","총금액":"19600"},
                    "2": {"사업장":"321321","카드번호":"4518444503742535","승인번호":"749820","승인일자":"2024-02-29","취소일자":"","승인시간":"","가맹점명":"커피숍","공급가액":"120000","부가세":"17800","총금액":"19600"}
                }
            }
        }

send(data)




</body>
