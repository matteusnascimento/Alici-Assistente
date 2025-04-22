
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')

# Base de conhecimento simples
faq = {
    "qual seu nome?": "Meu nome é Alici, sua assistente virtual!",
    "o que você faz?": "Sou uma IA capaz de te ajudar a automatizar redes sociais e responder mensagens.",
}

faq_embeddings = {q: model.encode(q, convert_to_tensor=True) for q in faq}

def generate_response(user_input):
    query_embedding = model.encode(user_input, convert_to_tensor=True)
    best_match = None
    best_score = 0.0
    for question, embedding in faq_embeddings.items():
        score = util.pytorch_cos_sim(query_embedding, embedding).item()
        if score > best_score:
            best_score = score
            best_match = question
    return faq.get(best_match, "Desculpe, ainda não entendi como responder isso.")
