
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
            modpid = pid % len(Rules['liveries'])
            imgdraw.polygon((p1,p2,p3), fill=Rules['liveries'][modpid]['fill'], outline ="white")

    def render_map(self,output_file,data):
        points = data['points']
        tiles = data['tiles']
        stride = data['stride']
        height = data['height']
        spacing = data['spacing']
        
        img = Image.new('RGB', (1200, 500))

        # create rectangle image 
        img1 = ImageDraw.Draw(img)

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
                img1.text((tx,ty),str(row*2),align='center')  #-4 because it still seems off-center
                l1 = (x,y)
                l2 = (x-spacing+5,y)
                img1.line((l1,l2))
                x = points[tile['points'][4]]['x']
                y = points[tile['points'][4]]['y']                   
                tx = x - spacing*2 - 10
                ty = y - 5                 
                img1.text((tx,ty),str(row*2+1),align='center')  #-4 because it still seems off-center
                l1 = (x,y)
                l2 = (x-spacing*2+5,y)
                img1.line((l1,l2))                   
            if col == stride - 2:
                x = points[tile['points'][1]]['x']
                y = points[tile['points'][1]]['y']                   
                tx = x + spacing
                ty = y - 5                 
                img1.text((tx,ty),str(row*2),align='center')  #-4 because it still seems off-center
                l1 = (x,y)
                l2 = (x+spacing-5,y)
                img1.line((l1,l2))
                x = points[tile['points'][2]]['x']
                y = points[tile['points'][2]]['y']                   
                tx = x + spacing*2
                ty = y - 5                 
                img1.text((tx,ty),str(row*2+1),align='center')  #-4 because it still seems off-center
                l1 = (x,y)
                l2 = (x+spacing*2-5,y)
                img1.line((l1,l2))                
                
        img.save(output_file, "JPEG")
