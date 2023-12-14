import pygame
import pygame_gui

import os
import sys

from game.game_logic import evaluate_hand
import game.cards as Cards
from game.player import Player
from game.table import Table

class TexasHoldemGUI:
    def __init__(self):
        pygame.init()
        self.width, self.height = 800, 600
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        pygame.display.set_caption("Texas Hold'em")

        self.background_color = pygame.Color('#000000')
        self.button_color = pygame.Color('#FFFFFF')
        self.button_rect = pygame.Rect((350, 275), (100, 50))

        self.card_images = self.load_card_images()

        self.manager = pygame_gui.UIManager((self.width, self.height))
        self.deal_button = pygame_gui.elements.UIButton(
            relative_rect=self.button_rect,
            text='Deal Cards',
            manager=self.manager
        )

        self.clock = pygame.time.Clock()
        self.is_running = True

        # Initialize Texas Hold'em game objects
        self.table = Table()
        self.deck = Cards.Deck()
        self.players = [Player(f"Player {i+1}") for i in range(2)]

    def load_card_images(self):
        card_images = {}
        for value in Cards.card_values:
            for suit in Cards.card_suits:
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
                    self.play_round()


            self.screen.fill(self.background_color)

            self.draw_players()
            self.draw_community_cards()

            pygame.draw.rect(self.screen, self.button_color, self.button_rect)

            self.manager.update(self.clock.tick(30) / 1000.0)
            self.manager.draw_ui(self.screen)

            pygame.display.flip()

        pygame.quit()
        sys.exit()

    def draw_players(self):
        player_container_width = 150
        player_container_height = 100
        player_x, player_y = 50, 450  
        card_offset = 20 

        for player in self.players:
            player_container_rect = pygame.Rect(player_x, player_y, player_container_width, player_container_height)
            pygame.draw.rect(self.screen, (255, 255, 255), player_container_rect, 2)

            for i, card in enumerate(player.hand):
                if isinstance(card.value, int):
                    key = os.path.join("images", f"{card.value}_of_{card.suit.lower()}.png")
                else:
                    key = os.path.join("images", f"{card.value.lower()[0]}_of_{card.suit.lower()}.png")
                try:
                    card_image = pygame.image.load(key)
                    card_image = pygame.transform.scale(card_image, (int(player_container_width / 5), int(player_container_height / 2)))
                except pygame.error:
                    print(f"Error: Image file not found for {key}")
                    continue

                x = player_x + i * card_offset
                y = player_y + 20
                self.screen.blit(card_image, (x, y))

            player_x += player_container_width + 20


    def draw_community_cards(self):

        community_container_width = 150
        community_container_height = 100

        flop_x = 50

        for i, card in enumerate(self.table.flop):
            key = os.path.join("images", f"{card.value}_of_{card.suit.lower()}.png")
            try:
                card_image = pygame.image.load(key)
                card_image = pygame.transform.scale(card_image, (int(community_container_width / 5), int(community_container_height / 2)))
            except pygame.error:
                print(f"Error: Image file not found for {key}")
                continue

            x = flop_x + i * 150
            y = 400
            self.screen.blit(card_image, (x, y))

        flop_x += len(self.table.flop) * 150

        turn_card = self.table.turncard
        if turn_card is not None:
            try:
                if isinstance(turn_card.value, int):
                    turn_value_str = str(turn_card.value)
                else:
                    turn_value_str = turn_card.value.lower()[0]

                turn_card_key = os.path.join("images", f"{turn_value_str}_of_{turn_card.suit.lower()}.png")
                print(f"Attempting to load image for turn card: {turn_card_key}")

                turn_card_image = self.card_images.get(turn_card_key) 
                if turn_card_image is None:
                    raise KeyError(f"Image file not found for {turn_card_key}")

                turn_card_image = pygame.transform.scale(turn_card_image, (int(community_container_width / 5), int(community_container_height / 2)))
            except KeyError as e:
                print(f"Error: {e}")
            else:
                x = flop_x + 50
                y = 400
                self.screen.blit(turn_card_image, (x, y))

        river_card = self.table.rivercard
        if river_card is not None:
            try:
                if isinstance(river_card.value, int):
                    river_card_str = str(river_card.value)
                else:
                    river_card_str = river_card.value.lower()[0]

                river_card_key = os.path.join("images", f"{river_card_str}_of_{river_card.suit.lower()}.png")
                print(f"Attempting to load image for river card: {river_card_key}")

                river_card_image = self.card_images.get(river_card_key)
                if river_card_image is None:
                    raise KeyError(f"Image file not found for {river_card_key}")

                river_card_image = pygame.transform.scale(river_card_image, (int(community_container_width / 5), int(community_container_height / 2)))
            except KeyError as e:
                print(f"Error: {e}")
            else:
                x = flop_x + 50
                y = 400
                self.screen.blit(river_card_image, (x, y))

    def play_round(self):
        # Reset the game state for a new round
        self.table = Table()
        self.deck = Cards.Deck()
        self.deck.shuffle()

        # Deal cards to players
        for player in self.players:
            player.hand = [self.deck.deal_card(), self.deck.deal_card()]

        # Reveal the flop
        flop_cards = [self.deck.deal_card() for _ in range(3)]
        self.table.reveal_flop(flop_cards)

        # Continue the game logic, and then reveal the turn card
        turn_card = self.deck.deal_card()
        self.table.reveal_turn(turn_card)

        # Continue the game logic, and then reveal the river card
        river_card = self.deck.deal_card()
        self.table.reveal_river(river_card)

        self.card_images = self.load_card_images()

        # Evaluate and print each player's hand
        for player in self.players:
            hole_cards = player.hand
            community_cards = self.table.flop + [self.table.turncard] + [self.table.rivercard]
            hand_strength, best_combination = evaluate_hand(hole_cards, community_cards)

            # Convert values and suits to strings for better display
            best_combination_str = [str(card) for card in best_combination]

            print(f"{player.name}'s hand strength: {hand_strength[0]}")
            print(f"{player.name}'s best combination: {', '.join(best_combination_str)}")
            print()