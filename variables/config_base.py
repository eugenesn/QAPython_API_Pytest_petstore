BASE_URL = 'https://petstore.swagger.io/v2'

HEADERS = {'accept': 'application/json',
           'Content-Type': 'application/json'}

PET_PHOTO_URLS_LIST = [
    'https://images.examples.com/pet_image_01.jpg',
    'https://images.examples.com/pet_image_02.jpg',
    'https://images.examples.com/pet_image_03.jpg',
    'https://images.examples.com/pet_image_04.jpg',
    'https://images.examples.com/pet_image_05.jpg',
]

PET_STATUS_LIST = ['available', 'pending', 'sold']

PET_CATEGORIES = ({"id": 1, "name": "dogs"},
                  {"id": 2, "name": "cats"},
                  {"id": 3, "name": "fish"})

PET_TAGS = ({"id": 1, "name": "tag_one"},
            {"id": 2, "name": "tag_two"},
            {"id": 3, "name": "tag_three"},
            {"id": 4, "name": "tag_four"},
            {"id": 5, "name": "tag_five"})

STORE_STATUS_LIST = ['placed', 'approved', 'delivered']
