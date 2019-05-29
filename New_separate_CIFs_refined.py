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

print("finished reading file")

k = []
for n in content:
    if 'data' in n:
        if n.split('_')[0] == 'data':
            k.append(n)

print("finished separating file")

q = []
for i in range(0,len(k)):
    try:
        m = content[content.index(k[i]):content.index(k[i+1])]
    except:
        m = content[content.index(k[i]):]
    q.append(m)

print("finished saving file to list")

cifs_dir_generate = args.cifs_dir_generate

n = []
get_s = []
count = 0
for i in q:
    s = ""
    for j in i:
        if "database_code_depnum_ccdc_archive" in j:
            try:
                s = j.split("'")[1].split(" ")[0] + "_" + j.split("'")[1].split(" ")[1]
            except Exception as e:
                print(e)
                print(s)
    try:
        with open(
            cifs_dir_generate + s + ".cif", "w+"
        ) as g:
            for item in i:
                g.write(item)
    except Exception as e:
        print(n)
        print(s)
