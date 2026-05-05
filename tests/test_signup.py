"""
Unit tests for the /signup endpoint
"""

import pytest


def test_signup_for_activity_success(client):
    """Test successfully signing up a student for an activity"""
    response = client.post(
        "/activities/Soccer Team/signup?email=newstudent@mergington.edu"
    )
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "newstudent@mergington.edu" in data["message"]
    assert "Soccer Team" in data["message"]


def test_signup_adds_participant_to_activity(client):
    """Test that signup actually adds the participant to the activity list"""
    # First, get the initial participant count
    response = client.get("/activities")
    initial_participants = response.json()["Soccer Team"]["participants"].copy()
    initial_count = len(initial_participants)
    
    # Sign up a new student
    new_email = "testnewstudent@mergington.edu"
    signup_response = client.post(
        f"/activities/Soccer Team/signup?email={new_email}"
    )
    assert signup_response.status_code == 200
    
    # Check that the participant was added
    response = client.get("/activities")
    updated_participants = response.json()["Soccer Team"]["participants"]
    assert len(updated_participants) == initial_count + 1
    assert new_email in updated_participants


def test_signup_nonexistent_activity_returns_404(client):
    """Test that signing up for a non-existent activity returns 404"""
    response = client.post(
        "/activities/Nonexistent Activity/signup?email=student@mergington.edu"
    )
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]


def test_signup_duplicate_email_returns_400(client):
    """Test that signing up with a duplicate email returns 400"""
    # Use an email that's already registered for Soccer Team
    response = client.post(
        "/activities/Soccer Team/signup?email=liam@mergington.edu"
    )
    assert response.status_code == 400
    data = response.json()
    assert "already signed up" in data["detail"]


def test_signup_multiple_activities_allowed(client):
    """Test that a student can sign up for multiple different activities"""
    new_email = "multiactivity@mergington.edu"
    
    # Sign up for first activity
    response1 = client.post(
        f"/activities/Soccer Team/signup?email={new_email}"
    )
    assert response1.status_code == 200
    
    # Sign up for second activity
    response2 = client.post(
        f"/activities/Chess Club/signup?email={new_email}"
    )
    assert response2.status_code == 200
    
    # Verify student is in both activities
    activities = client.get("/activities").json()
    assert new_email in activities["Soccer Team"]["participants"]
    assert new_email in activities["Chess Club"]["participants"]


def test_signup_returns_message_with_activity_and_email(client):
    """Test that signup response includes activity name and email"""
    test_email = "messagecheckemail@mergington.edu"
    response = client.post(
        f"/activities/Programming Class/signup?email={test_email}"
    )
    assert response.status_code == 200
    data = response.json()
    assert test_email in data["message"]
    assert "Programming Class" in data["message"]
