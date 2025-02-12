import requests
import xml.etree.ElementTree as ET
import json


def fetch_pubmed_data(query):
    # ESearch URL
    esearch_url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi'
    efetch_url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi'

    # ESearch parameters
    esearch_params = {
        'db': 'pubmed',
        'term': query,
        'retmax': 10,  # Number of records to return
        'retmode': 'xml'  # Return XML format
    }

    # Perform ESearch
    response = requests.get(esearch_url, params=esearch_params)
    if response.status_code == 200:
        root = ET.fromstring(response.content)
        idlist = [el.text for el in root.findall('.//IdList/Id')]

        print(f"Found {len(idlist)} articles.")

        # EFetch parameters
        efetch_params = {
            'db': 'pubmed',
            'id': ','.join(idlist),  # Comma-separated list of article IDs
            'retmode': 'xml'  # Return XML format
        }

        # Perform EFetch
        response = requests.get(efetch_url, params=efetch_params)
        if response.status_code == 200:
            # Parse XML response
            root = ET.fromstring(response.content)
            articles = []
            for article in root.findall('.//PubmedArticle'):
                # Extract article details
                article_data = {
                    'title': article.find('.//ArticleTitle').text if article.find(
                        './/ArticleTitle') is not None else 'No title available',
                    'authors': [],
                    'abstract': 'No abstract available'
                }
                for author in article.findall('.//Author'):
                    lastname = author.find('LastName')
                    firstname = author.find('ForeName')
                    initials = author.find('Initials')
                    if lastname is not None:
                        full_name = lastname.text
                        if firstname is not None:
                            full_name += ' ' + firstname.text
                        if initials is not None:
                            full_name += ' ' + initials.text
                        article_data['authors'].append(full_name)
                abstracts = article.findall('.//AbstractText')
                if abstracts:
                    article_data['abstract'] = ' '.join(
                        abstext.text for abstext in abstracts if abstext.text is not None)

                articles.append(article_data)

            # Save to JSON file
            with open('pubmed_search_results.json', 'w') as json_file:
                json.dump(articles, json_file, indent=4)

            print("Results saved to pubmed_search_results.json")
        else:
            print('Failed to fetch article details.')
    else:
        print('Failed to search PubMed.')


if __name__ == "__main__":
    query = input("Enter your search query: ")
    fetch_pubmed_data(query)