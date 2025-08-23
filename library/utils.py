from sklearn.metrics.pairwise import cosine_similarity
from .models import Loan, BookEmbedding
import numpy as np


def get_user_embedding(user):
    book_ids = Loan.objects.filter(
        user=user, is_return=True).values_list("book_id", flat=True)
    if len(book_ids) < 1:
        return False
    embeddings = BookEmbedding.objects.filter(
        book_id__in=book_ids).values_list("vector", flat=True)

    if not embeddings:
        return False

    embeddings = [np.array(vec) for vec in embeddings]
    avg_embedding = np.mean(embeddings, axis=0)
    return avg_embedding


def get_similar_books(user_embedding, user, top_n=5):
    read_book_ids = Loan.objects.filter(
        user=user,
        is_return=True  # فقط کتاب‌هایی که واقعاً خونده و پس داده
    ).values_list("book_id", flat=True)

    all_books = BookEmbedding.objects.exclude(book_id__in=read_book_ids)

    similarities = []

    for be in all_books:
        book_vector = np.array(be.vector)
        sim = cosine_similarity([user_embedding], [book_vector])[0][0]
        similarities.append((be.book, sim))

    similarities.sort(key=lambda x: x[1], reverse=True)
    return [book for book, score in similarities[:top_n]]
