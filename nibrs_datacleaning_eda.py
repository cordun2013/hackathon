#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 08:55:45 2017

Cleaning/EDA of NIBRS dataset. 

@author: catherineordun
"""
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


#===========================================
#NBIRS
#===========================================

#NIBRS - Incident 
#this is a huge 6GB tsv file 
# it is only for 2015
nibrs = pd.read_csv("/Users/catherineordun/Documents/Hackathon/DHHS/ICPSR_36851_incident/DS0001/36851-0001-Data.tsv", sep='\t')
#nibrs.to_csv("/Users/catherineordun/Documents/Hackathon/DHHS/nibrs.csv")

#extract only the variables we need related to drugs
nibrscodes= pd.read_csv("/Users/catherineordun/Documents/Hackathon/DHHS/nbirs_codes.csv")

#flatten to remove it as a list of lists
nibrslist = nibrscodes.values.T.flatten()

nibrs_bu = nibrs.copy()

nibrs_bu.columns.intersection(nibrslist)
nibrs_reduced = nibrs_bu[nibrs_bu.columns.intersection(nibrslist)]
#nibrs_reduced.to_csv("/Users/catherineordun/Documents/Hackathon/DHHS/nibrs_reduced_54vars.csv")

"""
ORI originating agency identifier
STATE
INCNUM
INCDAT
BH008 STATE ABBREVIATION
BH007 CITY NAME
BH010 COUNTRY DIVISION
BH011 COUNTRY REGION
BH013 CORE CITY
BH016 JUDICIAL DISTRICT
BH019 CURRENT POPULATION 1
BH020 UCR COUNTY CODE 1
BH021 MSA CODE 1
BH022 LAST POPULATION 1
BH041 MASTER FILE YEAR
BH054 FIPS COUNTY 1
BH055 FIPS COUNTY 2
BH056 FIPS COUNTY 3
BH057 FIPS COUNTY 4
BH058 FIPS COUNTY 5
V1007 INCIDENT DATE HOUR
V1008 TOTAL OFFENSE SEGMENTS
V1009 TOTAL VICTIM SEGMENTS
V1010 TOTAL OFFENDER SEGMENTS
V1011 TOTAL ARRESTEE SEGMENTS
V20061 - UCR OFFENSE CODE - 1 
V20062 - UCR OFFENSE CODE - 2
V20063 - UCR OFFENSE CODE - 3
V30121 SUSPECTED DRUG TYPE 1 - 1
V30122 SUSPECTED DRUG TYPE 1 - 2
V30123 SUSPECTED DRUG TYPE 1 -3 
V30131 ESTIMATED QUANTITY 1-1
V30132 ESTIMATED QUANTITY 1-2
V30133 ESTIMATED QUANTITY 1 -3
V30141 ESTIMATED QUANTITY - FRACTIONAL THOUSANDTHS 1 - 1
V30142 ESTIMATED QUANTITY - FRACTIONAL THOUSANDTHS 1 - 2
V30143 ESTIMATED QUANTITY - FRACTIONAL THOUSANDTHS 1 - 3
V20081 - OFFENDER(S) SUSPECTED OF USING 1 - 1
V20082 - OFFENDER(S) SUSPECTED OF USING 1-2
V20083 - OFFENDER(S)SUSPECTED OF USING 1 - 3
V20111 - LOCATION TYPE 1 
V20112 - LOCATION TYPE 2
V20113 - LOCATION TYPE 3
V20171 - TYPE WEAPON/FORCE INVOLVED 1 - 1
V20172 - TYPE WEAPON/FORCE INVOLVED 1 - 2
V20173 - TYPE WEAPON/FORCE INVOLVED 1 -3
V30061 - TYPE PROPERTY LOSS/ETC - 1
V30062 - TYPE PROPERTY LOSS/ETC - 2
V30063 - TYPE PROPERTY LOSS / ETC - 3
V30071 - PROPERTY DESCRIPTION - 1
V30072 - PROPERTY DESCRIPTION - 2
V30073 - PROPERTY DESCRIPTION - 3
V30081 - VALUE OF PROPERTY - 1
V30082 - VALUE OF PROPERTY - 2
V30083 - VALUE OF PROPERTY - 3
V5006 OFFENDER SEQUENCE NUMBER - 1
V5008 AGE OF OFFENDER - 1
V5008 SEX OF OFFENDER - 1
V5009 RACE OF OFFENDER - 1
V5011 ETHNICITY OF OFFENDER - 1
V6006 ARRESTEE SEQUENCE NUMBER - 1
V6009 ARREST DATE - 1
V6009 TYPE OF ARREST - 1
V6014 AGE OF ARRESTEE - 1
V6015 SEX OF ARRESTEE - 1
V6016 RACE OF ARRESTEE - 1
V6017 ETHNICITY OF ARRESTEE - 1
V60081 ARREST DATE - 1
ALLOFNS - ALL OFFENSE CODES FOR THE INCIDENT

"""
#pivot table of number of incidents by state, and drug    
"""
Specifically look for:
    
4 - Heroin
6 - Morphine
7 - Opium
8 - Other Narcotics
14 - Barbiturates
15 - Other Depressants

"""

nibrs_drugs = [4, 6, 7, 8, 14, 15]

#there were 4986608 records, when only looking at drugs of interest it goes down to 70133
nibrs_reduced_drugs = nibrs_reduced.loc[nibrs_reduced['V30121'].isin(nibrs_drugs)]
nibrs_stats = pd.pivot_table(nibrs_reduced_drugs,index=["BH008", "BH041","V30121"], values=["INCNUM"], 
                             aggfunc={"INCNUM": lambda x: len(x.unique())})

nibrs_stats.reset_index(inplace=True)
#2015 plot of number of criminal Group A incidents involving a V30121 SUSPECTED DRUG TYPE of Opium
(nibrs_stats.loc[(nibrs_stats["V30121"] == 7)]).plot(x='BH008', y='INCNUM', kind='bar',figsize=(20,6))
#and involving heroin
(nibrs_stats.loc[(nibrs_stats["V30121"] == 4)]).plot(x='BH008', y='INCNUM', kind='bar',figsize=(20,6))
#and other narcotics
(nibrs_stats.loc[(nibrs_stats["V30121"] == 8)]).plot(x='BH008', y='INCNUM', kind='bar',figsize=(20,6))

#seaborn to look at all data for the nibrs_drugs
nibrs_drugs_df = pd.pivot_table(nibrs_stats,index=["BH008"],values=["INCNUM"],
               columns=["V30121"],aggfunc=[np.sum])
nibrs_drugs_df.fillna(value=0, inplace=True)
nibrs_drugs_df.columns = nibrs_drugs_df.columns.droplevel()
nibrs_drugs_df.columns = nibrs_drugs_df.columns.droplevel()
nibrs_drugs_df.reset_index(inplace=True)

# Make the PairGrid
g = sns.PairGrid(nibrs_drugs_df.sort_values([8], ascending=False),
                 x_vars=nibrs_drugs_df.columns[1:7], 
                 y_vars=["BH008"],
                 size=10, aspect=.25)

# Draw a dot plot using the stripplot function
g.map(sns.stripplot, size=6, orient="h",
      palette="Reds_r", edgecolor="gray")

# Use the same x axis limits on all columns and add better labels
g.set(xlim=(0, 600), xlabel="Incidents w/Drug Involved", ylabel="")

# Use semantically meaningful titles for the columns
titles = ["4 - Heroin", "6 - Morphine", "7 - Opium",
          "8 - Other Narcotics", "14 - Barbiturates",
          "15 - Other Depressants"]

for ax, title in zip(g.axes.flat, titles):

    # Set a different title for each axes
    ax.set(title=title)

    # Make the grid horizontal instead of vertical
    ax.xaxis.grid(False)
    ax.yaxis.grid(True)

sns.despine(left=True, bottom=True)

#======
#correlation plot
#======

# Generate a mask for the upper triangle
mask = np.zeros_like(nibrs_drugs_df.corr(), dtype=np.bool)
mask[np.triu_indices_from(mask)] = True
# Set up the matplotlib figure
f, ax = plt.subplots(figsize=(11, 9))

# Generate a custom diverging colormap
cmap = sns.diverging_palette(220, 10, as_cmap=True)

# Draw the heatmap with the mask and correct aspect ratio
sns.heatmap(nibrs_drugs_df.corr(), mask=mask, cmap=cmap, vmax=.9, center=0,
            square=True, linewidths=.5, cbar_kws={"shrink": .5}, annot=True)

#======
#compared to all other drugs by state
#======

nibrs_alldrugs_stats = pd.pivot_table(nibrs_reduced,index=["BH008", "BH041","V30121"], values=["INCNUM"], 
                             aggfunc={"INCNUM": lambda x: len(x.unique())})
nibrs_alldrugs_stats.reset_index(inplace=True)


nibrs_alldrugs_df = pd.pivot_table(nibrs_alldrugs_stats,index=["BH008"],values=["INCNUM"],
               columns=["V30121"],aggfunc=[np.sum])
nibrs_alldrugs_df.fillna(value=0, inplace=True)
nibrs_alldrugs_df.columns = nibrs_alldrugs_df.columns.droplevel()
nibrs_alldrugs_df.columns = nibrs_alldrugs_df.columns.droplevel()
nibrs_alldrugs_df.reset_index(inplace=True)
nibrs_alldrugs_df.drop([-9, -8, -7, -6, 93], axis=1, inplace=True)

# Generate a mask for the upper triangle
mask = np.zeros_like(nibrs_alldrugs_df.corr(), dtype=np.bool)
mask[np.triu_indices_from(mask)] = True
# Set up the matplotlib figure
f, ax = plt.subplots(figsize=(11, 9))

# Generate a custom diverging colormap
cmap = sns.diverging_palette(220, 10, as_cmap=True)

# Draw the heatmap with the mask and correct aspect ratio
sns.heatmap(nibrs_alldrugs_df.corr(), mask=mask, cmap=cmap, vmax=.9, center=0,
            square=True, linewidths=.5, cbar_kws={"shrink": .5}, annot=True)


#===send to csv

nibrs_alldrugs_stats.to_csv("/Users/catherineordun/Documents/Hackathon/DHHS/nibrs_alldrugs_stats.csv")

nibrs_stats.to_csv("/Users/catherineordun/Documents/Hackathon/DHHS/nibrs_stats.csv")

nibrs_reduced_drugs.to_csv("/Users/catherineordun/Documents/Hackathon/DHHS/nibrs_reduced_drugs.csv")

