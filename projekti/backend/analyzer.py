import json
import nltk
import numpy as np
from collections import Counter
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sentence_transformers import SentenceTransformer, util
from textblob import TextBlob

# Ladataan tarvittavat NLTK-resurssit
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('vader_lexicon')

# Ladataan BERT-pohjainen malli
bert_model = SentenceTransformer("all-MiniLM-L6-v2")

class CVAnalyzer:
    def __init__(self, cv_text, job_text):
        self.cv_text = cv_text
        self.job_text = job_text
        self.stopwords = set(stopwords.words("english"))

    def word_count(self):
        """Laskee tekstin sanamäärän"""
        return len(word_tokenize(self.cv_text))

    def extract_keywords(self, text, n=15):
        """Poimii tärkeimmät avainsanat tekstistä, mutta rajoittaa määrää lyhyissä teksteissä"""
        words = [word.lower() for word in word_tokenize(text) if word.isalpha()]
        words = [word for word in words if word not in self.stopwords]
        counter = Counter(words)

        # Rajoitetaan avainsanojen määrää lyhyissä teksteissä
        max_keywords = min(n, max(5, len(words) // 3))
        keywords = set(word for word, _ in counter.most_common(max_keywords))

        return keywords if len(keywords) >= 3 else set()

    def sentiment(self):
        """Analysoi tekstin sävyn käyttäen sekä TextBlob että NLTK:n VADERiä"""
        # NLTK sentiment
        sia = SentimentIntensityAnalyzer()
        nltk_result = sia.polarity_scores(self.cv_text)
        
        # TextBlob sentiment (yksinkertaisempi)
        blob = TextBlob(self.cv_text)
        polarity = blob.sentiment.polarity
        
        # Yhdistetty tulos
        if polarity > 0 or nltk_result['compound'] > 0.05:
            return 'Positiivinen'
        elif polarity < 0 or nltk_result['compound'] < -0.05:
            return 'Negatiivinen'
        else:
            return 'Neutraali'

    def get_bert_synonyms(self, word, candidate_words, top_n=2):
        """Löytää BERTin avulla lähimmät sanat"""
        word_embedding = bert_model.encode(word, convert_to_tensor=True)
        candidate_embeddings = bert_model.encode(candidate_words, convert_to_tensor=True)

        similarities = util.pytorch_cos_sim(word_embedding, candidate_embeddings)[0]
        sorted_indices = np.argsort(-similarities)[:top_n]

        return {candidate_words[i] for i in sorted_indices if similarities[i] > 0.6}

    def expand_with_bert(self, word_set, candidate_words):
        """Korvaa sanat BERTin avulla synonyymeillä"""
        expanded_words = set(word_set)
        for word in word_set:
            expanded_words.update(self.get_bert_synonyms(word, candidate_words))
        return expanded_words

    def match_score(self):
        """Vertaa CV:tä työpaikkailmoitukseen käyttäen avainsanoja ja BERTin synonyymejä"""
        cv_keywords = self.extract_keywords(self.cv_text)
        job_keywords = self.extract_keywords(self.job_text)

        if not job_keywords:
            return 0

        # Jos CV sisältää liian vähän sanoja, osuvuus on 0%
        if len(cv_keywords) < 3:
            return 0

        # Laajennetaan synonyymeillä
        all_words = list(cv_keywords | job_keywords)
        expanded_cv = self.expand_with_bert(cv_keywords, all_words)
        expanded_job = self.expand_with_bert(job_keywords, all_words)

        # Lasketaan osuvuus
        match_percentage = len(expanded_cv & expanded_job) / len(expanded_job) * 100
        return round(match_percentage)

    def analyze(self):
        """Suorittaa kaikki analyysit ja palauttaa tuloksen"""
        result = {
            'word_count': self.word_count(),
            'cv_keywords': list(self.extract_keywords(self.cv_text)),
            'job_keywords': list(self.extract_keywords(self.job_text)),
            'sentiment': self.sentiment(),
            'match': self.match_score()
        }
        self.save_history(result)
        return result

    def save_history(self, data):
        """Tallentaa analyysitulokset JSON-tiedostoon"""
        with open('history.json', 'a', encoding='utf-8') as f:
            f.write(json.dumps(data, ensure_ascii=False) + '\n')

def read_file(file_path):
    """Lukee tekstitiedoston sisällön ja palauttaa sen"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return ""