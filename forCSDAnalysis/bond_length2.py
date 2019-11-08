import os
import glob

from ccdc import io, descriptors

cif_entry = io.EntryReader("/home/phunguyen/forCSDAnalysis/vdw/CONTCARna.cif")
a1 = cif_entry.attributes['_geom_bond_atom_site_label_1']
a2 = cif_entry.attributes['_geom_bond_atom_site_label_2']
length = cif_entry.attributes['_geom_bond_distance']

for a1, a2, length in zip(a1, a2, length):
    print a1, a2, length
