import os
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
        """
            Terminar de probar porque ubo fallas por tantas peticiones
        """
        summoner = self.start()
        summoner_id = summoner['id']
        url = f'https://la1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{summoner_id}'
        response = requests.get(url, headers=self.headers)

        champion_data = response.json()[0]
        champion_id = champion_data['championId']
        res = requests.get('http://ddragon.leagueoflegends.com/cdn/11.6.1/data/en_US/champion.json')
        data = res.json()['data']

        champion_name = None
        for x, y in data.items():
            key = int(y.get('key', 1))
            if key == champion_id:
                champion_name = y.get('name')
        # champion_name = [y.get('name') for x, y in data.items() if int(y.get('key', 1)) == champion_id]

        resp = requests.get(f'http://ddragon.leagueRoflegends.com/cdn/11.6.1/data/en_US/champion/{champion_name}.json')
        d = resp.json()['data']

        skin_num = []
        for x, y in d.items():
            for s in y.get('skins'):
                skin_num.append(s.get('num'))

        skin_r = random.choice(skin_num)
        skin_url = f'http://ddragon.leagueoflegends.com/cdn/img/champion/loading/{champion_name}_{skin_r}.jpg'
        return {'name': champion_name, 'lvl': champion_data['championLevel'], 'skin_url': skin_url}