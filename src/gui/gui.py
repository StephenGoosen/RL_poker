import pygame
import pygame_gui

import os
import sys
import re

from game.game_logic import hand_evaluation, compare_scores, GameLogic
from game.player import Player
from game.cards import Deck, change_card_str
import game.table as Tb
import game.config as cg

rank_mapping = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
suit_mapping = {'s': 'spades', 'h': 'hearts', 'd': 'diamonds', 'c': 'clubs'}

class Game:
    def __init__(self):
        pygame.init()
        self.width, self.height = 1280, 720
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        pygame.display.set_caption("Texas Hold'em")

        background_image = pygame.image.load(os.path.join("images", "background.png"))
        self.resized_image = pygame.transform.scale(background_image, (self.width, self.height))
        self.button_color = pygame.Color('#FFFFFF')
        self.button_rect = pygame.Rect((self.width/2.17, self.height/20), (100, 50))

        self.card_images = self.load_card_images()

        self.manager = pygame_gui.UIManager((self.width, self.height))
        self.deal_button = pygame_gui.elements.UIButton(
            relative_rect=self.button_rect,
            text='Deal Cards',
            manager=self.manager
        )

        self.clock = pygame.time.Clock()
        self.is_running = True
        self.hole_cards_dealt = False
        self.flop_dealt = False
        self.river_dealt = False
        self.turn_dealt = False
        self.dealing_cards = False
        self.game = GameLogic()
        print(f"Players: {self.game.players}")

    def load_card_images(self):
        img_suits = ['spades', 'hearts', 'diamonds', 'clubs']
        img_values = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
        card_images = {}
        for value in img_values:
            for suit in img_suits:
                file_path = os.path.join("images", f"{value}_of_{suit.lower()}.png")
                print(f"Loading image: {file_path}")
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
                    if not self.dealing_cards:
                        self.play_round()
                        self.dealing_cards = True 

            self.screen.blit(self.resized_image, (0, 0))

            self.draw_players_container()
            self.draw_community_container()

            if self.game.players_dealt:
                self.draw_players_cards()

            if self.game.flop_dealt:
                self.draw_community_cards()

            if self.game.turn_dealt:
                self.draw_community_cards()

            if self.game.river_dealt:
                self.draw_community_cards()

            pygame.draw.rect(self.screen, self.button_color, self.button_rect)

            self.manager.update(self.clock.tick(10) / 1000.0)
            self.manager.draw_ui(self.screen)

            pygame.display.flip()

            if self.dealing_cards and not self.cards_dealt:
                continue

            self.dealing_cards = False

        pygame.quit()
        sys.exit()

    def draw_players_container(self):
        self.player_container_width = 244
        self.player_container_height = 244
        self.player_x, self.player_y = [40, 338, 698, 996], [250, 450, 450, 250]

        container_image = pygame.image.load(os.path.join("images", "containers.png"))
        self.container_image = pygame.transform.scale(container_image, 
                                                      (self.player_container_width, self.player_container_height))

        for i in range(len(self.game.players)):
            player_container_rect = pygame.Rect(self.player_x[i], self.player_y[i], self.player_container_width, self.player_container_height)

            # Draw player's name
            font = pygame.font.Font(None, 30)
            text = font.render(self.game.players[i].name, True, (255, 255, 255))
            text_rect = text.get_rect(center=(self.player_x[i]+self.player_container_width // 2, self.player_y[i] + 34))
            self.screen.blit(self.container_image, (self.player_x[i], self.player_y[i]))
            self.screen.blit(text, text_rect)

    def draw_players_cards(self):
        self.card_offset = 25
        self.card_width = 128*.7
        self.card_height = 178*.7

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

                x = self.player_x[i] + (j * self.card_offset) + 122 - (self.card_width / 2)
                y = self.player_y[i] + 50
                self.screen.blit(card_image, (x - (self.card_offset / 2), y))

            font = pygame.font.Font(None, 22)
            score_text = f"{float(player.hand_strength):.3f}"
            hand_text = f"{player.hand_description}"
            chip_text = f"{player.chipcount}"
            score_surface = font.render(score_text, True, (255, 255, 255))
            hand_surface = font.render(hand_text, True, (255, 255, 255))
            chip_surface = font.render(chip_text, True, (255, 255, 255))
            chip_title = font.render("Total Chips", True, (255, 255, 255))
            score_rect = score_surface.get_rect(center=(self.player_x[i] + (self.player_container_width // 2) - 50, self.player_y[i] + self.player_container_height - 30))
            hand_rect = hand_surface.get_rect(center=(self.player_x[i] + (self.player_container_width // 2) - 50, self.player_y[i] + self.player_container_height - 50))
            chip_rect = chip_surface.get_rect(center=(self.player_x[i] + (self.player_container_width // 2) + 50, self.player_y[i] + self.player_container_height - 30))
            chip_title_rect = chip_title.get_rect(center=(self.player_x[i] + (self.player_container_width // 2) + 50, self.player_y[i] + self.player_container_height - 50))
            self.screen.blit(score_surface, score_rect)
            self.screen.blit(hand_surface, hand_rect)
            self.screen.blit(chip_surface, chip_rect)
            self.screen.blit(chip_title, chip_title_rect)

    def draw_community_container(self):
        self.community_container_width = 640
        self.community_container_height = 150
        self.community_container_x = self.width // 2 - self.community_container_width // 2
        self.community_container_y = self.height // 4 - self.community_container_height // 2
        community_container_rect = pygame.Rect(self.community_container_x, self.community_container_y, self.community_container_width, self.community_container_height)
        pygame.draw.rect(self.screen, (0, 255, 0), community_container_rect, 2)

    def draw_community_cards(self):

        if not self.cards_dealt:
            return
        
        flop_x = self.community_container_x + (self.community_container_width // 50)
        for card in self.flop_cards:
            self.draw_card(card, flop_x, self.community_container_y + 10, self.community_container_width, self.community_container_height)
            flop_x += (self.community_container_width // 5)

        turn_x = flop_x
        if self.turn_card is not None:
            self.draw_card(self.game.community_cards.turncard, turn_x, self.community_container_y + 10, self.community_container_width, self.community_container_height)

        river_x = turn_x + (self.community_container_width // 5)
        if self.river_card is not None:
            self.draw_card(self.game.community_cards.rivercard, river_x, self.community_container_y + 10, self.community_container_width, self.community_container_height)

    def draw_card(self, card, x, y, width, height):
        rank, suit = change_card_str(card)

        file_name = f"{rank}_of_{suit}.png"
        key = os.path.join("images", file_name)

        try:
            card_image = pygame.image.load(key)
            card_image = pygame.transform.scale(card_image, (int(width / 6), int(height / 1.2)))
        except pygame.error:
            print(f"Error: Image file not found for {key}")
            return

        self.screen.blit(card_image, (x, y))
        self.cards_drawn = True

    def play_round(self):
        self.game.initialize_gamestate()

        self.game.deck.shuffle()

        self.game.deal_hole_cards()
        for i in range(len(self.game.players)):
            print(self.game.players[i].hand)
            print(self.game.players[i].chipcount)
        self.game.players_dealt = True
        self.draw_players_cards()

        self.game.pre_flop()

        self.game.deck.deal_card()  # burn card
        self.game.community_cards.insert_flop([self.game.deck.deal_card() for _ in range(3)])
        self.flop_cards = self.game.community_cards.reveal_flop()
        self.game.flop_dealt = True


        self.game.deck.deal_card()  # burn card
        self.game.community_cards.insert_turn(self.game.deck.deal_card())
        self.turn_card = self.game.community_cards.reveal_turn()
        self.game.turn_dealt = True

        self.game.deck.deal_card()  # burn card
        self.game.community_cards.insert_river(self.game.deck.deal_card())
        self.river_card = self.game.community_cards.reveal_river()
        self.game.river_dealt = True

        self.cards_dealt = True

        community_cards = self.flop_cards + [self.turn_card] + [self.river_card]

        for player in self.game.players:
            hole_cards = player.hand

            x = hand_evaluation(player, hole_cards, community_cards)
            print(x)
    
                    