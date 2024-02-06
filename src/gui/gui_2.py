# gui.py

import pygame
import pygame_gui

import os
import sys

from game.game_logic import hand_evaluation, GameLogic
from game.cards import change_card_str


rank_mapping = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
suit_mapping = {'s': 'spades', 'h': 'hearts', 'd': 'diamonds', 'c': 'clubs'}

class Game:
    def __init__(self):
        pygame.init()
        self.width, self.height = 1280, 720
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Texas Hold'em")

        background_image = pygame.image.load(os.path.join("images", "background_2.png"))
        self.resized_image = pygame.transform.scale(background_image, (self.width, self.height))
        self.button_color = pygame.Color('#FFFFFF')
        self.button_rect = pygame.Rect((self.width/2 - 75, self.height/2 + 50), (150, 50))

        self.grid_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.draw_grid(self.grid_surface, cell_size=50, line_color=(255, 255, 255, 50))

    def draw_grid(self, surface, cell_size, line_color):
        for x in range(0, self.width, cell_size):
            pygame.draw.line(surface, line_color, (x, 0), (x, self.height), 1)

        for y in range(0, self.height, cell_size):
            pygame.draw.line(surface, line_color, (0, y), (self.width, y), 1)


        self.card_images = self.load_card_images()

        self.manager = pygame_gui.UIManager((self.width, self.height))
        self.deal_button = pygame_gui.elements.UIButton(
            relative_rect=self.button_rect,
            text='Deal Cards',
            manager=self.manager
        )

        self.round_states = ['Start Round', 'Deal Flop', 'Deal Turn', 'Deal River', 'End Round']
        self.current_round_state = 0    
        
        self.clock = pygame.time.Clock()
        self.is_running = True
        self.game = GameLogic()


    def load_card_images(self):
        img_suits = ['spades', 'hearts', 'diamonds', 'clubs']
        img_values = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
        card_images = {}
        for value in img_values:
            for suit in img_suits:
                file_path = os.path.join("images", f"{value}_of_{suit.lower()}.png")
                try:
                    card_images[file_path] = pygame.image.load(file_path)
                except pygame.error as e:
                    print(f"Error loading image: {e}")
                else:
                    pass
        return card_images


    def run(self):
        while self.is_running:
            pygame.event.pump()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.deal_button.rect.collidepoint(event.pos):
                    self.play_round()

            self.screen.blit(self.resized_image, (0, 0))
            #self.screen.blit(self.grid_surface, (0, 0))

            self.draw_players_container()
            self.draw_community_container()

            if self.game.players_dealt:
                self.draw_players_cards()

            if self.game.flop_dealt:
                self.draw_flop_cards()

            if self.game.turn_dealt:
                self.draw_turn_cards()

            if self.game.river_dealt:
                self.draw_river_cards()

            pygame.draw.rect(self.screen, self.button_color, self.button_rect)

            self.deal_button.set_text(self.round_states[self.current_round_state])

            self.manager.update(self.clock.tick(144) / 1000.0)
            self.manager.draw_ui(self.screen)

            pygame.display.flip()

        pygame.quit()
        sys.exit()

    def draw_players_container(self):
        self.player_container_width = 250
        self.player_container_height = 350
        self.player_x, self.player_y = [50, 985], [250, 250]

        for i in range(len(self.game.players)):

            # Draw player's name and chipcount
            font1 = pygame.font.Font(None, 32)
            font2 = pygame.font.Font(None, 25)

            name_text = font1.render(self.game.players[i].name, True, (255, 255, 255))

            chip_text = font2.render(f"{self.game.players[i].chipcount}", True, (255, 255, 255))
            chip_title_text = font2.render("Total Chips", True, (255, 255, 255))

            name_rect = name_text.get_rect(center=(self.player_x[i]+self.player_container_width // 2, self.player_y[i] + 24))

            if self.game.players[i] == self.game.players[0]:
                chip_rect = chip_text.get_rect(center=(self.player_x[i] + (self.player_container_width // 2) - 62, self.player_y[i] + self.player_container_height - 30))
                chip_title_rect = chip_title_text.get_rect(center=(self.player_x[i] + (self.player_container_width // 2) - 62, self.player_y[i] + self.player_container_height - 60))

            else:
                chip_rect = chip_text.get_rect(center=(self.player_x[i] + (self.player_container_width // 2) + 62, self.player_y[i] + self.player_container_height - 30))
                chip_title_rect = chip_title_text.get_rect(center=(self.player_x[i] + (self.player_container_width // 2) + 62, self.player_y[i] + self.player_container_height - 60))

            # Draw player's container
            self.screen.blit(name_text, name_rect)
            self.screen.blit(chip_text, chip_rect)
            self.screen.blit(chip_title_text, chip_title_rect)

    def draw_players_cards(self):
        self.card_offset = 25
        self.card_width = 128
        self.card_height = 178

        for i, player in enumerate(self.game.players):
            for j, card in enumerate(player.hand):
                rank, suit = change_card_str(player.hand[j])

                file_name = f"{rank}_of_{suit}.png"
                key = os.path.join("images", file_name)

                try:
                    card_image = pygame.image.load(key)
                    card_image = pygame.transform.scale(card_image, (self.card_width, self.card_height))
                except pygame.error:
                    print(f"Error: Image file not found for {key}")
                    continue
                
                if self.game.players[i] == self.game.players[0]:
                    x = self.player_x[i] + (j * self.card_offset) + 122 - (self.card_width / 2) + 26
                    y = self.player_y[i] + 63
                    self.screen.blit(card_image, (x - (self.card_offset / 2), y))
                else:
                    x = self.player_x[i] + (j * self.card_offset) + 122 - (self.card_width / 2) - 21
                    y = self.player_y[i] + 63
                    self.screen.blit(card_image, (x - (self.card_offset / 2), y))

            font = pygame.font.Font(None, 25)
      
            score_surface = font.render(f"{float(player.hand_strength):.3f}", True, (255, 255, 255))
            hand_surface = font.render(f"{player.hand_description}", True, (255, 255, 255))

            if self.game.players[i] == self.game.players[0]:
                hand_rect= hand_surface.get_rect(center=(self.player_x[i] + (self.player_container_width // 2) + 62, self.player_y[i] + self.player_container_height - 30))
                score_rect = score_surface.get_rect(center=(self.player_x[i] + (self.player_container_width // 2) + 62, self.player_y[i] + self.player_container_height - 60))
            
            else:
                hand_rect= hand_surface.get_rect(center=(self.player_x[i] + (self.player_container_width // 2) - 62, self.player_y[i] + self.player_container_height - 30))
                score_rect = score_surface.get_rect(center=(self.player_x[i] + (self.player_container_width // 2) - 62, self.player_y[i] + self.player_container_height - 60))
                
            self.screen.blit(score_surface, score_rect)
            self.screen.blit(hand_surface, hand_rect)

    def draw_community_container(self):

        self.community_container_width = 580
        self.community_container_height = 200
        self.community_container_x = 350
        self.community_container_y = 150

        self.flop_x = self.community_container_x + 24

        #community_container_rect = pygame.Rect(self.community_container_x, self.community_container_y, self.community_container_width, self.community_container_height)
        #pygame.draw.rect(self.screen, (0, 255, 0), community_container_rect, 2)

        font = pygame.font.Font(None, 40)
        pot = f"Pot: {int(self.game.pot)}"
        pot_surface = font.render(pot, True, (255, 255, 255))
        pot_rect = pot_surface.get_rect(center=(self.community_container_x + self.community_container_width // 2, self.community_container_y + self.community_container_height + 218))
        self.screen.blit(pot_surface, pot_rect)

    def draw_flop_cards(self):
        for card in self.flop_cards:
            self.draw_card(card, self.flop_x, self.community_container_y + 27, self.community_container_width, self.community_container_height)
            self.flop_x += 108

    def draw_turn_cards(self):
        self.turn_x = self.flop_x
        self.draw_card(self.game.community_cards.turncard, self.turn_x, self.community_container_y + 27, self.community_container_width, self.community_container_height)

    def draw_river_cards(self):
        self.river_x = self.turn_x + 108
        self.draw_card(self.game.community_cards.rivercard, self.river_x, self.community_container_y + 27, self.community_container_width, self.community_container_height)

    def draw_card(self, card, x, y, width, height):
        rank, suit = change_card_str(card)

        file_name = f"{rank}_of_{suit}.png"
        key = os.path.join("images", file_name)

        try:
            card_image = pygame.image.load(key)
            card_image = pygame.transform.scale(card_image, (100, 142))
        except pygame.error:
            print(f"Error: Image file not found for {key}")
            return

        self.screen.blit(card_image, (x, y))
        self.cards_drawn = True

    def play_round(self):
        if self.current_round_state == 0:
            # Start Round logic
            self.game.deal_hole_cards()

            for player in self.game.players:
                if player.game_in_play:
                    hand_evaluation(player, player.hand, [])

            self.draw_players_cards()
            pygame.display.flip()

            self.game.pre_flop()

            self.current_round_state += 1
            self.deal_button.set_text('Deal Flop')

        elif self.current_round_state == 1:
            # Deal Flop logic
            self.game.flop_dealt, self.flop_cards = self.game.flop()

            for player in self.game.players:
                if player.game_in_play:
                    hand_evaluation(player, player.hand, self.flop_cards)

            self.draw_flop_cards()
            self.manager.draw_ui(self.screen)
            pygame.display.flip()
            self.game.pre_turn()

            self.current_round_state += 1
            self.deal_button.set_text('Deal Turn')

        elif self.current_round_state == 2:
            # Deal Turn logic
            self.game.turn_dealt, self.turn_card = self.game.turn()

            for player in self.game.players:
                if player.game_in_play:
                    hand_evaluation(player, player.hand, self.flop_cards + [self.turn_card])

            self.draw_turn_cards()
            pygame.display.flip()
            self.game.pre_river()

            self.current_round_state += 1
            self.deal_button.set_text('Deal River')

        elif self.current_round_state == 3:
            # Deal River logic
            self.game.river_dealt, self.river_card = self.game.river()

            for player in self.game.players:
                if player.game_in_play:
                    hand_evaluation(player, player.hand, self.flop_cards + [self.turn_card] + [self.river_card])

            self.draw_river_cards()
            pygame.display.flip()
            self.game.showdown()

            self.current_round_state += 1
            self.deal_button.set_text('End Round')

        elif self.current_round_state == 4:
            # End Round logic

            self.game.end_round()
            self.game.new_round()

            self.current_round_state = 0
            self.deal_button.set_text('Start Round')

        

    
                    