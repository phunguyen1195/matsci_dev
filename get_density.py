#!/usr/bin/env python
# coding: utf-8

# In[5]:


import glob
import pandas as pd
import os

# In[132]:


allcontent = []
dic = {}
name = []

dest = "/home/phunguyen/dimethyl_sulfoxide_cifs_lis/"

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
#print(allcontent)
df = pd.DataFrame(list(zip(name, allcontent)), 
               columns =['Name', 'Content']) 

name_pkin = []
pkin = []
name_den = []
den = []
name_form = []
form = []
for i,row in df.iterrows():
    u = row["Content"]
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
    print(get_pages)
    
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

                
    density_space = "Calculated Density"
    d = []
    density = 0
    for i in u:
        if density_space in i:
            d = i.split()
    for j in range(0, len(d)):
        if d[j] == '=':
            try:
                get_den = d[j + 1].split('(')[0]
                density = float(get_den)
                den.append(density)
                name_den.append(row["Name"])
            except ValueError:
                print("Not a float")
                
    formula_space = "Sum_Formula"
    f = []
    formula = ""
    for i in u:
        try:
            if formula_space in i:
                f = i.split('=')
                formula = f[1].replace('\n','')
                form.append(formula)
                name_form.append(row["Name"])
        except ValueError:
            print("this is from formula")


# In[133]:


df_pkin_den = pd.DataFrame(list(zip(name_pkin, form, pkin, den)), 
               columns =['Name','Formula', 'packing_index', 'Density'])

df_pkin_den.to_csv("/home/phunguyen/data/dimethyl_sulfoxide_pkin_den_form.csv")

