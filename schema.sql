DROP TABLE IF EXISTS heights;
CREATE TABLE heights (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_ip TEXT NOT NULL,
    trudeau INTEGER NOT NULL,
    user_height INTEGER NOT NULL,
    user_gender TEXT NOT NULL,
    user_location TEXT
);
