DROP TABLE IF EXISTS trudeau;
CREATE TABLE trudeau (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_ip TEXT NOT NULL,
    height INTEGER NOT NULL,
    user_height INTEGER NOT NULL,
    user_gender TEXT NOT NULL,
    user_location TEXT
);

DROP TABLE IF EXISTS obama;
CREATE TABLE obama (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_ip TEXT NOT NULL,
    height INTEGER NOT NULL,
    user_height INTEGER NOT NULL,
    user_gender TEXT NOT NULL,
    user_location TEXT
);

DROP TABLE IF EXISTS merkel;
CREATE TABLE merkel (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_ip TEXT NOT NULL,
    height INTEGER NOT NULL,
    user_height INTEGER NOT NULL,
    user_gender TEXT NOT NULL,
    user_location TEXT
);
