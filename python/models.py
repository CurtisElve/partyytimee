from sqlmodel import Field, SQLModel, create_engine
from pydantic import EmailStr, BaseModel
from datetime import datetime
import datetime as dt
from typing import List, Optional
import json

class User(SQLModel, table=True):
    id : int | None = Field(default=None, primary_key=True)
    username : str
    email : EmailStr | None
    pfpURL : str | None
    firebase_uid: str | None = Field(default=None, index=True, unique=True, description="Firebase UID")
    email_verified: bool = Field(default=False, description="Is the email verified?")
    phone: str | None = Field(default=None, description="User's phone number")
    isHost: bool | None = Field(default=False)
    bio: str | None = Field(default=None, description="User's bio")
    saved_party_ids: str = Field(default="[]", description="JSON array of saved party IDs")
    current_party_id: int | None = Field(default=None, description="ID of party user is currently at")
    created_at: datetime | None = Field(default_factory=lambda: datetime.now(dt.UTC))
    updated_at: datetime | None = Field(default_factory=lambda: datetime.now(dt.UTC))

class Party(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(description="Party name")
    description: str | None = Field(default=None, description="Party description")
    
    # Host relationship
    host_id: int = Field(foreign_key="user.id", description="Host user ID")
    
    # Attendees as JSON list of user IDs (lighter than full User objects)
    attendee_ids: str = Field(default="[]", description="JSON array of user IDs")
    
    # Location with PostGIS support
    latitude: float | None = Field(default=None, description="Latitude")
    longitude: float | None = Field(default=None, description="Longitude")
    address: str | None = Field(default=None, description="Human readable address")
    
    # Party details
    start_time: datetime | None = Field(default=None, description="Party start time")
    end_time: datetime | None = Field(default=None, description="Party end time")
    max_attendees: int | None = Field(default=None, description="Maximum number of attendees")
    hashtags: str | None = Field(default=None, description="hashtags")
    media_url: str | None = Field(default=None, description="URL for party media/images")
    
    # Timestamps
    created_at: datetime | None = Field(default_factory=lambda: datetime.now(dt.UTC))
    updated_at: datetime | None = Field(default_factory=lambda: datetime.now(dt.UTC))

class newUser(BaseModel):
    email: EmailStr
    username : str
    phone: str = None
    bio: str = None

# Helper functions for Party model
def get_attendee_ids(party: Party) -> List[int]:
    """Get list of attendee user IDs from JSON string"""
    try:
        return json.loads(party.attendee_ids)
    except (json.JSONDecodeError, TypeError):
        return []

def set_attendee_ids(party: Party, attendee_ids: List[int]) -> None:
    """Set attendee user IDs as JSON string"""
    party.attendee_ids = json.dumps(attendee_ids)

def add_attendee(party: Party, user_id: int) -> bool:
    """Add a user to the party attendees"""
    attendee_ids = get_attendee_ids(party)
    if user_id not in attendee_ids:
        attendee_ids.append(user_id)
        set_attendee_ids(party, attendee_ids)
        return True
    return False

def remove_attendee(party: Party, user_id: int) -> bool:
    """Remove a user from the party attendees"""
    attendee_ids = get_attendee_ids(party)
    if user_id in attendee_ids:
        attendee_ids.remove(user_id)
        set_attendee_ids(party, attendee_ids)
        return True
    return False

# Helper functions for User saved parties
def get_saved_party_ids(user: User) -> List[int]:
    """Get list of saved party IDs from JSON string"""
    try:
        return json.loads(user.saved_party_ids)
    except (json.JSONDecodeError, TypeError):
        return []

def set_saved_party_ids(user: User, party_ids: List[int]) -> None:
    """Set saved party IDs as JSON string"""
    user.saved_party_ids = json.dumps(party_ids)

def add_saved_party(user: User, party_id: int) -> bool:
    """Add a party to user's saved parties"""
    saved_ids = get_saved_party_ids(user)
    if party_id not in saved_ids:
        saved_ids.append(party_id)
        set_saved_party_ids(user, saved_ids)
        return True
    return False

def remove_saved_party(user: User, party_id: int) -> bool:
    """Remove a party from user's saved parties"""
    saved_ids = get_saved_party_ids(user)
    if party_id in saved_ids:
        saved_ids.remove(party_id)
        set_saved_party_ids(user, saved_ids)
        return True
    return False

class Host(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", unique=True)
    card_on_file: Optional[str] = None
    parties_thrown: int = 0
    # ... other host fields ...
    created_at: datetime = Field(default_factory=lambda: datetime.now(dt.UTC))

class PartyRequest(SQLModel, table=True):
    """Tracks party join requests with pending/accepted status"""
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", description="User requesting to join")
    party_id: int = Field(foreign_key="party.id", description="Party being requested")
    accepted: bool = Field(default=False, description="Whether the request has been accepted by host")
    created_at: datetime = Field(default_factory=lambda: datetime.now(dt.UTC))
    updated_at: datetime | None = Field(default_factory=lambda: datetime.now(dt.UTC))