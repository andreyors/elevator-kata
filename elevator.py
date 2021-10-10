from enum import Enum
from math import inf

class Direction(Enum):
    UP = 1
    DOWN = 0
    
class Elevator:
    def __init__(self, floor = 1, direction = Direction.UP):
        self.current_floor = floor
        self.direction = direction
        self.requested_floors = []
        
    def request_floor(self, desired_floor):
        if desired_floor in self.requested_floors:
            return
        
        self.requested_floors.append(desired_floor)            
        self.requested_floors = sorted(self.requested_floors, key=self.request_weight)        
    
    def request_weight(self, requested_floor):
        """
        the case:
        
        - the elevator is on 3rd floor, is going up
        - there are two requests: 4th floor, 2nd floor
        
        we have diff in floors:
            for 4th floor: 1 
            for 2nd floor: -1
            
        we sort it normally if we keep direction
        if direction changes, we deprioritize it
        """        
        lift_goes_up = requested_floor - self.current_floor > 0
        if self.direction == Direction.DOWN and lift_goes_up:
            return inf
        
        return abs(requested_floor - self.current_floor)
        
    def state(self):
        return (self.current_floor, self.direction)
    
    def process(self):
        desired_floor = self.requested_floors.pop(0)
        
        if self.current_floor > desired_floor :
            self.direction = Direction.DOWN
        elif self.current_floor < desired_floor:
            self.direction = Direction.UP
            
        self.current_floor = desired_floor
