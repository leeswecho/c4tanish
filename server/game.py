import json
import os
import shutil

from renderer import Renderer

class Game():
    def __init__(self, loc='state.json'):
        self.own_path = os.path.dirname(__file__)
        self.loc = loc
        with open(self.loc) as f:
          self.data = json.load(f)
          
    def add_player(self, name):
        player = self.create_player_struct(name)
        player = self.add_player_to_list(player)
        self.init_player_files(player['id'])

    def get_players(self):
        return self.data['players']
    
    def get_player_by_name(self,name):
        for i in range(0, len(self.data['players'])):
            if name == self.data['players'][i]['name']:
                return self.data['players'][i]
        return None

    def init_player_files(self,player_id):
        player = self.data['players'][player_id]
        player_path = os.path.join(self.own_path,'players',player['name'])
        template_path = os.path.join(self.own_path,'players','template')

        # remove any pre-existing folders
        if os.path.exists(player_path):
            shutil.rmtree(player_path, ignore_errors=True)
        # copy template over to new directory
        shutil.copytree(template_path,player_path)

    def refresh_player_files(self):
        # render the map
        rnd = Renderer()
        map_path = os.path.join(self.own_path,'img','state.jpg')
        rnd.render_map(map_path,self.data)
        for player in self.data['players']:
            player_path = os.path.join(self.own_path,'players',player['name'])
            template_path = os.path.join(self.own_path,'players','template')            
            # replace template name with player name
            template_main_file = os.path.join(player_path,'template_main.html')
            main_file = os.path.join(player_path,'main.html')
            with open(template_main_file, "rt") as fin:
                with open(main_file, "wt") as fout:
                    for line in fin:
                        line = line.replace('-template-name-', player['name'])
                        line = line.replace('-template-player-number-', str(player['id']+1))
                        line = line.replace('-template-player-total-', str(len(self.data['players'])))                        
                        fout.write(line)

    def add_player_to_list(self,player):
        names = [i['name'] for i in self.data['players']]
        if player['name'] not in names:
            player['id'] = len(self.data['players'])
            self.data['players'].append(player)
        return player

    def create_player_struct(self,name):
        new_player = {'name':name}
        return new_player

    def commit(self, loc=None):
        if loc == None:
            loc = self.loc
        with open(self.loc,'w') as f:
          json.dump(self.data,f,indent=4)
