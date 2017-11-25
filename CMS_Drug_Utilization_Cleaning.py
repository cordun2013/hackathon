#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 25 17:25:07 2017

@author: catherineordun
"""


import numpy as np
import pandas as pd
from datetime import datetime
import timestring
import seaborn as sns



"""
Datasets are: 
    CMS State Drug Utilization Data 2017
    
    CMS State Drug Utilization Data 2016
        Ref for product codes: 
            https://data.medicaid.gov/State-Drug-Utilization/State-Drug-Utilization-Data-2016/3v6v-qk5s
    About CMS Product Codes: 
            Labeler Code: First segment of NDC that identifies the manufacturer, labeler, relabeler, packager, repackager or distributor of the drug.
            Product Code: Second segment of NDC.
            Package Size Code: Third segment of NDC. 

"""


#===============CMS ========================
#===========================================

"""
Brand Name Opioid Prescriptions:
    
For this dataset, you need to look up and filter down the opioid-related drugs. If you do this through
the Product Name, I used this set of opioid Rx drugs: 
Abstral (fentanyl)
Actiq (fentanyl)
Avinza (morphine sulfate extended-release capsules)
Butrans (buprenorphine transdermal system)
Demerol (meperidine [also known as isonipecaine or pethidine])
Dilaudid (hydromorphone [also known as dihydromorphinone])
Dolophine (methadone hydrochloride tablets)
Duragesic (fentanyl transdermal system)
Fentora (fentanyl)
Hysingla (hydrocodone)
Methadose (methadone)
Morphabond (morphine)
Nucynta ER (tapentadol extended-release oral tablets)
Onsolis (fentanyl)
Oramorph (morphine)
Oxaydo (oxycodone)
Roxanol-T (morphine)
Sublimaze (fentanyl)
Xtampza ER (oxycodone)
Zohydro ER (hydrocodone)

Combination Opioid Prescriptions:

Anexsia (hydrocodone containing acetaminophen)
Co-Gesic (hydrocodone containing acetaminophen)
Embeda (morphine sulfate and naltrexone extended-release capsules)
Exalgo (hydromorphone hydrochloride extended-release tablets)
Hycet (hydrocodone containing acetaminophen)
Hycodan (hydrocodone containing homatropine)
Hydromet (hydrocodone containing homatropine)
Ibudone (hydrocodone containing ibuprofen)
Kadian (morphine sulfate extended-release tablets)
Liquicet (hydrocodone containing acetaminophen)
Lorcet (hydrocodone containing acetaminophen)
Lorcet Plus (hydrocodone containing acetaminophen)
Lortab (hydrocodone containing acetaminophen)
Maxidone (hydrocodone containing acetaminophen)
MS Contin (morphine sulfate controlled-release tablets)
Norco (hydrocodone containing acetaminophen)
Opana ER (oxymorphone hydrochloride extended-release tablets)
OxyContin (oxycodone hydrochloride controlled-release tablets)
Oxycet (oxycodone containing acetaminophen)
Palladone (hydromorphone hydrochloride extended-release capsules)
Percocet (oxycodone containing acetaminophen)
Percodan (oxycodone containing aspirin)
Reprexain (hydrocodone containing ibuprofen)
Rezira (hydrocodone containing pseudoephedrine)
Roxicet (oxycodone containing acetaminophen)
Targiniq ER (oxycodone containing naloxone)
TussiCaps (hydrocodone containing chlorpheniramine)
Tussionex (hydrocodone containing chlorpheniramine)
Tuzistra XR (codeine containing chlorpheniramine)
Tylenol #3 and #4 (codeine containing acetaminophen)
Vicodin (hydrocodone containing acetaminophen)
Vicodin ES (hydrocodone containing acetaminophen)
Vicodin HP (hydrocodone containing acetaminophen)
Vicoprofen (hydrocodone containing ibuprofen)
Vituz (hydrocodone containing chlorpheniramine)
Xartemis XR (oxycodone containing acetaminophen)
Xodol (hydrocodone containing acetaminophen)
Zolvit (hydrocodone containing acetaminophen)
Zutripro (hydrocodone containing chlorpheniramine and pseudoephedrine)
Zydone (hydrocodone containing acetaminophen)

Generic: 

Fentanyl (fentanyl extended-release transdermal system)
Methadone hydrochloride (methadone hydrochloride tablets, methadone hydrochloride oral solution)
Morphine sulfate (morphine sulfate extended-release capsules, morphine sulfate extended-release tablets)
Oxymorphone hydrochloride (oxymorphone hydrochloride extended-release tablets)

REFERENCE: http://www.rehabcenter.net/list-opioids-united-states/

"""

#CMS
cms_2017 = pd.read_csv("/Users/catherineordun/Documents/Hackathon/DHHS/ready_data/State_Drug_Utilization_Data_2017.csv")
print(cms_2017.shape) #(2343727, 20)
cms_2017.dtypes
"""
cms_2017.dtypes
Out[4]: 
Utilization Type                   object
State                              object
Labeler Code                        int64
Product Code                        int64
Package Size                        int64
Year                                int64
Quarter                             int64
Product Name                       object
Suppression Used                     bool
Units Reimbursed                  float64
Number of Prescriptions           float64
Total Amount Reimbursed           float64
Medicaid Amount Reimbursed        float64
Non Medicaid Amount Reimbursed    float64
Quarter Begin                      object
Quarter Begin Date                 object
Latitude                          float64
Longitude                         float64
Location                           object
NDC                                 int64
dtype: object
"""
cms_2017.rename(columns={
        'Labeler Code':'label_code',
        'Product Code':'product_code',
        'Package Size':'package_size',
        'Product Name':'product_name',
        'Suppression Used':'suppression',
        'Units Reimbursed':'units_reimb',
        'Number of Prescriptions':'num_rx',
        'Total Amount Reimbursed':'total_amt_reimb',
        'Medicaid Amount Reimbursed':'med_amt_reimb',
        'Non Medicaid Amount Reimbursed':'nonmed_amt_reimb',
        'Quarter Begin':'qtr_begin', 
        'Quarter Begin Date':'qtr_begin_date'},inplace=True)


cms_2017.loc[(cms_2017["product_name"] == "ABSTRAL")]

""""
#You'll notice here that the Labeler Code + Product Code is equal to in the
nda_product file the following: 
    
PRODUCTNDC: 57881-332	

In order to determine the packagem dosage, and manufacturer, you need to merge together the product 
and package files from the NDA at FDA. 
"""
nda_product = pd.read_csv("/Users/catherineordun/Documents/Hackathon/DHHS/nda_product.csv")

#1. Now, we need to extract out from the cms_2017 file, all the drugs that are opioid drugs 
#2. Create a new field called PRODUCTNDC
#3. And merge with nda_product to get the dosage and manufacturer name
#4. Convert the 'STARTMARKETINGDATE' from float -> datetime

druglist= pd.read_csv("/Users/catherineordun/Documents/Hackathon/DHHS/druglist.csv")

#flatten to remove it as a list of lists
searchlist = druglist.values.T.flatten()

#capitalize all drug names in searchlist b/c the product_name is all capitalized
cap_searchlist = [element.upper() for element in searchlist]


#make sure all the product_names are capitalized in the dataframe so we get everything 
cms_2017['product_name'] = map(lambda x: str(x).upper(), cms_2017['product_name'])

#now search through to find a match
cms_2017_opioids = cms_2017.query('product_name in @cap_searchlist')
print(cms_2017_opioids['product_name'].nunique()) #33
print(len(searchlist)) #64
#About half of the searchlist is in the cms_2017

#make a new column called 'PRODUCTNDC'
cms_2017_opioids['PRODUCTNDC'] = cms_2017_opioids['label_code'].astype(str) + '-' +cms_2017_opioids['product_code'].astype(str)

#check it's right
cms_2017_opioids.loc[(cms_2017_opioids["product_name"] == "ABSTRAL")] #ok it works
nda_product.loc[(nda_product["PRODUCTNDC"] == "409-1201")] #there are products in CMS that aren't in the NDA products
#for example, the above 409-1201 is demerol and demerol is not in the nda PRODUCTS table
cms_2017_opioids.loc[(cms_2017_opioids["PRODUCTNDC"] == "409-1201")] #ok it works

#MERGE WITH NDA PRODUCT DF
cms_2017_opioids_fin = pd.merge(cms_2017_opioids, nda_product, on='PRODUCTNDC', how='left')
#how many are missing
cms_2017_opioids_fin['PRODUCTID'].isnull().sum() #1840
len(cms_2017_opioids_fin) #5265 total records

"""
cms_2017_opioids_fin.dtypes
Out[115]: 
Utilization Type              object
State                         object
label_code                     int64
product_code                   int64
package_size                   int64
Year                           int64
Quarter                        int64
product_name                  object
suppression                     bool
units_reimb                  float64
num_rx                       float64
total_amt_reimb              float64
med_amt_reimb                float64
nonmed_amt_reimb             float64
qtr_begin                     object
qtr_begin_date                object
Latitude                     float64
Longitude                    float64
Location                      object
NDC                            int64
PRODUCTNDC                    object
PRODUCTID                     object
PRODUCTTYPENAME               object
PROPRIETARYNAME               object
PROPRIETARYNAMESUFFIX         object
NONPROPRIETARYNAME            object
DOSAGEFORMNAME                object
ROUTENAME                     object
STARTMARKETINGDATE           float64
ENDMARKETINGDATE             float64
MARKETINGCATEGORYNAME         object
APPLICATIONNUMBER             object
LABELERNAME                   object
SUBSTANCENAME                 object
ACTIVE_NUMERATOR_STRENGTH     object
ACTIVE_INGRED_UNIT            object
PHARM_CLASSES                 object
DEASCHEDULE                   object
dtype: object
"""

#convert startmarketingdate and endmarketingdate to datetime
#startdate
cms_2017_opioids_fin['STARTMARKETINGDATE'].fillna(value=0, inplace=True)
cms_2017_opioids_fin['STARTMARKETINGDATE'] = map(lambda x: int(x), cms_2017_opioids_fin['STARTMARKETINGDATE'])
cms_2017_opioids_fin['STARTMARKETINGDATE'] = cms_2017_opioids_fin['STARTMARKETINGDATE'].apply(str)
cms_2017_opioids_fin['startdate'] = map(lambda x: x[0:4] + "-" + x[4:6] + "-" + x[6:], cms_2017_opioids_fin['STARTMARKETINGDATE'])
cms_2017_opioids_fin['startdate'].replace(to_replace='0--', value='1970-01-01', inplace=True)
cms_2017_opioids_fin['startdate'] = pd.to_datetime(cms_2017_opioids_fin['startdate'], format='%Y-%m-%d')

#enddate
cms_2017_opioids_fin['ENDMARKETINGDATE'].fillna(value=0, inplace=True)
cms_2017_opioids_fin['ENDMARKETINGDATE'] = map(lambda x: int(x), cms_2017_opioids_fin['ENDMARKETINGDATE'])
cms_2017_opioids_fin['ENDMARKETINGDATE'] = cms_2017_opioids_fin['ENDMARKETINGDATE'].apply(str)
cms_2017_opioids_fin['enddate'] = map(lambda x: x[0:4] + "-" + x[4:6] + "-" + x[6:], cms_2017_opioids_fin['ENDMARKETINGDATE'])
cms_2017_opioids_fin['enddate'].replace(to_replace='0--', value='1970-01-01', inplace=True)
cms_2017_opioids_fin['enddate'] = pd.to_datetime(cms_2017_opioids_fin['enddate'], format='%Y-%m-%d')
#send to csv
#cms_2017_opioids_fin.to_csv("/Users/catherineordun/Documents/Hackathon/DHHS/final_datasets/cms_2017_opioids_fin.csv")

#Pivot Table with Key STats
cms17_stats = pd.pivot_table(cms_2017_opioids_fin,index=["State", "Quarter", "product_name", "DOSAGEFORMNAME", "LABELERNAME", "ROUTENAME", "DEASCHEDULE"], 
                                values=['units_reimb', 'num_rx', 'total_amt_reimb', 
                                        'med_amt_reimb', 'nonmed_amt_reimb'], 
               aggfunc={'units_reimb': lambda x: x.sum(), 
                        'num_rx': lambda x: x.sum(), 
                        'total_amt_reimb': lambda x: x.sum(),
                        'med_amt_reimb': lambda x: x.sum(),
                        'nonmed_amt_reimb':lambda x: x.sum()})

cms17_stats_fin = cms17_stats.reset_index()
cms17_stats_fin.rename(columns={'units_reimb': 'units_reimb_sum', 
                                'num_rx':'num_rx_sum', 
                                'total_amt_reimb':'total_amt_reimb_sum',
                                'med_amt_reimb':'med_amt_reimb_sum',
                                'nonmed_amt_reimb':'nonmed_amt_reimb_sum'}, inplace=True)
#cms17_stats_fin.to_csv("/Users/catherineordun/Documents/Hackathon/DHHS/cms17_stats_fin.csv")


#=====CMS 2016

cms_2016 = pd.read_csv("/Users/catherineordun/Documents/Hackathon/DHHS/ready_data/State_Drug_Utilization_Data_2016.csv")
print(cms_2016.shape) #(4625479, 20)
cms_2016.dtypes
"""
cms_2016.dtypes
Out[7]: 
Utilization Type                   object
State                              object
Labeler Code                        int64
Product Code                        int64
Package Size                        int64
Year                                int64
Quarter                             int64
Product Name                       object
Suppression Used                     bool
Units Reimbursed                  float64
Number of Prescriptions           float64
Total Amount Reimbursed           float64
Medicaid Amount Reimbursed        float64
Non Medicaid Amount Reimbursed    float64
Quarter Begin                      object
Quarter Begin Date                 object
Latitude                          float64
Longitude                         float64
Location                           object
NDC                                 int64
dtype: object

"""
cms_2016.rename(columns={
        'Labeler Code':'label_code',
        'Product Code':'product_code',
        'Package Size':'package_size',
        'Product Name':'product_name',
        'Suppression Used':'suppression',
        'Units Reimbursed':'units_reimb',
        'Number of Prescriptions':'num_rx',
        'Total Amount Reimbursed':'total_amt_reimb',
        'Medicaid Amount Reimbursed':'med_amt_reimb',
        'Non Medicaid Amount Reimbursed':'nonmed_amt_reimb',
        'Quarter Begin':'qtr_begin', 
        'Quarter Begin Date':'qtr_begin_date'},inplace=True)

    #make sure all the product_names are capitalized in the dataframe so we get everything 
cms_2016['product_name'] = map(lambda x: str(x).upper(), cms_2016['product_name'])

#now search through to find a match
cms_2016_opioids = cms_2016.query('product_name in @cap_searchlist')
print(cms_2016_opioids['product_name'].nunique()) #33

#make a new column called 'PRODUCTNDC'
cms_2016_opioids['PRODUCTNDC'] = cms_2016_opioids['label_code'].astype(str) + '-' +cms_2016_opioids['product_code'].astype(str)

#check it's right
cms_2016_opioids.loc[(cms_2016_opioids["product_name"] == "ABSTRAL")] #ok it works
#MERGE WITH NDA PRODUCT DF
cms_2016_opioids_fin = pd.merge(cms_2016_opioids, nda_product, on='PRODUCTNDC', how='left')
len(cms_2016_opioids_fin) #11287
cms_2016_opioids_fin['PRODUCTID'].isnull().sum() #4039

#convert startmarketingdate and endmarketingdate to datetime
#startdate
cms_2016_opioids_fin['STARTMARKETINGDATE'].fillna(value=0, inplace=True)
cms_2016_opioids_fin['STARTMARKETINGDATE'] = map(lambda x: int(x), cms_2016_opioids_fin['STARTMARKETINGDATE'])
cms_2016_opioids_fin['STARTMARKETINGDATE'] = cms_2016_opioids_fin['STARTMARKETINGDATE'].apply(str)
cms_2016_opioids_fin['startdate'] = map(lambda x: x[0:4] + "-" + x[4:6] + "-" + x[6:], cms_2016_opioids_fin['STARTMARKETINGDATE'])
cms_2016_opioids_fin['startdate'].replace(to_replace='0--', value='1970-01-01', inplace=True)
cms_2016_opioids_fin['startdate'] = pd.to_datetime(cms_2016_opioids_fin['startdate'], format='%Y-%m-%d')

#enddate
cms_2016_opioids_fin['ENDMARKETINGDATE'].fillna(value=0, inplace=True)
cms_2016_opioids_fin['ENDMARKETINGDATE'] = map(lambda x: int(x), cms_2016_opioids_fin['ENDMARKETINGDATE'])
cms_2016_opioids_fin['ENDMARKETINGDATE'] = cms_2016_opioids_fin['ENDMARKETINGDATE'].apply(str)
cms_2016_opioids_fin['enddate'] = map(lambda x: x[0:4] + "-" + x[4:6] + "-" + x[6:], cms_2016_opioids_fin['ENDMARKETINGDATE'])
cms_2016_opioids_fin['enddate'].replace(to_replace='0--', value='1970-01-01', inplace=True)
cms_2016_opioids_fin['enddate'] = pd.to_datetime(cms_2016_opioids_fin['enddate'], format='%Y-%m-%d')
#send to csv
#cms_2016_opioids_fin.to_csv("/Users/catherineordun/Documents/Hackathon/DHHS/final_datasets/cms_2016_opioids_fin.csv")

cms16_stats = pd.pivot_table(cms_2016_opioids_fin,index=["State", "Quarter", "product_name", "DOSAGEFORMNAME", "LABELERNAME", "ROUTENAME", "DEASCHEDULE"], 
                                values=['units_reimb', 'num_rx', 'total_amt_reimb', 
                                        'med_amt_reimb', 'nonmed_amt_reimb'], 
               aggfunc={'units_reimb': lambda x: x.sum(), 
                        'num_rx': lambda x: x.sum(), 
                        'total_amt_reimb': lambda x: x.sum(),
                        'med_amt_reimb': lambda x: x.sum(),
                        'nonmed_amt_reimb':lambda x: x.sum()})

cms16_stats_fin = cms16_stats.reset_index()
cms16_stats_fin.rename(columns={'units_reimb': 'units_reimb_sum', 
                                'num_rx':'num_rx_sum', 
                                'total_amt_reimb':'total_amt_reimb_sum',
                                'med_amt_reimb':'med_amt_reimb_sum',
                                'nonmed_amt_reimb':'nonmed_amt_reimb_sum'}, inplace=True)

#cms16_stats_fin.to_csv("/Users/catherineordun/Documents/Hackathon/DHHS/cms16_stats_fin.csv")


