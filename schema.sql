DROP TABLE IF EXISTS responses;
CREATE TABLE responses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_ip TEXT NOT NULL,
    trudeau FLOAT NOT NULL,
    harper FLOAT NOT NULL,
    obama FLOAT NOT NULL,
    pizza TEXT NOT NULL,
    drink TEXT NOT NULL,
    user_height FLOAT NOT NULL,
    user_shoe INTEGER NOT NULL,
    user_gender TEXT NOT NULL
);

DROP TABLE IF EXISTS heights;
CREATE TABLE heights (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_ip TEXT NOT NULL,
    trudeau INTEGER NOT NULL,
    obama INTEGER NOT NULL,
    user_height FLOAT NOT NULL,
    user_gender TEXT NOT NULL,
    user_location TEXT
);
