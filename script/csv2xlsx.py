from email.header import Header
import pandas as pd

def csv2xlsx_pd(filename=None,startrows=0,endrows=1):
    skiprows = startrows-1
    nrows = endrows-startrows+1
    csv = pd.read_csv(filename + '.csv', delim_whitespace=True ,skiprows=skiprows, nrows=nrows, encoding='utf-8', header=None) # skiprows表示忽略前几行，nrows指往后读几行startrows+1~startrows+endrows
    df = csv.iloc[:,1:]
    df.to_excel(filename+'_{}_{}.xlsx'.format(startrows,endrows),index=None)
filename = './csvImp/哈利波特题库_12_18'
csv2xlsx_pd(filename,3,46)