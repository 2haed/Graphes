import asyncio
import csv
import json
from config import token
from typing import Optional
from aiovk import TokenSession, API
from aiovk.pools import AsyncVkExecuteRequestPool


async def load_users(filename="data.csv") -> dict:
    with open(filename, encoding='UTF-8-sig', newline='') as csv_file:
        data = csv.reader(csv_file)
        data_dict = {" ".join(row).split(';')[0]: " ".join(row).split(';')[1] for row in data}
    return data_dict


async def get_api() -> API:
    session = TokenSession(access_token=token)
    return API(session)


async def get_friend_list(user_id: str, vk: API) -> tuple[Optional[dict], bool]:
    try:
        return await vk.friends.get(user_id=user_id, order="random")['items'], True
    except Exception:
        return None, False


async def fetch_users(data_dict: dict) -> dict:
    responses = {}
    async with AsyncVkExecuteRequestPool() as pool:
        for user_id in data_dict.values():
            responses[user_id] = (pool.add_call("friends.get", token, {"user_id": user_id, "order": "random"}))
    return {user_id: response.result["items"] for user_id, response in responses.items() if response.ok}


async def fetch_more_users(data_dict: dict) -> dict:
    responses = {}
    async with AsyncVkExecuteRequestPool() as pool:
        for user_id in sum([x for x in data_dict.values()],[]):
            try:
                responses[user_id] = (pool.add_call("friends.get", token, {"user_id": user_id, "order": "random"}))
            except Exception:
                await asyncio.sleep(0.1)
                pass
    return {user_id: response.result["items"] for user_id, response in responses.items() if response.ok}


async def save_users(data_dict: dict):
    with open('ready_data.json', 'w') as json_file:
        json.dump(await fetch_users(data_dict), json_file, indent=4)


async def main() -> None:
    users = await load_users()
    first_iter = await fetch_users(users)
    second_iter = await fetch_more_users(first_iter)
    await save_users(second_iter)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    main_future = asyncio.ensure_future(main())
    loop.run_until_complete(main_future)
    asyncio.set_event_loop(loop)
