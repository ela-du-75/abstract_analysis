# Importation of libraries

import pandas as pd
import numpy as np
from tqdm import tqdm
import textstat 
import matplotlib.pyplot as plt
import nltk
from nltk import wordpunct_tokenize, sent_tokenize

def computations(output_aff_1_author,output_computations):

    db = pd.read_csv(output_aff_1_author, sep=';')

    data = pd.read_stata('data/ling_web.dta')

    # Some countries don't exist in the data, so they are renamed with a similar country
    db['country_renamed'] = db['country']

    # Function that computes the average word lenght
    def average_word_length(text):
        if pd.isnull(text) or not isinstance(text, str):
            return 0
        words = [word for word in wordpunct_tokenize(text.lower()) if word.isalpha()]
        if not words:
            return 0
        return sum(len(word) for word in words) / len(words)

    # Function that computes the proportion of sentences in the abstract longer than 15 words
    def proportion_long_sentences(text, threshold=15):
        if not isinstance(text, str) or not text.strip():
            return 0
        import re
        sentences = re.split(r'[.!?]', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        if not sentences:
            return 0
        long_sentences = [s for s in sentences if len(s.split()) > threshold]
        return len(long_sentences) / len(sentences)

    # renaming countries: either because they are named differently in the data or because they don't exist
    db['country_renamed'] = db['country_renamed'].replace({'South Korea':'Republic of Korea', 
                        'United Kingdom':'United Kingdom of Great Britain and Northern Ireland',
                        'Belgium':'Belgium and Luxembourg',
                        'Luxembourg':'Belgium and Luxembourg',
                        'Türkiye':'Turkey',
                        'The Gambia':'Gambia',
                        'Russia':'Russian Federation',
                        'Iran':'Iran (Islamic Republic of)',
                        'Hungaria':'Hungary',
                        'UAE' : 'United Arab Emirates',
                        'The Netherlands':'Netherlands',
                        'Czechia':'Czech Republic',
                        'Tanzania':'United Republic of Tanzania',
                        'Guam':'Philippines',
                        'Vietnam':'Viet Nam',
                        'Hong Kong' : 'China, Hong Kong Special Administrative Region',
                        'Moldova':'Republic of Moldova',
                        'Brunei':'Brunei Darussalam',
                        'Scotland':'United Kingdom of Great Britain and Northern Ireland', 
                        'Lituania':'Lithuania','Syria':'Syrian Arab Republic','Libya':'Libyan Arab Jamahiriya',
                        'Venezuela':'Venezuela (Bolivarian Republic of)','Ivory Coast':"Côte d'Ivoire",
                        'North Macedonia':'The former Yugoslav Republic of Macedonia',
                        'Congo Republic':'Democratic Republic of the Congo',
                        # Replaced countries:
                        'Palestine':'Jordan', 
                        'Ethiopia':'Eritrea', 
                        'Serbia':'Croatia', 
                        'Namibia':'South Africa',
                        'Puerto Rico':'Dominican Republic',
                        'Eswatini':'South Africa',
                        'Maldives':'Sri Lanka',
                        'Kosovo':'Albania',
                        'South Sudan':'Sudan',
                        'Monaco':'France',
                        'Réunion':'France',
                        'Faroe Islands':'Iceland',
                        'Macao':'China',
                        'Botswana':'South Africa',
                        'Liechtenstein':'Austria',
                        'DR Congo':'Democratic Republic of the Congo',
                        'Mongolia':'Kyrgyzstan',
                        'Laos':'Thailand'
                        })

    # Computing the measurements and putting proximity from the data
    for i in tqdm(range(len(db)), desc='Computing measurements (step 5/6)'):
        target_country = db.loc[i,'country_renamed']
        if target_country == 'United States':
            db.loc[i,'cle'] = 1
        else :
            db.loc[i,'cle'] = data.loc[(data['country_o'] == 'United States of America') & (data['country_d'] == target_country),'cle'].iloc[0]
        abstract = db.loc[i,'abstract']
        abstract = str(abstract)
        db.loc[i,'fk_grade_level'] = textstat.flesch_kincaid_grade(abstract)
        db.loc[i,'gunning_fog'] = textstat.gunning_fog(abstract)
        db.loc[i,'smog'] = textstat.smog_index(abstract)
        db.loc[i,'automated_readility'] = textstat.automated_readability_index(abstract)
        db.loc[i,'flesh_reading_ease'] = textstat.flesch_reading_ease(abstract)
        db.loc[i,'dale_chall'] = textstat.dale_chall_readability_score(abstract)
        tokens = wordpunct_tokenize(abstract.lower())
        db.loc[i,'ttr'] = len(set(tokens)) / len(tokens)
        db.loc[i,'avg_length_words'] = average_word_length(abstract)
        db.loc[i,'prop_more_15words'] = proportion_long_sentences(abstract)

    db.to_csv(output_computations, sep=';',index=False)

output_aff_1_author = 'outputs/aff_1_author.csv'
output_computations = 'outputs/computations.csv'
computations(output_aff_1_author,output_computations)