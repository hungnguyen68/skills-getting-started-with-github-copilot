import pytest


def test_get_activities_returns_all_activities(client):
    # Arrange
    url = "/activities"

    # Act
    response = client.get(url)

    # Assert
    assert response.status_code == 200
    activities = response.json()
    assert "Chess Club" in activities
    assert isinstance(activities["Chess Club"]["participants"], list)


def test_signup_for_activity_adds_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "teststudent@mergington.edu"
    url = f"/activities/{activity_name}/signup?email={email}"

    # Act
    response = client.post(url)

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"
    assert email in client.get("/activities").json()[activity_name]["participants"]


def test_signup_for_activity_duplicate_returns_400(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    url = f"/activities/{activity_name}/signup?email={email}"

    # Act
    response = client.post(url)

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_for_unknown_activity_returns_404(client):
    # Arrange
    activity_name = "Nonexistent Club"
    email = "teststudent@mergington.edu"
    url = f"/activities/{activity_name}/signup?email={email}"

    # Act
    response = client.post(url)

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_remove_participant_unregisters_student(client):
    # Arrange
    activity_name = "Chess Club"
    email = "daniel@mergington.edu"
    url = f"/activities/{activity_name}/participants?email={email}"

    # Act
    response = client.delete(url)

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {email} from {activity_name}"
    assert email not in client.get("/activities").json()[activity_name]["participants"]


def test_remove_nonexistent_participant_returns_404(client):
    # Arrange
    activity_name = "Chess Club"
    email = "notregistered@mergington.edu"
    url = f"/activities/{activity_name}/participants?email={email}"

    # Act
    response = client.delete(url)

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"


def test_remove_participant_unknown_activity_returns_404(client):
    # Arrange
    activity_name = "Ghost Club"
    email = "teststudent@mergington.edu"
    url = f"/activities/{activity_name}/participants?email={email}"

    # Act
    response = client.delete(url)

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
