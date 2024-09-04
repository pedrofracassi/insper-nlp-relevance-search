from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from typing import List, Set
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
import nltk
from nltk.tokenize import word_tokenize
import uvicorn
from nltk.corpus import stopwords
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

STOP_WORDS: Set[str] = set(stopwords.words('portuguese'))

DIGIT_PATTERN = re.compile(r'\d+')
SHORT_WORD_PATTERN = re.compile(r'\b\w{1,2}\b')
SPECIAL_CHAR_PATTERN = re.compile(r'[^\w\s]')

nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)
nltk.download('stopwords', quiet=True)

stop_words = set(stopwords.words('portuguese'))

def preprocess_text(text: str) -> str:
    text = text.lower()
    text = DIGIT_PATTERN.sub('', text)
    text = SHORT_WORD_PATTERN.sub('', text)
    text = SPECIAL_CHAR_PATTERN.sub('', text)
    tokens: List[str] = word_tokenize(text)
    tokens = [token for token in tokens if token not in STOP_WORDS]

    return ' '.join(tokens)

class QueryResponse(BaseModel):
    cid: str
    content: str
    relevance: float = Field(..., ge=0, le=1)

class QueryResult(BaseModel):
    results: List[QueryResponse]
    message: str

df = pd.read_csv('posts.csv')
df['text'] = df['text'].astype(str)
df['text_processed'] = df['text'].apply(preprocess_text)

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df['text_processed'])

app = FastAPI()

@app.get("/query", response_model=QueryResult)
async def query(q: str = Query(..., description="Query text")):
    if not q:
        raise HTTPException(status_code=400, detail="Query parameter is missing")
    
    query_text_processed = preprocess_text(q)
    query_vec = vectorizer.transform([query_text_processed])
    similarities = cosine_similarity(query_vec, X).flatten()
    
    indices = (-similarities).argsort()[:10]
    indices = [i for i in indices if similarities[i] > 0]

    results = [
        QueryResponse(
            cid=df.iloc[i]['cid'],
            content=df.iloc[i]['text'],
            relevance=float(similarities[i])
            # TODO: Adicionar link pra ver o site no bsky.app
        )
        for i in indices
    ]
    
    return QueryResult(results=results, message="OK")

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=3000)