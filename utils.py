#!/usr/bin/python3
"""
This is supposed to be the estimate_sentiment function.
Args:
Takes in the news, runs it through the huggingface model,
Return:
The probaility and the sentiments
"""

from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from dotenv import load_dotenv
from typing import Tuple 


device = "cuda:0" if torch.cuda.is_available() else "cpu"

load_dotenv()

tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert").to(device)
labels = ["positive", "negative", "neutral"]

def estimation_sentiment(news_headlines):
    """
    function = estimation_sentiment()
    Args: news
    Return: Probability, sentiment
    """
    if news_headlines:
        tokens = tokenizer(news_headlines, return_tensors="pt", padding=True).to(device)

        result = model(tokens["input_ids"], attention_mask=tokens["attention_mask"])[
            "logits"
        ]
        result = torch.nn.functional.softmax(torch.sum(result, 0), dim=-1)
        probability = result[torch.argmax(result)]
        sentiment = labels[torch.argmax(result)]
        return probability, sentiment
    else:
        return 0, labels[-1]


if __name__ == "__main__":
    tensor, sentiment = estimation_sentiment(['markets responded negatively to the news!','traders were displeased!'])
    print(tensor, sentiment)
    print(torch.cuda.is_available())