
from PIL import Image,ImageDraw
from rules import Rules

colmap = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z',
          'AA','AB','AC','AD','AE']

class Renderer():
    def __init__(self):
        pass

    def render_map(self,output_file,data):
        points = data['points']
        tiles = data['tiles']
        stride = data['stride']
        height = data['height']
        spacing = data['spacing']
        
        img = Image.new('RGB', (800, 500))

        # create rectangle image 
        img1 = ImageDraw.Draw(img)        

        for tile in tiles:
            shape = [(points[i]['x'],points[i]['y']) for i in tile['points']]
            #print(shape)
            tile_fill = Rules['terrain'][tile['type']]['fill']
            img1.polygon(shape, fill =tile_fill, outline ="red")

            row = tile['row']
            col = tile['col']
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
