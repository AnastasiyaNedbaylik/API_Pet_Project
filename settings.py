from faker import Faker

EXPECTED_PET_DATA = {
    "pet": {
        "id": int,
        "name": str,
        "type": str,
        "age": int,
        "gender": str,
        "owner_id": int,
        "pic": str,
        "owner_name": str,
        "likes_count": int,
        "liked_by_user": (int, type(None))  # Поле может быть int или None
    },
    "comments": list
}


class Data:
    VALID_EMAIL = ""
    VALID_PASSWORD = "fhfurbd4547474@!@!"
    # INCORRECT_EMAIL = 'autotest2gmail.com'
    BASE_URL = 'http://34.141.58.52:8000/'

    fake = Faker()

    USER_EMAIL = fake.email()
    USER_PASSWORD = fake.password()
    INCORRECT_EMAIL = fake.first_name()
