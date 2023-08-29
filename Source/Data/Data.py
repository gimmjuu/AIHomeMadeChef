from dataclasses import dataclass


@dataclass
class User:
    user_id: str
    user_pwd: str = None
    user_name: str = None
    user_taste: str = None


@dataclass
class Food:
    food_id: str


@dataclass
class Recipe:
    recipe_id: int
    recipe_name: str = None
    recipe_type: str = None
    recipe_stuff: str = None
    recipe_step: str = None


@dataclass
class Result:
    true_or_false: bool = None


@dataclass
class Like:
    like_user_id: str
    like_recipe_id: str


if __name__ == '__main__':
    usr1 = User('admin', '1234', '관리자')
