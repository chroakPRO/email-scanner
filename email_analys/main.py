import sys
import os 
import argparse
import re
from bs4 import BeautifulSoup

current_links = []
indexed_words = []
good_links = []
warnings = []

def fill_good_links(filename):
    with open(filename, 'r') as f:
        good_links.append(f)
    

def scan_links(list_of_links):

    # Printing the list of links to check for formarting
    print(list_of_links)
    print(index_words)
    print(good_links)
    print(warnings)
    state = False
    for i in list_of_links:
        if "http" in i or "https" in i:
            for j in good_links:
                if j in i:
                    state = True
                else: continue

            if state is True:
                break
            elif state is False:
                warnings.append("Unkown Links in Email.")

                    
def get_links(filename):
    try:
        with open('filname', 'rw') as source:
            soup = bs.BeautifulSoup(source, 'lxml')
        #Find all the href links in the source code.
            links = [link.get('href') for link in soup.find_all('a')]
        #Remove outgoing links, only keep local links.
            for link in links:
                if filename in link:
                    #if filename is in link, add to list.
                    current_links.append(link)
                elif not 'http' in link:
                    #if name has a . or / add to list
                    if '/' in link[0] or '.' in link[0]:
                        new_link = ''.join([filename,link])
                        current_links.append(new_link)
                    #if not, add / to item and then add to list.
                    else:
                        new_link = ''.join([filename,'/',link])
                        current_links.append(new_link)
                else:
                    pass
    #check if errors.
    except TypeError as e:
        print(e)
        print("Got a Typerror")
        return []
    except IndexError as e:
        print(e)
        return []
    except AttributeError as e:
        print(e)
        return []
    #Instead of dispalying the error, put into error log.
    except Exception as e:
        with open('error.txt', 'w') as f:
            f.write(str(e))
        return[]


def index_file(email):
    
    # Isolating format.
    file_format = email.split(".") 
    print(file_format)

    if file_format[1] == "txt":
        # Indexing index_words
        with open(email, "r") as f:
            for line in f:
                indexed_words.extend(line.split())

        for i in index_words:
            if "http" in i or "https" in i:
                current_links.append(i)


    elif file_format[1] == "html":
        print("Check html code")
        get_links(email)
    else:
        # Indexing index_words
        with open(email, "r") as f:
            for line in f:
                indexed_words.extend(line.split())
        
        for i in index_words:
            if "http" in i or "https" in i:
                current_links.append(i)

def main():
    parser = argparse.ArgumentParser(description='Phising email analyser')
    #Add group so either U or u is required.
    group = parser.add_mutually_exclusive_group(required=True)
    #Arg for list of urls
    group.add_argument('--file', '-F', metavar="",help='Input location to list with urls, 1 url per line. Eample -U ~/folder/list.txt')
    #Single url. (https://google.coom)
    parser.add_argument('--processes', '-p',metavar="",type=int, help='Type how many processes you wanna run. Empty = max, which is the amount of links scraped.')
    args = parser.parse_args()

    fill_good_links("safe_links.txt")
    index_file(args.file)
    scan_links(current_links)

if __name__ == "__main__":
    main()