from django.core.management.base import BaseCommand
from library.models import Book, BookEmbedding
from openai import OpenAI
import os
from tqdm import tqdm

token = os.environ.get('GITHUB_TOKEN')
endpoint = "https://models.github.ai/inference"

client = OpenAI(
    base_url=endpoint,
    api_key=token,
)

def get_batch_embeddings(texts, model="text-embedding-3-small"):
    try:
        response = client.embeddings.create(
            input=texts,
            model=model
        )
        return [item.embedding for item in response.data]
    except Exception as e:
        return [None] * len(texts)

BATCH_SIZE = 20

class Command(BaseCommand):
    help = "generate 1-to-1 embedding for all Book objects (batch version)"

    def handle(self, *args, **options):
        books = list(Book.objects.all().exclude(bookembedding__isnull=False))
        for i in tqdm(range(0, len(books), BATCH_SIZE)):
            batch_books = books[i:i+BATCH_SIZE]
            names = [book.name for book in batch_books]
            embeddings = get_batch_embeddings(names)

            for book, vector in zip(batch_books, embeddings):
                if vector:
                    BookEmbedding.objects.create(book=book, vector=vector)
