import json
import random
from renderer import Renderer

class MapGenerator():
    def __init__(self):
        pass

    def seed_tiles(self,tiles,stride):

        rowc = 5
        colc = 6
        
        for i in range(0,len(tiles)):
             tiles[i]['type'] = 6 # ocean
             row = tiles[i]['row']
             col = tiles[i]['col']
             diffrow = row - rowc
             diffcol = col - colc
             if (diffcol < 0) and (row % 2 == 0):
                 diffcol -= 1#+1 accounts for the convention bias
             norm = abs(diffrow/2) + abs(diffcol)
             if (norm < 5) and (abs(diffrow) < 5): # and (diffcol < 5):                 
                 tiles[i]['type'] = random.randint(0,5) # ocean
        return tiles

    def generate_mesh(self,xb=0,yb=0,sp=30,stride=15):
        points = []

        for j in range(0,stride*2):
            if j % 4 == 0:
                xoff = 0
                yoff = 0
            if j % 4 == 1:
                xoff = -sp/2
                yoff = 0
            if j % 4 == 2:
                xoff = -sp/2
                yoff = 0
            if j % 4 == 3:
                xoff = 0
                yoff = 0
            for i in range(0,stride):
                x = xb + i*sp + xoff
                y = yb + j*sp/3 + yoff
                new_point = {'x':x,'y':y}
                points.append(new_point)

        tiles = []

        for j in range(0,((stride*2)-6),4):
            for i in range(0,stride-1):
                p1 = j*stride+i
                p2 = (j+1)*stride+(i+1)
                p3 = (j+2)*stride+(i+1)
                p4 = (j+3)*stride+i
                p5 = (j+2)*stride+i
                p6 = (j+1)*stride+i
                row = int(j/2)
                col = i
                #print(row)
                new_tile = {'points':(p1,p2,p3,p4,p5,p6),'row':row,'col':col}
                tiles.append(new_tile)

                p1 = (j+2)*stride+(i+1)
                p2 = (j+3)*stride+(i+1)
                p3 = (j+4)*stride+(i+1)
                p4 = (j+5)*stride+(i+1)
                p5 = (j+4)*stride+i
                p6 = (j+3)*stride+i
                row = int((j/2) + 1)
                col = i
                #print(row)
                new_tile = {'points':(p1,p2,p3,p4,p5,p6),'row':row,'col':col}
                tiles.append(new_tile)            

        height = stride-3
        return (points,tiles,stride,height,sp)

mg = MapGenerator()
(points, tiles, stride, height, spacing) = mg.generate_mesh(xb=150,yb=50)
tiles = mg.seed_tiles(tiles,stride)


with open('state.json','r') as f:
    data = json.load(f)

data['points'] = points
data['tiles'] = tiles
data['stride'] = stride
data['height'] = height
data['spacing'] = spacing

with open('state.json','w') as f:
    json.dump(data,f,indent=4)

rnd = Renderer()
rnd.render_map('state.jpg',data)
