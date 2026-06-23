from groq import Groq
from dotenv import load_dotenv
import os
import json
import streamlit as st

load_dotenv()

try:
    api_key = st.secrets["GROQ_API_KEY"]
except:
    api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=api_key)

def generate_answer(question, relevant_chunks, language="English"):
    context = ""
    for chunk in relevant_chunks:
        context += f"Source: {chunk['filename']}\n"
        context += f"Content: {chunk['text']}\n\n"
    
    prompt = f"""You are a helpful assistant.
CRITICAL RULE 1: Answer using ONLY the context provided below.
CRITICAL RULE 2: Respond ONLY in {language} language.
CRITICAL RULE 3: Translate to {language} even if source is different language.
CRITICAL RULE 4: If answer not in context say "I cannot find this in the documents."

Context:
{context}

Question: {question}

Answer in {language}:"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000
    )
    
    return {
    "answer": response.choices[0].message.content,
    "sources": list(set([chunk['filename'] for chunk in relevant_chunks]))
    }


def summarize_document(text, filename, language="English"):
    length = len(text)
    sample = (
        text[:500] +
        text[length//4:length//4 + 500] +
        text[length//2:length//2 + 500] +
        text[-500:]
    )
    
    prompt = f"""Summarize this document in 2-3 sentences in {language} language.
Tell the user what topics it covers.

Filename: {filename}
Content: {sample}

Summary in {language}:"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500
    )
    
    return response.choices[0].message.content


def evaluate_answer(question, answer, relevant_chunks):
    context = ""
    for chunk in relevant_chunks:
        context += f"{chunk['text']}\n\n"
    
    prompt = f"""Evaluate this AI answer against source chunks.
    
Question: {question}
Answer: {answer}
Source: {context}

Respond in JSON only:
{{
    "faithfulness_score": <0-100>,
    "retrieval_quality": "<Good/Bad>",
    "diagnosis": "<one line>",
    "problem_area": "<Generation/Retrieval/None>"
}}"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200
    )
    
    try:
        text = response.choices[0].message.content.strip()
        text = text.replace("```json", "").replace("```", "")
        return json.loads(text)
    except:
        return {
            "faithfulness_score": 0,
            "retrieval_quality": "Unknown",
            "diagnosis": "Could not evaluate",
            "problem_area": "Unknown"
        }