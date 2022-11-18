# CourseProject

## Evaluation

**Have you completed what you have planned?**

I have completed the overall goal of creating a sentiment analysis Chrome extension, but I had to make some changes along the way. 

I had originally planned to create my own sentiment analysis model, but I had trouble creating an accurate model. My attempts performed poorly and took a significant amount of time to train. Because of this I used pre-trained models in the backend instead. These models were significanlty more accurate. The pre-trained models were also fast enough that I could use multiple models and return the highest rated answer.

I had also originally planned to create my backend in AWS. I was able to get the backend working in AWS, but it wasn't reliable. I set up an API Gateway connected to a Lambda function, which invoked a SageMaker endpoint that made predictions using my models. I ran into issues with the models sometimes taking too long for the API Gateway. The max API Gateway timeout of 30 seconds wasn't always enough time for the models to complete. This could have been addressed by putting my API on an EC2 instance or exposing the SageMaker endpoint directly. I chose not to do that becuase I didn't want to pay for it, so instead I ran the backend locally.

**Have you got the expected outcome? If not, discuss why.**

I was able to achieve the expected outcome but in a different way. Due to the resource requirements of training a sentiment analysis model, it proved to be more effective to utilize pre-trained models.

The pre-trained models performed well when they were evaluated using 500 reviews from this Amazon video game [review dataset](https://nijianmo.github.io/amazon/index). The notebook used for testing can be found in the model_testing directory.

Tutorial video can be found [here](https://uillinoisedu-my.sharepoint.com/:v:/g/personal/jcmcdow2_illinois_edu/EbUMzZWet8ZNtbpjDcAa4KwBk4EXIoTBX6Ksw5NaWKFXZQ?e=8SEylQ).

## Purpose

Chrome extenstion that allows sentiment analysis to be run on selected text. The UI accepts the selected text and sends a POST request to a backend. This backend server can be run locally. The backend is expected to be running at localhost:5000.

## Models

There are 5 options for running sentiment analysis.

<table>
  <tr>
    <th>Model</th>
    <th>Results</th>
    <th>Documentation</th>
    <th>Description</th>
    <th>Test Accuracy</th>
  </tr>
  <tr>
    <td>Combination</td>
    <td>Positive, Neutral, Negative</td>
    <td>
    </td>
    <td>Runs all 4 models and returns the highest scoring sentiment</td>
    <td>80%</td>
  </tr>
  <tr>
    <td>DistilBERT</td>
    <td>Positive, Negative</td>
    <td>
        <a href="https://huggingface.co/distilbert-base-uncased-finetuned-sst-2-english?text=I+like+you.+I+love+you">distilbert-base-uncased-finetuned-sst-2-english</a>
    </td>
    <td>Optimzed BERT fine-tuned for classification</td>
    <td>76.2%</td>
  </tr>
  <tr>
    <td>RoBERTa</td>
    <td>Positive, Negative</td>
    <td>
        <a href="https://huggingface.co/siebert/sentiment-roberta-large-english?text=I+like+you.+I+love+you">siebert/sentiment-roberta-large-english</a>
    </td>
    <td>Further trained BERT model fine-tuned for classification</td>
    <td>87.8%</td>
  </tr>
  <tr>
    <td>BERT Base</td>
    <td>Label_2 (Positive), Label_1 (Neutral), Label_0 (Negative)</td>
    <td>
        <a href="https://huggingface.co/Seethal/sentiment_analysis_generic_dataset?text=I+like+you.+I+love+you">Seethal/sentiment_analysis_generic_dataset</a>
    </td>
    <td>Base BERT model fine-tuned for classification</td>
    <td>72.2%</td>
  </tr>
  <tr>
    <td>BERT Twitter</td>
    <td>Label_2 (Positive), Label_1 (Neutral), Label_0 (Negative)</td>
    <td>
        <a href="https://huggingface.co/cardiffnlp/twitter-roberta-base-sentiment?text=I+like+you.+I+love+you">cardiffnlp/twitter-roberta-base-sentiment</a>
    </td>
    <td>Base BERT model trained on 58 million tweets and fine-tuned for classification</td>
    <td>76.8%</td>
  </tr>
</table>

### Combination

This option runs all 4 models and keeps a running total for the positive, neutral and negative score. It will return the sentiment with the highest cumulative score. This model tends to return postive or negative due to the fact that two models only return positive/negative. It's possible that neutral can be returned, but only if one neutral model receives a high score and all others are low. 

### DistilBERT

This option uses [distilbert-base-uncased-finetuned-sst-2-english](https://huggingface.co/distilbert-base-uncased-finetuned-sst-2-english?text=I+like+you.+I+love+you) which is a checkpoint of [distilbert-base-uncased](https://huggingface.co/distilbert-base-uncased?text=Paris+is+the+%5BMASK%5D+of+France.) that was tuned for text classification.

This model was created to be smaller and faster version of BERT. This allows the extension to make fast inferences. This model was trained on the same data as BERT, using BERT output as the labels. 

This model is case insentive and will return either POSITIVE or NEGATIVE.

### RoBERTa

This option uses [siebert/sentiment-roberta-large-english](https://huggingface.co/siebert/sentiment-roberta-large-english?text=I+like+you.+I+love+you) which is a checkpoint of [roberta-large](https://huggingface.co/roberta-large?text=The+goal+of+life+is+%3Cmask%3E) tuned for text classification. RoBERTa is another optimized version of BERT. RoBERTa proposes that BERT required additional training and hyper parameter tuning. The original paper can be found [here](https://arxiv.org/abs/1907.11692).

This model is case sensitive and will return either POSITIVE or NEGATIVE.

### BERT Base

This option uses [Seethal/sentiment_analysis_generic_dataset](https://huggingface.co/Seethal/sentiment_analysis_generic_dataset?text=I+like+you.+I+love+you) which fine tunes the BERT model to be used for text classification. 

The original BERT paper can be found [here](https://arxiv.org/abs/1810.04805).

This model is case insentive and will return Label_2 (Positive), Label_1 (Neutral), or Label_0 (Negative).

### BERT Twitter

This option uses [cardiffnlp/twitter-roberta-base-sentiment](https://huggingface.co/cardiffnlp/twitter-roberta-base-sentiment?text=I+like+you.+I+love+you). This model takes BERT and fine tunes it on 58 million tweets for text classification.

This model is case sentive and will return Label_2 (Positive), Label_1 (Neutral), or Label_0 (Negative).

## Installation

### Requirements

- Python3.9 (May work with other versions, but this is what I used)
- pip
- ability to run PyTorch
- virtual environment recommended

### Extension

- Follow the at "Loading an unpacked extension" instructions [here](https://developer.chrome.com/docs/extensions/mv3/getstarted/development-basics/#load-unpacked:~:text=%23-,Loading%20an%20unpacked%20extension,-To%20load%20an), and select the "extension" directory from this project

### Backend

Steps (virtual environment recommended)
- open terminal
- move into the project directory and install the dependencies from the requirements.txt file: ```pip install -r requirements.txt```
- start local server from local_backend directory with: ``` python3 -m flask run ```

Saving models (optional)

By default the backend will redownload the models everytime it is started. By setting certain environment variables you can store the models locally, and load from there. The following instructions work for zsh. Other shells may have different ways of setting environment variables 

- on the first run set the SAVE_MODELS to true: ``` export SAVE_MODELS=true && python3 -m flask run ```
- set the LOAD_MODELS variable for subsequent runs: ``` export LOAD_MODELS=true && python3 -m flask run ```

### Running Extension

- Pin extension following these [instructions](https://developer.chrome.com/docs/extensions/mv3/getstarted/development-basics/#load-unpacked:~:text=%23-,Pinning%20the%20extension,-By%20default%2C%20when)
- Select a web page and highlight any text
- Open extension
- Select model option
- Submit

After these steps, the sentiment should be displayed at the bottom of the modal.

## Citations

cardiffnlp/twitter-roberta-base-sentiment.
https://huggingface.co/cardiffnlp/twitter-roberta-base-sentiment?text=I+like+you.+I+love+you

distilbert-base-uncased-finetuned-sst-2-english.
https://huggingface.co/distilbert-base-uncased-finetuned-sst-2-english?text=I+like+you.+I+love+you

Justifying recommendations using distantly-labeled reviews and fined-grained aspects.
Jianmo Ni, Jiacheng Li, Julian McAuley.
Empirical Methods in Natural Language Processing (EMNLP), 2019.
https://nijianmo.github.io/amazon/index

More than a feeling: Accuracy and Application of Sentiment Analysis.
Hartmann, Jochen and Heitmann, Mark and Siebert, Christian and Schamp, Christina.
International Journal of Research in Marketing, 2022.
https://huggingface.co/siebert/sentiment-roberta-large-english?text=I+like+you.+I+love+you

Seethal/sentiment_analysis_generic_dataset.
https://huggingface.co/Seethal/sentiment_analysis_generic_dataset?text=I+like+you.+I+love+you

