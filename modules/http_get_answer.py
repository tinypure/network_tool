import subprocess  # For executing a shell command
import requests

def http_get_answer(request):
    return requests.get(url="http://127.0.0.1:5000/get?msg="+request).text.replace("<br>", "\n")