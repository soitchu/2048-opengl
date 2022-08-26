import math
import time
import pyglet
from pyglet import shapes
import random

class G_2048(pyglet.window.Window):

    def __init__(self, width, height):
        super().__init__(width, height, "2048")
        self.time = 0
        self.batch = pyglet.graphics.Batch()
        self.textBatch = pyglet.graphics.Batch()
 
        self.size = min(height, width)
        self.padding = 20
        self.boardLeft = (self.width - self.size)/2
        self.boardTop = (self.height - self.size)/2
        self.boardMain = shapes.Rectangle(self.boardLeft, self.boardTop , width=self.size,height=self.size,color=(85, 52, 165), batch=self.batch)
        self.tiles = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
        self.texts = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
        self.drawTiles()
        self.test = 0.0
        self.list = [[2,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
        self.animation = []
        self.queue = []
        self.canMove = True               
        self.updateGraphic()
        


    def drawTiles(self):
        self.tileSize = self.size/4 
        self.tilePadding = 10
        

        for i in range(0,4):
            for j in range(0,4):
                tileX = self.boardLeft + i*self.tileSize + self.tilePadding
                tileY = self.boardTop + j*self.tileSize + self.tilePadding
                tileHeight = self.tileSize - self.tilePadding*2
                tileWidth = self.tileSize - self.tilePadding*2
                tileColor=(111, 223, 223)
                tileObj = self.drawSquircle(tileX, tileY, tileWidth, tileHeight, tileColor)
                self.tiles[3-j][i] = tileObj
                self.texts[3-j][i]= pyglet.text.Label('2',
                          font_name='Arial',
                          font_size=16,
                          x=(tileX + tileWidth/2), y=(tileY + tileHeight/2),
                          anchor_x='center', anchor_y='center',color=(0,0,0,0), batch=self.textBatch)
                self.tiles[3-j][i].append(self.texts[3-j][i])
                

    def drawSquircle(self, x, y, width, height, color):

        x= x + 10
        y= y + 10
        height = height - 10
        width = width - 10
        tile = []
        tile.append(shapes.Rectangle(x, y, width - 10, height - 10, color = color, batch=self.batch))
        tile.append(shapes.Rectangle(x+width - 10, y,  10, height - 10, color = color, batch=self.batch))
        tile.append(shapes.Rectangle(x- 10, y,  10, height - 10, color = color, batch=self.batch))
        tile.append(shapes.Rectangle(x, y-10,  width - 10, 10, color = color, batch=self.batch))
        tile.append(shapes.Rectangle(x, y+height-10,  width - 10, 10, color = color, batch=self.batch))
        tile.append(shapes.Sector(x,y,10,start_angle=math.pi,angle=math.pi/2, batch=self.batch, color = color))
        tile.append(shapes.Sector(x+width - 10,y,10,start_angle=0,angle=-math.pi/2, batch=self.batch, color = color))
        tile.append(shapes.Sector(x+width - 10,y + height- 10,10,start_angle=math.pi/2,angle=-math.pi/2, batch=self.batch, color = color))
        tile.append(shapes.Sector(x,y + height- 10,10,start_angle=math.pi/2,angle=math.pi/2, batch=self.batch, color = color))

        for x in tile:
            x.opacity = 0
        return tile


    def on_draw(self):        
        self.clear()
        self.batch.draw()
        self.textBatch.draw()

    def updateGraphic(self):
        for i in range(0,4):
            for j in range(0,4):
                if(self.list[i][j] != 0):
                    value = self.list[i][j]
                    for x in self.tiles[i][j]:
                        x.opacity = 255
                        if len(x.color) == 3:
                            x.color = ( (50+(value*32)%155) , (50+(value*64)%155) , (50+(value*128)%155))
                    self.texts[i][j].color = (255,255,255,255)
                    self.texts[i][j].document.text = str(self.list[i][j]) 
                else:
                    for x in self.tiles[i][j]:
                        x.opacity = 0
                    self.texts[i][j].color = (0,0,0,0)
                    


    def move(self,x):
        if not self.canMove:
            self.queue.append(x)
            return

        inc = 1
        l = []
        changedPositions = []
        l2 = [0,4,1]
        indexMax = 0
        if(x == 1):
            inc = +1
            l = [3, -1, -1]
            indexMax = 3
        elif(x == 2):
            inc = -1
            l = [0, 4, 1]
            indexMax = 0
        elif(x == 3):
            inc = -1
            l = [0, 4, 1]
            indexMax = 0
        elif(x == 4):
            inc = 1
            l = [3, -1, -1]
            indexMax = 3

        moved = False
        if(x==2 or x ==1):
            for i in range(l2[0], l2[1], l2[2]):
                for j in range (l[0], l[1], l[2]):                
                    last = self.lastZero(i, x)

                    check = -1
                    if(x == 1):
                        check = last > j
                    elif(x == 2):
                        check = last < j

                    if(self.list[i][j] == 0):
                        continue
                    elif(last != j):
                        current = j
                        checkMove = False
                        animObj = {}
                        if(check and last != -1):
                            self.list[i][last] = self.list[i][j]
                            self.list[i][j] = 0
                            current = last
                            moved = True
                            checkMove = True
                            animObj = {
                                "from": [i,j],
                                "to": [i,last]
                            }
                            changedPositions.append(animObj)
                
                        if(current!=indexMax and self.list[i][current]==self.list[i][current + inc]):
                            if(checkMove):
                                animObj["to"][1] = current + inc
                            else:
                                animObj = {
                                    "from": [i,j],
                                    "to": [i,current + inc]
                                }
                                changedPositions.append(animObj)

                            self.list[i][current + inc]*=2
                            self.list[i][current]=0
                            moved = True
        
        elif(x == 3 or x == 4):
            for j in range(l2[0], l2[1], l2[2]):
                for i in range (l[0], l[1], l[2]):                
                    last = self.lastZero(j, x)

                    check = -1
                    if(x == 4):
                        check = last > i
                    elif(x == 3):
                        check = last < i

                    if(self.list[i][j] == 0):
                        continue
                    elif(last != i):
                        current = i
                        checkMove = False
                        animObj = {}
                        if(check and last != -1):
                            self.list[last][j] = self.list[i][j]
                            self.list[i][j] = 0
                            current = last
                            moved = True
                            checkMove = True
                            animObj = {
                                "from": [i,j],
                                "to": [last, j]
                            }
                            changedPositions.append(animObj)
                        
                        if(current!=indexMax and self.list[current][j]==self.list[current + inc][j]):
                            if(checkMove):
                                animObj["to"][0] = current + inc
                            else:
                                animObj = {
                                    "from": [i,j],
                                    "to": [current + inc, j]
                                }
                                changedPositions.append(animObj)


                            self.list[current + inc][j]*=2
                            self.list[current][j]=0
                            moved = True
        if(moved):
            self.animateStuff(changedPositions)


    def animateStuff(self, positions):
        for x in positions:
            xDist = x["to"][1] - x["from"][1]
            yDist = -x["to"][0] + x["from"][0]
            dir = ""
            sign = 0
            distance = 0
            if(xDist == 0):
                dir = "y"
                distance = yDist
            else:
                dir = "x"
                distance = xDist

            if(distance > 0):
                sign = 1
            else:
                sign = -1
            self.animation.append({
                "from" : x["from"],
                "to" : x["to"],
                "count" : 0,
                "sign" : sign,
                "done" : False,
                "direction" : dir,
                "reference" : x["from"],
                "distance" :  (distance)*self.tileSize,
            })
        self.count = 0
        self.countMax = 20
        self.canMove = False


    def newNum(self):
        insertData = [];
        max = 2;
        for i in range(0,4):
            for j in range(0,4):
                if (self.list[i][j] > max):
                    max = self.list[i][j];
                insertData
                if (self.list[i][j] == 0):
                    insertData.append([i, j]);
             

        if (len(insertData) == 0):
            return;
        
        temp1 = insertData[random.randint(0, len(insertData) - 1)];
        temp2 = min(8, 2**random.randint(1, math.log2(max)))
        

        self.list[temp1[0]][temp1[1]] = temp2

    def lastZero(self, x, dir):
        if(dir == 1):
            for i in range(3,-1,-1):
                if self.list[x][i] == 0:
                    return i
            return -1
        elif(dir == 2):
            for i in range(0, 4):
                if self.list[x][i] == 0:
                    return i
            return -1
        elif(dir == 3):
            for i in range(0, 4):
                if self.list[i][x] == 0:
                    return i
            return -1
        elif(dir == 4):
            for i in range(3,-1,-1):
                if self.list[i][x] == 0:
                    return i
            return -1


    def update(self, delta_time):
        if self.canMove == False:
            if(self.count < self.countMax):
                check = 0
                for i in range(0,6):
                    for x in self.animation:
                        if(x["done"]):
                            continue
                        check = 1
                        ref = x["reference"]
                        if x["direction"] == "x":
                            for elements in self.tiles[ref[0]][ref[1]]:
                                elements.x += 5*(x["sign"])

                        else:
                            for elements in self.tiles[ref[0]][ref[1]]:
                                elements.y += 5*(x["sign"])
                        
                        x["count"] += 1
                        if(abs(x["count"]*5) >= abs(x["distance"])):
                            x["done"] = 1

                        
                if(check == 0):
                    self.count = 100

            else:
                for x in self.animation:
                    
                    for element in self.tiles[x["to"][0]][x["to"][1]]:
                        if(x["direction"] == "x"):
                            element.x += -x["distance"]
                        else:
                            element.y += -x["distance"]
                    temp = self.tiles[x["to"][0]][x["to"][1]]
                    
                    self.tiles[x["to"][0]][x["to"][1]] = self.tiles[x["from"][0]][x["from"][1]]
                    self.tiles[x["from"][0]][x["from"][1]] = temp

                    temp = self.texts[x["to"][0]][x["to"][1]]
                    
                    self.texts[x["to"][0]][x["to"][1]] = self.texts[x["from"][0]][x["from"][1]]
                    self.texts[x["from"][0]][x["from"][1]] = temp

                self.animation = []
                self.canMove = True
                self.count = 0
                self.newNum();

                self.updateGraphic()
        else:
            if(len(self.queue) != 0):
                self.move(self.queue[0])
                del self.queue[0]         
                
if __name__ == "__main__":
    print("The controls are: W,A,S,D")
    demo = G_2048(720, 480)
    @demo.event
    def on_key_press(symbol, modifiers):
        if(symbol == 100):
            demo.move(1)
        elif(symbol == 97):

            demo.move(2)
        elif(symbol == 119):
            demo.move(3)

        elif(symbol == 115):
            demo.move(4)
    
    pyglet.clock.schedule_interval(demo.update, 1/100)
    pyglet.app.run()