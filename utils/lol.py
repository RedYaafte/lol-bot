import os
import json
import random
import requests
from dotenv import load_dotenv


class LolSettings:
    load_dotenv()
    def __init__(self, summoner, region):
        self.summoner = summoner
        self.region = region
        self.headers = {'X-Riot-Token': os.getenv('TOKEN_LOL')}
    
    def start(self):
        url = f'https://la1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{self.summoner}'
        response = requests.get(url, headers=self.headers)
        return response.json()


class Lol(LolSettings):
    def __init__(self, summoner, region):
        super().__init__(summoner, region)

    def greetings(self):
        summoner = self.start()
        name = summoner['name']
        lvl = summoner['summonerLevel']
        icon_id = summoner['profileIconId']

        greetings = f'Saludos invocador {name}, lvl {lvl}'
        icon_url = f'https://ddragon.leagueoflegends.com/cdn/11.6.1/img/profileicon/{icon_id}.png'
        return {'greetings': greetings, 'icon_url': icon_url}

    def ranks(self):
        pass

    def champion_mastery(self):
        summoner = self.start()
        summoner_id = summoner['id']
        url = f'https://la1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{summoner_id}'
        response = requests.get(url, headers=self.headers)
        champion_data = response.json()[0]
        champion_id = champion_data['championId']

        # For this step, do you need download  latest data dragon for https://developer.riotgames.com/docs/lol
        with open('es_MX/champion.json') as json_file: 
            data = json.load(json_file)

        champion_name = None
        for x, y in data['data'].items():
            key = int(y.get('key', 1))
            if key == champion_id:
                champion_name = y.get('name')

        with open(f'es_MX/champion/{champion_name}.json') as json_file: 
            d = json.load(json_file)

        skin_num = []
        for x, y in d['data'].items():
            for s in y.get('skins'):
                skin_num.append(s.get('num'))

        skin_r = random.choice(skin_num)
        skin_url = f'http://ddragon.leagueoflegends.com/cdn/img/champion/loading/{champion_name}_{skin_r}.jpg'
        return {
            'name': champion_name, 'lvl': champion_data['championLevel'],
            'points': champion_data['championPoints'], 'skin_url': skin_url}