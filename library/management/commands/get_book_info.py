from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
from azure.ai.inference import ChatCompletionsClient
from django.core.management.base import BaseCommand
from django.conf import settings
from library.models import Book
from json import loads
from tqdm import tqdm
import os

endpoint = "https://models.github.ai/inference"
token = os.environ.get('GITHUB_TOKEN')


client = ChatCompletionsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(token),
)

def get_book_info(text, model="meta/Meta-Llama-3.1-8B-Instruct"):
    response = client.complete(
        messages=[
            SystemMessage(str(settings.BOOK_INFO_SYSTEM_PROMPT)),
            UserMessage(text),
        ],
        temperature=0.5,
        top_p=1.0,
        max_tokens=4096,
        model=model
        )
    return response.choices[0].message.content

BATCH_SIZE = 25

class Command(BaseCommand):
    help = "get books info."

    def handle(self, *args, **options):
        books = list(Book.objects.filter(complited=False))
        for i in tqdm(range(0, len(books), BATCH_SIZE), desc="Processing books with LLM"):
            batch = books[i:i+BATCH_SIZE]
            prompt_lines = [f'id={b.id}, name="{b.name}"' for b in batch]
            prompt = "\n".join(prompt_lines)
            result = get_book_info(prompt)
            try:
                book_infos = loads(result)
            except Exception as e:
                print("LLM output JSON error:", e)
                continue
            for infos in book_infos:
                try:
                    id = infos['id']
                    title = infos['title']
                    author = infos['author']
                    publisher = infos['publisher']
                    year = infos['year']
                    notes = infos['notes']
                    book = Book.objects.get(id=id)
                    book.title = title
                    book.publisher = publisher
                    book.year = year
                    book.notes = notes
                    book.author = author
                except Exception as e:
                    print(e)
                book.complited = True
                book.save()

                
            
