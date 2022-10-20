import operator
import networkx as nx
import json
import vk_api
from config import token
import matplotlib.pyplot as plt


session = vk_api.VkApi(token=token)
vk = session.get_api()


def user_finder(user_id: str) -> str:
    return f"{vk.users.get(user_id=user_id)[0]['first_name']} {vk.users.get(user_id=user_id)[0]['last_name']}"


def count_centrality(function) -> dict:
    dictionary = function(G)
    sorted_tuples = sorted(dictionary.items(), key=operator.itemgetter(1), reverse=True)
    return {key: val for key, val in sorted_tuples}


def get_all_centralities(G):
    centralities_dict = count_centrality(lambda x: nx.degree_centrality(G))
    closeness_centrality = count_centrality(lambda x: nx.closeness_centrality(G))
    betweeness_centrality = count_centrality(lambda x: nx.betweenness_centrality(G))
    eigenvector_centrality = count_centrality(lambda x: nx.eigenvector_centrality(G))
    PageRank = count_centrality(lambda x: nx.pagerank(G))
    print(f'Max degree centrality equals: {user_finder(next(iter(centralities_dict)))}')
    print(
        f'Degree centrality: {centralities_dict}\n'
        f'Closeness centrality: {closeness_centrality}\nBetweeness centrality:{betweeness_centrality}\n'
        f'Eigenvector centrality: {eigenvector_centrality}\nPage Rank: {PageRank}')


with open('ready_data.json', 'r') as json_file:
    data = json.load(json_file)
    data = {key: tuple(val) for key, val in data.items()}

G = nx.DiGraph(data)
get_all_centralities(G)
