"""Tests for signup endpoint"""

import pytest


def test_signup_success(client):
    """Test successful signup for an activity"""
    # Get initial participant count
    response = client.get("/activities")
    initial_count = len(response.json()["Basketball"]["participants"])
    
    # Sign up a new student
    response = client.post(
        "/activities/Basketball/signup",
        params={"email": "newstudent@mergington.edu"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "newstudent@mergington.edu" in data["message"]
    
    # Verify the student was added
    response = client.get("/activities")
    new_count = len(response.json()["Basketball"]["participants"])
    assert new_count == initial_count + 1
    assert "newstudent@mergington.edu" in response.json()["Basketball"]["participants"]


def test_signup_nonexistent_activity(client):
    """Test signup for a non-existent activity"""
    response = client.post(
        "/activities/Nonexistent/signup",
        params={"email": "student@mergington.edu"}
    )
    
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]


def test_signup_duplicate_student(client):
    """Test that a student cannot sign up twice for the same activity"""
    # First signup
    client.post(
        "/activities/Tennis Club/signup",
        params={"email": "duplicate@mergington.edu"}
    )
    
    # Second signup (duplicate)
    response = client.post(
        "/activities/Tennis Club/signup",
        params={"email": "duplicate@mergington.edu"}
    )
    
    assert response.status_code == 400
    data = response.json()
    assert "already signed up" in data["detail"]


def test_signup_already_registered_student(client):
    """Test that already registered students cannot sign up again"""
    response = client.post(
        "/activities/Basketball/signup",
        params={"email": "james@mergington.edu"}
    )
    
    assert response.status_code == 400
    data = response.json()
    assert "already signed up" in data["detail"]


def test_signup_multiple_activities(client):
    """Test that a student can sign up for multiple activities"""
    email = "multi@mergington.edu"
    
    # Sign up for Basketball
    response1 = client.post(
        "/activities/Basketball/signup",
        params={"email": email}
    )
    assert response1.status_code == 200
    
    # Sign up for Tennis Club
    response2 = client.post(
        "/activities/Tennis Club/signup",
        params={"email": email}
    )
    assert response2.status_code == 200
    
    # Verify both signups
    response = client.get("/activities")
    assert email in response.json()["Basketball"]["participants"]
    assert email in response.json()["Tennis Club"]["participants"]
