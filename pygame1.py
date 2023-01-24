import pygame_gui as gui
import pygame
import random
import math
import sys
import os

FPS = 60


def load_image(name, color_key=None):
    fullname = os.path.join('src', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    if color_key is not None:
        image = image.convert()
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


class Game:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.display_size = [600, 800]

        self.display = pygame.display.set_mode(self.display_size)
        pygame.display.set_caption('Game')

        self.background = pygame.image.load('src/1613402985_112-p-bezhevii-kosmos-fon-164.jpg')

        self.PlayerImg = pygame.image.load('src/pngwing.com.png')
        self.PlayerImg = pygame.transform.scale(self.PlayerImg, (100, 100))
        self.EnemyImg = pygame.image.load('src/1646099128_5-adonius-club-p-monstr-piksel-art-25.png')
        self.EnemyImg = pygame.transform.scale(self.EnemyImg, (50, 50))
        self.PlayerX = self.display_size[0] / 2 - self.PlayerImg.get_size()[0] / 2
        self.PlayerY = self.display_size[1] - self.PlayerImg.get_size()[1] - 30

        self.PlayerMoveX = 0
        self.PlayerSpeed = 2

        self.Score = 0
        self.BestScore = 0
        self.Score_x = 5
        self.Score_y = 30
        self.HP = 100
        self.HP_x = 5
        self.HP_y = 5

        self.run = True
        self.Time1 = 0
        self.Reload1 = 120

        self.Enemy = []
        self.EnemyCount = 5

        self.Bullet = []
        self.BulletSpeed = 2
        self.font = pygame.font.Font('src/Proserpina-Deco.ttf', 16)
        self.BulletImg = pygame.image.load('src/estes-mini-honest-john-2446.png')
        self.BulletImg = pygame.transform.scale(self.BulletImg, (50, 70))

    def terminate(self):
        print("Game: exit")
        pygame.quit()
        sys.exit()

    def show_text(self):
        self.text_hp = self.font.render('HP: ' + str(self.HP), True, (255, 255, 255))
        self.display.blit(self.text_hp, (self.HP_x, self.HP_y))

        self.text_score = self.font.render('SCORE: ' + str(self.Score), True, (255, 255, 255))
        self.display.blit(self.text_score, (self.Score_x, self.Score_y))

    def PlayerUpdate(self):

        self.PlayerX += self.PlayerMoveX

        if self.PlayerX < 0:
            self.PlayerX = 0

        if self.PlayerX + self.PlayerImg.get_size()[0] > self.display_size[0]:
            self.PlayerX = self.display_size[0] - self.PlayerImg.get_size()[0]

    def EnemyCreate(self):
        EnemyX = random.randrange(0, self.display_size[0] - self.EnemyImg.get_size()[0])
        EnemyY = 30

        EnemyMoveX = random.randrange(-3, 3)
        EnemyMoveY = random.randrange(1, 2)

        return [EnemyX, EnemyY, EnemyMoveX * 0.3, EnemyMoveY * 0.2]

    def EnemyUpdate(self, Enemy):
        Enemy[1] += Enemy[3]
        Enemy[0] += Enemy[2]

        if Enemy[0] < 0:
            Enemy[0] = 0
            Enemy[2] = -Enemy[2]

        if Enemy[0] + self.EnemyImg.get_size()[0] > self.display_size[0]:
            Enemy[0] = self.display_size[0] - self.EnemyImg.get_size()[0]
            Enemy[2] = -Enemy[2]

        if Enemy[1] > self.display_size[1]:
            self.HP -= 5
            Enemy = self.EnemyCreate()

        return Enemy

    def isCollision(self, X1, Y1, Img1, X2, Y2, Img2):
        first = pygame.Rect(X1, Y1, Img1.get_width(), Img1.get_height())
        second = pygame.Rect(X2, Y2, Img2.get_width(), Img2.get_height())

        return first.colliderect(second)

    def BulletCreate(self):
        BulletX = self.PlayerX + self.PlayerImg.get_width() / 2 - self.BulletImg.get_width() / 2
        BulletY = self.PlayerY - self.BulletImg.get_height()
        BulletMoveX = 0
        BulletMoveY = -1 * math.sqrt(self.BulletSpeed * self.BulletSpeed - BulletMoveX * BulletMoveX)
        self.Bullet.append([BulletX, BulletY, BulletMoveX, BulletMoveY])

    def BulletUdpate(self, Bullet):
        Bullet[0] += Bullet[2]
        Bullet[1] += Bullet[3]
        return Bullet

    def play(self):
        next = "start"
        while next != "quit":
            if next == "start":
                next = self.start_screen()
            elif next == "level":
                next = self.play_level()
            elif next == "dead":
                next = self.dead()
        self.terminate()

    def start_screen(self):
        print("Game: start")
        intro_text = ["Space invaders", ""]

        fon = pygame.transform.scale(load_image('img.png'),
                                     (self.display_size[0], self.display_size[1]))
        self.display.blit(fon, (0, 0))

        self.ui = gui.UIManager((self.display_size[0], self.display_size[1]), "src/theme.json")
        text_coord = 200
        for line in intro_text:
            intro_rect = pygame.Rect(10, text_coord, self.display_size[0], 40)
            text_coord += 10
            text_coord += intro_rect.height
            lbl = gui.elements.UILabel(intro_rect, line, manager=self.ui)

        play_button = gui.elements.UIButton(relative_rect=pygame.Rect((250, text_coord + 10), (100, 50)),
                                            text='play >',
                                            manager=self.ui)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    return "quit"
                if event.type == gui.UI_BUTTON_PRESSED:
                    if event.ui_element == play_button:
                        return "level"
                #
                self.ui.process_events(event)
            #
            self.ui.draw_ui(self.display)

            pygame.display.flip()
            ms = self.clock.tick(FPS) / 1000.0
            self.ui.update(ms)

    def play_level(self):
        for i in range(self.EnemyCount):
            self.Enemy.append(self.EnemyCreate())

        while True:
            if self.Time1 != 0:
                self.Time1 += 1
            if self.Time1 > self.Reload1:
                self.Time1 = 0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                    if event.key in (pygame.K_LEFT, pygame.K_a):
                        self.PlayerMoveX = -self.PlayerSpeed
                    if event.key in (pygame.K_RIGHT, pygame.K_d):
                        self.PlayerMoveX = self.PlayerSpeed

                if event.type == pygame.MOUSEBUTTONDOWN:
                    key = pygame.mouse.get_pressed()
                    if key[0] and self.Time1 == 0:
                        self.Time1 = 1
                        self.BulletCreate()

                if event.type == pygame.KEYUP:
                    if self.PlayerMoveX < 0:
                        if event.key in (pygame.K_LEFT,
                                         pygame.K_a):
                            self.PlayerMoveX = 0
                    if self.PlayerMoveX > 0:
                        if event.key in (pygame.K_RIGHT,
                                         pygame.K_d):
                            self.PlayerMoveX = 0

            for i in range(self.EnemyCount):
                self.Enemy[i] = self.EnemyUpdate(self.Enemy[i])

            for bullet in self.Bullet:
                bullet = self.BulletUdpate(bullet)
                if bullet[1] < 0:
                    self.Bullet.remove(bullet)

            self.PlayerUpdate()

            if self.Score % 100 == 0 and self.Score != 0 and self.Score % 1000 != 0:
                self.Enemy.append(self.EnemyCreate())
                self.EnemyCount += 1
                if self.Reload1 > 75:
                    self.Reload1 -= 5
                self.Score += 5

            for enemy in self.Enemy:
                if self.isCollision(self.PlayerX, self.PlayerY, self.PlayerImg,
                                    enemy[0], enemy[1], self.EnemyImg):
                    self.Enemy.remove(enemy)
                    self.Enemy.append(self.EnemyCreate())
                    self.HP -= 10
                    continue

                for bullet in self.Bullet:
                    if self.isCollision(bullet[0], bullet[1], self.BulletImg,
                                        enemy[0], enemy[1], self.EnemyImg):
                        self.Bullet.remove(bullet)
                        self.Enemy.remove(enemy)
                        self.Enemy.append(self.EnemyCreate())
                        self.Score += 5
                        break

            self.display.blit(self.background, (0, 0))

            self.display.blit(self.PlayerImg, (self.PlayerX, self.PlayerY))

            for enemy in self.Enemy:
                self.display.blit(self.EnemyImg, (enemy[0], enemy[1]))

            for bullet in self.Bullet:
                self.display.blit(self.BulletImg, (bullet[0], bullet[1]))

            self.show_text()

            pygame.display.update()
            if self.HP <= 0:
                return "dead"

    def dead(self):
        print("Game: dead")
        intro_text = ["You're dead", "", f"Your score is {self.Score}"]

        self.EnemyCount = 5
        self.Reload1 = 120
        fon = pygame.transform.scale(load_image('img.png'),
                                     (self.display_size[0], self.display_size[1]))
        self.display.blit(fon, (0, 0))

        self.ui = gui.UIManager((self.display_size[0], self.display_size[1]), "src/theme.json")
        text_coord = 200
        for line in intro_text:
            intro_rect = pygame.Rect(10, text_coord, self.display_size[0], 40)
            text_coord += 10
            text_coord += intro_rect.height
            lbl = gui.elements.UILabel(intro_rect, line, manager=self.ui)

        play_button = gui.elements.UIButton(relative_rect=pygame.Rect((225, text_coord + 30), (150, 50)),
                                            text='Play again >',
                                            manager=self.ui)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    return "quit"
                if event.type == gui.UI_BUTTON_PRESSED:
                    if event.ui_element == play_button:
                        self.HP = 100
                        self.Score = 0
                        self.Enemy = []
                        self.Bullet = []
                        return "level"
                #
                self.ui.process_events(event)
            #
            self.ui.draw_ui(self.display)

            pygame.display.flip()
            ms = self.clock.tick(FPS) / 1000.0
            self.ui.update(ms)


game = Game()
game.play()
