from imp import source_from_cache
import shutil

source_file = r'C:/RPADATA/RPA_240_SYC_1118/Input/패키징_본사_2022-07-16~2022-07-30.xlsx'
destination = r'C:/RPADATA/RPA_240_SYC_1118/Input/test/패키징_본사_2022-07-16~2022-07-30.xlsx"'
'''
source_file = r'\\130.1.22.33\a360data\RPA_240_SYC_1118\Master\백업\RPA_회계_회사명_사업장_M_YYYYMM_New.xlsx'
destination = r'\\130.1.22.33\a360data\RPA_240_SYC_1118\Master\RPA_회계_회사명_사업장_M_YYYYMM_New_py.xlsx"'
'''
shutil.copy(source_file, destination)

