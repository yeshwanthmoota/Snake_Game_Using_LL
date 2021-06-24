from constants import *
import pygame

class Node(): # Nodes of a Double Linked list

    def __init__(self, x, y, dir_num, prev, next):
        self.x = x # x-coordinate
        self.y = y # y-coordinate
        self.vel_direction = dir_num # direction number
        self.prev = prev
        self.next = next
        self.change_value = 0 # can be 0 or 1. 1 - for change, 0 - no change
    
    def update_x_y(self): # This function is the velocity function which updates the x and y of the nodes.
        if self.vel_direction == 1: # go up

            if self.y + SNAKE_NODE_SIDE > 0:
                self.y -= SNAKE_SPEED
            else: # Snake's node has gone off screen
                # We have to move to snake's node to the bottom of the screen to show continuity in the screen
                # Here self.y + SNAKE_NODE_SIDE <= 0
                self.y = HEIGHT - SNAKE_NODE_SIDE

        if self.vel_direction == 2: # go down

            if self.y < HEIGHT:
                self.y += SNAKE_SPEED
            else: # Snake's node has gone off screen
                # We have to move to snake's node to the top of the screen to show continuity in the screen
                # Here self.y >= HEIGHT
                self.y = 0

        if self.vel_direction == 3: # go left

            if self.x + SNAKE_NODE_SIDE > 0:
                self.x -= SNAKE_SPEED
            else: # Snake's node has gone off screen
                # We have to move to snake's node to the right of the screen to show continuity in the screen
                # Here self.x + SNAKE_NODE_SIDE <= 0
                self.x = WIDTH - SNAKE_NODE_SIDE
        if self.vel_direction == 4: # go right

            if self.x < WIDTH:
                self.x += SNAKE_SPEED
            else: # Snake's node has gone off screen
                # We have to move to snake's node to the left of the screen to show continuity in the screen
                # Here self.x >= WIDTH
                self.x = 0

class Snake(): # head of the Linked list



    def __init__(self):
        self.head = None # This is just the header node which points to the Snake.


    def initialize_snake(self):
        for i in range(SNAKE_BIRTH_LENGTH):
            self.insert_node()



    def insert_node(self): # inserts the node at the end of the snake => the tail part of the snake
        if(self.head is None):
            node = Node(WIDTH//2,HEIGHT//2, 4, None,None) # first node is created
            self.head = node # first node of the snake
        else:
            ptr = Snake()
            ptr = self.head
            while ptr.next is not None:
                ptr = ptr.next

            # now ptr.next = None => now ptr is at the last position in the Linked list

            # Now ptr.vel_direction tells the velocity direction of the last part of the node.

            if ptr.vel_direction == 1: # last node is moving in upwards 
                node = Node(ptr.x, ptr.y + SNAKE_NODE_SIDE, 1, ptr, None) # Node is inserted
                ptr.next = node

            elif ptr.vel_direction == 2: # last node is moving in downwards
                node = Node(ptr.x, ptr.y - SNAKE_NODE_SIDE, 2, ptr, None) # Node is inserted
                ptr.next = node

            elif ptr.vel_direction == 3: # last node is moving towards left
                node = Node(ptr.x + SNAKE_NODE_SIDE, ptr.y, 3, ptr, None) # Node is inserted
                ptr.next = node

            elif ptr.vel_direction == 4: # last node is moving towards right
                node = Node(ptr.x - SNAKE_NODE_SIDE, ptr.y, 4, ptr, None) # Node is inserted
                ptr.next = node

    def __len__(self):
        ptr = Snake()
        ptr = self.head
        count = 0

        while ptr is not None:
            count += 1
            ptr = ptr.next

        return count


    def update_all_nodes(self):
        ptr = Snake()
        ptr = self.head
        while ptr is not None:
            ptr.update_x_y()
            ptr = ptr.next

    def snake_movement(self):
        # This function is responsible for change in directions of all nodes with respect to the node before them.  
        ptr = Snake()
        ptr = self.head

        while ptr.next is not None:
            ptr = ptr.next
        # Now ptr.next is None => ptr is at the last node of the linked list
        while ptr is not self.head:
            if ptr.prev.change_value == 1:
                ptr.vel_direction = ptr.prev.vel_direction
                ptr.change_value = 1 # change the value since vel_direction changed
                ptr.prev.change_value = 0 # reset value to zero
            ptr = ptr.prev # move ptr backwards in the list


    def draw_snake(self, gameDisplay):
        ptr = Snake()
        ptr = self.head
        while ptr is not None:
            pygame.draw.rect(gameDisplay, WHITE, pygame.Rect(ptr.x, ptr.y, SNAKE_NODE_SIDE, SNAKE_NODE_SIDE), 2) # drawing node
            pygame.draw.rect(gameDisplay, GREEN, pygame.Rect(ptr.x + 2, ptr.y + 2, SNAKE_NODE_SIDE - 6, SNAKE_NODE_SIDE - 6), 0)
            ptr = ptr.next
        pygame.display.update()