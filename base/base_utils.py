import json
import random
import numpy as np
import importlib_resources

from datetime import datetime
from faker import Faker

from variables.config_base import PET_CATEGORIES, PET_PHOTO_URLS_LIST, PET_TAGS, PET_STATUS_LIST, STORE_STATUS_LIST

fake = Faker()


def get_schema(schema_filename):
    filename = str(importlib_resources.files('json_schemas').joinpath(schema_filename))
    with open(filename, 'r') as file:
        schema = json.load(file)
    return schema


def make_new_pet_body():
    name = fake.first_name()
    category = random.choice(PET_CATEGORIES)
    photo_urls = random.sample(PET_PHOTO_URLS_LIST, k=random.randint(1, len(PET_PHOTO_URLS_LIST)))
    tags = random.sample(PET_TAGS, k=random.randint(1, len(PET_TAGS)))
    status = random.choice(PET_STATUS_LIST)
    return {"name": name,
            "category": category,
            "photoUrls": photo_urls,
            "tags": tags,
            "status": status
            }


def make_new_order_body(status=STORE_STATUS_LIST[0], complete=True):
    pet_id = random.randint(1, np.iinfo(np.int64).max)
    quantity = random.randint(1, np.iinfo(np.int32).max)
    ship_date = datetime.now().isoformat()
    status = status
    complete = complete
    return {"petId": pet_id,
            "quantity": quantity,
            "shipDate": ship_date,
            "status": status,
            "complete": complete
            }


def make_new_user_body():
    username = fake.user_name()
    first_name = fake.first_name()
    last_name = fake.last_name()
    email = fake.email()
    password = fake.password()
    phone = fake.phone_number()
    user_status = 0
    return {"username": username,
            "firstName": first_name,
            "lastName": last_name,
            "email": email,
            "password": password,
            "phone": phone,
            "userStatus": user_status
            }
