import json
import re
import string

import contractions
import nltk

from textblob import TextBlob

from rake_nltk import Rake

from nltk.sentiment import SentimentIntensityAnalyzer
from clustering.models.models import Article, ArticleAnalysis
from news_clustering.misc import json_dumps

stopwords = set(nltk.corpus.stopwords.words("english"))


def get_article_sentience(article):
    sia = SentimentIntensityAnalyzer()
    return sia.polarity_scores(article)


def analyse_article(
    article: Article, task_id: str = None, force_analyse: bool = False, *args, **kwargs
):
    article_id = task_id

    article_text = re.sub(
        r"(?:((?:https?:\/\/(?:www\.)?)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&\/\/=]*))|(\(\@\S+\)))\s?",
        "",
        article.article,
    )
    article_text = re.sub(
        r"\s{2,10}",
        " ",
        article_text,
    )
    if not force_analyse:
        analysis_obj, exists = ArticleAnalysis.objects.get_or_create(article=article)
    else:
        exists = False
        analysis_obj = ArticleAnalysis.objects.create(article=article)

    word_token = TextBlob(article_text)

    if word_token.sentiment.polarity <= -0.05:
        analysis_obj.sentiment = "Negative"
    elif word_token.sentiment.polarity >= 0.05:
        analysis_obj.sentiment = "Positive"
    elif (word_token.sentiment.polarity >= -0.05) & (
        word_token.sentiment.polarity <= 0.05
    ):
        analysis_obj.sentiment = "Neutral"

    analysis_obj.sentiment_analysis = json_dumps(
        {**word_token.sentiment._asdict(), **get_article_sentience(article_text)}
    )
    # analysis_obj.tokenised = json_dumps(word_token.sentences)
    keywords = {
        k.translate(str.maketrans("", "", string.punctuation)): v
        for k, v in word_token.word_counts.items()
        if k not in stopwords and not k.isnumeric()
    }
    analysis_obj.keywords = set(
        [
            re.sub(r"[^\w\s]", "", k)
            for k in word_token.noun_phrases
            if k not in stopwords
        ]
    )

    # # text_keywords = extract_keywords(article_text)
    # if analysis_obj.tokenised is None:
    #     analysis_obj.tokenised = json_dumps(get_tokenised_text(article_text))
    #
    # if analysis_obj.sentiment is None:
    #     analysis_obj.sentiment = json_dumps(get_article_sentience(article_text))
    #
    # if analysis_obj.keywords is None:
    #     analysis_obj.keywords = json_dumps(extract_keywords(article_text))

    analysis_obj.save()
    article.analysis = analysis_obj
    article.save()
    return analysis_obj


def get_tokenised_text(article_text):
    fixed_sentence = contractions.fix(article_text)
    tokenised = nltk.sent_tokenize(fixed_sentence)
    filtered = [w for w in tokenised if w.lower() not in stopwords]
    removed_punc = [
        re.sub(
            r"(?:((?:https?:\/\/(?:www\.)?)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&\/\/=]*))|(\(\@\S+\)))\s?",
            "",
            w,
        )
        for w in filtered
        if w.lower() not in string.punctuation + r"''``"
    ]

    return removed_punc


def extract_keywords(article_text):
    rake = Rake(max_length=1, include_repeated_phrases=False)
    rake.extract_keywords_from_text(article_text)
    keyword_extracted = rake.get_ranked_phrases()
    return keyword_extracted
