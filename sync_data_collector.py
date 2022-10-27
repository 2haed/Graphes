import csv
import json
from data.config import token, base_url
import requests


def load_users(filename="data/data.csv") -> list:
    with open(filename, encoding='UTF-8-sig', newline='') as csv_file:
        data = csv.reader(csv_file)
        id_list = [" ".join(row).split(';')[1] for row in data]
    return id_list


def save_our_group(dictionary) -> None:
    with open('data/group.json', 'w') as json_file:
        json.dump(dictionary, json_file, indent=4)


def fetch_users():
    data_dict = load_users()
    json_dict = {}
    for user_id in data_dict:
        request = requests.get(f"{base_url}/friends.get?user_id={user_id}&access_token={token}&v=5.131").json()
        if list(request.items())[0][0] != 'error':
            json_dict[user_id] = request['response']['items']
            for friend_of_user in request['response']['items']:
                new_request = requests.get(
                    f"{base_url}/friends.get?user_id={friend_of_user}&access_token={token}&v=5.131").json()
                if list(new_request.items())[0][0] != 'error':
                    json_dict[friend_of_user] = new_request['response']['items']
                else:
                    continue
        else:
            continue
    return json_dict


def main():
    save_our_group(fetch_users())


if __name__ == '__main__':
    main()
