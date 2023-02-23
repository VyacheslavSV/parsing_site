import json

import requests
from bs4 import BeautifulSoup

URL_PERSON_SITE = 'https://www.bundestag.de' \
                  '/ajax/filterlist/en/members/863330-863330?limit=20&noFilterSet=true&offset={i}'
FILE_PERSON_LIST = 'persons_url_list.txt'


def soup_funktion(url) -> BeautifulSoup:
    """
   Returns a BeautifulSoup object from a given URL using the 'lxml' parser.
   Args: str
   Returns: BeautifulSoup
   """
    return BeautifulSoup(requests.get(url).content, 'lxml')


def parser_person_in_page() -> list[str]:
    """
    Parses the persons page and returns a list of URLs for each person's page.
    Returns: list[str]
    """
    persons_list = []
    for i in range(0, 740, 20):
        url = URL_PERSON_SITE
        soup = soup_funktion(url)
        persons = soup.find_all('a')

        for person in persons:
            persons_page_url = person.get('href')
            persons_list.append(persons_page_url)
    return persons_list


def save_file_with_persons_list(persons_list: list[str]) -> None:
    """
    Saves the given list of URLs to a file.
    Args: list[str]
    """
    with open(FILE_PERSON_LIST, 'a') as file:
        for line in persons_list:
            file.write(f'{line}\n')


def read_file_person_list() -> list[str]:
    """
    Reads the saved list of URLs from the file and returns them as a list.
    Returns: list[str]
    """
    with open(FILE_PERSON_LIST) as file:
        lines = [line.strip() for line in file]
        return lines


def parser_person_page(lines: list[str]) -> list[dict[str, list[str]]]:
    """
    Parses each person's page from the given list of URLs and returns a list of
    dictionaries containing their name, company, and social network URLs.
    Args: list[str]
    Returns:list[dict[str, list[str]]]
    """
    data_list = []
    for line in lines:
        soup = soup_funktion(line)
        person_info = soup.find(
            'div', {
                'class': 'col-xs-8 col-md-9 bt-biografie-name'}).find('h3').text
        person_name_company = person_info.strip().split(', ')
        person_name = person_name_company[0]
        person_company = person_name_company[1]
        social_networks = soup.find_all('a', {'class': "bt-link-extern"})
        social_networks_url = []
        for item in social_networks:
            social_networks_url.append(item.get('href'))
        data = {
            'person_name': person_name,
            'person_company': person_company,
            'social_networks_url': social_networks_url,
        }
        data_list.append(data)
    return data_list


def create_json_file(data_list: list[dict[str, list[str]]]) -> None:
    """
    Creates a JSON file with the given data.
    Args: list[dict[str, list[str]]]
    """
    with open('data.json', 'w') as json_file:
        json.dump(data_list, json_file, indent=3)


def starts_cod_to_parse():
    """
    Runs the entire script to parse information from a website and save it to a JSON file.
    """
    persons_list = parser_person_in_page()
    save_file_with_persons_list(persons_list)
    lines = read_file_person_list()
    data_list = parser_person_page(lines)
    create_json_file(data_list)
    print('File Json create')


if __name__ == "__main__":
    starts_cod_to_parse()
