import spacy
import pandas as pd

from openai import OpenAI
from datetime import datetime
from constants import system_prompt, assistant_content
#from bodhiguru.settings import get_env_variable

nlp = spacy.load("en_core_web_sm")
#openapikey = get_env_variable("api_key")
#client = OpenAI(api_key=openapikey)

def string_to_words(username, user_response, power_words, negative_words):
    for word in power_words:
        if word in user_response:
            user_response = user_response.replace(word, '')
    for word in negative_words:
        if word in user_response:
            user_response = user_response.replace(word, '')
            
    user_response = nlp(user_response)
    user_response_filtered_text = " ".join(token.text for token in user_response if not token.is_stop)
    user_response_filtered_text = user_response_filtered_text.replace(',', '').strip(" ")
    user_response_filtered_text = user_response_filtered_text.split(" ")
    user_response_filtered_text = [item for item in user_response_filtered_text if item.strip()]
    return user_response_filtered_text

def detect_words(word):
    completion = client.chat.completions.create(
        model="ft:gpt-3.5-turbo-0125:personal::9Ms8VCR8",
        messages=[ 
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": word},
            {"role": "assistant", "content": assistant_content}
        ]
    )
    
    return completion.choices[0].message.content

def save_words_to_excel(user_response_filtered_text):
    print("Trying to save words to excel...")
    try:
        df_existing = pd.read_excel('words.xlsx')
    except FileNotFoundError:
        df_existing = pd.DataFrame(columns=['Words', 'Type', 'Competency'])
    new_data = {'Words': [], 'Type': [], 'Competency': []}
    for word in user_response_filtered_text:
        if word not in df_existing['Words'].values:
            print("adad")
            detected_response = detect_words(word)
            type, competency = "", ""
            print(detected_response)
            if 'and' in detected_response:
                type, competency = detected_response.split(' and ')
            elif '&' in detected_response:
                type, competency = detected_response.split(' & ')
            elif ',' in detected_response:
                type, competency = detected_response.split(', ')
            elif '-' in detected_response:
                type, competency = detected_response.split(' - ')
            new_data['Words'].append(word)
            new_data['Type'].append(type)
            new_data['Competency'].append(competency)
    df_new = pd.DataFrame(new_data)
    if not df_new.empty:
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
    else:
        df_combined = df_existing
    df_combined.to_excel('words.xlsx', index=False)
    print("File Generated Successfully!")
