import requests
import datetime
import asyncio
import aiohttp
from models import Swapi, init_models, Session, engine
from more_itertools import chunked


MAX_CHUNK = 10

async def get_people(pers_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://swapi.py4e.com/api/people/{pers_id}/') as response:
            json_data = await response.json()
            return json_data


async def get_films(pers_id):
        json_data = await get_people(pers_id)
        if json_data is None:
            pass
        else:
            films_urls = json_data.get('films')
            films_list = []
            for films_url in films_urls:
                async with aiohttp.ClientSession() as session:
                    async with session.get(films_url) as response:
                        about_film = await response.json()
                        films_list.append(about_film.get('title'))

        films = ', '.join(films_list)
        return films


async def get_species(pers_id):
    json_data = await get_people(pers_id)
    species_urls = json_data.get('species')
    species_list = []
    for species_url in species_urls:
        async with aiohttp.ClientSession() as session:
            async with session.get(species_url) as response:
                about_species = await response.json()
                species_list.append(about_species.get('name'))

    species = ', '.join(species_list)
    return species


async def get_starships(pers_id):
    json_data = await get_people(pers_id)
    starships_urls = json_data.get('starships')
    starships_list = []
    for starships_url in starships_urls:
        async with aiohttp.ClientSession() as session:
            async with session.get(starships_url) as response:
                about_starships = await response.json()
                starships_list.append(about_starships.get('name'))

    starships = ', '.join(starships_list)
    return starships


async def get_vehicles(pers_id):
    json_data = await get_people(pers_id)
    vehicles_urls = json_data.get('vehicles')
    vehicles_list = []
    for vehicles_url in vehicles_urls:
        async with aiohttp.ClientSession() as session:
            async with session.get(vehicles_url) as response:
                about_vehicles = await response.json()
                vehicles_list.append(about_vehicles.get('name'))

    vehicles = ', '.join(vehicles_list)
    return vehicles


async def get_data():
    coroutines = [get_people(person) for person in range(1, 11)]
    persons = await asyncio.gather(*coroutines)
    coroutines_films = [get_films(person) for person in range(1, 11)]
    films = await asyncio.gather(*coroutines_films)
    coroutines_species = [get_species(person) for person in range(1, 11)]
    species = await asyncio.gather(*coroutines_species)
    coroutines_starships = [get_starships(person) for person in range(1, 11)]
    starships = await asyncio.gather(*coroutines_starships)
    coroutines_vehicles = [get_vehicles(person) for person in range(1, 11)]
    vehicles = await asyncio.gather(*coroutines_vehicles)
    counter = 0
    list = []
    for person in persons:
        person_data = dict(birth_year=person.get('birth_year'),
                               eye_color=person.get('eye_color'),
                               gender=person.get('gender'),
                                hair_color=person.get('hair_color'),
                                height=person.get('height'),
                                mass=person.get('mass'),
                                name=person.get('name'),
                                skin_color=person.get('skin_color'),
                                homeworld=person.get('homeworld'),
                                films=films[counter],
                                species=species[counter],
                                starships=starships[counter],
                                vehicles=vehicles[counter])
        counter += 1
        list.append(person_data)
    return list



async def main_insert_people():
    await init_models()
    person_data = await get_data()
    # print(person_data)
    async with Session() as session:
        orm_objects = [Swapi(birth_year=person['birth_year'],
                             eye_color=person['eye_color'],
                             films_list=person['films'],
                             gender=person['gender'],
                             hair_color=person['hair_color'],
                             height=person['height'],
                             homeworld=person['homeworld'],
                             mass=person['mass'],
                             name=person['name'],
                             skin_color=person['skin_color'],
                             species_list=person['species'],
                             starships_list=person['starships'],
                             vehicles_list=person['vehicles']) for person in person_data]
        session.add_all(orm_objects)
        await session.commit()



# async def main():
#     # await init_models()
#     async with aiohttp.ClientSession() as session:
#         p_ids = chunked(range(1, 101), MAX_CHUNK)
#         for p_ids_ch in p_ids:
#             coroutines = [get_people(p_id, session) for p_id in p_ids_ch]
#             results = await asyncio.gather(*coroutines)
#             asyncio.create_task(insert_people(results))
#             # print(results)
#         main_task = asyncio.current_task()
#         all_tasks = asyncio.all_tasks()
#         all_tasks.remove(main_task)
#         await asyncio.gather(*all_tasks)



# asyncio.run(insert_people(datata))
# asyncio.run(get_data())
# asyncio.run(get_species(1))
# asyncio.run(get_films_03())
# asyncio.run(get_starships(1))
# asyncio.run(get_vehicles(1))
asyncio.run(main_insert_people())


