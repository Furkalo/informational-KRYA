
class ScoreManager:
    def __init__(self, font):
        self.font = font
        self.best_scores_file = 'high_scores.txt'
        self.load_best_scores()

    def load_best_scores(self):
        try:
            with open(self.best_scores_file, 'r') as file:
                self.best_freeplay = int(file.readline().strip())
                self.best_ammo = int(file.readline().strip())
                self.best_timed = int(file.readline().strip())
        except (FileNotFoundError, ValueError):
            self.best_freeplay = 0
            self.best_ammo = 0
            self.best_timed = 0

    def save_best_scores(self):
        with open(self.best_scores_file, 'w') as file:
            file.write(f'{self.best_freeplay}\n{self.best_ammo}\n{self.best_timed}')

    def update_best_scores(self, mode, points, time_passed):
        updated = False
        if mode == 0 and (time_passed < self.best_freeplay or self.best_freeplay == 0):
            self.best_freeplay = time_passed
            updated = True
        elif mode == 1 and points > self.best_ammo:
            self.best_ammo = points
            updated = True
        elif mode == 2 and points > self.best_timed:
            self.best_timed = points
            updated = True

        return updated

    def draw_score(self, screen, points, total_shots, time_passed, mode, ammo, time_remaining):
        texts = [
            f'Points: {points}',
            f'Total Shots: {total_shots}',
            f'Time Elapsed: {time_passed}',
            f'Freeplay!' if mode == 0 else
            f'Ammo Remaining: {ammo}' if mode == 1 else
            f'Time Remaining {time_remaining}'
        ]

        for i, text in enumerate(texts):
            rendered = self.font.render(text, True, 'black')
            screen.blit(rendered, (320, 660 + i * 27))