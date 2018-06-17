from kivy.app import App
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from kivy.uix.behaviors import ButtonBehavior
from kivy.animation import Animation
from kivy.properties import NumericProperty, ObjectProperty, ListProperty
from kivy.core.image import Image
from kivy.graphics.vertex_instructions import Rectangle
from random import shuffle, choice
import os


h, l = 4, 7
card_width, card_height = 70, 150
separation = 10
x_init, y_init = 50, 50
delay = 5
font_size = 30


class Card(Button):

    def __init__(self, value, **kwargs):
        super(Card, self).__init__(**kwargs)
        self.back = Image('img/interrogation_mark.jpeg')
        print value
        self.front = Image(value)
        self.value = value
        self.rect = Rectangle(pos=(self.x, self.y), texture=self.back.texture, size=(self.width, self.height))
        self.final_size = (0, self.height)
        self.init_size = (self.width, self.height)
        self.final_position = (self.x + self.width/2, self.y)
        self.init_position = (self.x, self.y)
        self.canvas.add(self.rect)
        self.turned_back = True
        self.background_color = [0, 0, 0, 0]

    def change_pict(self, *args):
        if self.turned_back:
            self.rect.texture = self.back.texture
        else:
            self.rect.texture = self.front.texture
        
    def on_click(self, call_back_function, *args):
        print self.value
        print self.turned_back
        anim1 = Animation(size=self.final_size,
                          pos=self.final_position)
        anim1.bind(on_complete = self.change_pict)
        anim2 = Animation(size=self.init_size, pos= self.init_position)
        if call_back_function is not None:
            anim2.bind(on_complete=call_back_function)
        self.animation = anim1 + anim2
        self.animation.start(self.rect)
        self.turned_back = (not self.turned_back)


class MemoryLayout(GridLayout):

    def __init__(self, **kwargs):
        images = ['img/%s' % img for img in os.listdir('img') if img.lower().endswith(('jpg', 'jpeg')) and 'interrogation' not in img]
        
        super(MemoryLayout, self).__init__(**kwargs)
        # values = 2 * range((h * l) / 2)
        values = 2 * images
        # shuffle(values)
        self.clicks = 0
        self.clicked = []
        self.can_play = True
        self.player = 0
        self.cards = []
        self.scores = [0, 0]
        
        # adding the cards on the layout
        for i in range(h):
            for j in range(l):
                tmp_value = values.pop()
                tmp_card = Card(tmp_value, 
                                x=x_init + (card_width + separation) * i,
                                y=y_init + (card_height + separation) * j,
                                width=card_width,
                                height=card_height,
                                font_size=font_size,
                                on_press=lambda x: self.click(x))
                self.cards.append(tmp_card)
                self.add_widget(tmp_card)

        # adding the scores on the layout
        self.add_widget(Label(x=800, y=1200, text="score", width=100, height=100, font_size=40))
        self.add_widget(Label(x=800, y=1150, text="player 1", width=100, height=100, font_size=40))
        self.add_widget(Label(x=800, y=1100, text="player 2", width=100, height=100, font_size=40))

        self.player1_score_label = Label(x=950, y=1150, text=str(self.scores[0]), width=100, height=100, font_size=40)
        self.player2_score_label = Label(x=950, y=1100, text=str(self.scores[1]), width=100, height=100, font_size=40)
        
        self.add_widget(self.player1_score_label)
        self.add_widget(self.player2_score_label)
        self.scores_label = [self.player1_score_label, self.player2_score_label]
        
    def turn_back(self, *args):
        for card in self.clicked:
            card.on_click(None)
        self.clicked = []
        self.can_play = True

        if self.player == 1:
            Clock.schedule_once(self.AI_play, delay)

    def remove_cards(self, *args):
        print "inside remove_cards"
        print self.clicked
        for card in self.clicked:
            print "removing", card.value
            self.remove_widget(card)
        self.clicked = []
        self.cards = filter(lambda x: x.value != self.current_value, self.cards)
        if len(self.cards) == 0:
            # no card left, so the game is over
            for label in self.scores_label:
                self.remove_widget(label)
            self = self.__init__()
        return
    
    def click(self, card):
        print self.player
        if not self.can_play:
            return

        self.clicks += 1
        self.clicked.append(card)
        if self.clicks % 2 == 0:
            if self.clicked[0].value == self.clicked[1].value:
                self.current_value = self.clicked[0].value
                print "same cards!"
                print self.clicked
                self.scores[self.player] += 1
                self.scores_label[self.player].text = str(self.scores[self.player])

                card.on_click(self.remove_cards)
                if self.player == 1:
                    Clock.schedule_once(self.AI_play, delay)
                return
            else:
                self.player = 1 - self.player                
                card.on_click(None)
            self.can_play = False
            Clock.schedule_once(self.turn_back, delay)
            
        else:
            card.on_click(None)

    def AI_choice(self):
        # need to pick randomly two cards in self.cards
        # a = choice(range(len(self.cards) - 1))
        # b = choice(range(a + 1, len(self.cards)))
        a, b = 1, 15
        choice1 = self.cards[a]
        choice2 = self.cards[b]
        print a, b
        return choice1, choice2

    def AI_play(self, *args):
        print "AI is playing now"
        print args
        c1, c2 = self.AI_choice()
        self.click(c1)
        def click_next(*args):
            self.click(c2)
        Clock.schedule_once(click_next, delay)

class MemoryApp(App):
    def build(self):
        return MemoryLayout()

def main():
    MemoryApp().run()


if __name__ == "__main__":
    main()
