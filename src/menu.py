import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK


class Menu:
    def __init__(self, screen, menu_music):
        self.screen = screen
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)
        
        pygame.mixer.music.load(menu_music)
        pygame.mixer.music.play(-1)
        
        self.button_width = 300
        self.button_height = 60
        self.button_spacing = 20
        
        button_x = (SCREEN_WIDTH - self.button_width) // 2
        start_y = SCREEN_HEIGHT // 2 - 80
        
        self.buttons = {
            "start": pygame.Rect(button_x, start_y, self.button_width, self.button_height),
            "shop": pygame.Rect(button_x, start_y + self.button_height + self.button_spacing, self.button_width, self.button_height),
            "quests": pygame.Rect(button_x, start_y + (self.button_height + self.button_spacing) * 2, self.button_width, self.button_height),
        }
        
    def draw(self):
        self.screen.fill(WHITE)
        
        title = self.font_large.render("Cat Runner", True, BLACK)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
        self.screen.blit(title, title_rect)
        
        for button_name, button_rect in self.buttons.items():
            pygame.draw.rect(self.screen, BLACK, button_rect, 2)
            
            if button_name == "start":
                text = "Начать игру"
            elif button_name == "shop":
                text = "Магазин"
            elif button_name == "quests":
                text = "Задания"
            
            text_surface = self.font_medium.render(text, True, BLACK)
            text_rect = text_surface.get_rect(center=button_rect.center)
            self.screen.blit(text_surface, text_rect)
        
        pygame.display.flip()
    
    def handle_click(self, pos):
        for button_name, button_rect in self.buttons.items():
            if button_rect.collidepoint(pos):
                return button_name
        return None
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                return self.handle_click(event.pos)
        return None

