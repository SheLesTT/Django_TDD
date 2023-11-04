from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home_page(request):


    resp = render(request, "home.html", {"new_text_item": request.POST.get("item_text", "")})
    # print("I am resp", resp.content.decode())
    return resp
    # pass