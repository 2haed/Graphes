import operator
import networkx as nx
import json
from matplotlib import pyplot as plt
from data.config import token, base_url
import requests


def draw_graph(G):
    nx.draw(G, with_labels=True)
    plt.show()


def user_finder(user_id: str) -> str:
    return requests.get(f"{base_url}/users.get?user_id={user_id}&access_token={token}&v=5.131").json()['response'][0][
               'first_name'] + " " + \
           requests.get(f"{base_url}/users.get?user_id={user_id}&access_token={token}&v=5.131").json()['response'][0][
               'last_name']


def count_centrality(function, G) -> dict:
    dictionary = function(G)
    sorted_tuples = sorted(dictionary.items(), key=operator.itemgetter(1), reverse=True)
    return {key: val for key, val in sorted_tuples}


def get_max_user(dictionary) -> str:
    return f'Max degree centrality equals: {user_finder(next(iter(dictionary)))}'


def get_all_centralities(G):
    centralities_dict = count_centrality(lambda x: nx.degree_centrality(G), G)
    closeness_centrality = count_centrality(lambda x: nx.closeness_centrality(G), G)
    betweeness_centrality = count_centrality(lambda x: nx.betweenness_centrality(G, k=10), G)
    eigenvector_centrality = count_centrality(lambda x: nx.eigenvector_centrality(G), G)
    page_rank = count_centrality(lambda x: nx.pagerank(G), G)

    print(
        f'Degree centrality: {get_max_user(centralities_dict)}, {list(centralities_dict.items())[:5]}...\n'
        f'Closeness centrality: {get_max_user(closeness_centrality)}, {list(closeness_centrality.items())[:5]}...\n'
        f'Betweeness centrality: {get_max_user(betweeness_centrality)}, {list(betweeness_centrality.items())[:5]}...\n'
        f'Eigenvector centrality: {get_max_user(eigenvector_centrality)}, {list(eigenvector_centrality.items())[:5]}...\n'
        f'Page Rank: {get_max_user(page_rank)}, {list(page_rank.items())[:5]}...')


def main():
    with open('data/group.json', 'r') as json_file:
        data = json.load(json_file)
        data = {key: tuple(val) for key, val in data.items()}
    G = nx.DiGraph(data)
    get_all_centralities(G)


if __name__ == '__main__':
    main()
