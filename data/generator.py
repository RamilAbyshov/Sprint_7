from faker import Faker
import random
from data import test_data

faker = Faker("ru_RU")


def generate_courier():
    return {
        "login": faker.unique.user_name(),
        "password": faker.password(length=10),
        "firstName": faker.first_name()
    }


def generate_order_data(colors=None):
    if colors is None:
        colors = random.choice([
            test_data.COLORS_BLACK,
            test_data.COLORS_GREY,
            test_data.COLORS_BOTH,
            test_data.COLORS_NONE
        ])
    return {
        "firstName": faker.first_name(),
        "lastName": faker.last_name(),
        "address": faker.street_address(),
        "metroStation": str(random.randint(1, 200)),
        "phone": faker.phone_number(),
        "rentTime": random.randint(1, 10),
        "deliveryDate": faker.date_this_year().isoformat(),
        "comment": faker.sentence(),
        "color": colors
    }
