import json
from settings import Data
import requests

Data = Data()


class Pets:

    def __init__(self):
        self.base_url = Data.BASE_URL  # 'http://34.141.58.52:8000/'

    def register_user(self) -> json:
        """ Positive: Create a new user"""
        try:
            data = {"email": Data.USER_EMAIL,
                    "password": Data.USER_PASSWORD, "confirm_password": Data.USER_PASSWORD}
            response = requests.post(self.base_url + 'register', data=json.dumps(data))
            status = response.status_code
            return status
        except requests.exceptions.RequestException as e:
            raise Exception(f"Ошибка при выполнении запроса: {e}")

    def register_user_and_delete(self) -> json:
        """ Positive: Create and delete a new user"""
        try:
            data = {"email": Data.USER_EMAIL,
                    "password": Data.USER_PASSWORD, "confirm_password": Data.USER_PASSWORD}
            response = requests.post(self.base_url + 'register', data=json.dumps(data))
            user_id = response.json()['id']
            token = response.json()['token']
            headers = {'Authorization': f'Bearer {token}'}
            params = {'id': user_id}
            response = requests.delete(self.base_url + f'users/{user_id}', headers=headers, params=params)
            status = response.status_code
            return status
        except requests.exceptions.RequestException as e:
            raise Exception(f"Ошибка при выполнении запроса: {e}")

    def register_user_without_confirm_password(self) -> json:
        """ Negative: User registration without confirm password"""
        try:
            data = {"email": Data.USER_EMAIL,
                    "password": Data.USER_PASSWORD}
            response = requests.post(self.base_url + 'register', data=json.dumps(data))
            status = response.status_code
            return status
        except requests.exceptions.RequestException as e:
            raise Exception(f"Ошибка при выполнении запроса: {e}")

    def register_user_with_incorrect_emails(self) -> json:
        """ Negative: User registration with incorrect emails"""
        try:
            data = {"email": Data.INCORRECT_EMAIL,
                    "password": Data.USER_PASSWORD, "confirm_password": Data.USER_PASSWORD}
            response = requests.post(self.base_url + 'register', data=json.dumps(data))
            status = response.status_code
            return status
        except requests.exceptions.RequestException as e:
            raise Exception(f"Ошибка при выполнении запроса: {e}")

    def register_user_with_inv_passwords(self) -> json:
        """ Negative: User registration without invalid confirm password"""
        try:
            data = {"email": Data.USER_EMAIL,
                    "password": Data.USER_PASSWORD, "confirm_password": f'invalid{Data.USER_PASSWORD}'}
            response = requests.post(self.base_url + 'register', data=json.dumps(data))
            status = response.status_code
            returned_response = response.json()['detail']
            return status, returned_response
        except requests.exceptions.RequestException as e:
            raise Exception(f"Ошибка при выполнении запроса: {e}")

    def get_token(self) -> json:
        """ Request to Swagger to receive user-token using email and password"""
        try:
            data = {
                "email": Data.VALID_EMAIL,
                "password": Data.VALID_PASSWORD
            }
            response = requests.post(self.base_url + "login", data=json.dumps(data))
            token = response.json()['token']
            user_id = response.json()['id']
            status = response.status_code
            return token, user_id, status
        except requests.exceptions.RequestException as e:
            raise Exception(f"Ошибка при выполнении запроса: {e}")

    def login_with_invalid_email(self) -> json:
        """Negative: Login with invalid email"""
        try:
            data = {
                "email": f'invalid{Data.VALID_EMAIL}',
                "password": Data.VALID_PASSWORD
            }
            response = requests.post(self.base_url + "login", data=json.dumps(data))
            returned_response = response.json()['detail']
            status = response.status_code
            return status, returned_response
        except requests.exceptions.RequestException as e:
            raise Exception(f"Ошибка при выполнении запроса: {e}")

    def login_with_invalid_password(self) -> json:
        """Negative: Login with invalid password"""
        try:
            data = {
                "email": Data.VALID_EMAIL,
                "password": f'invalid{Data.VALID_PASSWORD}'
            }
            response = requests.post(self.base_url + "login", data=json.dumps(data))
            returned_response = response.json()['detail']
            status = response.status_code
            return status, returned_response
        except requests.exceptions.RequestException as e:
            raise Exception(f"Ошибка при выполнении запроса: {e}")

    def get_list_users(self):
        """ Receiving User Id """
        try:
            token = Pets().get_token()[0]
            headers = {'Authorization': f'Bearer {token}'}
            response = requests.get(self.base_url + 'users', headers=headers)
            status = response.status_code
            user_id = response.text
            return status, user_id
        except requests.exceptions.RequestException as e:
            raise Exception(f"Ошибка при выполнении запроса: {e}")

    def add_pet(self):
        """Create a new pet"""
        try:
            token = Pets().get_token()[0]
            user_id = Pets().get_token()[1]
            headers = {'Authorization': f'Bearer {token}'}
            data = {"name": 'Molly',
                    "type": 'dog',
                    "age": 3,
                    "owner_id": user_id
                    }
            response = requests.post(self.base_url + 'pet', data=json.dumps(data), headers=headers)
            status = response.status_code
            pet_id = response.json()['id']
            return status, pet_id
        except requests.exceptions.RequestException as e:
            raise Exception(f"Ошибка при выполнении запроса: {e}")

    def add_pet_without_req_data(self):
        """Create a new pet without required data - name"""
        try:
            token = Pets().get_token()[0]
            user_id = Pets().get_token()[1]
            headers = {'Authorization': f'Bearer {token}'}
            data = {"type": 'dog',
                    "age": 3,
                    "owner_id": user_id
                    }
            response = requests.post(self.base_url + 'pet', data=json.dumps(data), headers=headers)
            status = response.status_code
            return status
        except requests.exceptions.RequestException as e:
            raise Exception(f"Ошибка при выполнении запроса: {e}")

    def get_pet(self):
        """Getting pet data by pet Id"""
        try:
            token = Pets().get_token()[0]
            pet_id = Pets().add_pet()[1]
            headers = {'Authorization': f'Bearer {token}'}
            response = requests.get(self.base_url + f'pet/{pet_id}', headers=headers)
            status = response.status_code
            pet_data = response.json()
            pet_info = response.json()['pet']
            current_pet_id = pet_info['id']
            likes_count = pet_info['likes_count']
            return status, pet_data, current_pet_id, likes_count, pet_info
        except requests.exceptions.RequestException as e:
            raise Exception(f"Ошибка при запросе: {e}")

    def add_pet_photo(self):
        """Uploading an image to a pet"""
        try:
            token = Pets().get_token()[0]
            pet_id = Pets().add_pet()[1]
            headers = {'Authorization': f'Bearer {token}'}
            files = {'pic': ('dog.jpg', open(r'/Users/anastasiya.niadbailik/Automation/API_Pet_Project/images/dog.jpg',
                                             'rb'), 'image/jpeg')}
            response = requests.post(self.base_url + f'pet/{pet_id}/image', headers=headers, files=files)
            status = response.status_code
            link = response.json()['link']
            return status, link
        except requests.exceptions.RequestException as e:
            raise Exception(f"Ошибка при выполнении запроса: {e}")

    def edit_pet(self):
        """Update pet data"""
        try:
            token = Pets().get_token()[0]
            pet_id = Pets().add_pet()[1]
            headers = {'Authorization': f'Bearer {token}'}
            data = {"id": pet_id,
                    "name": 'NewMolly',
                    "type": 'cat',
                    "age": 7,
                    "gender": 'Male',
                    }
            response = requests.patch(self.base_url + 'pet', data=json.dumps(data), headers=headers)
            status = response.status_code
            updated_pet_id = response.json()['id']
            res = requests.get(self.base_url + f'pet/{updated_pet_id}', headers=headers)
            updated_pet_data = res.json()
            # print(updated_pet_data)
            return status, updated_pet_id, updated_pet_data
        except requests.exceptions.RequestException as e:
            raise Exception(f"Ошибка при выполнении запроса: {e}")

    def like_my_pet(self):
        """Like my pet"""
        token = Pets().get_token()[0]
        current_pet_id = Pets().get_pet()[2]
        initially_like_count = Pets().get_pet()[3]
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.put(self.base_url + f'pet/{current_pet_id}/like', headers=headers)
        status = response.status_code
        response = requests.get(self.base_url + f'pet/{current_pet_id}', headers=headers)
        current_pet_data = response.json()['pet']
        current_pet_id = current_pet_data['id']
        current_likes_count = current_pet_data['likes_count']
        # print(status, current_pet_id, initially_like_count, current_likes_count)
        return status, current_pet_id, initially_like_count, current_likes_count

    #
    #
    # def like_not_my_pet(self): #somthing went wrong during implementation :)
    #     token = Pets().get_token()[0]
    #     headers = {'Authorization': f'Bearer {token}'}
    #     data = {"id": 23537
    #             }
    #     response_get = requests.get(self.base_url + f'pet/{23537}', headers=headers)
    #     status_get = response_get.status_code
    #     # pet_data = response.json()
    #     pet_info = response_get.json()['pet']
    #     current_pet_id = pet_info['id']
    #     initially_likes_count = pet_info['likes_count']
    #     response = requests.put(self.base_url + f'pet/{current_pet_id}/like', data=json.dumps(data), headers=headers)
    #     status = response.status_code
    #     if status == 403:
    #         raise Exception(f"You already like it")
    #     new_response_get = requests.get(self.base_url + f'pet/{current_pet_id}', headers=headers)
    #     pet_data_after = new_response_get.json()['pet']
    #     pet_id = pet_data_after['id']
    #     current_likes_count = pet_info['likes_count']
    #     print(status, initially_likes_count, current_likes_count, pet_id)
    #     return status, initially_likes_count, current_likes_count, pet_id

    def like_pet_twice(self):
        """Negative test: check double like the same pet"""
        try:
            token = Pets().get_token()[0]
            pet_id = Pets().like_my_pet()[1]
            headers = {'Authorization': f'Bearer {token}'}
            response = requests.put(self.base_url + f'pet/{pet_id}/like', headers=headers)
            status = response.status_code
            returned_response = response.json()['detail']
            return status, returned_response
        except requests.exceptions.RequestException as e:
            raise Exception(f"Ошибка при выполнении запроса: {e}")

    def add_pet_comment(self):
        """Adding a comment to a pet"""
        try:
            token = Pets().get_token()[0]
            pet_id = Pets().add_pet()[1]
            headers = {'Authorization': f'Bearer {token}'}
            data = {"message": "Sooo cute pet!!!!!"
                    }
            response = requests.put(self.base_url + f'pet/{pet_id}/comment', data=json.dumps(data), headers=headers)
            status = response.status_code
            response = requests.get(self.base_url + f'pet/{pet_id}', headers=headers)
            comment_data = response.json()['comments']
            comment = comment_data[-1]
            comment_text = comment['message']
            return status, comment_data, comment_text
        except requests.exceptions.RequestException as e:
            raise Exception(f"Ошибка при выполнении запроса: {e}")

    def delete_pet(self):
        """Removing a pet"""
        try:
            token = Pets().get_token()[0]
            current_pet_id = Pets().get_pet()[2]
            headers = {'Authorization': f'Bearer {token}'}
            response = requests.delete(self.base_url + f'pet/{current_pet_id}', headers=headers)
            status = response.status_code
            returned_response = response.json()
            response_get = requests.get(self.base_url + f'pet/{current_pet_id}', headers=headers)
            status_get = response_get.status_code
            if status_get == 200:
                raise Exception(f"Питомец все еще существует")
            return status, returned_response
        except requests.exceptions.RequestException as e:
            raise Exception(f"Ошибка при выполнении запроса: {e}")


# Pets().get_token()
# Pets().register_user()
# Pets().register_user_and_delete()
# Pets().register_user_with_incorrect_emails()
# Pets().register_user_without_confirm_password()
# Pets().register_user_with_inv_passwords()
# Pets().login_with_invalid_email()
# Pets().login_with_invalid_password()
# Pets().get_list_users()
# Pets().add_pet()
# Pets().add_pet_without_req_data()
# Pets().get_pet()
# Pets().add_pet_photo()
# Pets().edit_pet()
# Pets().like_my_pet()
# Pets().like_not_my_pet()
# Pets().like_pet_twice()
# Pets().add_pet_comment()
# Pets().delete_pet()
