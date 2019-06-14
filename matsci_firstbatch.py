#!/usr/bin/env python
# coding: utf-8

# In[45]:


from pymatgen import Structure
from pymatgen.analysis.structure_analyzer import OxideType
from pymatgen.analysis.structure_analyzer import oxide_type
from pymatgen.analysis.structure_analyzer import VoronoiAnalyzer
from pymatgen.analysis.structure_analyzer import VoronoiConnectivity
from pymatgen.analysis.structure_analyzer import average_coordination_number
from pymatgen.analysis.structure_analyzer import contains_peroxide
from pymatgen.analysis.structure_analyzer import get_dimensionality
from pymatgen.analysis.structure_analyzer import get_max_bond_lengths
from pymatgen.analysis.structure_analyzer import sulfide_type
# from pymatgen.alchemy.filters import AbstractStructureFilter
from pymatgen.analysis.diffraction.core import DiffractionPatternCalculator
from pymatgen.analysis.diffraction.neutron import NDCalculator
from pymatgen.analysis.diffraction.xrd import XRDCalculator
from pymatgen.symmetry.structure import SymmetrizedStructure
from pymatgen.alchemy.materials import TransformedStructure
from pymatgen.analysis.defects.core import Defect
from pymatgen.analysis.defects.core import Vacancy
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer
from pymatgen.analysis.magnetism.analyzer import CollinearMagneticStructureAnalyzer
from pymatgen.analysis.chemenv.coordination_environments.coordination_geometry_finder import LocalGeometryFinder
import logging
from pymatgen.ext.matproj import MPRester
from pymatgen.analysis.chemenv.coordination_environments.chemenv_strategies import SimplestChemenvStrategy, MultiWeightsChemenvStrategy
from pymatgen.analysis.chemenv.coordination_environments.structure_environments import LightStructureEnvironments
import glob
import os
import pandas as pd
import numpy as np
import matplotlib


# In[4]:


def read_cifformat_file (directory):
    database_dict = {}
    lststructure = []
    lstnamefile = []
    for filepath in glob.iglob(directory + '*.cif'):
        try:
            structure = Structure.from_file(filepath)
            lststructure.append(structure)
            lstnamefile.append(filepath)
        except:
            print (filepath)
            continue
    database_dict= {"namefile":lstnamefile, "structure":lststructure}
    return database_dict


# In[4]:


def getMultiWeightsChemenvStrategy (struct):
        # Setup the local geometry finder
    lgf = LocalGeometryFinder()
    lgf.setup_parameters(centering_type='centroid', include_central_site_in_centroid=True)

    #you can also save the logging to a file, just remove the comment

#     logging.basicConfig(#filename='chemenv_structure_environments.log',
#                         format='%(levelname)s:%(module)s:%(funcName)s:%(message)s',
#                         level=logging.DEBUG)
    lgf.setup_structure(structure=struct)
    se = lgf.compute_structure_environments(maximum_distance_factor=1.41,only_cations=False)
    strategy = MultiWeightsChemenvStrategy.stats_article_weights_parameters()
    lse = LightStructureEnvironments.from_structure_environments(strategy=strategy, structure_environments=se)
    return lse.coordination_environments


# In[5]:


def getSimplestChemenvStrategy (struct):
        # Setup the local geometry finder
    lgf = LocalGeometryFinder()
    lgf.setup_parameters(centering_type='centroid', include_central_site_in_centroid=True)

    #you can also save the logging to a file, just remove the comment

#     logging.basicConfig(#filename='chemenv_structure_environments.log',
#                         format='%(levelname)s:%(module)s:%(funcName)s:%(message)s',
#                         level=logging.DEBUG)
    lgf.setup_structure(structure=struct)
    se = lgf.compute_structure_environments(maximum_distance_factor=1.41,only_cations=False)
    strategy = SimplestChemenvStrategy(distance_cutoff=1.4, angle_cutoff=0.3)
    lse = LightStructureEnvironments.from_structure_environments(strategy=strategy, structure_environments=se)
    return lse.coordination_environments


# In[6]:


def list_getSimplestChemenvStrategy (list_struc):
    get_list = []
    for structure in list_struc:
        try:
            get_list.append(getSimplestChemenvStrategy (structure))
        except:
            get_list.append("N/A")
            continue
    return get_list


# In[7]:


def list_getMultiWeightsChemenvStrategy (list_struc):
    get_list = []
    for structure in list_struc:
        try:
            get_list.append(getMultiWeightsChemenvStrategy (structure))
        except:
            get_list.append("N/A")
            continue
    return get_list


# In[8]:


def list_oxide_type (list_struc):
    return [ oxide_type(structure, relative_cutoff=1.2, return_nbonds=True) for structure in list_struc]
    


# In[9]:


def list_number_of_facets_with_i_vertices (list_struc):
    return [ VoronoiAnalyzer().analyze(structure, n=0) for structure in list_struc]
    


# In[10]:


def list_the_solid_angle_of_polygon_between_atomi_and_imagej_of_atomj (list_struc):
    return [ VoronoiConnectivity(structure,cutoff=10).connectivity_array for structure in list_struc]


# In[11]:


def list_Voronoi_Neighbors (list_struc):
    return [VoronoiConnectivity(structure,cutoff=10).get_connections() for structure in list_struc]


# In[12]:


def list_maximum_connectivity (list_struc):
    return [VoronoiConnectivity(structure,cutoff=10).max_connectivity for structure in list_struc]


# In[13]:


def list_contains_peroxide (list_struc):
    return [contains_peroxide(structure, relative_cutoff=1.1) for structure in list_struc]


# In[14]:


def list_dimensionality (list_struc):
    get_list = []
    for structure in list_struc:
        print(structure.formula)
        try:
            get_list.append(get_dimensionality(structure, max_hkl=2, el_radius_updates=None, min_slab_size=5, min_vacuum_size=5, standardize=True, bonds=None))
        except:
            get_list.append("N/A")
            continue
    return get_list


# In[15]:


def list_maximum_bond_length (list_struc):
    return [get_max_bond_lengths(structure, el_radius_updates=None) for structure in list_struc]


# In[16]:


def list_sulfide_type (list_struc):
    get_list = []
    for structure in list_struc:
        try:
            get_list.append(sulfide_type(structure))
        except:
            get_list.append("N/A")
            continue
    return get_list


# In[6]:


def list_formula (list_struc):
    return [structure.formula for structure in list_struc]


# In[40]:


def list_volume (list_struc):
    return [structure.volume for structure in list_struc]


# In[35]:


def list_density (list_struc):
    return [structure.density for structure in list_struc]


# In[49]:


def list_a (list_struc):
    return [structure.lattice.a for structure in list_struc]


# In[50]:


def list_b (list_struc):
    return [structure.lattice.b for structure in list_struc]


# In[51]:


def list_c (list_struc):
    return [structure.lattice.c for structure in list_struc]


# In[52]:


def list_alpha (list_struc):
    return [structure.lattice.alpha for structure in list_struc]


# In[53]:


def list_beta (list_struc):
    return [structure.lattice.beta for structure in list_struc]


# In[54]:


def list_gamma (list_struc):
    return [structure.lattice.gamma for structure in list_struc]


# In[45]:


def list_angles (list_struc):
    return [structure.lattice.angles for structure in list_struc]


# In[5]:


def list_get_crystal_system (list_struc):
    return [SpacegroupAnalyzer(structure).get_crystal_system() for structure in list_struc]


# In[13]:


def list_get_hall (list_struc):
    return [SpacegroupAnalyzer(structure).get_hall() for structure in list_struc]


# In[17]:


def list_get_ir_reciprocal_mesh (list_struc):
    return [SpacegroupAnalyzer(structure).get_ir_reciprocal_mesh() for structure in list_struc]


# In[21]:


def list_get_lattice_type (list_struc):
    return [SpacegroupAnalyzer(structure).get_lattice_type() for structure in list_struc]


# In[25]:


def list_get_space_group_number (list_struc):
    return [SpacegroupAnalyzer(structure).get_space_group_number() for structure in list_struc]


# In[85]:


def list_number_of_magnetic_sites (list_struc):
    return [CollinearMagneticStructureAnalyzer(structure).number_of_magnetic_sites for structure in list_struc]


# In[92]:


def list_number_of_unique_magnetic_sites (list_struc):
    return [CollinearMagneticStructureAnalyzer(structure).number_of_unique_magnetic_sites() for structure in list_struc]


# In[100]:


def list_types_of_magnetic_specie (list_struc):
    return [CollinearMagneticStructureAnalyzer(structure).types_of_magnetic_specie for structure in list_struc]


# In[103]:


def list_magmoms (list_struc):
    return [CollinearMagneticStructureAnalyzer(structure).magmoms for structure in list_struc]


# In[109]:


def list_ordering (list_struc):
    return [CollinearMagneticStructureAnalyzer(structure).ordering for structure in list_struc]


# In[21]:


def list_get_pattern (list_struc):
    ls = []
    for structure in list_struc:
        i = NDCalculator()
        ls.append(i.get_pattern(structure))
    return ls


# In[17]:


def list_TransformedStructure (list_struc):
    return [TransformedStructure(structure) for structure in list_struc]


# In[29]:


def list_get_pattern_xrd (list_struc):
    ls = []
    for structure in list_struc:
        i = XRDCalculator()
        ls.append(i.get_pattern(structure))
    return ls


# In[10]:


def list_Defect (list_struc):
    ls = []
    for structure in list_struc:
        i = Vacancy(structure)
        ls.append(i.bulk_structure)
    return ls
#need defect sites


# In[30]:


def get_dataframe_from_cifdir (directory):
    get_struct = read_cifformat_file (directory)
    get_lststruct = get_struct["structure"]
    get_namefile = get_struct["namefile"]
    dict_struct = {}
    dict_struct
    dict_struct["name file"] = get_namefile
    dict_struct["formula"] = list_formula(get_lststruct)
#     dict_struct["a"] = list_a(get_lststruct)
#     dict_struct["b"] = list_b(get_lststruct)
#     dict_struct["c"] = list_c(get_lststruct)
#     dict_struct["alpha"] = list_alpha(get_lststruct)
#     dict_struct["beta"] = list_beta(get_lststruct)
#     dict_struct["gamma"] = list_gamma(get_lststruct)
#     dict_struct["angles"] = list_angles(get_lststruct)
#     dict_struct["volume"] = list_volume(get_lststruct)
#     dict_struct["density"] = list_density(get_lststruct)
#     dict_struct["oxide type"] = list_oxide_type(get_lststruct)
#     dict_struct["number of facets with i vertices"] = list_number_of_facets_with_i_vertices (get_lststruct)
#     dict_struct["the solid angle of polygon between atomi and imagej of atomj"] = list_the_solid_angle_of_polygon_between_atomi_and_imagej_of_atomj (get_lststruct)
#     dict_struct["Voronoi Neighbors"] = list_Voronoi_Neighbors (get_lststruct)
#     dict_struct["maximum connectivity"] = list_maximum_connectivity (get_lststruct)
#     dict_struct["contains peroxide"] = list_contains_peroxide (get_lststruct)
#     #checking
#     dict_struct["dimensionality"] = list_dimensionality (get_lststruct)
#     dict_struct["maximum bond length"] = list_maximum_bond_length (get_lststruct)
#     dict_struct["sulfide type"] = list_sulfide_type (get_lststruct)
#     dict_struct["MultiWeights Chemenv Strategy"] = list_getMultiWeightsChemenvStrategy (get_lststruct)
#     dict_struct["Simplest Chemenv Strategy"] = list_getSimplestChemenvStrategy (get_lststruct)
#     dict_struct["Crystal System"] = list_get_crystal_system(get_lststruct)
#     dict_struct["Hall"] = list_get_hall(get_lststruct)
#     dict_struct["ir reciprocal mesh"] = list_get_ir_reciprocal_mesh(get_lststruct)
#     dict_struct["lattice type"] = list_get_lattice_type(get_lststruct)
#     dict_struct["space group number"] = list_get_space_group_number(get_lststruct)
#     dict_struct["number of magnetic sites"] = list_number_of_magnetic_sites(get_lststruct)
#     dict_struct["number of unique magnetic sites"] = list_number_of_unique_magnetic_sites(get_lststruct)
#     dict_struct["types of magnetic specie"] = list_types_of_magnetic_specie(get_lststruct)
#     dict_struct["magmoms"] = list_magmoms(get_lststruct)
#     dict_struct["ordering"] = list_ordering(get_lststruct)
#     dict_struct["diffraction pattern"] = list_get_pattern(get_lststruct)
    dict_struct["AbstractStructureFilter"] = list_TransformedStructure(get_lststruct)
    dict_struct["diffraction pattern"] = list_get_pattern(get_lststruct)
    dict_struct["diffraction pattern xrd"] = list_get_pattern_xrd(get_lststruct)
#     dick_struct["Defect"] = list_Defect(get_lststruct)
    df = pd.DataFrame.from_dict(dict_struct)
    
    
    return df

