import json
import os
import shutil
import random

from renderer import Renderer
from rules import Rules
from utils import CoordDecode
from utils import resource_string
from operator import add

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

    def roads_touching(self,pointid):
        # get all the p1 and p2 points in all the roads
        r1 = [i['p1'] for i in self.data['roads']]
        r2 = [i['p2'] for i in self.data['roads']]

        ret = []
        # if we find our pointid in the first list,
        # get the index of the road
        if pointid in r1:
            ret.append(r1.index(pointid))
        # if we find our pointid in the second list,
        # get the index of the road            
        if pointid in r2:
            ret.append(r2.index(pointid))

        return ret

    def villages_touching(self, pointid):
        v1 = [i['point'] for i in self.data['villages']]

        ret = []
        if pointid in v1:
            ret.append(v1.index(pointid))
        return ret

    def cities_touching(self, pointid):
        c1 = [i['point'] for i in self.data['cities']]

        ret = []
        if pointid in c1:
            ret.append(c1.index(pointid))
        return ret   

    def ok_loc_to_build_village_or_city(self, pointid,playerid):
        rds = self.roads_touching(pointid)
        vls = self.villages_touching(pointid)
        cts = self.cities_touching(pointid)

        # if no roads connect, fail
        if len(rds) == 0:
            return False
        # if something is already there, fail
        if len(vls+cts) > 0:
            return False

        # getting here implies at least one road is touching,
        # just make sure that road is friendly
        if self.data['roads'][rds[0]]['owner'] != playerid:
            return False
        else:
            return True

    def afford(self,playerid,cost):
        resources = self.data['players'][playerid]['resources']
        for i in range(0,len(cost)):
            if cost[i] > resources[i]:
                return False
        return True        
   
    def ok_loc_to_build_road(self,p1id,p2id,playerid):
        rds = self.roads_touching(p1id) + self.roads_touching(p2id)
        vls = self.villages_touching(p1id) + self.villages_touching(p2id)
        cts = self.cities_touching(p1id) + self.cities_touching(p2id)

        # if the road is touching nothing, fail        
        if len(rds+vls+cts) == 0:
            return False

        # getting here implies we're touching at least one of something.
        # we disqualify if any of these are not friendly
        if len(rds) > 0:
            if self.data['roads'][rds[0]]['owner'] != playerid:
                return False
        if len(vls) > 0:
            if self.data['villages'][vls[0]]['owner'] != playerid:
                return False
        if len(cts) > 0:
            if self.data['cities'][cts[0]]['owner'] != playerid:
                return False            
        return True
            
    def build_village(self,player_name,buildat):
        player = self.get_player_by_name(player_name)
        player_id = player['id']
        cd = CoordDecode(self.data['stride'],self.data['width'])
        pointid = cd.decode(buildat)
        if (pointid == None):
            print("ERROR: invalid inputs")
            self.set_ret_msg(player_id,'ERROR: invalid inputs')
        else:
            if pointid in [i['point'] for i in self.data['villages']]:
                print("ERROR: village already exists")
                self.set_ret_msg(player_id,'ERROR: village already exists')
            else:
                num_villages = [i['owner'] for i in self.data['villages']].count(player_id)
                if num_villages < Rules['free_villages']:
                    # build village for free
                    new_village = {'point':pointid,'owner':player_id}
                    self.data['villages'].append(new_village)
                    self.set_ret_msg(player_id,'Build Village: SUCCESS (free)')
                elif not self.ok_loc_to_build_village_or_city(pointid,player_id):
                    print("ERROR: invalid location to build village")
                    self.set_ret_msg(player_id,'ERROR: invalid location to build village')
                elif not self.afford(player_id, Rules['costs']['village']):
                    print("ERROR: not enough resources to build village")
                    self.set_ret_msg(player_id,'ERROR: not enough resources to build village')                    
                else:
                    # build village while deducting resources
                    new_village = {'point':pointid,'owner':player_id}
                    self.data['villages'].append(new_village)
                    self.pay(player_id, Rules['costs']['village'])                    
                    self.set_ret_msg(player_id,'Build Village: SUCCESS')

    def pay(self,playerid,cost):
        for i in range(0,len(cost)):
            self.data['players'][playerid]['resources'][i] -= cost[i]        
                                             
    def build_city(self,player_name,buildat):
        player = self.get_player_by_name(player_name)
        player_id = player['id']
        cd = CoordDecode(self.data['stride'],self.data['width'])
        pointid = cd.decode(buildat)
        if (pointid == None):
            print("ERROR: invalid inputs")
            self.set_ret_msg(player_id,'ERROR: invalid inputs')
        else:
            if pointid in [i['point'] for i in self.data['cities']]:
                print("ERROR: city already exists")
                self.set_ret_msg(player_id,'ERROR: city already exists')
            else:
                if not self.ok_loc_to_build_village_or_city(pointid,player_id):
                    print("ERROR: village already exists")
                    self.set_ret_msg(player_id,'ERROR: invalid location to build city')
                elif not self.afford(player_id, Rules['costs']['city']):
                    print("ERROR: not enough resources to build city")
                    self.set_ret_msg(player_id,'ERROR: not enough resources to build city')                
                else:
                    new_city = {'point':pointid,'owner':player_id}
                    self.data['cities'].append(new_city)
                    self.pay(player_id, Rules['costs']['city'])
                    self.set_ret_msg(player_id,'Build City: SUCCESS')

    def set_ret_msg(self,player_id,msg):
        self.data['players'][player_id]['ret'] = msg
        
    def set_status_msg(self,player_id,msg):
        self.data['players'][player_id]['status'] = msg

    def roll_dice(self,player_name):
        player_rolled = self.get_player_by_name(player_name)
        # do a dice roll
        roll = random.randint(1,12)
        game_msg = [player_name + ' rolled a ' + str(roll) + '!']
        rgained = [[0]*len(Rules['resources'])]*len(self.data['players'])
        cd = CoordDecode(self.data['stride'],self.data['width'])
        for village in self.data['villages']:
            adjtiles = cd.get_touching_tiles_index(village['point'])
            owner_id = village['owner']
            if owner_id < len(self.data['players']):
                for adjtileid in adjtiles:
                    tile = self.data['tiles'][adjtileid]
                    tiletype = tile['type']
                    if roll == tile['dice']:                        
                        # add what we got
                        rgained[owner_id] = list( map(add, rgained[owner_id], Rules['terrain'][tiletype]['yield']))
        for city in self.data['cities']:
            adjtiles = cd.get_touching_tiles_index(city['point'])
            owner_id = city['owner']
            if owner_id < len(self.data['players']):            
                for adjtileid in adjtiles:
                    tile = self.data['tiles'][adjtileid]
                    tiletype = tile['type']
                    if roll == tile['dice']:                    
                        # add what we got...twice
                        rgained[owner_id] = list( map(add, rgained[owner_id], Rules['terrain'][tiletype]['yield']))
                        rgained[owner_id] = list( map(add, rgained[owner_id], Rules['terrain'][tiletype]['yield']))   
        for i in range(0,len(rgained)):
            player = self.data['players'][i]
            game_msg.append(player['name'] + ' got ' + resource_string(rgained[i]))
            self.data['players'][i]['resources'] = list( map(add, self.data['players'][i]['resources'], rgained[i]))
            
        self.data['game_msg'] = game_msg
        self.data['turn'] += 1
        
    def build_road(self,player_name,fromstr,tostr):
        player = self.get_player_by_name(player_name)
        player_id = player['id']
        cd = CoordDecode(self.data['stride'],self.data['width'])
        prepidfrom = cd.decode(fromstr)
        prepidto = cd.decode(tostr)
        if (prepidfrom == None) or (prepidto == None):
            print("ERROR: invalid inputs")
            self.set_ret_msg(player_id,'ERROR: invalid inputs')
        else:
            if prepidfrom < prepidto:
                pidfrom = prepidfrom
                pidto = prepidto
            else:
                pidfrom = prepidto
                pidto = prepidfrom
            isadj = cd.isadjindex(pidfrom,pidto)
            if not isadj:
                print("ERROR: road points not adjacent")
                self.set_ret_msg(player_id,'ERROR: road points not adjacent')
            else:
                if (pidfrom,pidto) in [(i['p1'],i['p2']) for i in self.data['roads']]:
                    print("ERROR: road already exists")
                    self.set_ret_msg(player_id,'ERROR: road already exists')
                elif not self.ok_loc_to_build_road(pidfrom,pidto,player_id):
                    print("ERROR: invalid location to build road")
                    self.set_ret_msg(player_id,'ERROR: invalid location to build road')
                elif not self.afford(player_id, Rules['costs']['road']):
                    print("ERROR: insufficient resources to build road")
                    self.set_ret_msg(player_id,'ERROR: insufficient resources to build road')
                else:                    
                    new_road = {'p1':pidfrom,'p2':pidto,'owner':player_id}
                    self.data['roads'].append(new_road)
                    self.pay(player_id, Rules['costs']['road'])
                    self.set_ret_msg(player_id,'Build Road: SUCCESS')

    def refresh_player_files(self):
        # render the map
        rnd = Renderer()
        map_path = os.path.join(self.own_path,'img','state.jpg')
        rnd.render_map(map_path,self.data)
        for player in self.data['players']:
            retmsg = player['ret']
            retcolor = '#000000'
            if 'SUCCESS' in retmsg:
                retcolor = '#00FF00'
            if 'ERROR' in retmsg:
                retcolor = '#FF0000'                
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
                        line = line.replace('-template-player-message-color-',retcolor)
                        line = line.replace('-template-player-message-',retmsg)
                        line = line.replace('-template-resource0-img-',Rules['resources'][0]['img'])
                        line = line.replace('-template-resource1-img-',Rules['resources'][1]['img'])
                        line = line.replace('-template-resource2-img-',Rules['resources'][2]['img'])
                        line = line.replace('-template-resource3-img-',Rules['resources'][3]['img'])
                        line = line.replace('-template-resource4-img-',Rules['resources'][4]['img'])
                        line = line.replace('-template-resource5-img-',Rules['resources'][5]['img'])
                        line = line.replace('-template-resource0-name-',Rules['resources'][0]['name'])
                        line = line.replace('-template-resource1-name-',Rules['resources'][1]['name'])
                        line = line.replace('-template-resource2-name-',Rules['resources'][2]['name'])
                        line = line.replace('-template-resource3-name-',Rules['resources'][3]['name'])
                        line = line.replace('-template-resource4-name-',Rules['resources'][4]['name'])
                        line = line.replace('-template-resource5-name-',Rules['resources'][5]['name'])
                        line = line.replace('-template-resource0-qty-',str(player['resources'][0]))
                        line = line.replace('-template-resource1-qty-',str(player['resources'][1]))
                        line = line.replace('-template-resource2-qty-',str(player['resources'][2]))
                        line = line.replace('-template-resource3-qty-',str(player['resources'][3]))
                        line = line.replace('-template-resource4-qty-',str(player['resources'][4]))
                        line = line.replace('-template-resource5-qty-',str(player['resources'][5]))                       
                        fout.write(line)

    def add_player_to_list(self,player):
        names = [i['name'] for i in self.data['players']]
        if player['name'] not in names:
            player['id'] = len(self.data['players'])
            player['livery_id'] = player['id'] % len(Rules['liveries'])
            self.data['players'].append(player)
        return player

    def create_player_struct(self,name):        
        new_player = {'name':name, 'ret':'','status':''}
        new_player['resources'] = [0] * len(Rules['resources'])
        
        return new_player

    def commit(self, loc=None):
        if loc == None:
            loc = self.loc
        with open(self.loc,'w') as f:
          json.dump(self.data,f,indent=4)
