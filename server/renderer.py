
from PIL import Image,ImageDraw
from rules import Rules

colmap = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z',
          'AA','AB','AC','AD','AE']

class Renderer():
    def __init__(self):
        pass

    def sub_render_players(self, imgdraw,data):
        players = data['players']

        tx = 900
        ty = 80
        imgdraw.text((tx,ty),'Players:',fill='#ffffff',align='left')
        for player in players:
            name = player['name']
            pid = player['id']
            tx = 930
            ty = 100 + pid*20
            imgdraw.text((tx,ty),name,fill='#ffffff',align='left')
            bx = 900
            by = 100 + pid*20
            p1 = (bx+10,by+4)
            p2 = (bx+16,by+16)
            p3 = (bx+4,ty+16)
            livery_id = player['livery_id']
            imgdraw.polygon((p1,p2,p3), fill=Rules['liveries'][livery_id]['fill'], outline ="white")

    def sub_render_roads(self,imgdraw,data):
        roads = data['roads']
        points = data['points']
        for road in roads:
            p1 = (points[road['p1']]['x'],points[road['p1']]['y'])
            p2 = (points[road['p2']]['x'],points[road['p2']]['y'])
            owner = road['owner']
            modowner = owner % len(Rules['liveries'])
            linefill = Rules['liveries'][modowner]['fill']
            if owner < len(data['players']):
                livery = data['players'][owner]['livery_id']
                linefill = Rules['liveries'][livery]['fill']
            imgdraw.line((p1,p2), fill=linefill, width=5)

    def sub_render_cities(self,imgdraw,data):
        cities = data['cities']
        points = data['points']
        for city in cities:
            x0 = points[city['point']]['x']
            x1 = points[city['point']]['x'] - 8
            x2 = points[city['point']]['x'] + 8
            y0 = points[city['point']]['y'] - 8
            y1 = points[city['point']]['y'] + 8
            y2 = points[city['point']]['y'] + 8            
            owner = city['owner']
            modowner = owner % len(Rules['liveries'])
            citfill = Rules['liveries'][modowner]['fill']
            if owner < len(data['players']):
                livery = data['players'][owner]['livery_id']
                citfill = Rules['liveries'][livery]['fill']
            imgdraw.polygon(((x0,y0),(x1,y1),(x2,y2)), fill = citfill, outline ='white')            

    def sub_render_villages(self,imgdraw,data):
        villages = data['villages']
        points = data['points']
        for village in villages:
            x1 = points[village['point']]['x'] - 5
            x2 = points[village['point']]['x'] + 5
            y1 = points[village['point']]['y'] - 5
            y2 = points[village['point']]['y'] + 5            
            owner = village['owner']
            modowner = owner % len(Rules['liveries'])
            vilfill = Rules['liveries'][modowner]['fill']
            if owner < len(data['players']):
                livery = data['players'][owner]['livery_id']
                vilfill = Rules['liveries'][livery]['fill']
            imgdraw.ellipse((x1,y1,x2,y2), fill = vilfill, outline ='white')

    def render_map(self,output_file,data):
        points = data['points']
        tiles = data['tiles']
        stride = data['stride']
        height = data['height']
        spacing = data['spacing']
        
        img = Image.new('RGB', (1200, 500))

        # create rectangle image 
        img1 = ImageDraw.Draw(img)

        # render map text
        for i in range(0, len(data['game_msg'])):
            img1.text((900,300+i*10),data['game_msg'][i], align='left')

        # render turn
        img1.text((900,50),'TURN ' + str(data['turn']), align='left')

        #render player names
        self.sub_render_players(img1,data)

        for tile in tiles:
            shape = [(points[i]['x'],points[i]['y']) for i in tile['points']]
            #print(shape)
            tile_fill = Rules['terrain'][tile['type']]['fill']
            img1.polygon(shape, fill =tile_fill, outline ="red")

            row = tile['row']
            col = tile['col']
            if tile['dice'] != 0:
                x = points[tile['points'][0]]['x']
                y = points[tile['points'][0]]['y']
                tx = x
                ty = y - 5 + spacing / 2 
                img1.text((tx,ty),str(tile['dice']),fill='#000000',align='center') 
            if row == 0:
                x = points[tile['points'][0]]['x']
                y = points[tile['points'][0]]['y']
                tx = x
                ty = y - spacing                
                img1.text((tx-2,ty),colmap[col*2],align='center')   #-4 because it still seems off-center
                l1 = (x,y)
                l2 = (x,y-spacing+15)
                img1.line((l1,l2))
            if row == 1:
                x = points[tile['points'][0]]['x']
                y = points[tile['points'][0]]['y']
                tx = x
                ty = y - spacing*2                
                img1.text((tx-2,ty),colmap[col*2+1],align='center')  #-4 because it still seems off-center
                l1 = (x,y)
                l2 = (x,y-spacing*2+15)
                img1.line((l1,l2))                
            if row == height - 1:
                x = points[tile['points'][3]]['x']
                y = points[tile['points'][3]]['y']                
                tx = x
                ty = y + spacing                  
                img1.text((tx-2,ty),colmap[col*2+1],align='center')  #-4 because it still seems off-center
                l1 = (x,y)
                l2 = (x,y+spacing-5)
                img1.line((l1,l2))                  
            if row == height - 2:
                x = points[tile['points'][3]]['x']
                y = points[tile['points'][3]]['y']                
                tx = x
                ty = y + spacing*2                  
                img1.text((tx-2,ty),colmap[col*2],align='center')  #-4 because it still seems off-center
                l1 = (x,y)
                l2 = (x,y+spacing*2-5)
                img1.line((l1,l2))
            if col == 0:
                x = points[tile['points'][5]]['x']
                y = points[tile['points'][5]]['y']                   
                tx = x - spacing - 10
                ty = y - 5                 
                img1.text((tx,ty),str(row*2+1),align='center')  #-4 because it still seems off-center
                l1 = (x,y)
                l2 = (x-spacing+5,y)
                img1.line((l1,l2))
                x = points[tile['points'][4]]['x']
                y = points[tile['points'][4]]['y']                   
                tx = x - spacing*2 - 10
                ty = y - 5                 
                img1.text((tx,ty),str(row*2+2),align='center')  #-4 because it still seems off-center
                l1 = (x,y)
                l2 = (x-spacing*2+5,y)
                img1.line((l1,l2))                   
            if col == stride - 2:
                x = points[tile['points'][1]]['x']
                y = points[tile['points'][1]]['y']                   
                tx = x + spacing
                ty = y - 5                 
                img1.text((tx,ty),str(row*2+1),align='center')  #-4 because it still seems off-center
                l1 = (x,y)
                l2 = (x+spacing-5,y)
                img1.line((l1,l2))
                x = points[tile['points'][2]]['x']
                y = points[tile['points'][2]]['y']                   
                tx = x + spacing*2
                ty = y - 5                 
                img1.text((tx,ty),str(row*2+2),align='center')  #-4 because it still seems off-center
                l1 = (x,y)
                l2 = (x+spacing*2-5,y)
                img1.line((l1,l2))                

        #render stuff
        self.sub_render_roads(img1,data)
        self.sub_render_villages(img1,data)
        self.sub_render_cities(img1,data)
                
        img.save(output_file, "JPEG")
