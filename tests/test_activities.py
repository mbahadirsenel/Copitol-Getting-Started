"""Tests for activities endpoints"""

import pytest


def test_get_activities(client):
    """Test getting all activities"""
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    
    # Check that we have expected activities
    assert "Basketball" in data
    assert "Tennis Club" in data
    assert "Drama Club" in data
    
    # Check structure of an activity
    activity = data["Basketball"]
    assert "description" in activity
    assert "schedule" in activity
    assert "max_participants" in activity
    assert "participants" in activity
    assert isinstance(activity["participants"], list)


def test_activity_has_correct_fields(client):
    """Test that each activity has all required fields"""
    response = client.get("/activities")
    activities = response.json()
    
    required_fields = {"description", "schedule", "max_participants", "participants"}
    
    for activity_name, activity_data in activities.items():
        assert required_fields.issubset(activity_data.keys()), \
            f"Activity {activity_name} missing required fields"


def test_initial_participants(client):
    """Test that initial participants are loaded correctly"""
    response = client.get("/activities")
    activities = response.json()
    
    # Basketball should have james@mergington.edu
    assert "james@mergington.edu" in activities["Basketball"]["participants"]
    
    # Drama Club should have two participants
    assert len(activities["Drama Club"]["participants"]) == 2
    assert "maya@mergington.edu" in activities["Drama Club"]["participants"]
    assert "lucas@mergington.edu" in activities["Drama Club"]["participants"]
