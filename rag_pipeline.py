from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import ollama

# -----------------------------------
# Embedding Model
# -----------------------------------
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

# -----------------------------------
# Global Variables
# -----------------------------------
chunks = []
index = None


# -----------------------------------
# Chunking
# -----------------------------------
def chunk_text(text, chunk_size=500):

    return [
        text[i:i + chunk_size]
        for i in range(0, len(text), chunk_size)
    ]


# -----------------------------------
# Build Vector Database
# -----------------------------------
def build_vector_db(articles):

    global chunks, index

    chunks = []

    # Split articles into chunks
    for article in articles:

        article_chunks = chunk_text(article)

        chunks.extend(article_chunks)

    # Convert chunks into embeddings
    embeddings = embedding_model.encode(chunks)

    embeddings = np.array(embeddings).astype('float32')

    # Create FAISS index
    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)

    index.add(embeddings)


# -----------------------------------
# Retrieve Relevant Chunks
# -----------------------------------
def retrieve(query, k=5):

    global index

    # Prevent crash if no data loaded
    if index is None:

        return ["No news data loaded."]

    # Convert query into embedding
    query_embedding = embedding_model.encode([query])

    query_embedding = np.array(query_embedding).astype('float32')

    # Search similar chunks
    distances, indices = index.search(query_embedding, k)

    relevant_chunks = []

    for idx in indices[0]:

        if idx < len(chunks):

            relevant_chunks.append(chunks[idx])

    return relevant_chunks


# -----------------------------------
# Generate Answer using Ollama
# -----------------------------------
def generate_answer(query):

    relevant_chunks = retrieve(query)

    context = " ".join(relevant_chunks)

    prompt = f"""
    You are an intelligent AI news analyst.

    Answer ONLY using the provided context.

    Rules:
    - Be factual
    - Give concise answers
    - If answer not available in context, say:
      "I could not find enough news information."

    CONTEXT:
    {context}

    QUESTION:
    {query}

    ANSWER:
    """

    response = ollama.chat(
        model='llama3',
        messages=[
            {
                'role': 'user',
                'content': prompt
            }
        ]
    )

    return response['message']['content']


# -----------------------------------
# Extract Topic from Query
# -----------------------------------
def extract_topic(query):

    prompt = f"""
    Extract the main news topic from this query.

    Return ONLY the topic.

    Query:
    {query}
    """

    response = ollama.chat(
        model='llama3',
        messages=[
            {
                'role': 'user',
                'content': prompt
            }
        ]
    )

    topic = response['message']['content']

    return topic.strip()