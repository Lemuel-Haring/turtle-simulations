
import turtle 
import random

global screen
screen = turtle.Screen()
global world_food
world_food = []


class IndependantAgents(turtle.Turtle):
    def __init__(self) -> None:
        super().__init__(shape="turtle")
        self.penup()
        self.max_energy = 1000
        self.energy = 200
        self.birthcost = self.energy
        
        self.life_status = True
        self.energy_efficiency = random.randint(1, 5)
        self.move_range = random.randint(40, 100)
        self.sight_range = self.move_range
        self.speed(0)

    def explore(self):
        self.left(random.randint(-90, 90))
        self.move()

    def move(self, distance=None):
        if (distance is not None):
            self.forward(distance)
            self.energy_change(-abs(distance))
        else:
            self.forward(self.move_range)
            self.energy_change(-abs(self.move_range))
        



    def energy_change(self, energy_change: int):
        """Calculates net energy after energy change. Negative values for fatigue"""
        self.energy += int(energy_change/self.energy_efficiency)
        if self.energy <= 0:
            self.life_status = False
        if self.energy >= self.max_energy:
            self.energy = self.max_energy

    def find_food(self):
        for food in world_food:
            if self.distance(food.position()) < self.sight_range:
                #TODO add self.move() in
                self.goto(food.position())
                self.energy_change(self.distance(food.position()))
                self.energy_change(food.calory_value)
                food.depleted()
                break

    def _draw_circle(self, radius, color="black"):
        screen.tracer()
        pen = turtle.Turtle(visible=False, shape="triangle")
        pen.color(color)
        pen.speed(0)
        pen.pensize(6)
        pen.penup()
        pen.setposition(self.position())
        pen.setheading(self.heading())
        pen.right(90)
        pen.forward(radius)
        pen.setheading(self.heading())
        pen.pendown()
        pen.pencolor(color)
        pen.circle(radius)
        screen.update()
        pen.clear()
        del pen
        

    def display_vision_range(self):
        """Displays the vision range of the object with a circle"""
        self._draw_circle(self.sight_range, color="red")

    def reproduce(self):
        """If another turtle of the same color is nearby,
        go to the turtle possition and makea new copy of the 
        turtle that initiated the mating"""
        if self.energy > 2*self.birthcost:
            possible_partners = [this_object for this_object in turtle.turtles() if ( (this_object.shape() == "turtle") and (this_object.color()==self.color()) ) and self.distance(this_object.position()) < self.move_range]
            if len(possible_partners) >=1:
                # only reproduce if food is around
                reproduced = False
                if not reproduced:
                        #now go make babies
                        self.goto(possible_partners[0].position())
                        self.energy_change(-abs(self.birthcost))
                        my_clone = self.clone()
                        blocks.append(my_clone)
                        self.clear()
                        my_clone.clear()
                        print("reproduced")


    def act(self):
        self.pendown()
        self.display_vision_range()
        self.find_food()
        self.explore()
        self.reproduce()
        self.clear()
        self.penup()

        
        



    
def gen_counter(count_status: bool):
    x = 0
    while count_status:
        x += 1
        yield x

class Food(turtle.Turtle):
    def __init__(self, shape: str = "circle") -> None:
        super().__init__(shape)
        screen.tracer()
        self.hideturtle()
        self.penup()
        self.color("orange")
        self.goto( (random.randint(-250,250), random.randint(-250,250) ) )
        world_food.append(self)
        self.showturtle()
        screen.update()
        self.speed(0)
        self.calory_value = 100
        self.type = "food"

    def depleted(self) -> None:
        # world_food.remove(self)
        #NOTE this only removes the food from the global list and not let the item disapear
        self.hideturtle()
        world_food.remove(self)

class SuperFood(Food):
    def __init__(self, shape: str = "circle") -> None:
        super().__init__(shape)
        self.color("green")
        self.calory_value = 300








turtles_in_sim = 20
# some colors for better PRESENTATION! mhahaha
 
colors= ["#FF0000"
            , "#00FFFF"
            , "#9932CC"
            , "#9932CC"
            , "#FF0000"] 
# ( random.random(0, 255+1), random.randint(0, 255+1) , random.randint(0, 255+1))
colors = [ ( colors[random.randint(0, len(colors)-1) ]) for _ in range(0, turtles_in_sim)]

# creating the blocks
blocks = [IndependantAgents() for _ in range(0,len(colors)+1)]
[blocks[i].color(colors[i]) for i in range(0, len(colors))]

active_status = True

[Food() for _ in range(0,20)]
while active_status:
    if next(gen_counter(active_status)) > 1000000:
        break
    
    #spawn fruit
    #TODO
    [Food() for _ in range(0,10) if len(world_food) < 20]
    [SuperFood() for _ in range(0,1)]
    print(f"Amount of food: {len(world_food)}")


    #Entities act
    [block.act() for block in blocks if block.life_status ==True]
    [block.color("grey") for block in blocks if block.life_status ==False]  #make all the dead turtles the same dead color
    

    

    turtles_alive = [block.life_status for block in blocks]
    if not True in turtles_alive:
        active_status = False

    print(f"-->Objects running:{len(turtle.turtles())}")
    for this_turtle in turtle.turtles():
        if this_turtle.shape() == "triangle":
            print("deleting draw arrows")
            # it might be better to not initiate the arrows everytime and deleting them
            # possible to just hide the arrows, (the will auto relocate to the turtle once the draw sequence starts)
            turtle.turtles().remove(this_turtle)
    print(f"Objects running:{len(turtle.turtles())}<--")
    
    
    
    
print("All the turtles died")

screen.exitonclick()