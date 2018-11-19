# -*- coding: utf-8 -*-

import json, urllib, webbrowser

print("\n")
print("Loading...\n")

# MacOS
chrome_path = 'open -a /Applications/Google\ Chrome.app %s'

# Windows
# chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'

# Linux
# chrome_path = '/usr/bin/google-chrome %s'

batch_num = 5

action_urls = []
api_base = "http://api.indeed.com/ads/apisearch?publisher="
standard_q = "&limit=25&radius=25&userip=1.2.3.4&useragent=Mozilla/%2F4.0%28Firefox%29&v=2&format=json"

"""Go to indeed and find a search query you'd like to sift through"""

def set_batch():
    print("\nHow many auto-apply jobs would you like to open at once?")
    while True:
        batch_num = input("Enter Tab Open Count:  ")
        try:
            val = int(batch_num)
            if val > 0 and val < 26:
                break
            else:
                print("pick a number greater than 0 and less than 26")
        except ValueError:
            print("Amount must be a number, try again")
    return val

batch_num = set_batch()

print("\nPaste the search URL (e.g. https://www.indeed.com/jobs?q=sql&l=19009) you want to use")
search_query = input("Paste url here:  ")

print("\nNow we need a publisher API key below")
secret_key = input("Enter API key here:")

q = search_query.split('?q=',1)[1].replace('#','')
complete_url = api_base + secret_key + "&q=" + q + standard_q


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

with urllib.request.urlopen(complete_url) as q_result:
    print("\nRunning query for "+ q + "...\n")
    q_data = json.loads(q_result.read().decode())
    result_count = q_data['totalResults']
    number_pages =  int(round(result_count / 25, 0) + 1)

    """go to all pages and search through raw results"""
    for i in range(1, number_pages):
        page = (i*25)-25
        page_url = api_base + secret_key + "&q=" + q + standard_q + "&start=" + str(page)
        print("searching results from page "+ str(i) + "...\n")

        with urllib.request.urlopen(page_url) as p_result:
            page_data = json.loads(p_result.read().decode())
            page_results = page_data["results"]
            if len(page_results) > 0:
                for result in page_results:

                    # filter out those with no autoapply
                    if result["indeedApply"] is True:
                        target_url = result["url"]
                        if target_url not in action_urls:
                            action_urls.append(target_url)

    if len(action_urls) > 0:
        blocks = list(chunks(action_urls, batch_num))
        block_num = 0;
        print(" Opening " + str(batch_num) + " at a time. \n")
        for block in blocks:
            block_num += 1
            print("Press enter to open batch number " + str(block_num))
            bla = input()
            for block_url in block:
                webbrowser.get(chrome_path).open(block_url)
    else:
        print("No auto apply urls found")
