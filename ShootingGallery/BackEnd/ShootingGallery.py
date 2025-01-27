import pygame
import time

from ShootingGallery.BackEnd.Gun import Gun
from ShootingGallery.BackEnd.ResourceManager import ResourceManager
from ShootingGallery.BackEnd.ScoreManager import ScoreManager
from ShootingGallery.BackEnd.SoundManager import SoundManager
from ShootingGallery.BackEnd.Target import Target


class ShootingGallery:
    def __init__(self):
        self.game_over = None
        self.menu = None
        pygame.init()
        self.WIDTH, self.HEIGHT = 900, 800
        self.screen = pygame.display.set_mode([self.WIDTH, self.HEIGHT])
        pygame.display.set_caption('Shooting Gallery')

        self.resource_manager = ResourceManager()
        self.sound_manager = SoundManager()

        self.font = self.resource_manager.load_font('assets/font/myFont.ttf', 32)
        self.big_font = self.resource_manager.load_font('assets/font/myFont.ttf', 60)

        self.bgs = [self.resource_manager.load_image(f'assets/bgs/{i}.png') for i in range(1, 4)]
        self.banners = [self.resource_manager.load_image(f'assets/banners/{i}.png') for i in range(1, 4)]
        self.gun_images = [pygame.transform.scale(self.resource_manager.load_image(f'assets/guns/{i}.png'), (100, 100)) for i in range(1, 4)]

        self.menu_img = self.resource_manager.load_image('assets/menus/mainMenu.png')
        self.game_over_img = self.resource_manager.load_image('assets/menus/GameOver.png')
        self.pause_img = self.resource_manager.load_image('assets/menus/pause.png')

        self.target_images = [[], [], []]
        for i in range(1, 3):
            self.target_images[i-1] = [pygame.transform.scale(self.resource_manager.load_image(f'assets/targets/{i}/{j}.png'), (120 - (j * 18), 80 - (j * 12))) for j in range(1, 4)]
        self.target_images[2] = [pygame.transform.scale(self.resource_manager.load_image(f'assets/targets/3/{j}.png'), (120 - (j * 18), 80 - (j * 12))) for j in range(1, 5)]

        self.gun = Gun(self.WIDTH, self.HEIGHT, self.gun_images)
        self.score_manager = ScoreManager(self.font)

        self.reset_game_state()
        print("reset game state is trigegred...")
        self.clock = pygame.time.Clock()
        self.fps = 60

    def reset_game_state(self):
        self.level = 0
        self.mode = 0
        self.points = 0
        self.total_shots = 0
        self.ammo = 0
        print("state ammo to zero")
        self.time_passed = 0
        self.time_remaining = 0
        self.counter = 1
        self.menu = True
        self.game_over = False
        self.pause = False
        self.clicked = False
        self.new_coords = True
        self.shot = False

        self.targets_config = {1: [10, 5, 3], 2: [12, 8, 5], 3: [15, 12, 8, 3]}
        self.target_coords = [[], [], []]
        print("Скидання стану гри...")

    def initialize_targets(self):
        if self.level == 0:
            self.target_coords = [[], [], []]
            return

        self.target_coords = [[], [], []] if self.level < 3 else [[], [], [], []]

        for i in range(len(self.target_coords)):
            my_list = self.targets_config[self.level]
            for j in range(my_list[i]):
                x = self.WIDTH // (my_list[i]) * j
                y = 300 - (i * (150 if self.level < 3 else 100)) + 30 * (j % 2)
                self.target_coords[i].append(Target(x, y, self.target_images[self.level - 1][i], speed_multiplier=i))

    def run(self):
        running = True
        while running:
            self.clock.tick(self.fps)
            for event in pygame.event.get():
                running = self.handle_event(event)

            self.update_game_state()
            self.draw()
            pygame.display.flip()

        pygame.quit()

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            return False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            if (0 < mouse_pos[0] < self.WIDTH) and (0 < mouse_pos[1] < self.HEIGHT - 200):
                self.shot = True
                self.total_shots += 1
                if self.mode == 1:
                    self.ammo -= 1

            if (670 < mouse_pos[0] < 860) and (660 < mouse_pos[1] < 715):
                self.resume_level = self.level
                self.pause = True
                self.clicked = True
            elif (670 < mouse_pos[0] < 860) and (715 < mouse_pos[1] < 760):
                print("reset")
                self.menu = True
                self.clicked = True
                self.new_coords = True

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.clicked:
            self.clicked = False

        return True

    def update_game_state(self):
        if self.level != 0:
            self.counter = (self.counter % 60) + 1
            if self.counter == 1:
                self.time_passed += 1
                if self.mode == 2:
                    self.time_remaining -= 1

        if self.new_coords:
            self.initialize_targets()
            self.new_coords = False

        self.game_over = False
        if self.level == 1:
            self.process_level_targets(0)
        elif self.level == 2:
            self.process_level_targets(1)
        elif self.level == 3:
            self.process_level_targets(2)

        self.check_level_completion()

    def process_level_targets(self, level_index):
        for target_row in self.target_coords:
            for target in target_row:
                target.move(self.WIDTH)

        if self.shot:
            mouse_pos = pygame.mouse.get_pos()
            hit_any_target = False

            for row_index, target_row in enumerate(self.target_coords):
                self.target_coords[row_index] = [target for target in target_row if not target.rect.collidepoint(mouse_pos)]
                if len(self.target_coords[row_index]) < len(target_row):
                    hit_any_target = True
                    self.points += 10 * ((row_index + 1) ** 2)

            if hit_any_target:
                sounds = ['bird', 'plate', 'laser']
                self.sound_manager.play_sound(sounds[min(level_index, len(sounds) - 1)])

            self.shot = False

    def check_level_completion(self):
        target_count = len([t for row in self.target_coords for t in row])

        if (self.level == 3 and target_count == 0) or \
                (self.mode == 1 and self.ammo == 0) or \
                (self.mode == 2 and self.time_remaining == 0):
            print("handle_game_over is triggered")
            self.handle_game_over()

        if target_count == 0 and self.level < 3:
            self.level += 1
            self.new_coords = True
            print("first issue is triggered")

    def handle_game_over(self):
        if self.level == 3 and len([t for row in self.target_coords for t in row]) == 0:
            self.game_over = True
            print("game over anter complecion 3rd game")

            if self.score_manager.update_best_scores(self.mode, self.points, self.time_passed):
                self.score_manager.save_best_scores()
        else:
            self.new_coords = False

            if self.score_manager.update_best_scores(self.mode, self.points, self.time_passed):
                self.score_manager.save_best_scores()
            self.game_over = True

    def draw(self):
        self.screen.fill('black')

        if self.level > 0:
            self.screen.blit(self.bgs[self.level - 1], (0, 0))
            self.screen.blit(self.banners[self.level - 1], (0, self.HEIGHT - 200))

        if self.menu:
            self.draw_menu()
        elif self.game_over and not self.menu:
            self.draw_game_over()
        elif self.pause:
            self.draw_pause()
        else:
            self.draw_game_play()

    def draw_menu(self):
        self.screen.blit(self.menu_img, (0, 0))
        mouse_pos = pygame.mouse.get_pos()
        clicks = pygame.mouse.get_pressed()

        menu_buttons = [
            (pygame.Rect((170, 524), (260, 100)), self.mode_select, 0),
            (pygame.Rect((475, 524), (260, 100)), self.mode_select, 1),
            (pygame.Rect((170, 661), (260, 100)), self.mode_select, 2),
            (pygame.Rect((475, 661), (260, 100)), self.reset_scores, None)
            # Add a placeholder
        ]

        best_scores = [
            self.score_manager.best_freeplay,
            self.score_manager.best_ammo,
            self.score_manager.best_timed
        ]

        for i, (button, action, mode_or_reset) in enumerate(menu_buttons):
            if button.collidepoint(mouse_pos) and clicks[0] and not self.clicked:
                action(mode_or_reset)
                break

            # Draw best scores
            if i < 3:
                score_text = self.font.render(str(best_scores[i]), True, 'white')
                if i < 2:
                    self.screen.blit(score_text, (340 + i * 320, 580))
                if i == 2:
                    self.screen.blit(score_text, (120 + i * 120, 716))

    def mode_select(self, mode):
        self.mode = mode
        self.level = 1
        self.menu = False
        self.time_passed = 0
        self.points = 0
        self.total_shots = 0
        self.clicked = True
        self.new_coords = True

        if mode == 1:
            self.ammo = 81
        elif mode == 2:
            self.time_remaining = 30

    def reset_scores(self, _):
        self.score_manager.load_best_scores()
        self.reset_game_state()
        self.score_manager.best_freeplay = 0
        self.score_manager.best_ammo = 0
        self.score_manager.best_timed = 0
        self.score_manager.save_best_scores()
        self.clicked = True
        print("reset button")

    def draw_pause(self):
        """Display the pause screen."""
        # Draw the background image for the pause screen
        self.screen.blit(self.pause_img, (0, 0))

        # Get the current mouse position and button states
        mouse_position = pygame.mouse.get_pos()
        mouse_clicks = pygame.mouse.get_pressed()

        # Define buttons: (rect area, action function)
        buttons = [
            (pygame.Rect((170, 661), (260, 100)), self.resume_game),  # Resume the game
            (pygame.Rect((475, 661), (260, 100)), self.return_to_menu)  # Return to the main menu
        ]

        # Check if any button is clicked
        for button, action in buttons:
            if button.collidepoint(mouse_position) and mouse_clicks[0] and not self.clicked:
                action()  # Call the corresponding action
                break

    def draw_game_over(self):
        """Display the game-over screen."""
        print("Game-over screen is triggered")
        # Draw the background image for the game-over screen
        self.screen.blit(self.game_over_img, (0, 0))

        # Get the current mouse position and button states
        mouse_position = pygame.mouse.get_pos()
        mouse_clicks = pygame.mouse.get_pressed()

        # Determine the score to display based on the game mode
        displayed_score = self.time_passed if self.mode == 0 else self.points
        score_text = self.big_font.render(str(displayed_score), True, 'white')
        self.screen.blit(score_text, (650, 570))

        # Define buttons: (rect area, action function)
        buttons = [
            (pygame.Rect((170, 661), (260, 100)), self.exit_game),  # Exit the game
            (pygame.Rect((475, 661), (260, 100)), self.return_to_menu)  # Return to the main menu
        ]

        if self.return_to_menu:
            print("return_to_menu")

        # Check if any button is clicked
        for button, action in buttons:
            if button.collidepoint(mouse_position) and mouse_clicks[0] and not self.clicked:
                action()  # Call the corresponding action
                break

    def return_to_menu(self):
        self.game_over = False
        self.pause = False
        time.sleep(0.25)
        self.menu = True


    def exit_game(self):
        # Зберегти найкращі результати перед виходом
        self.score_manager.save_best_scores()
        # Закрити Pygame і завершити програму
        pygame.quit()
        quit()

    def resume_game(self):
        self.level = self.resume_level
        self.pause = False
        self.clicked = True

    def draw_game_play(self):
        # Draw moving targets
        for row in self.target_coords:
            for target in row:
                target.draw(self.screen)

        # Draw gun and score
        self.gun.draw(self.screen, self.level, pygame.mouse.get_pos())
        self.score_manager.draw_score(
            self.screen, self.points, self.total_shots,
            self.time_passed, self.mode, self.ammo, self.time_remaining
        )