# PartyTime Backend

This repository houses the engine for a comprehensive social event platform. Since the beginning, I designed this as a production-ready system designed to handle complex interactions between users and event organizers.

### 🌎 The Scope of the System

The main feat of this project is its breadth. The API manages an extensive set of endpoints—including:
- identity and secure access middleware via Firebase
- geo-spacial search
- user saved parties, pending host approval, saved tickets
- host command centre - creating parties and managing attendees etc.
- complex user, party, host, and request models with CRUD functionality and nuanced relationships
It was built to serve a **Swift (iOS)** frontend, ensuring that every data response and error code is standardized for a seamless mobile experience.


### The Tech Stack

The stack was chosen for speed, type safety, and production reliability:

- **FastAPI:** The asynchronous core of the API.
    
- **SQLModel & SQLAlchemy:** Bridges the gap between Python and the database, making complex queries clean and fast.
    
- **Pydantic:** Enforces strict data validation for every byte entering or leaving the system.
    
- **Firebase Admin SDK:** Handles the heavy lifting of secure user authentication.
    

### Architecture & Core Logic

Rather than just "saving data," the backend operates as a state machine that enforces the rules of the platform:

- **Host/Guest Duality:** Any user can transition into a "Host" role, which instantly unlocks an entirely separate suite of management tools and permission sets without cluttering the standard user experience.
    
- **The Request Lifecycle:** To give hosts total control, the system implements a `pending -> accepted/rejected` workflow for every event. It manages the "line" at the door digitally, ensuring only vetted guests gain access.
    
- **Security as Middleware:** Identity management is deeply integrated with **Firebase**. Instead of basic checks, a dedicated security layer verifies tokens and maps them to the local database context on every single request.
    
- **Data Integrity:** The system uses a relational schema managed by **Alembic** migrations to handle the intricate foreign-key relationships between users, the parties they throw, and the requests they send.
    
 
### 🌟 Notable Features

- **Intelligent Search & Scoring:** I implemented a custom search engine that doesn't just look for words—it scores them. Matches in a party’s name are weighted more heavily than matches in the description, ensuring the most relevant results float to the top.
    
- **On-the-Fly Geospatial Logic:** Since the app deals with the physical world, the backend calculates distances between users and events using the Haversine formula directly in Python, allowing for location-based sorting even on a lightweight database setup.
    

### Future Improvements

This backend is architected to scale horizontally. The next steps for the project include:

- **Database Migration:** Moving to **PostgreSQL** to take advantage of **PostGIS** for even faster, native spatial indexing as the event density grows.
    
- **Live Updates:** Integrating **WebSockets** so hosts receive instant, push-based notifications the moment someone new requests to join their party.
    
- **Monetization:** Connecting with **Stripe** to handle host onboarding and ticketed event payments.
    
- **Deployement:** Actually putting this on a server and launching it for real!
