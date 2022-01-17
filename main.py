from turtle import update
import pygame, sys, random, path_util
from anim_data import animations
from monsters_data import monsters

pygame.init()
pygame.font.init()
pygame.mixer.init()
clock = pygame.time.Clock()
sWidth, sHeight = 720, 480
sWidth, sHeight = 1280, 720
screen = pygame.display.set_mode((sWidth, sHeight))
pygame.display.set_caption("Turn based JRPG prototype")
PROJECT_PATH = path_util.get_project_directory()

monogram = pygame.font.Font(f"{PROJECT_PATH}/font/monogram.ttf", 54)
monogramLarge = pygame.font.Font(f"{PROJECT_PATH}/font/monogram.ttf", 102)
monogramXL = pygame.font.Font(f"{PROJECT_PATH}/font/monogram.ttf", 158)

pygame.mouse.set_visible(False)


mixer = pygame.mixer
mixer.music.load(f"{PROJECT_PATH}/audio/mysterious_dungeon.wav")
mixer.music.set_volume(0.05)
music_playing = 0
game_paused = 0
debug_enabled = 0

floor_image = pygame.image.load(f"{PROJECT_PATH}/sprites/level/floor.png")
floor_image = pygame.transform.scale(floor_image, (floor_image.get_width()*100, floor_image.get_height()*100))

def printg(text, x, y, color=(255,255,255)):
    text = monogram.render(text, True, color)
    screen.blit(text, (x, y))

def printgLarge(text, x, y, color=(255,255,255)):
    text = monogramXL.render(text, True, color)
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


class EnemyShadow():
    def __init__(self):
        self.shadowSurface = pygame.surface.Surface((50,50))
        self.shadowRect = pygame.rect.Rect(0, 0, 50,50)
        self.shadowSurface.set_alpha(150)
        
    def update(self):
        pygame.draw.rect(self.shadowSurface, (20,20,20), self.shadowRect)
        screen.blit(self.shadowSurface, (0, 0))
        self.shadowRect.bottom += 10

class HealthBar(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hbRect = pygame.rect.Rect(x, y, 302, 52)
        # backdrop for healthbar
        self.bdRect = pygame.rect.Rect(x, y, 310, 60)
        self.percentage = 1.00

    def update(self, surface):
        self.hbRect = pygame.rect.Rect(self.x, self.y, 50, 300*self.percentage)
        pygame.draw.rect(screen, (15,15,15), self.bdRect)
        pygame.draw.rect(screen, (255,0,0), self.hbRect)

    def change_percentage(self, value):
        self.percentage = value


class Mouse(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        cursorIMG = pygame.image.load(f"{PROJECT_PATH}/sprites/cursor/cursor.png")
        self.cursorIMG = pygame.transform.scale(cursorIMG, (cursorIMG.get_width()*2, cursorIMG.get_height()*2))
        hoverIMG = pygame.image.load(f"{PROJECT_PATH}/sprites/cursor/cursorHover.png")
        self.hoverIMG = pygame.transform.scale(hoverIMG, (hoverIMG.get_width()*2, hoverIMG.get_height()*2))
        
        self.image=self.cursorIMG
        self.rect = self.image.get_rect()
    
    def update(self, surface):
        pos = pygame.mouse.get_pos()
        screen.blit(self.image, (pos[0], pos[1]))

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
        self.paused = False
        # button states
        self.LEFT = False
        self.UP = False
        self.RIGHT = False
        self.DOWN = False
        self.ACTIONA = False
        self.ACTIONB = False
        self.ROLL = False
        self.RUN = False
        self.transparent = pygame.Surface((sWidth, sHeight))
        self.last_pause = 0
        self.hp = 84
        self.sp = 42
        self.attack = 9
        self.defense = 30
        self.level = 0

    def update(self, surface):
        if self.paused:
            self.transparent.set_alpha(150)
            screen.blit(self.transparent, (0, 0))
        
        # pygame.draw.circle(transparent, (30,30,30), (0, 0), 20)

        # pygame.draw.circle(screen, (30,30,30), (self.rect.x, self.rect.y), 10)
        
        if not self.paused:
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
        

class Dragon(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.name = random.choice(("dragon0","dragon1","dragon2","dragon3","dragon4","dragon5","dragon6","dragon7","dragon8","dragon9","dragon10"))
        self.image = pygame.image.load(monsters[self.name]["sprite"])
        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image, (self.image.get_width()*4, self.image.get_height()*4))
        self.image = pygame.transform.flip(self.image, True, False)
        self.hp = monsters[self.name]["stats"]["hp"]
        self.sp = monsters[self.name]["stats"]["sp"]
        self.attack = monsters[self.name]["stats"]["attack"]
        self.defense = monsters[self.name]["stats"]["defense"]

    def update(self, surface):
        self.rect.right = sWidth - 450
        self.rect.bottom = 200
        current_time = pygame.time.get_ticks()
        printg(f"tick: {current_time}",0,0)
        if current_time % 100 == 0:
            knight.hp -= random.randint(4, self.attack)

    def reset(self):
        self.name = random.choice(("dragon0","dragon1","dragon2","dragon3","dragon4","dragon5","dragon6","dragon7","dragon8","dragon9","dragon10"))
        self.image = pygame.image.load(monsters[self.name]["sprite"])
        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image, (self.image.get_width()*4, self.image.get_height()*4))
        self.image = pygame.transform.flip(self.image, True, False)
        self.hp = monsters[self.name]["stats"]["hp"] + 15 * knight.level
        self.sp = monsters[self.name]["stats"]["sp"] + 4 * knight.level
        self.attack = monsters[self.name]["stats"]["attack"]
        self.defense = monsters[self.name]["stats"]["defense"]
        

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
        self.right = 300
        self.top = 300

class EyeProjectile(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(animations["flyingeye"]["projectile"][0])
        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image, (self.image.get_width(), self.image.get_height()))
        self.current_image = 0
        self.in_menu = False

    def update(self, surface):
        if self.current_image > len(animations["flyingeye"]["projectile"]):
            self.current_image = 0
        self.image = pygame.image.load(animations["flyingeye"]["projectile"][int(self.current_image)])
        if not self.in_menu:
            self.image = pygame.transform.scale(self.image, (self.image.get_width()*3, self.image.get_height()*3))
        else:
            self.image = pygame.transform.scale(self.image, (self.image.get_width()*6, self.image.get_height()*6))
        self.current_image += 0.2

class Wall(pygame.sprite.Sprite):
    # def __init__(self, x=random.randint(0, sHeight), y=random.randint(0, sWidth)):
    def __init__(self, x=100, y=100):
        super().__init__()
        self.image = pygame.image.load(f"{PROJECT_PATH}/sprites/level/border.png")
        self.image = pygame.transform.scale(self.image, (self.image.get_width()*3, self.image.get_height()*3))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.current_image = 0

    def update(self, surface):
        for i in range(10):
            screen.blit(self.image, (i*self.image.get_width(), 0))
            screen.blit(self.image, (i*self.image.get_width(), sHeight-self.image.get_height()))
        # collision, doesn't work
        # pygame.draw.circle(screen, (255,0,0), (self.rect.x, self.rect.y), 10)
        # if self.rect.bottom < knight.rect.top:
        #     knight.rect.top = self.rect.bottom

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
        printg("tab to main menu", 500, 600, (0,180,0))

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
        elif self.current_scene == "battle":
            self.battle()

    def menu(self):
        global music_playing; music_playing = 0; mixer.music.stop()
        global parallax_background, converted_layers
        
        options = ['game', 'settings', 'debug']
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                pass
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
                    knight.last_pause = pygame.time.get_ticks()
                    self.current_scene = options[self.menu_option]

        screen.fill((20,20,20))
        
        
        screen.blit(converted_layers[0], (0,0))
        screen.blit(converted_layers[1], (0,0))
        screen.blit(converted_layers[2], (0,0))
        screen.blit(converted_layers[3], (0,0))
        screen.blit(converted_layers[4], (0,0))

        
        printgLarge("RPG Prototype", sWidth // 4 - 30, -10, (255,255,255))
        printgLarge("RPG Prototype", sWidth // 4 - 30, 0, (0,255,0))
        printg("included in demo: Overworld + Battle + Debug", sWidth // 4 - 100, 150, (0, 0, 0))
        
        playerGroup.draw(screen)
        playerGroup.update(screen)
        # screen.blit(knight.image, knight.rect.center)
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

    

    def battle(self):
        global music_playing, game_paused
        player_commands = ["attack", "heal", "negotiate"]
        
        screen.fill((20,20,20))
        for cmd in range(len(player_commands)):
            if cmd != self.menu_option:
                printg(player_commands[cmd], sWidth // 4 + 250*cmd, 550, (255,255,255))
            else:
                printg(player_commands[cmd], sWidth // 4 + 250*cmd, 550, (0, 255, 0))
            
        if music_playing == 0:
            mixer.music.play()
            music_playing = 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    knight.DOWN, knight.UP = True, False
                    knight.current_animation = "roll"
                elif event.key == pygame.K_UP:
                    knight.UP, knight.DOWN = True, False
                    knight.current_animation = "run"
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_TAB:
                    self.current_scene = "debug"
                if event.key == pygame.K_RIGHT:
                    if self.menu_option != len(player_commands)-1:
                        self.menu_option += 1
                if event.key == pygame.K_LEFT:
                    if self.menu_option != 0:
                        self.menu_option -= 1
                if event.key == pygame.K_UP:
                    pass
                if event.key == pygame.K_DOWN:
                    knight.DOWN = False
                if event.key == pygame.K_RETURN:
                    if player_commands[self.menu_option] == "attack":
                        knight.current_animation = "attackA"
                        dragon.hp -= random.randint(2, knight.attack)
                    elif player_commands[self.menu_option] == "heal":
                        knight.current_animation = "roll"
                        knight.hp += random.randint(1, knight.defense)
                    elif player_commands[self.menu_option] == "negotiate":
                        knight.current_animation = "attackB"
                        dragon.hp -= random.randint(1, knight.attack // 2)
                        
        
        knight.in_menu = True
        knight.direction = "right"
        knight.rect.left = -200
        knight.rect.top = -150

        printg(f"Player HP: {knight.hp}", sWidth // 4, sHeight - 100, (255,0,0))
        printg(f"Player SP: {knight.sp}", sWidth // 4, sHeight - 50, (0,255,0))
        printg(f"Enemy HP: {dragon.hp}", sWidth // 2 + 30, sHeight - 100, (255,0,0))
        printg(f"Enemy SP: {dragon.sp}", sWidth // 2 + 30, sHeight - 50, (0,255,0))

        if dragon.hp <= 0:
            knight.level += 1
            self.current_scene = "game"
            dragon.reset()


        playerGroup.draw(screen)
        playerGroup.update(screen)
        eyeEnemy.update(screen)
        eGroup.draw(screen)
        eGroup.update(screen)
        clock.tick(60)
        pygame.display.flip()



    def game(self):
        global music_playing, game_paused, bgv, fgv, enemiesOW

        options_menu = ["resume", "main menu", "toggle debug commands", "enter battle", "quit"]
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
                    knight.current_animation = "idle"
                if event.key == pygame.K_LEFT:
                    knight.LEFT = False
                    knight.current_animation = "idle"
                if event.key == pygame.K_UP:
                    knight.UP = False
                    if knight.paused:
                        if self.menu_option != 0:
                            self.menu_option -= 1
                if event.key == pygame.K_DOWN:
                    knight.DOWN = False
                    if knight.paused:
                        if self.menu_option != len(options_menu)-1:
                            self.menu_option += 1
                if event.key == pygame.K_RETURN:
                    if options_menu[self.menu_option] == "quit":
                        pygame.quit()
                        sys.exit()
                    if options_menu[self.menu_option] == "settings":
                        self.current_scene = "settings"
                    if options_menu[self.menu_option] == "main menu":
                        self.menu_option = 0
                        self.current_scene = "menu"
                    if options_menu[self.menu_option] == "enter battle":
                        self.menu_option = 0
                        self.current_scene = "battle"
                    if knight.paused == True:
                        knight.paused = False
                        knight.last_pause = pygame.time.get_ticks()
                        knight.paused = False
                        game_paused = False
                    if knight.paused == False:
                        if pygame.time.get_ticks() > knight.last_pause+360 and pygame.time.get_ticks() > 2000:
                            knight.paused = True
                            game_paused = True

        if knight.rect.left < -100:
            knight.rect.left = -100
        if knight.rect.right > sWidth - 200:
            knight.rect.right = sWidth - 200
        if knight.rect.top < -100:
            knight.rect.top = -100
        if knight.rect.bottom > sHeight - 200:
            knight.rect.bottom = sHeight - 200

        knight.in_menu = False
        
        bgv += 0.5
        fgv -= 0.1
        # pygame.draw.circle(screen, ((int(fgv),int(fgv),int(fgv))), (200, 200), int(fgv))
        screen.fill((20,20,20))
        screen.blit(floor_image, (0,0))
        # screen.fill((int(bgv),int(bgv),int(bgv)))
        knight.update(screen)
        objGroup.draw(screen)
        objGroup.update(screen)
        for shadow in enemiesOW:
            shadow.update()

        playerGroup.draw(screen)
        playerGroup.update(screen)
        # hb.update(screen)
        cursorGroup.update(screen)

        # hb.update(screen)

        printgLarge(f"level: {knight.level}", sWidth // 4 -300, sHeight - 160)

        if not knight.paused:
            printg("game", sWidth-270, 0, (255, 0, 0))
            if pygame.time.get_ticks() % 100 == 0:
                # screen transitions
                for i in range(2000):
                    screen.fill((i%255,i%255,i%255))
                self.current_scene = "battle"
        else:
            printgLarge("Game Paused", sWidth//4-30, 0, (0, 255, 0))
            for item in range(len(options_menu)):
                if self.menu_option == item:
                    printg(options_menu[item], sWidth // 2, item*100+200, (0, 255, 0))
                else:
                    printg(options_menu[item], sWidth // 2, item*100+200, (255, 255, 255))

        clock.tick(60)
        pygame.display.flip()

    def combat(self):
        pass


eGroup = pygame.sprite.Group()
objGroup = pygame.sprite.Group()
playerGroup = pygame.sprite.Group()
cursorGroup = pygame.sprite.Group()

projectile = EyeProjectile()
knight = Knight()
eyeEnemy = FlyingEye()
dragon = Dragon()
eGroup.add(dragon)
# eGroup.add(projectile)
# eGroup.add(knight)
playerGroup.add(knight)
hb = HealthBar(200, 200)
objGroup.add(Wall())
cursorGroup.add(Mouse())

enemiesOW = []
enemiesOW.append(EnemyShadow())

g = Game()

while True:
    g.state_machine()
    clock.tick(60)