'''
Please have python 3.6 or higher installed
run by using command python separate_CIFs_refined.py --cif_dir ___your directory to cif___ --cifs_dir_generate ___your new location to save separated cifs___
'''

import glob
import os
import subprocess
import pandas as pd
import shutil

print("starting now")

dir = "/home/phunguyen/dimethyl_sulfoxide_cifs/"

#for filepath in glob.iglob(dir + "*.cif"):
#    try:
#        cmd = "platon -o -K " + os.path.basename(filepath)
#        k = subprocess.run(
#            [cmd],
#            shell=True,
#            cwd=dir,
#            stdin=subprocess.PIPE,
#            stdout=subprocess.PIPE,
#            stderr=subprocess.PIPE,
#        )
#        k.wait()
#        print ("finished with: " + os.path.basename(filepath))
#        if k.returncode == None:
#            print("error with process")
#    except:
#        print(filepath)
#        continue

dest = "/home/phunguyen/dimethyl_sulfoxide_cifs_lis/"
a = []
for file in os.listdir(dir):
    if file.endswith(".lis"):
        a.append(os.path.join(dir , file))

for f in a:
        shutil.move(f, dest)
print ("finished moving all .lis")

allcontent = []
dic = {}
name = []
for filepath in glob.iglob(dest + "*.lis"):
    content = []
    try:
        print(filepath)
        with open(filepath) as f:
            content = f.readlines()
            allcontent.append(content)
            name.append(os.path.basename(filepath))
            dic[os.path.basename(filepath)] = content
    except:
        continue

df = pd.DataFrame(list(zip(name, allcontent)), 
               columns =['Name', 'Content']) 

name_pkin = []
pkin = []
name_solare = []
solare = []
for i,row in df.iterrows():
    u = row["Content"]
#    get_ux.append(u[-1])
    find_content_page = ""
    for n in u:
        if "Page - Index" in n:
            find_content_page = n
            m = u[u.index(find_content_page) :]
            rest_content = u[: u.index(find_content_page)]

    get_pages = []
    for n in m:
        if "Page" in n:
            get_pages.append(n)

    pages = []
    for n in get_pages:
        p = n.split()
        if p[1].isdigit():
            pages.append(n)

    find_pages_in_rest_content = []
    for o in pages:
        s = " " + o.split()[1] + "\n"
        for n in rest_content:
            if "Page" in n and s in n:
                find_pages_in_rest_content.append(n)

    get_content_based_on_pages = []
    for i in range(0, len(find_pages_in_rest_content)):
        try:
            t = u[
                u.index(find_pages_in_rest_content[i]) : u.index(
                    find_pages_in_rest_content[i + 1]
                )
            ]
        except:
            try:
                t = u[u.index(find_pages_in_rest_content[i]) :]
            except:
                continue
        get_content_based_on_pages.append(t)

    find_void = "PLATON-VOIDS"
    void_data = []
    for i in range(0, len(find_pages_in_rest_content)):
        if find_void in find_pages_in_rest_content[i]:
            try:
                void_data = u[
                    u.index(find_pages_in_rest_content[i]) : u.index(
                        find_pages_in_rest_content[i + 1]
                    )
                ]
                break
            except:
                continue

    filled_space = "Percent Filled Space"
    
    t = []
    Packing_Index = 0
    for i in void_data:
        if filled_space in i:
            t = i.split()

    for j in range(0, len(t)):
        if t[j] == "Space":
            try:
                Packing_Index = float(t[j + 1])
                pkin.append(Packing_Index)
                name_pkin.append(row["Name"])
            except ValueError:
                print("Not a float")

    solvent_area = "Total Potential Solvent Area Vol"
    b = []
    solvent_area_number = 0
    for i in void_data:
        if solvent_area in i:
            b = i.split()
#            get_uy.append(u[-1])

    for j in range(0, len(b)):
        if b[j] == "Vol":
            try:
                solvent_area_number = float(b[j + 1])
                solare.append(solvent_area_number)
                name_solare.append(row["Name"])
            except ValueError:
                print("Not a float")

df_pkin = pd.DataFrame(list(zip(name_pkin, pkin)), 
               columns =['Name', 'packing_index'])

df_solare = pd.DataFrame(list(zip(name_solare, solare)), 
               columns =['Name', 'solvent_area_number']) 
df_pkin.to_csv("/home/phunguyen/data/dimethyl_sulfoxide_pkin.csv")
df_solare.to_csv("/home/phunguyen/data/dimethyl_sulfoxide_solare.csv")

