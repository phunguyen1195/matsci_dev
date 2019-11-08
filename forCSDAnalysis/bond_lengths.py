import os
import glob

from ccdc import io, descriptors

directory = '/home/phunguyen/forCSDAnalysis/vdw/'

cif_files = glob.glob(os.path.join(directory, '*.cif'))
print (cif_files)
for cif_file in cif_files:
    filename1 = os.path.basename(cif_file)
    filename2 = filename1.split(".")[0]
    s ="/home/phunguyen/forCSDAnalysis/bond_length/" +  filename2 + ".txt"
    f= open(s ,"w+")
    with io.MoleculeReader(cif_file) as rdr:
        cif = rdr[0]
        for a1 in cif.atoms:
            for a2 in cif.atoms:
                s2 = "(" + a1.label + "," + a2.label + ")" + ":" + str(descriptors.MolecularDescriptors.atom_distance(a1, a2)) + "\n"
                f.write(s2)
                print a1.label, a2.label, descriptors.MolecularDescriptors.atom_distance(a1, a2)
    f.close()

#cif_entry = io.EntryReader(cif_file)
#a1 = cif_entry.attributes['_geom_bond_atom_site_label_1']
#a2 = cif_entry.attributes['_geom_bond_atom_site_label_2']
#length = cif_entry.attributes['_geom_bond_distance']

#for a1, a2, length in zip(a1, a2, length):
#     print a1, a2, length
