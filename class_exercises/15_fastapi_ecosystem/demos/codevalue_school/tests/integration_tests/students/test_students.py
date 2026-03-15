"""Integration tests for /students/ endpoints."""

from fastapi import status
from tests import constants
from httpx import AsyncClient

from tests.test_utils import create_auth_token_for_user, set_auth_cookie

EXPECTED_FIXTURE_STUDENT_COUNT = 3


class TestGetAllStudents:
    """Integration tests for GET /students/ endpoint."""

    async def test_admin_gets_all_students(self, async_client: AsyncClient) -> None:
        token = await create_auth_token_for_user(constants.ADMIN_USER_EMAIL)
        set_auth_cookie(async_client, token)

        response = await async_client.get(constants.STUDENTS_ENDPOINT)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == EXPECTED_FIXTURE_STUDENT_COUNT
        for student in data:
            assert constants.STUDENT_ID_KEY in student
            assert constants.FIRST_NAME_KEY in student
            assert constants.LAST_NAME_KEY in student
            assert constants.EMAIL_KEY in student
            assert constants.CREATED_AT_KEY in student

    async def test_unauthenticated_is_unauthorized(self, async_client: AsyncClient) -> None:
        response = await async_client.get(constants.STUDENTS_ENDPOINT)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    async def test_student_role_is_forbidden(self, async_client: AsyncClient) -> None:
        token = await create_auth_token_for_user(constants.STUDENT_USER_EMAIL)
        set_auth_cookie(async_client, token)

        response = await async_client.get(constants.STUDENTS_ENDPOINT)

        assert response.status_code == status.HTTP_403_FORBIDDEN


class TestGetStudentById:
    """Integration tests for GET /students/{student_id} endpoint."""

    async def test_admin_gets_student_by_id(self, async_client: AsyncClient) -> None:
        token = await create_auth_token_for_user(constants.ADMIN_USER_EMAIL)
        set_auth_cookie(async_client, token)

        all_response = await async_client.get(constants.STUDENTS_ENDPOINT)
        fixture_student = next(
            student for student in all_response.json()
            if student[constants.EMAIL_KEY] == constants.FIXTURE_STUDENT_EMAIL_JOHN
        )
        student_id = fixture_student[constants.STUDENT_ID_KEY]

        response = await async_client.get(f"{constants.STUDENTS_ENDPOINT}{student_id}")

        assert response.status_code == status.HTTP_200_OK
        assert response.json()[constants.STUDENT_ID_KEY] == student_id
        assert response.json()[constants.EMAIL_KEY] == constants.FIXTURE_STUDENT_EMAIL_JOHN

    async def test_non_existent_id_is_not_found(self, async_client: AsyncClient) -> None:
        token = await create_auth_token_for_user(constants.ADMIN_USER_EMAIL)
        set_auth_cookie(async_client, token)

        response = await async_client.get(f"{constants.STUDENTS_ENDPOINT}{constants.NON_EXISTENT_ID}")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    async def test_unauthenticated_is_unauthorized(self, async_client: AsyncClient) -> None:
        response = await async_client.get(f"{constants.STUDENTS_ENDPOINT}1")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestCreateStudent:
    """Integration tests for POST /students/ endpoint."""

    async def test_admin_creates_student(self, async_client: AsyncClient) -> None:
        token = await create_auth_token_for_user(constants.ADMIN_USER_EMAIL)
        set_auth_cookie(async_client, token)
        new_student_payload = {
            constants.FIRST_NAME_KEY: "New",
            constants.LAST_NAME_KEY: "Student",
            constants.EMAIL_KEY: "new.student@school.test",
        }

        response = await async_client.post(constants.STUDENTS_ENDPOINT, json=new_student_payload)

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data[constants.EMAIL_KEY] == new_student_payload[constants.EMAIL_KEY]
        assert data[constants.FIRST_NAME_KEY] == new_student_payload[constants.FIRST_NAME_KEY]
        assert constants.STUDENT_ID_KEY in data

    async def test_duplicate_email_is_bad_request(self, async_client: AsyncClient) -> None:
        token = await create_auth_token_for_user(constants.ADMIN_USER_EMAIL)
        set_auth_cookie(async_client, token)
        payload = {
            constants.FIRST_NAME_KEY: "Dup",
            constants.LAST_NAME_KEY: "Student",
            constants.EMAIL_KEY: constants.FIXTURE_STUDENT_EMAIL_JOHN,
        }

        response = await async_client.post(constants.STUDENTS_ENDPOINT, json=payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    async def test_unauthenticated_is_unauthorized(self, async_client: AsyncClient) -> None:
        payload = {
            constants.FIRST_NAME_KEY: "X",
            constants.LAST_NAME_KEY: "Y",
            constants.EMAIL_KEY: "x@y.com",
        }
        response = await async_client.post(constants.STUDENTS_ENDPOINT, json=payload)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestUpdateStudent:
    """Integration tests for PUT /students/{student_id} endpoint."""

    async def test_admin_updates_student(self, async_client: AsyncClient) -> None:
        token = await create_auth_token_for_user(constants.ADMIN_USER_EMAIL)
        set_auth_cookie(async_client, token)
        update_payload = {
            constants.FIRST_NAME_KEY: "Updated",
            constants.LAST_NAME_KEY: "Student",
            constants.EMAIL_KEY: "update.student@school.test",
        }

        create_resp = await async_client.post(constants.STUDENTS_ENDPOINT, json=update_payload)
        student_id = create_resp.json()[constants.STUDENT_ID_KEY]
        updated_payload = {
            constants.FIRST_NAME_KEY: "Updated2",
            constants.LAST_NAME_KEY: "Student",
            constants.EMAIL_KEY: update_payload[constants.EMAIL_KEY],
        }
        response = await async_client.put(
            f"{constants.STUDENTS_ENDPOINT}{student_id}", json=updated_payload
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json()[constants.FIRST_NAME_KEY] == "Updated2"

    async def test_non_existent_id_is_not_found(self, async_client: AsyncClient) -> None:
        token = await create_auth_token_for_user(constants.ADMIN_USER_EMAIL)
        set_auth_cookie(async_client, token)
        payload = {
            constants.FIRST_NAME_KEY: "X",
            constants.LAST_NAME_KEY: "Y",
            constants.EMAIL_KEY: "noone@school.test",
        }

        response = await async_client.put(
            f"{constants.STUDENTS_ENDPOINT}{constants.NON_EXISTENT_ID}", json=payload
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestDeleteStudent:
    """Integration tests for DELETE /students/{student_id} endpoint."""

    async def test_admin_deletes_student(self, async_client: AsyncClient) -> None:
        token = await create_auth_token_for_user(constants.ADMIN_USER_EMAIL)
        set_auth_cookie(async_client, token)
        delete_payload = {
            constants.FIRST_NAME_KEY: "Delete",
            constants.LAST_NAME_KEY: "Me",
            constants.EMAIL_KEY: "delete.me@school.test",
        }

        create_resp = await async_client.post(constants.STUDENTS_ENDPOINT, json=delete_payload)
        student_id = create_resp.json()[constants.STUDENT_ID_KEY]

        response = await async_client.delete(f"{constants.STUDENTS_ENDPOINT}{student_id}")

        assert response.status_code == status.HTTP_204_NO_CONTENT

    async def test_non_existent_id_is_not_found(self, async_client: AsyncClient) -> None:
        token = await create_auth_token_for_user(constants.ADMIN_USER_EMAIL)
        set_auth_cookie(async_client, token)

        response = await async_client.delete(
            f"{constants.STUDENTS_ENDPOINT}{constants.NON_EXISTENT_ID}"
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
