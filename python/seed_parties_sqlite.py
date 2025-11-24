import os
import sqlite3
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "database.db")

PARTIES = [
    ("Now Spanning Day Party", "all-day groove crossing midnight", 1, "[]", 40.7128, -74.0060, "Lower East Side, New York, NY", "2025-09-15 00:05:00.000000", "2026-09-16 00:05:00.000000", 150, "#allnight #groove #nyc"),
    ("Now Spanning City Crawl", "bar hop across districts", 1, "[]", 34.0522, -118.2437, "Downtown, Los Angeles, CA", "2025-09-15 06:00:00.000000", "2026-09-16 03:00:00.000000", 120, "#crawl #downtown #la"),
    ("Now Spanning Rooftop Chill", "sunset to after-hours on the roof", 1, "[]", 41.8781, -87.6298, "West Loop, Chicago, IL", "2025-09-15 18:30:00.000000", "2026-09-16 00:30:00.000000", 90, "#rooftop #afterhours #chill"),
    ("Now Spanning Brunch Beats", "brunch into late-night DJ sets", 1, "[]", 29.7604, -95.3698, "Montrose, Houston, TX", "2025-09-15 09:00:00.000000", "2026-09-16 02:00:00.000000", 110, "#brunch #beats #houston"),
    ("Now Spanning Neon Splash", "paint and glow marathon", 1, "[]", 25.7617, -80.1918, "Wynwood, Miami, FL", "2025-09-15 14:00:00.000000", "2026-09-16 04:30:00.000000", 140, "#neon #splash #miami"),
    ("Now Spanning Techno Tram", "mobile tram techno ride", 1, "[]", 52.5200, 13.4050, "Mitte, Berlin, DE", "2025-09-15 20:00:00.000000", "2026-09-16 06:00:00.000000", 160, "#tram #techno #berlin"),
    ("Now Spanning Riverfront Jam", "river views and live sets", 1, "[]", 39.9526, -75.1652, "Penn's Landing, Philadelphia, PA", "2025-09-15 16:45:00.000000", "2026-09-16 01:15:00.000000", 95, "#riverfront #jam #philly"),
    ("Now Spanning Arcade Takeover", "retro arcade until dawn", 1, "[]", 47.6062, -122.3321, "Pioneer Square, Seattle, WA", "2025-09-15 13:15:00.000000", "2026-09-16 05:45:00.000000", 80, "#arcade #retro #seattle"),
    ("Now Spanning Night Market", "food, music, and makers", 1, "[]", 37.7749, -122.4194, "Embarcadero, San Francisco, CA", "2025-09-15 17:00:00.000000", "2026-09-16 00:00:00.000000", 200, "#nightmarket #sf #streetfood"),
    ("Now Spanning Silent Forest", "silent disco in the park", 1, "[]", 51.5074, -0.1278, "Hyde Park, London, UK", "2025-09-15 19:30:00.000000", "2026-09-16 02:30:00.000000", 130, "#silentdisco #forest #london"),
]

SQL = (
    "INSERT INTO party (name, description, host_id, attendee_ids, latitude, longitude, address, start_time, end_time, max_attendees, hashtags, created_at, updated_at) "
    "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
)

now_str = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S.%f")

with sqlite3.connect(DB_PATH) as conn:
    cur = conn.cursor()
    rows = [
        (
            name,
            desc,
            host_id,
            attendee_ids,
            lat,
            lng,
            addr,
            start,
            end,
            max_att,
            tags,
            now_str,
            now_str,
        )
        for (name, desc, host_id, attendee_ids, lat, lng, addr, start, end, max_att, tags) in PARTIES
    ]
    cur.executemany(SQL, rows)
    conn.commit()
print(f"Inserted {len(PARTIES)} parties into {DB_PATH}") 
