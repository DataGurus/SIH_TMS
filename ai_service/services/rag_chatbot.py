import redis
import time
from langchain.vectorstores import FAISS
from langchain.docstore.document import Document
from langchain.embeddings import HuggingFaceEmbeddings
import pandas as pd
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from google import genai

# Connect to local Redis server
r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

CACHE_KEY = "query_cache"
CACHE_TTL = 120  # Time window in seconds

def add_query_to_cache(query: str):
    cached = r.get(CACHE_KEY)

    if cached:
        concatenated = cached + " | " + query
        r.set(CACHE_KEY, concatenated, ex=CACHE_TTL)
    else:
        r.set(CACHE_KEY, query, ex=CACHE_TTL)

def get_aggregated_query():
    return r.get(CACHE_KEY)

def clear_cache():
    r.delete(CACHE_KEY)


# Load dataset
df = pd.read_csv(r'C:\Users\Rahul\Documents\Project\tourist_management\ai_service\services\rag_knowledge_base.csv')

# Initialize embedding model using LangChain wrapper
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Prepare documents for FAISS
documents = []
for _, row in df.iterrows():
    content = " | ".join([
        row['user_age_group'],
        row['user_gender'],
        row['user_mobility'],
        row['time_part_of_day'],
        row['time_official_hours'],
        row['location'],
        str(row['constraints_triggered']),  # Convert list to string
        row['event_type'],
        row['event_detail'],
    ])
    metadata = {"solution_required": row['solution_required']}
    documents.append(Document(page_content=content, metadata=metadata))

# Build FAISS index
vector_store = FAISS.from_documents(documents, embedding_model)

# Save FAISS index locally
vector_store.save_local('faiss_minilm_index')

"""All info stored in FAISS successfully

Now define all query handling functions - for static, dynamic
"""

# Initialize embedding model
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Load FAISS index safely
vector_store = FAISS.load_local(
    'faiss_minilm_index',
    embedding_model,
    allow_dangerous_deserialization=True
)

# Initialize Gemma API Client
client = genai.Client(api_key='YOUR_GEMMA_API_KEY')


def restructure_solution(solution_text):
    prompt = f"""
You are an expert travel assistant specialized in simplifying technical and unstructured information into clear and actionable advice.

The following are multiple raw solutions retrieved from a knowledge database in response to a user query:

\"\"\"
{solution_text}
\"\"\"

Your task is to:
1. Rephrase and merge these solutions into a coherent, concise, and easy-to-understand paragraph.
2. Eliminate redundancy and irrelevant details.
3. Focus on practical, actionable steps or important information that the user can immediately follow.

Output the rephrased result as a concise paragraph without bullet points or numbered lists, written in simple language suitable for any tourist.

Final concise solution:
"""
    try:
        response = client.models.generate_content(
            model="gemma-3-27b-it",
            contents=prompt
        )
        return response.text.strip()
    except Exception as e:
        print(f"Error calling Gemma API: {e}")
        return "Failed to restructure solution"

def service_get_rag_response(user_query: str) -> str:
    """
    Handles user queries by aggregating recent queries from Redis cache,
    retrieving static info from FAISS, and generating a final response using Gemma.
    """
    print(f"\n[INFO] Handling user query: {user_query}")

    print("Retrieving static information from FAISS knowledge base...")
    docs = vector_store.similarity_search(user_query, k=5)

    if not docs:
        return "No relevant static information found."

    # Combine top k retrieved solutions into a single block
    combined_solutions = "\n\n".join(
        f"Solution #{i+1}: {doc.metadata.get('solution_required', 'No solution found')}"
        for i, doc in enumerate(docs)
    )

    print("Restructuring combined solutions into concise actionable format...")
    concise_solution = restructure_solution(combined_solutions)

    return concise_solution
