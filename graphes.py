import operator
import networkx as nx
import json
import vk_api
from matplotlib import pyplot as plt
from config import token


def draw_graph(G):
    nx.draw(G, with_labels=True)
    plt.show()


def user_finder(user_id: str, vk) -> str:
    return f"{vk.users.get(user_id=user_id)[0]['first_name']} {vk.users.get(user_id=user_id)[0]['last_name']}"


def count_centrality(function, G) -> dict:
    dictionary = function(G)
    sorted_tuples = sorted(dictionary.items(), key=operator.itemgetter(1), reverse=True)
    return {key: val for key, val in sorted_tuples[:3]}


def get_all_centralities(G, vk):
    centralities_dict = count_centrality(lambda x: nx.degree_centrality(G), G)
    closeness_centrality = count_centrality(lambda x: nx.closeness_centrality(G), G)
    betweeness_centrality = count_centrality(lambda x: nx.betweenness_centrality(G), G)
    eigenvector_centrality = count_centrality(lambda x: nx.eigenvector_centrality(G), G)
    page_rank = count_centrality(lambda x: nx.pagerank(G), G)
    print(f'Max degree centrality equals: {user_finder(next(iter(centralities_dict)), vk)}')
    print(
        f'Degree centrality: {centralities_dict}...\n'
        f'Closeness centrality: {closeness_centrality}...\nBetweeness centrality: {betweeness_centrality}...\n'
        f'Eigenvector centrality: {eigenvector_centrality}...\nPage Rank: {page_rank}...')


def main():
    with open('ready_data.json', 'r') as json_file:
        data = json.load(json_file)
        data = {key: tuple(val) for key, val in data.items()}
    session = vk_api.VkApi(token=token)
    vk = session.get_api()
    G = nx.DiGraph(data)
    get_all_centralities(G, vk)
    draw_graph(G)


if __name__ == '__main__':
    main()
