# -*- coding: utf-8 -*-
"""
SCRIPT THAT CONTAINS SUPPORT DICTIONARIES AND FUNCTIONS FOR FI SCRIPT
"""

import numpy as np
import sys

def stopifnot(cond):
    if not cond:
        sys.exit('Error! Condition is not met')

###############################################################################
# -------------------------------- BBD PAPERS ------------------------------- # 
###############################################################################

di_cn_bbd = {'JOURNAL':'journal', 'Impact Factor':'IF',
 'YEAR OF PUBLICATION':'year', 'GEOGRAPHIC LOCATION (Mainland)':'geo',
 'h index of corresponding author':'h_index',
 'Citation':'citation', 'Weighted Citation Index':'wcitation',
 'PLUM- USAGE':'plum1', 'PLUM- CAPTURES':'plum2', 'PLUM- SOCIAL MEDIA':'plum3',
 'Study Design':'study_design', 'Type of Randomization':'type_random',
 'Allocation Concealment':'concealment', 'Blinding':'blinding', 'TOPIC':'topic', 
 'Sample Size Justfucation':'power_just', 'Reported p Value':'pval_rep', 
 'Losses to FU':'fu_loss', 'Primary or Secondary Outcome':'outcome',
 'STATISTICIAN OR EPIDEMIOLOGIST SUPPORT':'statistician', 'RECIVED FUNDING':'funding'}

di_design_bbd = {1:'RCT', 2:'Observational', 3:'Case Matched', 4:'Retrospective',
 5:'Qualitative', 6:'Case control', 7:'cohort', 8:'pseudo RCT'}

di_random_bbd = {1:'Simple', 2:'Blocked', 3:'Not Stated', 
                 4:'NA', 5:'electronic'}

di_topic_bbd = {1:'Nocturnal Enuresis', 2:'rUTI', 3:'OAB',
 4:'Dysfunctional voiding', 5:'Incontinence', 6:'voiding postponement'}

di_journal_bbd = \
 {1:'Journal of Urology', 2:'Journal of pediatric urology',
  3:'Urology',4:'Korean Journal of Urology', 5:'Archives of disease in childhood',
  6:'International Braz J Urol', 7:'BJU international', 8:'Lasers in medical science',
  9:'ISRN Urology', 10:'Pediatrics', 11:'Saudi medical journal', 12:'Acta Pædiatrica',
  13:'Archivio italiano di urologia, andrologia', 14:'Renal Failure', 15:'Pediatric Nephrology',
  16:'Amer J Clin Hypn', 17:'ChildPsychol. Psychi', 18:'Behaviour research and therapy',
  19:'International Urology and Nephrology',20:'Turkish Journal of Medical Sciences',
  21:'Clinical Pediatrics', 22:'Iranian Journal of Medical Sciences',
  23:'International Journal of Therapy and Rehabilitation', 24:'Neurourology and Urodynamics',
  25:'The Turkish Journal of Pediatrics', 26:'Australian & New Zealand Continence Journal',
  27:'Therapeutic Advances in Urology', 28:'INDIAN PEDIATRICS', 29:'Eur Urol',
  30:'Eur Arch Otorhinolaryngol', 31:'Scand J Urol Nephrol', 32:'Pediatria i Medycyna Rodzinna',
  33:'Eur J Pediatr', 34:'Journal of Child Psychology and Psychiatry and Allied Disciplines',
  35:'Medicine', 36:'J Ped Surgery', 37:'Pediatrics international', 38:'Pak J Med Sci',
  39:'International Journal of Clinical and Experimental Medicine',
  40:'European Neurology', 41:'Academic pediatrics',
  42:'Iranian Journal of Pediatrics', 43:'CMAJ', 44:'Arch Iran Med',
  45:'Neuropsychiatric Disease and Treatment', 
  46:'Developmental Medicine and Child Neurology',
  47:'American journal of diseases of children', 48:'Turkish J Urol',
  49:'Indian journal of pediatrics', 
  50:'JOURNAL OF CHILD AND ADOLESCENT PSYCHOPHARMACOLOGY',
  51:'Urologia Internassi', 52:'journal of paediatrics',
  53:'archives disease in childhood', 54:'Al-Kindy College Medical Journal',
  55:'The Journal of International Medical Research', 
  56:'Jsaudi journal of kidney disease', 
  57:'Journal of Developmental and Behavioral Pediatrics',
  58:'Journal of the Formosan Medical Association'}
 
di_geo_bbd = {1:'Egypt',2:'Iran',3:'Italy',4:'Canada', 5:'Saudi Arabia',6:'Israel',
               7:'Greece',
  8:'Iraq',9:'Austria',10:'USA',11:'Turkey', 13:'Belgium', 14:'India', 15:'Brazil',
  16:'Australia', 17:'Denmark', 18:'England', 19:'China', 20:'Germany', 21:'Japan',
  22:'Russia',23:'Poland',24:'Finland',25:'Netherlands',26:'Korea', 27:'Sweden',
  28:'Portugal', 29:'Taiwan', 30:'Slovenia', 31:'Serbia'}
 
###############################################################################
# -------------------------------- PHN PAPERS ------------------------------- # 
###############################################################################
 
di_cn_phn = {'Study ID':'ID','JOURNAL':'journal', 'Impact Factor':'IF',
 'YEAR OF PUBLICATION':'year', 'GEOGRAPHIC LOCATION (Mainland)':'geo',
 'h index of corresponding author':'h_index',
 'Times Cited':'citation',
 'n of Group 1':'Group 1', 'n of Group 2':'Group 2',
 'Study Design':'study_design', 'Type of Randomization':'type_random',
 'Allocation Concealment':'concealment', 'Blinding':'blinding', 'TOPIC':'topic', 
 'Sample Size Justification':'power_just', 'Reported p Value':'pval_rep', 
 'Losses to FU':'fu_loss', 'Primary or Secondary Outcome':'outcome',
 'STATISTICIAN OR EPIDEMIOLOGIST SUPPORT':'statistician', 'RECIVED FUNDING':'funding'}

di_design_phn = {1:'Observational', 2:'RCT', 3:'cohort study'}

di_random_phn = {0:'NA',1:'Not Specified',
                 2:'Simple',3:'Blocked',4:'Stratified'}

di_topic_phn = {1: 'VUR', 2: 'Prenatal Hydronephrosis', 3: 'Stones',
   4:'UPJO', 5:'Ureterocele/duplex anomalies',6:'PHN', 7:'HUN',
   8:'UTI', 9:'PUV'}

di_journal_phn = {1:'J Urol', 2:'J Ped Urol',3:'International Urology Nephrology',
 4:'BJUI',5:'Pediatric Nephrology',6:'Urology',7:'Journal of pediatrics',
 8:'Journal of endourology',9:'NEJM',10:'American Journal of Roentgenology',
 11:'Acta Pediatricia', 12:'Urologia Internationalis', 13:'Radiology',
 14:'Renal Failure', 15:'Clinical Radiology',16:'world J Urol',
 17:'JOURNAL OF LAPAROENDOSCOPIC & ADVANCED SURGICAL TECHNIQUES',
 18:'Journal of Pediatric Surgery', 19:'Nephrology, Dialysis, Transplantation',
 20:'Pediatrics', 21:'Journal of Nuclear Medicine', 22:'korean j urol',
 23:'urolithiasis', 24:'Prenatal Diagnosis', 25:'European Urology',
 26:'european journal of radiology', 27:'pediatric radiology',
 28:'Pediatric Surgery International', 29:'pediatric anesthesia',
 30:'ANZ J Surg', 31:'Urological Research',
 32:'Surgical Endoscopy and Other Interventional Techniques',
 33:'Birth Defects Research Part A', 34:'International journal of urology',
 35:'Journal of MRI', 36:'Iran J Pediatr',
 37:'Scandinavian Journal of Urology and Nephrology',
 38:'Journal of the Society of Laparoendoscopic Surgeons', 
 39:'Anesthesia and Analgesia'}

di_geo_phn = {1:'Canada', 2:'USA', 3:'Turkey', 4:'Kuwait', 5:'Italy',6:'India',
              7:'Iran',8:'France',9:'Sweden',10:'Korea',11:'Israel',
              12:'Australia',13:'Germany',14:'Netherlands',15:'Greece',
              16:'Switzerland',17:'England',18:'Austria',19:'Brazil',20:'Japan',
              21:'Saudi Arabia',22:'Egypt',23:'Hungary',24:'Chile',25:'Romania',
              26:'Norway',27:'China',28:'Poland',29:'Taiwan'}

###############################################################################
# -------------------------------- REVERSE FI ------------------------------- # 
###############################################################################

di_cn_neg = {'Covidence Paper ID':'ID','JOURNAL':'journal', 'Impact Factor':'IF',
 'YEAR OF PUBLICATION':'year', 'GEOGRAPHIC LOCATION (Mainland)':'geo',
 'h index of corresponding author':'h_index',
 'Times Cited':'citation','weighted':'wcitation',
 'Plum Usage':'plum1', 'Plum Capture':'plum2', 'Plum SM':'plum3',
 'n of control':'Group 1', 'n of experimental':'Group 2',
 'Study Design':'study_design', 'Type of Randomization':'type_random',
 'Allocation Concealment':'concealment', 'Blinding':'blinding', 'TOPIC':'topic', 
 'Sample Size Justification':'power_just', 'Reported p Value':'pval_rep', 
 'Losses to FU':'fu_loss', 'Primary or Secondary Outcome':'outcome',
 'STATISTICIAN OR EPIDEMIOLOGIST SUPPORT':'statistician', 'RECIVED FUNDING':'funding'}

di_design_neg = {1:'Prospective',2:'Retrospective',3:'RCT'}

di_random_neg = {0:'NA',1:'Not Specified',2:'Stated'}

di_topic_neg = {1:'pyeloplasty',2:'Medical topic',3:'VUR',4:'robotics',
    5:'nephrectomy',6:'Megaureter',7:'Reimplantation',8:'BBD'}

di_journal_neg = {1:'Urology', 2:'Iranian Journal of Pediatrics', 3:'BMJ',
 4:'Pediatric Surgery International', 5:'J ped urol', 6:'J Urol', 7:'BJUI',
 8:'Investigative and clinical urology',
 9:'Annals of the Royal College of Surgeons of England',10:'Acta Paediatrica',
 11:'European Urology', 12:'Plos',13:'Jama peds',
 14:'Journal of Antimicrobial Chemotherapy',15:'Behaviour Research and Therapy',
 16:'j ped surg',17:'Int Urol Nephrol',18:'Iranian Journal of Child Neurology',
19:'The Journal of international medical research'}

di_geo_neg = {1:'France', 2:'Iran', 3:'Turkey', 4:'England', 5:'USA',
 6:'Japan', 7:'Egypt', 8:'Canada', 9:'Italy', 10:'Australia', 11:'Switzerland',
 12:'Korea', 13:'Austria', 14:'China', 15:'Poland', 16:'Sweden', 17:'Germany',
 18:'England', 19:'Netherlands', 20:'Brazil', 21:'Belgium'}

############################################################################
# -------------------------------- GENERAL ------------------------------- # 
############################################################################

di_blinding = {0:'No', 1:'Yes', 2:'Not specified', 3:'NA'}

di_conceal = {0:'No', 1:'Yes', 2:'Not specified', 3:'NA', 4:'NA'}

di_funding =  {0:'No', 1:'Yes', 2:'Not specified'}

di_outcome = {0: 'Primary', 1:'Primary', 2:'Secondary'}

di_power = {0:'No', 1:'Yes', np.NaN:'NA'}

di_statistician =  {0:'No', 1:'Yes', 2:'Not specified'}

# General columns to drop
cn_drop = ['AUTHORS','Corresponding','Pubmed ID','TITLE','Article Title',
           'Gender 1st', 'Gender Corresponding',
           'Number needed to flip results','Control','Experimental',
           'FI','FQ','COMMENTS','Sample Size','Outcome',
           'Prospective/Retrospective','Population',
           'h index without self citations','weighted',
           'fu_loss', # Not reported as a number
           ]


