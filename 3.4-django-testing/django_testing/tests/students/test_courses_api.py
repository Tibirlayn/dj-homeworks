import pytest
from rest_framework import status
from students.models import Course


@pytest.mark.django_db
def test_retrieve_course(client, course_factory):
    # Arrange
    course = course_factory()

    # Act
    response = client.get(f'/api/v1/courses/{course.id}/')

    # Assert
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data['name'] == course.name


@pytest.mark.django_db
def test_list_courses(client, course_factory):
    # Arrange
    courses = course_factory(_quantity=10)

    # Act
    response = client.get('/api/v1/courses/')

    # Assert
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == len(courses)
    for i, m in enumerate(data):
        assert m['name'] == courses[i].name


@pytest.mark.django_db
def test_filter_courses_by_id(client, course_factory):
    # Arrange
    courses = course_factory(_quantity=10)
    course_id = courses[0].id


    response = client.get('/api/v1/courses/', data={'id': [course_id]})

    # Assert
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 1
    assert data[0]['id'] == course_id


@pytest.mark.django_db
def test_filter_courses_by_name(client, course_factory):
    # Arrange
    courses = course_factory(_quantity=10)
    course_name = courses[0].name

    # Act
    response = client.get('/api/v1/courses/', data={'name': course_name})

    # Assert
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) >= 1
    for course in data:
        assert course['name'] == course_name


@pytest.mark.django_db
def test_create_course(client):
    # Arrange
    count = Course.objects.count()
    data = {'name': 'Python123'}

    # Act
    response = client.post('/api/v1/courses/', data=data)

    # Assert
    assert response.status_code == status.HTTP_201_CREATED
    assert Course.objects.count() == count + 1
    assert Course.objects.latest('id').name == 'Python'


@pytest.mark.django_db
def test_update_course(client, course_factory):
    # Arrange
    course = course_factory()
    data = {'name': 'New Name'}

    # Act
    response = client.patch(f'/api/v1/courses/{course.id}/', data=data)

    # Assert
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data['name'] == 'New Name'
    assert Course.objects.get(id=course.id).name == 'New Name'


@pytest.mark.django_db
def test_delete_course(client, course_factory):
    # Arrange
    course = course_factory()
    count = Course.objects.count()

    # Act
    response = client.delete(f'/api/v1/courses/{course.id}/')

    # Assert
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Course.objects.count() == count - 1
