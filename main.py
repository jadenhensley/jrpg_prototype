import pygame, sys, random, path_util
from anim_data import animations

pygame.init()
pygame.font.init()
pygame.mixer.init()
clock = pygame.time.Clock()
sWidth, sHeight = 720, 480
sWidth, sHeight = 1280, 720
screen = pygame.display.set_mode((sWidth, sHeight))
pygame.display.set_caption("roguelike/RPG project prototype")
PROJECT_PATH = path_util.get_project_directory()

monogram = pygame.font.Font(f"{PROJECT_PATH}/font/monogram.ttf", 54)
monogramLarge = pygame.font.Font(f"{PROJECT_PATH}/font/monogram.ttf", 102)



mixer = pygame.mixer
mixer.music.load(f"{PROJECT_PATH}/audio/mysterious_dungeon.wav")
mixer.music.set_volume(0.05)
music_playing = 0

floor_image = pygame.image.load(f"{PROJECT_PATH}/sprites/level/floor.png")
floor_image = pygame.transform.scale(floor_image, (floor_image.get_width()*100, floor_image.get_height()*100))

def printg(text, x, y, color=(255,255,255)):
    text = monogram.render(text, True, color)
    screen.blit(text, (x, y))

bgv = 20
fgv = 200

parallax_background = [
    f"{PROJECT_PATH}/sprites/background/parallax_mountain_pack/layers/parallax-mountain-bg.png",
    f"{PROJECT_PATH}/sprites/background/parallax_mountain_pack/layers/parallax-mountain-mountain-far.png",
    f"{PROJECT_PATH}/sprites/background/parallax_mountain_pack/layers/parallax-mountain-mountains.png",
    f"{PROJECT_PATH}/sprites/background/parallax_mountain_pack/layers/parallax-mountain-trees.png",
    f"{PROJECT_PATH}/sprites/background/parallax_mountain_pack/layers/parallax-mountain-foreground-trees.png"
]

converted_layers = []

for layer in parallax_background:
            temp = pygame.image.load(layer)
            temp = pygame.transform.scale(temp, (sWidth, sHeight))
            converted_layers.append(temp)


class Knight(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(animations["knight"]["idle"][0])
        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image, (self.image.get_width(), self.image.get_height()))
        self.current_image = 0
        self.current_animation = "idle"
        self.velocity = 0
        self.direction = "right"
        self.in_menu = False
        # button states
        self.LEFT = False
        self.UP = False
        self.RIGHT = False
        self.DOWN = False
        self.ACTIONA = False
        self.ACTIONB = False
        self.ROLL = False
        self.RUN = False
    
    def update(self, surface):
        self.movement_state_machine()
        self.anim_state_machine(surface)


    def movement_state_machine(self):
        if self.LEFT:
            self.rect.left -= 10
        if self.RIGHT:
            self.rect.right += 10
        if self.UP:
            self.rect.top -= 10
        if self.DOWN:
            self.rect.bottom += 10
        if self.ACTIONA:
            self.current_animation = "actionA"
        if self.ACTIONB:
            self.current_animation = "actionB"
    
    def anim_state_machine(self, surface):
        if self.current_animation == "idle":
            if self.current_image > len(animations["knight"]["idle"]):
                self.current_image = 0
            self.image = pygame.image.load(animations["knight"]["idle"][int(self.current_image)])
            if not self.in_menu:
                self.image = pygame.transform.scale(self.image, (self.image.get_width()*3, self.image.get_height()*3))
            else:
                self.image = pygame.transform.scale(self.image, (self.image.get_width()*8, self.image.get_height()*8))
            self.current_image += 0.2
        if self.current_animation == "run":
            if self.current_image > len(animations["knight"]["run"]):
                self.current_image = 0
            self.image = pygame.image.load(animations["knight"]["run"][int(self.current_image)])
            if not self.in_menu:
                self.image = pygame.transform.scale(self.image, (self.image.get_width()*3, self.image.get_height()*3))
                self.current_image += 0.4
            else:
                self.image = pygame.transform.scale(self.image, (self.image.get_width()*8, self.image.get_height()*8))
                self.current_image += 0.8
        if self.current_animation == "attackA":
            if self.current_image > len(animations["knight"]["attackA"]):
                self.current_image = 0
            self.image = pygame.image.load(animations["knight"]["attackA"][int(self.current_image)])
            if not self.in_menu:
                self.image = pygame.transform.scale(self.image, (self.image.get_width()*3, self.image.get_height()*3))
            else:
                self.image = pygame.transform.scale(self.image, (self.image.get_width()*8, self.image.get_height()*8))
            self.current_image += 0.2
        if self.current_animation == "attackB":
            if self.current_image > len(animations["knight"]["attackB"]):
                self.current_image = 0
            self.image = pygame.image.load(animations["knight"]["attackB"][int(self.current_image)])
            if not self.in_menu:
                self.image = pygame.transform.scale(self.image, (self.image.get_width()*3, self.image.get_height()*3))
            else:
                self.image = pygame.transform.scale(self.image, (self.image.get_width()*8, self.image.get_height()*8))
            self.current_image += 0.2
        if self.current_animation == "roll":
            if self.current_image > len(animations["knight"]["roll"]):
                self.current_image = 0
            self.image = pygame.image.load(animations["knight"]["roll"][int(self.current_image)])
            if not self.in_menu:
                self.image = pygame.transform.scale(self.image, (self.image.get_width()*3, self.image.get_height()*3))
            else:
                self.image = pygame.transform.scale(self.image, (self.image.get_width()*8, self.image.get_height()*8))
            self.current_image += 0.2
        if self.current_animation == "death":
            if self.current_image > len(animations["knight"]["death"]):
                self.current_image = 0
            self.image = pygame.image.load(animations["knight"]["death"][int(self.current_image)])
            if not self.in_menu:
                self.image = pygame.transform.scale(self.image, (self.image.get_width()*3, self.image.get_height()*3))
            else:
                self.image = pygame.transform.scale(self.image, (self.image.get_width()*8, self.image.get_height()*8))
            self.current_image += 0.2
        if self.direction == "left":
            self.image = pygame.transform.flip(self.image, True, False)

class Wizard(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

class FlyingEye(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(animations["flyingeye"]["chasing"][0])
        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image, (self.image.get_width(), self.image.get_height()))
        self.current_image = 0

    def update(self, surface):
        if self.current_image > len(animations["flyingeye"]["chasing"]):
            self.current_image = 0
        self.image = pygame.image.load(animations["flyingeye"]["chasing"][int(self.current_image)])
        self.image = pygame.transform.scale(self.image, (self.image.get_width()*3, self.image.get_height()*3))
        self.current_image += 0.2

class EyeProjectile(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(animations["flyingeye"]["projectile"][0])
        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image, (self.image.get_width(), self.image.get_height()))
        self.current_image = 0

    def update(self, surface):
        if self.current_image > len(animations["flyingeye"]["projectile"]):
            self.current_image = 0
        self.image = pygame.image.load(animations["flyingeye"]["projectile"][int(self.current_image)])
        self.image = pygame.transform.scale(self.image, (self.image.get_width()*3, self.image.get_height()*3))
        self.current_image += 0.2

class Wall(pygame.sprite.Sprite):
    def __init__(self, x=random.randint(0, sHeight), y=random.randint(0, sWidth)):
        super().__init__()
        self.image = pygame.image.load(f"{PROJECT_PATH}/sprites/level/border.png")
        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image, (self.image.get_width()*3, self.image.get_height()*3))
        self.rect.x = x
        self.rect.y = y
        self.current_image = 0

class HealthBar():
    def __init__(self):
        self.percent = 100
    

class Game():
    def __init__(self):
        self.current_scene = "menu"
        self.menu_option = 0
    
    def debug(self):
        global music_playing; music_playing = 0; mixer.music.stop()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RETURN:
                    knight.current_animation = random.choice(["run", "idle", "death", "roll", "attackA", "attackB"])
                if event.key == pygame.K_TAB:
                    self.current_scene = "menu"
        
        screen.fill((20,20,20))
        printg("debug/testing", sWidth-270, 0, (0,255,0))
        printg("enter to cycle animations", 500, 400, (0,180,0))

        eGroup.draw(screen)
        eGroup.update(screen)
        knight.in_menu = False
        knight.rect.right = sWidth - 200
        

        clock.tick(60)
        pygame.display.flip()


    def state_machine(self):
        if self.current_scene == "debug":
            self.debug()
        elif self.current_scene == "menu":
            self.menu()
        elif self.current_scene == "game":
            self.game()
        elif self.current_scene == "settings":
            self.menu()
        elif self.current_scene == "combat":
            self.combat()

    def menu(self):
        global music_playing; music_playing = 0; mixer.music.stop()
        global parallax_background, converted_layers
        
        options = ['game', 'settings', 'debug']
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_TAB:
                    self.current_scene = "game"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    knight.current_animation = "roll"
                    if self.menu_option != len(options)-1:
                        self.menu_option += 1
                if event.key == pygame.K_UP:
                    knight.current_animation = "run"
                    if self.menu_option != 0:
                        self.menu_option -= 1
                if event.key == pygame.K_RETURN:
                    self.current_scene = options[self.menu_option]

        screen.fill((20,20,20))
        
        
        screen.blit(converted_layers[0], (0,0))
        screen.blit(converted_layers[1], (0,0))
        screen.blit(converted_layers[2], (0,0))
        screen.blit(converted_layers[3], (0,0))
        screen.blit(converted_layers[4], (0,0))

        

        printg("main menu", sWidth // 2, 0, (255,0,0))
        
        playerGroup.draw(screen)
        playerGroup.update(screen)
        knight.update(screen)
        knight.rect.right = 0
        knight.rect.bottom = 0
        knight.in_menu = True
            
        
        for item in range(len(options)):
            if self.menu_option == item:
                printg(options[item], sWidth // 2, item*100+200, (0, 255, 0))
            else:
                printg(options[item], sWidth // 2, item*100+200, (0, 0, 0))

        clock.tick(60)
        pygame.display.flip()


    def game(self):
        global music_playing, bgv, fgv
        if music_playing == 0:
            mixer.music.play()
            music_playing = 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    knight.current_animation = "attackA"
                elif event.key == pygame.K_x:
                    knight.current_animation = "attackB"
                elif event.key == pygame.K_c:
                    knight.current_animation = "roll"
                    if knight.direction == "right":
                        knight.rect.right += 150
                    if knight.direction == "left":
                        knight.rect.left -= 150
                elif event.key == pygame.K_RIGHT:
                    knight.RIGHT, knight.LEFT = True, False
                    knight.current_animation = "run"
                    knight.direction = "right"
                elif event.key == pygame.K_LEFT:
                    knight.LEFT, knight.RIGHT = True, False
                    knight.current_animation = "run"
                    knight.direction = "left"
                elif event.key == pygame.K_DOWN:
                    knight.DOWN, knight.UP = True, False
                    knight.current_animation = "run"
                elif event.key == pygame.K_UP:
                    knight.UP, knight.DOWN = True, False
                    knight.current_animation = "run"
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_TAB:
                    self.current_scene = "debug"
                if event.key == pygame.K_RIGHT:
                    knight.RIGHT = False
                if event.key == pygame.K_LEFT:
                    knight.LEFT = False
                if event.key == pygame.K_UP:
                    knight.UP = False
                if event.key == pygame.K_DOWN:
                    knight.DOWN = False
        
        if knight.rect.left < -100:
            knight.rect.left = -100
        if knight.rect.right > sWidth - 200:
            knight.rect.right = sWidth - 200
        if knight.rect.top < -100:
            knight.rect.top = -100
        if knight.rect.bottom > sHeight - 200:
            knight.rect.bottom = sHeight - 200

        knight.in_menu = False

        print(knight.RIGHT)
        
        bgv += 0.5
        fgv -= 0.1
        # screen.fill((int(bgv),int(bgv),int(bgv)))
        # pygame.draw.circle(screen, ((int(fgv),int(fgv),int(fgv))), (200, 200), int(fgv))
        screen.fill((20,20,20))
        screen.blit(floor_image, (0,0))
        knight.update(screen)
        objGroup.draw(screen)
        objGroup.update(screen)

        playerGroup.draw(screen)
        playerGroup.update(screen)
        printg("game", sWidth-270, 0, (255, 0, 0))
        clock.tick(60)
        pygame.display.flip()

    def combat(self):
        pass


eGroup = pygame.sprite.Group()
objGroup = pygame.sprite.Group()
playerGroup = pygame.sprite.Group()
projectile = EyeProjectile()
knight = Knight()
eGroup.add(FlyingEye())
eGroup.add(projectile)
eGroup.add(knight)
playerGroup.add(knight)
objGroup.add(Wall())

g = Game()

while True:
    g.state_machine()
    clock.tick(60)
