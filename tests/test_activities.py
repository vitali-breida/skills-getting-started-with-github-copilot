"""
Unit tests for the /activities endpoint
"""

import pytest


def test_get_activities_returns_success(client):
    """Test that GET /activities returns a 200 status code"""
    response = client.get("/activities")
    assert response.status_code == 200


def test_get_activities_returns_dict(client):
    """Test that GET /activities returns a dictionary of activities"""
    response = client.get("/activities")
    data = response.json()
    assert isinstance(data, dict)
    assert len(data) > 0


def test_get_activities_contains_expected_activities(client):
    """Test that GET /activities contains all expected activities"""
    response = client.get("/activities")
    data = response.json()
    expected_activities = [
        "Soccer Team",
        "Swimming Club",
        "Drama Club",
        "Creative Arts",
        "Mathletes",
        "Debate Team",
        "Chess Club",
        "Programming Class",
        "Gym Class"
    ]
    for activity in expected_activities:
        assert activity in data


def test_get_activities_has_required_fields(client):
    """Test that each activity has all required fields"""
    response = client.get("/activities")
    data = response.json()
    
    required_fields = ["description", "schedule", "max_participants", "participants"]
    
    for activity_name, activity_data in data.items():
        for field in required_fields:
            assert field in activity_data, f"Activity '{activity_name}' missing field '{field}'"


def test_get_activities_response_structure(client):
    """Test that activity data has correct structure"""
    response = client.get("/activities")
    data = response.json()
    
    for activity_name, activity_data in data.items():
        assert isinstance(activity_data["description"], str)
        assert isinstance(activity_data["schedule"], str)
        assert isinstance(activity_data["max_participants"], int)
        assert isinstance(activity_data["participants"], list)
        assert activity_data["max_participants"] > 0
        
        # All participants should be strings (emails)
        for participant in activity_data["participants"]:
            assert isinstance(participant, str)
