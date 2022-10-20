import operator
import networkx as nx
import json
import vk_api
from config import token
import matplotlib.pyplot as plt


session = vk_api.VkApi(token=token)
vk = session.get_api()


def user_finder(user_id):
    return f"{vk.users.get(user_id=user_id)[0]['first_name']} {vk.users.get(user_id=user_id)[0]['last_name']}"


def count_degree_centralities(G):
    dictionary = nx.degree_centrality(G)
    sorted_tuples = sorted(dictionary.items(), key=operator.itemgetter(1), reverse=True)
    return {k: v for k, v in sorted_tuples}


with open('ready_data.json', 'r') as json_file:
    data = json.load(json_file)
    for key, val in data.items():
        data[key] = tuple(val)
    G = nx.DiGraph(data)
    centralities_dict = {key: str(round(val*100, 2))+'%' for key, val in count_degree_centralities(G).items()}
    closeness_dict = nx.betweenness_centrality(G)
    print(closeness_dict)
    # print(f'Max degree centrality equals: {user_finder(next(iter(count_degree_centralities(G))))}')
    # print(f'Degree centralities: {centralities_dict}')

