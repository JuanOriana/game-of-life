import pygame

SELECTED_COLOR = (255,255,200)
class Button:
    def __init__(self, i, j, width, height, color, label):
        self.rect = pygame.Rect(i, j, width, height)
        self.originalColor = color
        self.color = color
        self.label = label
        self.pressed = False

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        if self.pressed:
            pygame.draw.rect(screen, SELECTED_COLOR, self.rect,width=2)
        # Text centering
        screen.blit(self.label, (self.rect.x + self.rect.width // 2 - self.label.get_width() // 2,
                                 self.rect.y + self.rect.height // 2 - self.label.get_height() // 2))

    def collides(self, coor):
        return self.rect.collidepoint(coor)

    def toggle(self):
        self.pressed = True
        self.color = (self.color[0]//2,self.color[1]//2,self.color[2]//2)

    def untoggle(self):
        self.pressed = False
        self.color = self.originalColor