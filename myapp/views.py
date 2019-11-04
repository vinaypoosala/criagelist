from django.shortcuts import render
from bs4 import BeautifulSoup
from requests.compat import quote_plus
import requests
from .models import Search
BASE_CRIAGLIST_URL = "https://{}.craigslist.org/search/jjj?query={}"

# Create your views here.
def home(request):
    return render(request,template_name='base.html')
def new_search(request):
    if request.POST.get('location'):
        location = request.POST.get('location')
    else:
        location='hyderabad'    
    search = request.POST.get('search')
    Search.objects.create(search=search)
    final_url = BASE_CRIAGLIST_URL.format(location,search)
    #print(final_url)
    
    response = requests.get(final_url)
    data = response.text
    soup = BeautifulSoup(data,features='html.parser')
    post_listings = soup.find_all('li',{'class' :'result-row'})
    

    final_list=[]
    for post in post_listings:
        post_title = post.find(class_='result-title').text
        post_url = post.find('a').get('href')
        if post.find(class_='result-price'):
            post_price = post.find(class_='result-price').string
        else:
            post_price='N/A'
        final_list.append((post_title,post_price,post_url))
    #search_content = {'search':search, 'final_  list':final_list}
    #print(final_list)

    return render(request, 'myapp/new_search.html' , {'search':search,'final_list':final_list})    