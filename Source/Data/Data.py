from dataclasses import dataclass


@dataclass
class User:
    user_id: str
    user_pwd: str = None
    user_name: str = None


@dataclass
class Food:
    food_id: str


@dataclass
class Recipe:
    recipe_id: str
    recipe_name: str
    recipe_stuff: str
    recipe_step: str


if __name__ == '__main__':
    usr1 = User('admin', '1234', '관리자')
