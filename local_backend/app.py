from flask import Flask, request
from transformers import pipeline
import os

distilbert = None
roberta = None
bert_base = None
bert_twitter = None


if "LOAD_MODELS" in os.environ and os.environ['LOAD_MODELS'] == 'true':
    print('* Loading saved models')
    distilbert = pipeline('sentiment-analysis',model='./models/distilbert') 
    roberta = pipeline("sentiment-analysis",model='./models/roberta') 
    bert_base = pipeline("sentiment-analysis",model='./models/bert_mlm') 
    bert_twitter = pipeline("sentiment-analysis",model='./models/roberta_twitter') 
else:
    print('* Downloading models')
    distilbert = pipeline("sentiment-analysis",model="distilbert-base-uncased-finetuned-sst-2-english") # https://huggingface.co/distilbert-base-uncased-finetuned-sst-2-english?text=I+like+you.+I+love+you
    roberta = pipeline("sentiment-analysis",model="siebert/sentiment-roberta-large-english") # https://huggingface.co/siebert/sentiment-roberta-large-english?text=I+like+you.+I+love+you
    bert_base = pipeline("sentiment-analysis",model="Seethal/sentiment_analysis_generic_dataset") # https://huggingface.co/Seethal/sentiment_analysis_generic_dataset?text=I+like+you.+I+love+you
    bert_twitter = pipeline("sentiment-analysis",model="cardiffnlp/twitter-roberta-base-sentiment") # https://huggingface.co/cardiffnlp/twitter-roberta-base-sentiment?text=I+like+you.+I+love+you

if "SAVE_MODELS" in os.environ and os.environ['SAVE_MODELS'] == 'true':
    distilbert.save_pretrained('./models/distilbert')
    roberta.save_pretrained('./models/roberta')
    bert_twitter.save_pretrained('./models/roberta_twitter')
    bert_base.save_pretrained('./models/bert_mlm')

models = {
    'distilbert': distilbert,
    'roberta': roberta,
    'bert_base': bert_base,
    'bert_twitter': bert_twitter
}

label_to_class = {
    'LABEL_2': 'POSITIVE',
    'LABEL_1': 'NEUTRAL',
    'LABEL_0': 'NEGATIVE',
}

app = Flask(__name__)

@app.route("/",methods = ['POST'])
def classify():
    try:
        sentiment = ''
        model = request.json['model']
        text = request.json['text']

        if model == 'combination':
            pos_score = 0
            neg_score = 0
            neu_score = 0

            results = [
                distilbert(text),
                roberta(text),
                bert_base(text),
                bert_twitter(text)
            ]

            for res in results:
                parsed = parse_label(res[0])
                if(parsed['label'] == 'POSITIVE'):
                    pos_score += parsed['score']
                elif parsed['label'] == 'NEGATIVE':
                    neg_score += parsed['score']
                else:
                    neu_score += parsed['score']

            if pos_score > neg_score and pos_score > neu_score:
                sentiment = 'POSITIVE'
            elif neg_score > pos_score and neg_score > neu_score:
                sentiment = 'NEGATIVE'
            else:
                sentiment = 'NEUTRAL'
        else:
            print(model)
            res = models[model](text)
            sentiment = parse_label(res[0])['label']

        return {
            'statusCode': 200,
            'body': sentiment
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': str(e)
        }


def parse_label(result):
    label_in = result['label']
    label = label_to_class[label_in] if label_in in label_to_class else label_in

    return { 
        'label': label, 
        'score': result['score'] 
    }
