import sqlite3
import xml.etree.ElementTree as ET

def parse_xml_and_insert_into_db(xml_file, db_file):
    print('XML파일 읽기')
    conn = sqlite3.connect(db_file)
    print('XML파일 읽기 완료')
    cursor = conn.cursor()
    print('conn 완료')
    cursor.execute('''CREATE TABLE IF NOT EXISTS restaurant (
                        id INTEGER PRIMARY KEY,
                        sitePostNo TEXT,
                        rdnPostNo TEXT,
                        uptaeNm TEXT,
                        siteArea TEXT,
                        siteWhlAddr TEXT,
                        rdnWhlAddr TEXT,
                        bplcNm TEXT
                    )''')

    tree = ET.parse(xml_file)
    print('tree 완료')
    root = tree.getroot()
    print('root  완료')
    for row in root.findall('.//row'):
        site_PostNo = row.find('sitePostNo').text if row.find('sitePostNo') is not None else None
        rdn_PostNo = row.find('rdnPostNo').text if row.find('rdnPostNo') is not None else None
        uptae_Nm = row.find('uptaeNm').text if row.find('uptaeNm') is not None else None
        site_Area = row.find('siteArea').text if row.find('siteArea') is not None else None
        
        # Handling deprecation warning by checking for None explicitly
        site_WhlAddr_elem = row.find('siteWhlAddr')
        site_WhlAddr = site_WhlAddr_elem.text.replace(',', '/') if site_WhlAddr_elem is not None and site_WhlAddr_elem.text else None
        
        rdn_WhlAddr_elem = row.find('rdnWhlAddr')
        rdn_WhlAddr = rdn_WhlAddr_elem.text.replace(',', '/') if rdn_WhlAddr_elem is not None and rdn_WhlAddr_elem.text else None
        
        bplc_Nm = row.find('bplcNm').text if row.find('bplcNm') is not None else None
        
        cursor.execute('''INSERT INTO restaurant (sitePostNo, rdnPostNo, uptaeNm, siteArea, siteWhlAddr, rdnWhlAddr, bplcNm) 
                            VALUES (?, ?, ?, ?, ?, ?, ?)''', 
                    (site_PostNo, rdn_PostNo, uptae_Nm, site_Area, site_WhlAddr, rdn_WhlAddr, bplc_Nm))


    conn.commit()
    conn.close()

xml_file_path = 'C:/RPA_Download/07_24_04_P_XML/fulldata_07_24_04_P_일반음식점.xml'
sqlite_file_path = 'commRes.db'

parse_xml_and_insert_into_db(xml_file_path, sqlite_file_path)
