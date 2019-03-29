#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#Libraries for manipulating datafiles, using sentiment analysis, and doing numerical operations,
#text analysis, api creation
import pandas as pd
import numpy as np
from google.cloud import language
from lexicalrichness import LexicalRichness as lr
from tqdm import tqdm # package for tracking for loops
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from json import dumps


app = Flask(__name__)
#sets the route for the api 
@app.route('/',methods = ['POST'])
def index():
    print (request)  
    user_input = request.form["data"]
    print(user_input)
    if (user_input!=""):
        unique_term, mtld_score = MTLD(user_input)
        user_memory_desc = [user_input]
        gc_df = Sentiment_Analysis (user_memory_desc)
        sentiment_score = float(gc_df['sentiment_score'])
        sentiment_magnitude = float(gc_df ['sentiment_magnitude'])
        specificity = Specificity(unique_term, mtld_score, sentiment_score,sentiment_magnitude)
        output = str(Response (specificity))
        result = {'Response': [output]}
        return jsonify(result)
    else:
        return jsonify({'Response': ["no value"]})

#generates the response
def Response (spec):
    try_again = "Please try again. Unfortunately, this answer is not specific enough. Please try to adjust your answer so it's clearer that it's a memory for an event that happenedonly once, and provide some more details about it if you can. You can also choose a memory of a different experience if you need to."
    
    success= "OK! Continue to the next tab, and keep up the good work with the details!"
    i =int (spec)
    if (i < 3):
        return (try_again)
    else:
        return(success)

#func connects with google service account for sentiment analysis  
def gc_sentiment(text):
    path = 'memoryproject-234423-117c3b81583d.json' #FULL path to your service account key
    client = language.LanguageServiceClient.from_service_account_json(path)
    document = language.types.Document(content=text,type=language.enums.Document.Type.PLAIN_TEXT)
    annotations = client.analyze_sentiment(document=document)
    score = annotations.document_sentiment.score
    magnitude = annotations.document_sentiment.magnitude
    return score, magnitude

#function evaluates the textual diversity of a given text (text analysis)
def MTLD(input_data):
    lex = lr(input_data)
    unique_term = lex.terms
    mtld_score = lex.mtld(threshold = 0.72)
    print (mtld_score)
    return(unique_term, mtld_score)

#function does sentiment analysis
def Sentiment_Analysis(user_input):
    gc_results = [gc_sentiment(row) for row in tqdm(list(user_input), ncols = 100)]
    gc_score, gc_magnitude = zip(*gc_results) # Unpacking the result into 2 lists
    gc = list(zip(user_input, gc_score, gc_magnitude))
    columns = ['description', 'sentiment_score', 'sentiment_magnitude']
    gc_df = pd.DataFrame(gc, columns = columns)
    return (gc_df)

#function evaluates the memory specificity
def Specificity (unique_term, mtld_score, sentiment_score, sentiment_magnitude):
    specificity = ""
     
    
    if (unique_term<15 or mtld_score <15):
        if((-0.5 < sentiment_score < 0.5) and sentiment_magnitude <=1):
            return("1")
        elif((sentiment_score >= 0.5 or sentiment_score <=-0.5) and sentiment_magnitude >1):
            return("2")
        else:
            return("1")       
            
    elif(unique_term<20 or mtld_score <25):
        if((sentiment_score < 0.5 and sentiment_score > -0.5) and sentiment_magnitude <=1.5):
            return("2")
        elif((sentiment_score >= 0.5 or sentiment_score <=-0.5) and sentiment_magnitude >1.5):
            return("3")
        else:
            return("2")
                
    elif (unique_term<25 or mtld_score <30):
        if(sentiment_score < 0.5 and sentiment_score > -0.5 and sentiment_magnitude <=2):
            return("3")
        elif((sentiment_score >= 0.5 or sentiment_score <=-0.5) and sentiment_magnitude>2):
            return("4")
        else:
            return("3")
        
    elif (unique_term>=25 or mtld_score >30):
        if((sentiment_score < 0.5 and sentiment_score > -0.5) and sentiment_magnitude <=2):
            return("4")
        elif((sentiment_score >= 0.5 or sentiment_score <=-0.5) and sentiment_magnitude >2):
            return("5")
        else:
            return("4")
        
#checks if the flask name is not modified
if __name__ == '__main__':
    app.config["TESTING"] = True
    app.run(port='5000')    


# In[ ]:




