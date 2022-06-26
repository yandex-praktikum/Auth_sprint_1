from enum import Enum


class Message(str, Enum):
    film_not_found = "film not found"
    person_not_found = "person not found"
    genre_not_found = "genre not found"
