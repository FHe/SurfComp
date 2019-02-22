# -*- coding: utf-8 -*-
"""
Created on Thu Nov  8 15:06:19 2018

@author: DaniJ
"""

import numpy as np
from Species import Aq_Species
from Reaction import Reaction
from Database import Database
from Database_SC import Database_SC
from ChemSys import ChemSys
from ChemSys_Surf import ChemSys_Surf
from creating_databaseObject_from_text_type1 import *
from getting_Information_from_databaseSC_file_v1 import *
from getting_informationSC_input_file_v1 import *
from Read_input_file_type1 import *
# Read database
database = 'Type5_Database_JustSolution.txt'
# Instantiating database
names_aqueous_primary_species, names_aqueous_secondary_species, Aq_Species_list_pri, Aq_Species_list_sec, Aq_Reaction_list = creating_databaseObject_from_text_type1 (database)


D = Database()
D.set_names_aq_primary_species(names_aqueous_primary_species)
D.set_aq_list_pri_class(Aq_Species_list_pri)
D.set_names_aq_secondary_species (names_aqueous_secondary_species)
D.set_aq_list_sec_class( Aq_Species_list_sec)
D.set_aq_reactions_list(Aq_Reaction_list)


# Check S
D.create_log_k_vector()
D.create_charge_vector()
D.create_S()

#print(D.log_k_vector == [14.0, 10.329, 2.98, 3.224, 11.399, 11.435, 16.681, -12.78, -11.44])


#
#
# Reading input
infile = 'Type5_Input_JustSolution.txt'
# Instantiating input
list_prim, list_val = Read_input_file_type1 (infile)
C = ChemSys( list_prim, list_val, D)
C.calculate_U_f1()



c = C.speciation_noactivitycoefficient(tolerance = 1e-12)

c2 = C.speciation_noactivitycoefficient_Westall1980(tolerance = 1e-12)

#C.print_speciation()

print(c)
print(c2)


#######################################   FROM HERE STARTS THE SORPTION PART ##########################################################################################
# Westall 1980
# Read database
database_file = 'Type5_Database_SC_Westall1980_CCMexample.txt'
# Instantiating database
n_aq_sp_pri, n_aq_sp_sec, n_sorpt_sp_pri, n_sorpt_sp_sec, Aq_sp_list_pri, Aq_sp_list_sec, Sorp_sp_list_pri, Sorp_sp_list_sec, Aq_list_react, Sorp_list_react = getting_Information_from_databaseSC_file_v1 (database_file)


DS = Database_SC()
DS.set_names_aq_primary_species ( n_aq_sp_pri)
DS.set_names_aq_secondary_species ( n_aq_sp_sec)
DS.set_names_sorpt_primary_species (n_sorpt_sp_pri)
DS.set_names_sorpt_secondary_species (n_sorpt_sp_sec)
DS.set_aq_list_pri_class (Aq_sp_list_pri)
DS.set_aq_list_sec_class (Aq_sp_list_sec)
DS.set_sorpt_list_pri_class (Sorp_sp_list_pri)
DS.set_sorpt_list_sec_class (Sorp_sp_list_sec)
DS.set_aq_reactions_list (Aq_list_react)
DS.set_sorpt_reactions_list (Sorp_list_react)

# Reading input
infile = 'Type5_Input_SC_CCM_Westall1980_CCMexample.txt'
# Instantiating input
list_aq_component, list_aq_value, names_pri_sorpt, list_sorption_comp  = getting_informationSC_input_file_v1 (infile)

#
CS = ChemSys_Surf()
CS.define_system_from_input_and_database ( DS, list_aq_component, list_aq_value, names_pri_sorpt, List_pri_sorpt_class = list_sorption_comp)


CS.create_U()
#print(CS.U)


######################################################################################################################################################################
#Applying alorithm

# Read database
database_file = 'Type5_Database_SC.txt'
# Instantiating database
n_aq_sp_pri, n_aq_sp_sec, n_sorpt_sp_pri, n_sorpt_sp_sec, Aq_sp_list_pri, Aq_sp_list_sec, Sorp_sp_list_pri, Sorp_sp_list_sec, Aq_list_react, Sorp_list_react = getting_Information_from_databaseSC_file_v1 (database_file)
#
DS = Database_SC()
DS.set_names_aq_primary_species ( n_aq_sp_pri)
DS.set_names_aq_secondary_species ( n_aq_sp_sec)
DS.set_names_sorpt_primary_species (n_sorpt_sp_pri)
DS.set_names_sorpt_secondary_species (n_sorpt_sp_sec)
DS.set_aq_list_pri_class (Aq_sp_list_pri)
DS.set_aq_list_sec_class (Aq_sp_list_sec)
DS.set_sorpt_list_pri_class (Sorp_sp_list_pri)
DS.set_sorpt_list_sec_class (Sorp_sp_list_sec)
DS.set_aq_reactions_list (Aq_list_react)
DS.set_sorpt_reactions_list (Sorp_list_react)

DS.create_pseudo_S()

#print(DS.pseudoS)
# In this case, unless change on the database, this matrix should be the Pseudo S matrix of the database clase.
DSPseudoS = np.array([[1, 0, 0,  0,  0,  1,  0,  0,  0,  0,  0,  0,  0,  0,  0], [0,  0, -1,  0,  0, -1,  1,  0,  0,  0,  0,  0,  0,  0,  0], [-3,  0,  0, -1,  0,  0,  0,  1,  0,  0,  0,  0,  0,  0,  0], [-1,  0,  0, -1,  0,  0,  0,  0,  1,  0,  0,  0,  0,  0,  0], \
                    [-2,  0,  0, -1,  0,  0,  0,  0,  0,  1,  0,  0,  0,  0,  0], [-1,  0,  0,  0, -1,  0,  0,  0,  0,  0,  1,  0,  0,  0,  0], [1,  0,  0,  0, -1,  0,  0,  0,  0,  0,  0,  1,  0,  0,  0], \
                    [-2,  0,  0, -1, -1,  1,  0,  0,  0, 0,  0,  0,  1,  0,  0], [-1,  0,  0, -1, -1,  1,  0,  0,  0,  0,  0, 0,  0,  1,  0], [0, 0,  0, -1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]])

print(np.array_equal(DS.pseudoS, DSPseudoS))



# Reading input
infile = 'Type5_Input_SC_CCM.txt'
# Instantiating input
list_aq_component, list_aq_value, names_pri_sorpt, list_sorption_comp  = getting_informationSC_input_file_v1 (infile)

#
CS = ChemSys_Surf()
CS.define_system_from_input_and_database ( DS, list_aq_component, list_aq_value, names_pri_sorpt, List_pri_sorpt_class = list_sorption_comp)
CS.create_pseudo_S()
#print(CS.pseudoS) 


# In this case, unless change on the database, this matrix should be the Pseudo S matrix of the database clase.
CSPseudoS = np.array([[1, 0, 0,  1,  0,  0,  0,  0,  0,  0,  0,  0], [-3, -1,  0,  0,  1,  0,  0,  0,  0,  0,  0,  0], [-1,  -1,  0,  0,  0,   1,  0,  0,  0,  0,  0,  0], \
                    [-2, -1,  0,  0,  0,  0,  1,  0,  0,  0,  0,  0], [-1, 0, -1,  0,  0,  0,  0,   1,  0,  0,  0,  0], [1,  0, -1,  0,  0,  0,  0,  0,  1,  0,  0,  0], \
                    [-2, -1, -1,  1,  0,  0,  0, 0,  0,   1,  0,  0], [-1, -1, -1,  1,  0,  0,  0,  0,  0, 0,   1,  0], [0, -1, -1, 0, 0, 0, 0, 0, 0, 0, 0,  1]])

print(np.array_equal(CS.pseudoS, CSPseudoS))


CS.create_S ()
#print(CS.S) 

CS_S = np.array([[1, 0, 0, 0, 1,  0,  0,  0,  0,  0,  0,  0,  0], [-3, -1,  0, 0, 0,  1,  0,  0,  0,  0,  0,  0,  0], [-1,  -1,  0,  0, 0,  0,   1,  0,  0,  0,  0,  0,  0], \
                    [-2, -1,  0, 0, 0,  0,  0,  1,  0,  0,  0,  0,  0], [-1, 0, -1, -1, 0,  0,  0,  0,   1,  0,  0,  0,  0], [1,  0, -1, 1, 0,  0,  0,  0,  0,  1,  0,  0,  0], \
                    [-2, -1, -1,  0, 1,  0,  0,  0, 0,  0,   1,  0,  0], [-1, -1, -1, 1,  1,  0,  0,  0,  0,  0, 0,   1,  0], [0, -1, -1, 3,  0, 0, 0, 0, 0, 0, 0, 0,  1]])

print(np.array_equal(CS.S, CS_S))


CS.create_U ()
print(CS.U)
CS.create_log_k_vector()

        #if type_I == 5:
            # Case example 5
            # c_ = [H+, AsO4-3, SurfOH, Boltzman_SurfOH, OH-, H3AsO4, HAsO4-2, H2AsO4-, SurfOH2+, SurfO-, SurfH2AsO4, SurfHAsO4-, SurfOHAsO4-3]
#c_guess = np.array([7.864e-09, 2.626e-28, 5.373e-02, 9.975e-01, 1.315e-06, 5.634e-32, 6.126e-25, 4.211e-26, 8.133e-03, 8.133e-03, 1.219e-10, 2.488e-08, 4.910e-19])
c_guess = np.array([7.864e-09, 2.626e-28, 5.373e-02, 2.459e-07, 1.315e-06, 5.634e-32, 6.126e-25, 4.211e-26, 8.133e-03, 8.133e-03, 1.219e-10, 2.488e-08, 4.910e-19])
CS.speciation_Westall1980_CCM (c_guess = c_guess)
CS.print_speciation()

####################################
# Read database
database_file = 'Type5_Database_SC_try2.txt'
# Instantiating database
n_aq_sp_pri, n_aq_sp_sec, n_sorpt_sp_pri, n_sorpt_sp_sec, Aq_sp_list_pri, Aq_sp_list_sec, Sorp_sp_list_pri, Sorp_sp_list_sec, Aq_list_react, Sorp_list_react = getting_Information_from_databaseSC_file_v1 (database_file)
#
DS2 = Database_SC()
DS2.set_names_aq_primary_species ( n_aq_sp_pri)
DS2.set_names_aq_secondary_species ( n_aq_sp_sec)
DS2.set_names_sorpt_primary_species (n_sorpt_sp_pri)
DS2.set_names_sorpt_secondary_species (n_sorpt_sp_sec)
DS2.set_aq_list_pri_class (Aq_sp_list_pri)
DS2.set_aq_list_sec_class (Aq_sp_list_sec)
DS2.set_sorpt_list_pri_class (Sorp_sp_list_pri)
DS2.set_sorpt_list_sec_class (Sorp_sp_list_sec)
DS2.set_aq_reactions_list (Aq_list_react)
DS2.set_sorpt_reactions_list (Sorp_list_react)
# Reading input
infile = 'Type5_Input_SC_TLM_try2.txt'
# Instantiating input
list_aq_component, list_aq_value, names_pri_sorpt, list_sorption_comp  = getting_informationSC_input_file_v1 (infile)
CS1 = ChemSys_Surf()
CS1.define_system_from_input_and_database ( DS2, list_aq_component, list_aq_value, names_pri_sorpt, List_pri_sorpt_class = list_sorption_comp)
CS1.create_pseudo_S()
CS1.create_S ()
CS1_S = np.array([[ 1.,  0.,  0.,  0.,  0.,  0.,  1.,  0.,  0.,  0.,  0.,  0.,  0., 0.,  0.], [-3., -1.,  0.,  0.,  0.,  0.,  0.,  1.,  0.,  0.,  0.,  0.,  0.,0.,  0.], [-1., -1.,  0.,  0.,  0.,  0.,  0.,  0.,  1.,  0.,  0.,  0.,  0., 0.,  0.], \
                    [-2., -1.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  1.,  0.,  0.,  0., 0.,  0.], [-1.,  0., -1., -1.,  0.,  0.,  0.,  0.,  0.,  0.,  1.,  0.,  0., 0.,  0.], [1.,  0., -1.,  1.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  1.,  0., 0.,  0], \
                    [-2., -1., -1., -3.,  3.,  0.,  1.,  0.,  0.,  0.,  0.,  0.,  1., 0.,  0.], [-1., -1., -1., -2.,  3.,  0.,  1.,  0.,  0.,  0.,  0.,  0.,  0., 1.,  0.], [0., -1., -1.,  0.,  3.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,0.,  1]])

print(np.array_equal(CS1.S, CS1_S))


CS1.create_U ()
CS1.create_log_k_vector()
# c_ = ['H+', 'Na+', 'Cl-', 'SOH', 'SOH_Boltzf_psi_0', 'SOH_Boltzf_psi_beta', 'SOH_Boltzf_psi_diffuselayer', 'OH-', 'SOH2+', 'SO-', 'SOH2Cl', 'SONa']
c_guess = np.array([1.602e-08, 7.412e-24, 2.503e-05, 5.371e-02, 4.872e-01, 4.902e-01 , 6.325e-01, 6.366e-07, 8.143e-03, 8.117e-03, 8.945e-35, 2.500e-05])
#CS1.set_constant_ionic_strength (7.293e-06)
CS1.speciation_Westall1980_TLM (tolerance = 1e-6, max_iterations = 100, c_guess = c_guess)
CS1.print_speciation()




##################################

# Reading input
infile = 'Type5_Input_SC_TLM.txt'
# Instantiating input
list_aq_component, list_aq_value, names_pri_sorpt, list_sorption_comp  = getting_informationSC_input_file_v1 (infile)
CS1 = ChemSys_Surf()
CS1.define_system_from_input_and_database ( DS, list_aq_component, list_aq_value, names_pri_sorpt, List_pri_sorpt_class = list_sorption_comp)
CS1.create_pseudo_S()
CS1.create_S ()
CS1_S = np.array([[ 1.,  0.,  0.,  0.,  0.,  0.,  1.,  0.,  0.,  0.,  0.,  0.,  0., 0.,  0.], [-3., -1.,  0.,  0.,  0.,  0.,  0.,  1.,  0.,  0.,  0.,  0.,  0.,0.,  0.], [-1., -1.,  0.,  0.,  0.,  0.,  0.,  0.,  1.,  0.,  0.,  0.,  0., 0.,  0.], \
                    [-2., -1.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  1.,  0.,  0.,  0., 0.,  0.], [-1.,  0., -1., -1.,  0.,  0.,  0.,  0.,  0.,  0.,  1.,  0.,  0., 0.,  0.], [1.,  0., -1.,  1.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  1.,  0., 0.,  0], \
                    [-2., -1., -1., -3.,  3.,  0.,  1.,  0.,  0.,  0.,  0.,  0.,  1., 0.,  0.], [-1., -1., -1., -2.,  3.,  0.,  1.,  0.,  0.,  0.,  0.,  0.,  0., 1.,  0.], [0., -1., -1.,  0.,  3.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,0.,  1]])

print(np.array_equal(CS1.S, CS1_S))


CS1.create_U ()
CS1.create_log_k_vector()
# c_ = [H+, AsO4-3, SurfOH, Boltzman_SurfOH_0, Boltzmann_SurfOH_b, Boltzman_Surf_D, OH-, H3AsO4, HAsO4-2, H2AsO4-, SurfOH2+, SurfO-, SurfH2AsO4, SurfHAsO4-, SurfOHAsO4-3]
c_guess = np.array([8.727e-09, 1.404e-28, 5.373e-02, 0.8903, 9.008e-01, 9.107e-01, 1.162e-06, 9.293e-34,1.225e-24, 7.706e-27, 5.925e-04, 5.789e-04, 2.025e-09, 2.298e-08, 5.638e-17])
#CS1.set_constant_ionic_strength (7.293e-06)
CS1.speciation_Westall1980_TLM (tolerance = 1e-6, max_iterations = 100, c_guess = c_guess)
CS1.print_speciation()
