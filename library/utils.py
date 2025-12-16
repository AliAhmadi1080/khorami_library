from sklearn.metrics.pairwise import cosine_similarity
from .models import Loan, Book
import numpy as np


def get_user_embedding(user):
    book_ids = Loan.objects.filter(
        user=user, is_return=True).values_list("book_id", flat=True)
    if len(book_ids) < 1:
        return False
    embeddings = Book.objects.filter(
        id__in=book_ids).values_list("embedding", flat=True)

    if not embeddings:
        return False
    embeddings = [np.array(vec) for vec in embeddings]
    avg_embedding = np.mean(embeddings, axis=0)
    return avg_embedding


def get_similar_books(user_embedding, user, top_n=5):
    read_book_ids = Loan.objects.filter(
        user=user,
        is_return=True 
    ).values_list("book_id", flat=True)

    all_books = Book.objects.exclude(id__in=read_book_ids)

    similarities = []

    for be in all_books:
        book_vector = np.array(be.embedding)
        try:
            sim = cosine_similarity([user_embedding], [book_vector])[0][0]
        except:
            continue
        similarities.append((be.id, sim))

    similarities.sort(key=lambda x: x[1], reverse=True)
    return [Book.objects.get(id=book) for book, score in similarities[:top_n]]
