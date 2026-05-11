from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
from langchain_ollama import OllamaLLM

from qdrant_client.http.exceptions import UnexpectedResponse

import json
import re


COLLECTION_NAME = "resume_rag"

QDRANT_URL = "http://qdrant:6333"

OLLAMA_MODEL = "qwen2.5:1.5b"

OLLAMA_URL = "http://ollama:11434"


embedding_model = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5"
)


llm = OllamaLLM(
    model=OLLAMA_MODEL,
    base_url=OLLAMA_URL,
    temperature=0
)


def get_retriever():

    try:

        vector_db = QdrantVectorStore.from_existing_collection(
            embedding=embedding_model,
            url=QDRANT_URL,
            collection_name=COLLECTION_NAME,
        )

        return vector_db.as_retriever(
            search_type="mmr",
            search_kwargs={"k": 5}
        )

    except UnexpectedResponse:

        return None


def clean_json(text: str):

    text = text.strip()

    text = re.sub(r"^```json", "", text)

    text = re.sub(r"```$", "", text)

    return text.strip()


def extract_skills(text: str):

    prompt = f"""
Extract all technical skills from the text.

Return ONLY valid JSON array.

Text:
{text}
"""

    response = llm.invoke(prompt)

    return json.loads(
        clean_json(response)
    )


def analyze_job(job_description: str):

    retriever = get_retriever()

    if retriever is None:

        return {
            "error":
            "Please upload resume first"
        }

    docs = retriever.invoke(
        job_description
    )

    context = "\n\n".join(
        doc.page_content
        for doc in docs
    )

    jd_skills = [
        skill.lower()
        for skill in extract_skills(
            job_description
        )
    ]

    resume_skills = [
        skill.lower()
        for skill in extract_skills(
            context
        )
    ]

    matched_skills = list(
        set(jd_skills)
        &
        set(resume_skills)
    )

    missing_skills = list(
        set(jd_skills)
        -
        set(resume_skills)
    )

    score = (
        int(
            (
                len(matched_skills)
                /
                len(jd_skills)
            ) * 100
        )
        if jd_skills
        else 50
    )

    prompt = f"""
You are a resume evaluator.

Resume Context:
{context}

Job Description:
{job_description}

Matched Skills:
{matched_skills}

Missing Skills:
{missing_skills}

Write a concise professional summary.

Do not generate score.
Do not generate skill lists.
"""

    summary = llm.invoke(prompt)

    return {
        "score": score,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "summary": summary.strip()
    }