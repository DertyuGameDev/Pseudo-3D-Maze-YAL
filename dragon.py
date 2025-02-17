import pygame

from load_image import load_image


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y, all_sprites):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption('Пример 1')
    size = width, height = 500, 500
    screen = pygame.display.set_mode(size)

    running = True
    screen.fill("white")

    all_sprites = pygame.sprite.Group()
    dragon = AnimatedSprite(load_image("dragon_sheet8x2.png"), 8, 2, 50, 50)
    clock = pygame.time.Clock()
    screen.fill("black")
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        all_sprites.update()

        screen.fill("black")
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(15)

    pygame.quit()
