"""Tests for unregister endpoint"""

import pytest


def test_unregister_success(client):
    """Test successful unregistration from an activity"""
    email = "unregister_test@mergington.edu"
    
    # First sign up
    client.post(
        "/activities/Basketball/signup",
        params={"email": email}
    )
    
    # Get initial count
    response = client.get("/activities")
    initial_count = len(response.json()["Basketball"]["participants"])
    
    # Unregister
    response = client.delete(
        "/activities/Basketball/unregister",
        params={"email": email}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "Unregistered" in data["message"]
    
    # Verify the student was removed
    response = client.get("/activities")
    new_count = len(response.json()["Basketball"]["participants"])
    assert new_count == initial_count - 1
    assert email not in response.json()["Basketball"]["participants"]


def test_unregister_nonexistent_activity(client):
    """Test unregistration from a non-existent activity"""
    response = client.delete(
        "/activities/Nonexistent/unregister",
        params={"email": "student@mergington.edu"}
    )
    
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]


def test_unregister_not_registered_student(client):
    """Test unregistration of a student not in the activity"""
    response = client.delete(
        "/activities/Basketball/unregister",
        params={"email": "notregistered@mergington.edu"}
    )
    
    assert response.status_code == 400
    data = response.json()
    assert "not registered" in data["detail"]


def test_unregister_original_participant(client):
    """Test unregistration of an originally registered participant"""
    response = client.delete(
        "/activities/Basketball/unregister",
        params={"email": "james@mergington.edu"}
    )
    
    assert response.status_code == 200
    
    # Verify the participant was removed
    response = client.get("/activities")
    assert "james@mergington.edu" not in response.json()["Basketball"]["participants"]


def test_unregister_then_signup_again(client):
    """Test that a student can sign up again after unregistering"""
    email = "rejoin@mergington.edu"
    
    # Sign up
    client.post(
        "/activities/Tennis Club/signup",
        params={"email": email}
    )
    
    # Unregister
    client.delete(
        "/activities/Tennis Club/unregister",
        params={"email": email}
    )
    
    # Sign up again
    response = client.post(
        "/activities/Tennis Club/signup",
        params={"email": email}
    )
    
    assert response.status_code == 200
    
    # Verify signed up
    response = client.get("/activities")
    assert email in response.json()["Tennis Club"]["participants"]
