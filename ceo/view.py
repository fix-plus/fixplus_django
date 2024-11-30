from django.http import HttpResponse
import os


def robots_txt(request):
    file_path = os.path.join(os.path.dirname(__file__), '..', 'ceo', 'robots.txt')
    with open(file_path, 'r') as file:
        content = file.read()
    return HttpResponse(content, content_type='text/plain')


