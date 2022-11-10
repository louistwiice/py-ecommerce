from django.utils.translation import gettext_lazy as _


class Colors:
    BLACK, WHITE, RED, GREEN, YELLOW, BLUE, PINK, GRAY, BROWN, ORANGE, PURPLE = "black", "white", "red", "green", \
                                                                                "yellow", "blue", "pink", "gray", \
                                                                                "brown", "orange", "purple"

    CHOICES = (
        (BLACK, _("Black")),
        (WHITE, _("White")),
        (RED, _("Red")),
        (GREEN, _("Green")),
        (YELLOW, _("Yellow")),
        (BLUE, _("Blue")),
        (PINK, _("Pink")),
        (GRAY, _("Gray")),
        (BROWN, _("Brown")),
        (ORANGE, _("Orange")),
        (PURPLE, _("Purple")),
    )



