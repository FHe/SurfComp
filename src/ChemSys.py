# -*- coding: utf-8 -*-
"""
Created on Wed Aug  1 11:08:12 2018

@author: Lützenkirchen, Heberling, Jara
"""

class ChemSys:
    # Constructor
    def __init__(self, list_prim, list_val, DatabaseC):
        '''
            list_prim = ['Cl-', 'H2O', 'H+']        It is supossed to be the primary species in the system, it should be in accordance with the database.
            
            list_val  = [5 4 20]                    It is supposed to be the concentration values of the primary species stated in list_prim, namely Cl- = 5. So far units are mol/L          
        
            DatabaseC                               It is supposed to be the database that is going to be used in order to built the stochiometric matrix of these system, and the pertinant secondary species, log_k values, etc
            
            precondition: The DatabaseC class should have run the create_S or check_consistency_species, previously. Otherwise, The method will fail.
        '''
        DatabaseC.check_consistency_species()       # This method is run to assure that what is written below this line has sense.
        # Getting index of list_prim in the database
        indices_ps = self.Index_InputPrimaryspeciesinDatabase ( list_prim, DatabaseC.name_primary_species)
        # Sorting list_prim and list_val according to the indices, AFTER THIS STEP THE LIST BECOMES TUPLE !!!!!!!!!!!
        indices_ps, list_prim, list_val = zip(*sorted(zip(indices_ps, list_prim, list_val)))
        # name_prymary_species is like list_prim but order following the order of the Database
        self.name_primary_species = list(list_prim)                        
        # It is the list of species = [Species1, Species2, Species3] related to name_primary_species
        self.list_species = [DatabaseC.list_species[i] for i in indices_ps]
        # Check which Reactions in the database occur in the ChemSys --> from there the secondary species will be obtained.
        indices_r_inDatabase, self.name_secondary_species = self.Index_reactionsinDatabase ( DatabaseC.list_reactions, DatabaseC.n_reactions)
        # Add secondary species in the list of species
        self.Add_secondary_species (DatabaseC)
        # Get the list of reactions from the Database
        self.list_reactions = [DatabaseC.list_reactions[i] for i in indices_r_inDatabase]
        
    # Setters
    
    # Initializations functions
    # Searching
    # Returns the indice of the chemical species in the database
    def Index_InputPrimaryspeciesinDatabase (self, list1, list2):
        '''
            The function returns a list of indices of the position of list1 in list2. --> E.g. list1 =[a c], list2 = [a b c d] function returns listindices = [1,3]
            Precondition1: list1 <= list2
            Precondition2: list1 is completely include in list2. Otherwise an error occurs
        '''
        assert len(list1) <= len(list2), "List of species in the chemical system must be equal or smaller than the list os primary species on the database"
        list_indices = []  
        for i in list1:
            # appends the index of the list2 that coincide with list1.
            list_indices.append(list2.index(i))
        return list_indices
    
    # Returns the index of the reactions that can occur according to the database
    def Index_reactionsinDatabase (self, l_dic_react, len_l_dic_react):
        '''
            The function returns two list. One with the indices of the reactions that occur in the ChemSys according to the inputed Database, and the other the secondary species in each reaction. 
            Both, list are in agremment. e.g. l_ind_reaction = [0, 4, 6, 9], l_secondary_species = ['A' 'B' 'C' 'F']  From reaction 0 of the database the secondary species obtained is A, from 6 is C, and so on.
        '''
        list_indices_r=[]
        list_secondary_species_r=[]
        for i in range(0, len_l_dic_react):
            temp_d_r = l_dic_react[i].reaction
            list_temp_d_r = list(temp_d_r.keys())
            n_s = 0
            for d in list_temp_d_r:
                c = self.name_primary_species.count(d)
                if c != 1 and c!= 0:
                    raise ValueError('[ChemSys class, method Index_ReactionsinDatabase] It seems that the name_primary_species property is wrong.')
                elif c == 0:
                    n_s += 1
                    n_s_name = d
            if n_s == 1:
                list_indices_r.append(i)
                list_secondary_species_r.append(n_s_name)       
        return list_indices_r, list_secondary_species_r
    
    # Adds secondary species
    def Add_secondary_species (self, DatabaseC):
        '''
            Adds the secondary species in the list of species
        '''
        l = DatabaseC.name_primary_species + DatabaseC.name_secondary_species
        for i in self.name_secondary_species:
            pos = l.index(i)
            self.list_species.append(DatabaseC.list_species[pos])
            
    # Calculations
        
        
        
        
        
        
        
        
        
    