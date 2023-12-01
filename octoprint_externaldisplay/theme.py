from collections import namedtuple

Theme = namedtuple("Theme", ["backgrounds", "foreground", "accent", "danger", "hot", "cold"])

default_theme = Theme(
    backgrounds=["#2E2E3A", "#48485B"],
    foreground="#8C93A8",
    accent="#F4E9CD",
    danger="#DF2935",
    hot="#C0392B",
    cold="#2980B9"
)
