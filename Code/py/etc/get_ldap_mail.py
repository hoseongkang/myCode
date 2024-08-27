from ldap3 import Server, Connection, ALL, ALL_ATTRIBUTES, SUBTREE
import re

ldap_server = Server("ldap://*****:389")
ldap_conn = Connection(ldap_server, 'sy\\SYC223351', '*****', auto_bind=True)
ldap_conn.bind()

base_dn = 'DC=sy,DC=com'
search_filter = '(&(objectClass=user)(sAMAccountName=syc223007))'  #syc219417 이건 514
attributes = ['mail','displayName','sAMAccountName','userAccountControl','givenName','networkAddress']
# attributes = '*'
ldap_conn.search(search_base=base_dn, search_filter=search_filter, search_scope=SUBTREE, attributes=attributes)
pattern = re.compile(r'\[.*?\]')

for entry in ldap_conn.entries:
    print(entry.mail)
    strName = re.sub(pattern, '', str(entry.givenName))
    print(strName)
    print(entry.sAMAccountName)
    user_account_control  = entry.userAccountControl.value
    if user_account_control & 2:
        print("disabled")
    else:
        print("enabled")

# from ldap3 import Server, Connection, SUBTREE

# ldap_server = Server("ldap://*****:389")
# ldap_conn = Connection(ldap_server, 'sy\\SYC223351', '*****', auto_bind=True)

# base_dn = 'DC=sy,DC=com'
# search_filter = '(&(objectClass=user)(networkAddress=' + '130.1.15.38' + '))'  # Include the condition for laddr attribute
# attributes = ['*']

# ldap_conn.search(search_base=base_dn, search_filter=search_filter, search_scope=SUBTREE, attributes=attributes)

# for entry in ldap_conn.entries:
#     print(entry.mail)
#     print(entry.givenName)
#     print(entry.sAMAccountName)
#     user_account_control = entry.userAccountControl.value
#     if user_account_control & 2:
#         print("disabled")
#     else:
#         print("enabled")
