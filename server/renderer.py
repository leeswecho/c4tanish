
from PIL import Image,ImageDraw
from rules import Rules

class Renderer():
    def __init__(self):
        pass

    def render_map(self,output_file,data):
        points = data['points']
        tiles = data['tiles']
        
        img = Image.new('RGB', (500, 500))

        # create rectangle image 
        img1 = ImageDraw.Draw(img)

        for tile in tiles:
            shape = [(points[i]['x'],points[i]['y']) for i in tile['points']]
            #print(shape)
            tile_fill = Rules['terrain'][tile['type']]['fill']
            img1.polygon(shape, fill =tile_fill, outline ="red")

        img.save(output_file, "JPEG")
