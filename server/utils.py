from rules import Rules

def resource_string(resources):
    ret = ''
    count = 0
    for i in range(0,len(resources)):
        if resources[i] > 0:
            if count > 0:
                ret += ','
            count += 1
            ret += str(resources[i])
            ret += ' ' + Rules['resources'][i]['name']
    return ret

class CoordDecode():
    def __init__(self, stride,width):
        self.stride = stride
        self.width = width

    def validate_coord(self, coord):
        coordlen = len(coord)
        if coordlen < 2:
            return False
        if coordlen > 4:
            return False       
        if not coord[0].isalpha():
            return False
        if not coord[coordlen-1].isnumeric():
            return False
        return True
        
    def decode(self,coord):
        # convert to upper
        coord = coord.upper()
        if not self.validate_coord(coord):
            print('invalid coord: ' + coord)
            return None            
        # check if single or double alpha
        if coord[1].isalpha():            
            prow = int(coord[2:])            
            pcol = (ord(coord[0])-ord('A')+1)*26 + ord(coord[1])-ord('A')            
        else:
            prow = int(coord[1:])
            pcol = ord(coord[0])-ord('A')
        # validate what we just got (first-pair rows can't have "odd" columns)
        if (pcol % 2 == 1) and (prow % 4 in [0,3]):
            print('invalid coord: ' + coord)
            return None
        # validate what we just got (second-pair rows can't have "even" columns)            
        if (pcol % 2 == 0) and (prow % 4 in [1,2]):
            print('invalid coord: ' + coord)
            return None            
        # account for oddities of my weird coordinate system
        # (this accounts for the fact that both 'A' and 'B'
        # "share" column 0, etc.)
        pcol = int(pcol / 2)
        # (this accounts for the convention that second-pair rows "move left"
        # so its "alphabet" column is one higher than its actual one)
        if prow % 4 in [1,2]:
            pcol += 1
        # get the point index
        index = prow*self.stride + pcol
        return index

    def get_touching_tiles(self,coord):
        point_id = self.decode(coord)
        return self.get_touching_tiles_index(point_id)
        
    def get_touching_tiles_index(self,point_id):
        prow = int(point_id / self.stride)
        pcol = point_id % self.stride

        row = int(prow / 2)
        rowrem = prow % 2
        col = pcol

        if (prow % 4) == 0:
            bst = row*self.width + col
            tchset = (bst,bst-self.width,bst-self.width-1)
        elif (prow % 4) == 1:
            bst = row*self.width + col
            tchset = (bst,bst-1,bst-self.width-1)
        elif (prow % 4) == 2:
            bst = row*self.width + col
            tchset = (bst-1,bst-self.width,bst-self.width-1)
        else:   # (prow % 4) == 3:
            bst = row*self.width + col
            tchset = (bst,bst-1,bst-self.width)            
        return tchset

    def isadjindex(self, i1, i2):
        prow = int(i1 / self.stride)
        
        if (prow % 4) == 0:
            adjset = (-self.stride,self.stride,self.stride+1)
        elif (prow % 4) == 1:
            adjset = (-self.stride,self.stride,-self.stride-1)
        elif (prow % 4) == 2:
            adjset = (-self.stride,self.stride,self.stride-1)
        else:   # (prow % 4) == 3:
            adjset = (-self.stride,self.stride,-self.stride+1)
        diff = i2-i1        
        if diff in adjset:
            return True
        else:
            return False
        
    def isadj(self, coord1, coord2):
        i1 = self.decode(coord1)
        i2 = self.decode(coord2)
        return self.isadjindex(i1,i2)

    def encode(self, index):
        prow = int(index / self.stride)
        pcol = index % self.stride
        srow = str(prow)
        # 13 because odd and even rows interleave the alphabet
        # amongst each other's columns
        if pcol >= 13:
            n1 = pcol / 13
            n2 = pcol % 13
            ord1 = ord('A')+n1
            ord2 = (ord('A')+n2*2)
            if prow % 4 in [1,2]:
                ord2 -= 1    #-1 because of row "move back" convention
            scol = chr(ord1)+chr(ord2)
        else:
            ord1 = (ord('A')+pcol*2)
            if prow % 4 in [1,2]:
                ord1 -= 1    #-1 because of row "move back" convention        
            scol = chr(ord1)            
        return scol + srow


if __name__ == "__main__":
    cd = CoordDecode(15,14)
