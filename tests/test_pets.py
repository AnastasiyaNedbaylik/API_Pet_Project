import pytest

from api.api_pet import Pets
from settings import EXPECTED_PET_DATA

pet = Pets()


@pytest.mark.smoke
def test_get_token():
    token, user_id, status = pet.get_token()
    assert token
    assert status == 200
    assert user_id is not None


@pytest.mark.smoke
def test_register_user():
    status = pet.register_user()
    assert status == 200, f"Ожидался статус 200, но получен статус {status}"


@pytest.mark.smoke
def test_register_and_delete_user():
    status = pet.register_user_and_delete()
    assert status == 200, f"Ожидался статус 200, но получен статус {status}"


@pytest.mark.xfail
@pytest.mark.regression
def test_register_user_with_incorrect_emails():
    status = pet.register_user_with_incorrect_emails()
    assert status == 422, f"Ожидался статус 422, но получен статус {status}"


@pytest.mark.regression
def test_register_user_without_confirm_password():
    status = pet.register_user_without_confirm_password()
    assert status == 422, f"Ожидался статус 422, но получен статус {status}"


@pytest.mark.regression
def test_register_user_with_inv_passwords():
    status, returned_response = pet.register_user_with_inv_passwords()
    assert status == 400, f'Ожидался статус 400, но получен статус {status}'
    assert returned_response == 'Username is taken or pass issue'


@pytest.mark.regression
def test_login_with_invalid_email():
    status, returned_response = pet.login_with_invalid_email()
    assert status == 400, f'Ожидался статус 400, но получен статус {status}'
    assert returned_response == 'Username is taken or pass issue'


@pytest.mark.regression
def test_login_with_invalid_password():
    status, returned_response = pet.login_with_invalid_password()
    assert status == 400, f'Ожидался статус 400, но получен статус {status}'
    assert returned_response == 'Username is taken or pass issue'


@pytest.mark.smoke
def test_get_list_users():
    status, user_id = pet.get_list_users()
    assert status == 200, f'Ожидался статус 200, но получен статус {status}'
    assert user_id is not None


@pytest.mark.smoke
def test_add_pet():
    status, pet_id = pet.add_pet()
    assert status == 200, f'Ожидался статус 200, но получен статус {status}'
    assert pet_id is not None


@pytest.mark.regression
def test_dd_pet_without_req_data():
    status = pet.add_pet_without_req_data()
    assert status == 422, f'Ожидался статус 422, но получен статус {status}'


@pytest.mark.smoke
def test_get_pet():
    status = pet.get_pet()[0]
    pet_data = pet.get_pet()[1]
    assert status == 200
    assert isinstance(pet_data, dict), "Полученные данные не соответствуют ожидаемой структуре"
    assert all(key in pet_data for key in EXPECTED_PET_DATA)


@pytest.mark.smoke
def test_add_pet_photo():
    status, link = pet.add_pet_photo()
    assert status == 200, f'Ожидался статус 200, но получен статус {status}'
    assert link


@pytest.mark.smoke
def test_eit_pet():
    status = pet.edit_pet()[0]
    updated_pet_data = pet.edit_pet()[2]
    assert status == 200, f'Ожидался статус 200, но получен статус {status}'
    assert updated_pet_data["pet"]["name"] == 'NewMolly', 'Не удалось изменить имя питомца'
    assert updated_pet_data["pet"]["type"] == 'cat', 'Не удалось изменить тип питомца'
    assert updated_pet_data["pet"]["age"] == 7, 'Не удалось изменить возраст питомца'
    assert updated_pet_data["pet"]["gender"] == 'Male', 'Не удалось изменить возраст питомца'


@pytest.mark.smoke
def test_like_my_pet():
    status, current_pet_id, initially_like_count, current_likes_count = pet.like_my_pet()
    assert status == 200, f'Ожидался статус 200, но получен статус {status}'
    assert current_pet_id is not None
    assert initially_like_count != current_likes_count


# @pytest.mark.regression
# def test_like_not_my_pet():
#     status, current_pet_id, initially_like_count, current_likes_count = pet.like_not_my_pet()
#     assert status == 200, f'Ожидался статус 200, но получен статус {status}'
#     assert current_pet_id is not None
#     assert initially_like_count != current_likes_count

@pytest.mark.regression
def test_like_pet_twice():
    status, returned_response = pet.like_pet_twice()
    assert status == 403
    assert returned_response == "You already liked it"


@pytest.mark.smoke
def test_delete_pet():
    status, returned_response = pet.delete_pet()
    assert status == 200
    assert len(returned_response) == 0
