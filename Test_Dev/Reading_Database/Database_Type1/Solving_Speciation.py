# -*- coding: utf-8 -*-
"""
Created on Wed Aug  1 10:25:11 2018

@author: DaniJ
"""
from Species import Aq_Species
from Reaction import Reaction
from Database import Database
from creating_databaseObject_from_text_type1 import *
# Read database
database = 'Type1_Database.txt'
infile = 'Type1_Input.txt'
# Instantiating database
Species_list, Reaction_list, primary_species_list, secondary_species_list = creating_databaseObject_from_text_type1 (database)

D = Database()
D.set_species_list(Species_list)
D.set_reaction_list(Reaction_list)
D.set_primary_species(primary_species_list)
D.set_secondary_species(secondary_species_list)

# Check S
D.create_log_k_vector()
D.create_charge_vector()
D.create_S()

#print(D.log_k_vector == [14.0, 10.329, 2.98, 3.224, 11.399, 11.435, 16.681, -12.78, -11.44])


#
#
# Reading input

# Instantiating input


# Calculating Speciation

# Pre-processing Results