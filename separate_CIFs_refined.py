'''
Please have python 3.6 or higher installed
run by using command python separate_CIFs_refined.py --cif_dir ___your directory to cif___ --cifs_dir_generate ___your new location to save separated cifs___
'''

import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--cif_dir', type=str, default=None, help='Directory of CIF needed separating')
parser.add_argument('--cifs_dir_generate', type=str, default=None, help='Directory where new separated CIFs will be')

args = parser.parse_args()


cif_dir = args.cif_dir
with open(cif_dir) as f:
    content = f.readlines()

k = []
for n in content:
    if 'data' in n:
        if n.split('_')[0] == 'data':
            k.append(n)

q = []
for i in range(0,len(k)):
    try:
        m = content[content.index(k[i]):content.index(k[i+1])]
    except:
        m = content[content.index(k[i]):]
    q.append(m)


cifs_dir_generate = args.cifs_dir_generate
for i in q:
    s = ""
    for j in i:
        if 'database_code_depnum_ccdc_archive' in j:
            s = j.split("'")[1].split(" ")[0]+ "_" + j.split("'")[1].split(" ")[1]
    f= open(cifs_dir_generate + '/' + s + ".cif","w+")
    for item in i:
        f.write(item)
