from django.shortcuts import render
import googlesearch as gs
import requests as rq
from bs4 import BeautifulSoup as bs


def search(request):

    if "search_query" in request.GET:
        query = request.GET["search_query"]
        final_data = {}
        data = gs.search(query, num=10, stop=10, pause=2)
        i = 0
        for link in data:
            single_data = {}
            try:
                reqs = rq.get(link)
                soup = bs(reqs.text, 'html.parser')
                title_data = soup.find_all('title')

                for title in title_data:
                    single_data['title'] = title.get_text()
                    single_data['link'] = link
            except rq.exceptions.ConnectionError as errc:
                print("Error Connecting:", errc)
            finally:
                pass

            if len(single_data) != 0:
                final_data[i] = single_data
                i = i + 1

        return render(request, 'search.html', context={"data": final_data, "query": query})

    else:
        return render(request, 'search.html', context={"data": "nothing"})

