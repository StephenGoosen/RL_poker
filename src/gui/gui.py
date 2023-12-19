import pygame
import pygame_gui

import os
import sys
import re

from game.game_logic import hand_evaluation, compare_scores, Hand
from pokereval.card import Card
from game.player import Player
from game.cards import Deck, change_card_str
import game.table as Tb

rank_mapping = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
suit_mapping = {'s': 'spades', 'h': 'hearts', 'd': 'diamonds', 'c': 'clubs'}


class Game:
    def __init__(self):
        pygame.init()
        self.width, self.height = 1280, 720
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        pygame.display.set_caption("Texas Hold'em")

        self.background_color = pygame.Color('#000000')
        self.button_color = pygame.Color('#FFFFFF')
        self.button_rect = pygame.Rect((600, 20), (100, 50))

        self.card_images = self.load_card_images()

        self.manager = pygame_gui.UIManager((self.width, self.height))
        self.deal_button = pygame_gui.elements.UIButton(
            relative_rect=self.button_rect,
            text='Deal Cards',
            manager=self.manager
        )

        self.clock = pygame.time.Clock()
        self.is_running = True
        self.cards_dealt = False
        self.dealing_cards = False
        self.flop_cards = []
        self.turn_card = None
        self.river_card = None

        self.deck = Deck()
        self.community_cards = Tb.Community_Cards()
        self.players = [Player(f"Player {i+1}") for i in range(2)]


    def reset_deck(self):
        self.deck = Deck()

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
                    print("Image loaded successfully")
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

            self.screen.fill(self.background_color)

            self.draw_players()
            self.community_container()

            if self.cards_dealt:
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

    def draw_players(self):
        player_container_width = 180
        player_container_height = 300
        player_x, player_y = 20, 200  
        card_offset = 20 

        for player in self.players:
            player_container_rect = pygame.Rect(player_x, player_y, player_container_width, player_container_height)
            pygame.draw.rect(self.screen, (255, 255, 255), player_container_rect, 2)

            # Draw player's cards
            for i, card in enumerate(player.hand):
                rank, suit = change_card_str(player.hand[i])

                file_name = f"{rank}_of_{suit}.png"
                key = os.path.join("images", file_name)

                try:
                    card_image = pygame.image.load(key)
                    card_image = pygame.transform.scale(card_image, (int(player_container_width / 1.5), int(player_container_height / 2)))
                except pygame.error:
                    print(f"Error: Image file not found for {key}")
                    continue

                x = player_x + i * card_offset
                y = player_y + 20
                self.screen.blit(card_image, (x, y))

            # Draw player's name
            font = pygame.font.Font(None, 30)  # You can change the font and size
            text = font.render(player.name, True, (255, 255, 255))
            text_rect = text.get_rect(center=(player_x + player_container_width // 2, player_y + player_container_height + 20))
            self.screen.blit(text, text_rect)

            # Draw hand and hand strength
            font = pygame.font.Font(None, 18)
            score_text = f"Hand Strength: {float(player.hand_strength):.3f}"
            hand_text = f"Hand: {player.hand_description}"
            score_surface = font.render(score_text, True, (255, 255, 255))
            hand_surface = font.render(hand_text, True, (255, 255, 255))
            score_rect = score_surface.get_rect(center=(player_x + player_container_width // 2, player_y + player_container_height + 60))
            hand_rect = hand_surface.get_rect(center=(player_x + player_container_width // 2, player_y + player_container_height + 90))
            self.screen.blit(score_surface, score_rect)
            self.screen.blit(hand_surface, hand_rect)

            player_x += player_container_width + 20

    def community_container(self):
        self.community_container_width = 700
        self.community_container_height = 300
        self.community_container_x = 550
        self.community_container_y = 200
        community_container_rect = pygame.Rect(self.community_container_x, self.community_container_y, self.community_container_width, self.community_container_height)
        pygame.draw.rect(self.screen, (255, 255, 255), community_container_rect, 2)

    def draw_community_cards(self):

        if not self.cards_dealt:
            return
        
        flop_x = self.community_container_x  
        for card in self.community_cards.flop:
            self.draw_card(card, flop_x, self.community_container_y + 20, self.community_container_width, self.community_container_height)
            flop_x += 150 

        turn_x = flop_x
        if self.community_cards.turncard is not None:
            self.draw_card(self.community_cards.turncard, turn_x, self.community_container_y + 20, self.community_container_width, self.community_container_height)

        river_x = turn_x + 150
        if self.community_cards.rivercard is not None:
            self.draw_card(self.community_cards.rivercard, river_x, self.community_container_y + 20, self.community_container_width, self.community_container_height)

    def draw_card(self, card, x, y, width, height):
        rank, suit = change_card_str(card)

        file_name = f"{rank}_of_{suit}.png"
        key = os.path.join("images", file_name)

        try:
            card_image = pygame.image.load(key)
            card_image = pygame.transform.scale(card_image, (int(width / 8), int(height / 2)))
        except pygame.error:
            print(f"Error: Image file not found for {key}")
            return

        self.screen.blit(card_image, (x, y))
        self.cards_drawn = True

    def reset_community_cards(self):
        self.community_cards = Tb.Community_Cards()

    def play_round(self):
        self.deck.shuffle()
        self.reset_community_cards()

        for player in self.players:
            player.hand = [self.deck.deal_card(), self.deck.deal_card()]

        self.deck.deal_card()  # burn card
        self.flop_cards = [self.deck.deal_card() for _ in range(3)]
        self.community_cards.reveal_flop(self.flop_cards)

        self.deck.deal_card()  # burn card
        self.turn_card = self.deck.deal_card()
        self.community_cards.reveal_turn(self.turn_card)

        self.deck.deal_card()  # burn card
        self.river_card = self.deck.deal_card()
        self.community_cards.reveal_river(self.river_card)

        community_cards = self.flop_cards + [self.turn_card] + [self.river_card]

        for card in community_cards:
            rank, suit = change_card_str(card)
            print(f"{rank} of {suit}")

        for player in self.players:
            hole_cards = player.hand  # Use player.hand directly

            # Use the hand_evaluation function to evaluate hands
            hand_evaluation(player, hole_cards, community_cards)


        self.cards_dealt = True
        self.reset_deck()
        self.cards_drawn = False

        return None