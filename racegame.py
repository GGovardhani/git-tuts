import pygame
from pygame.locals import *
import random 

pygame.init()
pygame.font.init()

width = 500
height = 500
screen_size = (width, height)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('p car race')

gray = (100, 100, 100)
green = (75, 200, 56)
red = (200, 0, 0)
white = (255, 255, 255)
yellow = (255, 232, 0)

## game settings
gameover = False
speed = 2
score = 0 

## markers size 
marker_width = 10
marker_height = 50

## road and edge markers 
road = (100, 0, 300, height)
left_edge = (95, 0, marker_width, height)
right_edge = (395, 0, marker_width, height)

## coordinates 
left_lane = 150
center_lane = 250
right_lane = 350
lanes = (left_lane, center_lane, right_lane)

## for movement of the lane
lane_marker_move_y = 0

class Vehicle(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)

        image_scale = 45 / image.get_rect().width
        new_width = int(image.get_rect().width * image_scale)
        new_height = int(image.get_rect().height * image_scale)
        self.image = pygame.transform.scale(image, (new_width, new_height))

        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

class PlayerVehicle(Vehicle):
    def __init__(self, x, y):
        image = pygame.image.load(r'D:\c++\basics\images\car.png')
        super().__init__(image, x, y)

## players starting 
player_x = 250
player_y = 400
player_group  = pygame.sprite.Group()
player = PlayerVehicle(player_x, player_y)
player_group.add(player)

images_filenames = ['schoolbus.png','taxi.png','van.png','truck.png']
vehicle_images = []
for image_filename in images_filenames:
    image = pygame.image.load('images/' + image_filename)
    vehicle_images.append(image)

vehicle_group = pygame.sprite.Group()
crash = pygame.image.load('images/crash.png')
crash_rect = crash.get_rect()

## game loop 
clock = pygame.time.Clock()
fps = 120
running = True
while running:
    clock.tick(fps)

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        if gameover:
            # Disable player movement after game over
            if event.type == KEYDOWN and event.key in (K_a, K_d):
                continue

        if event.type == KEYDOWN:
            if event.key == K_a and player.rect.left > left_edge[0] + marker_width:
                player.rect.x -= 100
            elif event.key == K_d and player.rect.right < right_edge[0]:
                player.rect.x += 100
            
            for vehicle in vehicle_group:
                if pygame.sprite.collide_rect(player, vehicle):
                    gameover = True
                    if event.key == K_a:
                        player.rect.left = vehicle.rect.right
                        crash_rect.center = [player.rect.left, (player.rect.center[1] + vehicle.rect.center[1] / 2)]
                    elif event.key == K_d:
                        crash_rect.center = [player.rect.right, (player.rect.center[1] + vehicle.rect.center[1] / 2)]

    ## show the grass
    screen.fill(green)

    ## draw the road
    pygame.draw.rect(screen, gray, road)

    ## draw the edge markers 
    pygame.draw.rect(screen, yellow, left_edge)
    pygame.draw.rect(screen, yellow, right_edge)

    lane_marker_move_y += speed * 2
    if lane_marker_move_y >= marker_height * 2:
        lane_marker_move_y = 0

    for y in range(marker_height * -2, height, marker_height * 2):
        pygame.draw.rect(screen, white, (left_lane + 45, y + lane_marker_move_y, marker_width, marker_height))
        pygame.draw.rect(screen, white, (center_lane + 45, y + lane_marker_move_y, marker_width, marker_height))

    ## draw player's car
    player_group.draw(screen)

    if len(vehicle_group) < 2 and not gameover:
        add_vehicle = True
        for vehicle in vehicle_group:
            if vehicle.rect.top < vehicle.rect.height * 1.5:
                add_vehicle = False 
        if add_vehicle:
            lane = random.choice(lanes)
            image = random.choice(vehicle_images)
            vehicle = Vehicle(image, lane, height / -2)
            vehicle_group.add(vehicle)
            
    for vehicle in vehicle_group:
        if not gameover:
            vehicle.rect.y += speed  
            if vehicle.rect.top >= height:
                vehicle.kill()
                score += 1

                if score > 0 and score % 5 == 0:
                    speed += 1

    vehicle_group.draw(screen)

    ## font creation for score display
    font = pygame.font.Font(pygame.font.get_default_font(), 16)
    text = font.render('score: ' + str(score), True, white)
    text_rect = text.get_rect()
    text_rect.center = (50, 450)
    screen.blit(text, text_rect)

    if pygame.sprite.spritecollide(player, vehicle_group, True):
        gameover = True
        crash_rect.center = [player.rect.center[0], player.rect.top]

    if gameover:
        screen.blit(crash, crash_rect)  # corrected 'blit'
        pygame.draw.rect(screen, red, (0, 50, width, 100))
        font = pygame.font.Font(pygame.font.get_default_font(), 20)
        text = font.render('gameover, play again? (enter Y or N)', True, white)
        text_rect = text.get_rect()
        text_rect.center = (width / 2, 100)
        screen.blit(text, text_rect)

    pygame.display.update()

pygame.quit()
