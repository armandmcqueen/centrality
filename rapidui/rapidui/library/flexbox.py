import streamlit as st
from abc import ABC, abstractmethod


class CardContents:
    pass


class BaseCard(ABC):
    @abstractmethod
    def __init__(self, parent_container, contents: CardContents):
        """ This should create the card and set (render) its initial contents """
        pass

    @abstractmethod
    def empty(self):
        pass

    @abstractmethod
    def update(self, contents: CardContents):
        pass


class UniformFlexbox:
    """A flexbox-like layout for displaying Cards that can be updated in real-time (i.e. without rerunning)"""

    def __init__(self, num_cols: int, card_type: type[BaseCard], border: bool = True):
        self.num_cols = num_cols
        self.cols = st.columns(self.num_cols)
        self.cards = []
        self.card_type = card_type
        self.border = border

    def set_initial_cards(self, contents: list[CardContents]) -> None:
        assert (
            len(self.cards) == 0
        ), "Can't set cards if there are already cards. Use update_cards instead."
        for ind, content in enumerate(contents):
            card_container = self.cols[ind % self.num_cols].container(
                border=self.border
            )
            card = self.card_type(card_container, content)
            self.cards.append(card)

    def update_cards(self, contents: list[CardContents]) -> None:
        """
        Given a new set of measurements, update the cards to represent them. This will completely
        rewrite the cards and add any new ones.

        Note that if the number of cards decreases, there will be ghosts because we can't actually
        truly delete a card - the border still shows up.
        """
        rewrites = contents[: len(self.cards)]
        additions = contents[len(self.cards) :]
        for ind, content in enumerate(rewrites):
            self.cards[ind].update(content)

        if len(rewrites) < len(self.cards):
            # Any cards with an index >= len(rewrites) need to be emptied
            for card in self.cards[len(rewrites) :]:
                card.empty()

        for ind, content in enumerate(additions):
            real_ind = ind + len(rewrites)
            card_container = self.cols[real_ind % self.num_cols].container(
                border=self.border
            )
            card = self.card_type(card_container, content)
            self.cards.append(card)


