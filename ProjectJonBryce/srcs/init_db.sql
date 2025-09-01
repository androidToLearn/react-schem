
DROP TABLE IF EXISTS likes2;

CREATE TABLE
IF NOT EXISTS likes2
(
    id_user INTEGER,
    id_vacation INTEGER
);


DROP TABLE IF EXISTS roles;

CREATE TABLE
IF NOT EXISTS roles
(
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL
);

DROP TABLE IF EXISTS users111;

CREATE TABLE
IF NOT EXISTS users111
(
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    second_name TEXT NOT NULL,
    password TEXT NOT NULL,
    email TEXT NOT NULL,
    id_role INTEGER
);

DROP TABLE IF EXISTS country;

CREATE TABLE
IF NOT EXISTS country
(
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL
);

DROP TABLE IF EXISTS vacations;


CREATE TABLE
IF NOT EXISTS vacations
(
    id SERIAL PRIMARY KEY,
    id_country INTEGER NOT NULL,
    description TEXT NOT NULL,
    date_start TEXT NOT NULL,
    date_end TEXT NOT NULL,
    price INTEGER NOT NULL,
    image_name TEXT NOT NULL
);

INSERT INTO roles
    (name)
VALUES
    ('Admin');
INSERT INTO roles
    (name)
VALUES
    ('User');

INSERT INTO users111
    (name, second_name, password, email, id_role)
VALUES
    ('dan', 'shmueli', '12345', 'dan@gmail.com', 1),
    ('ישי', 'רחמוט', '1234', '1@gmail.com', 0);

INSERT INTO country
    (name)
VALUES
    ('Israel'),
    ('Australia'),
    ('USA'),
    ('Bulgaria'),
    ('France'),
    ('Brazil'),
    ('Antarctica'),
    ('China'),
    ('India'),
    ('Slovakia');

INSERT INTO vacations
    (id_country, description, date_start, date_end, price, image_name)
VALUES
    (4, 'חופשת החלומות', '2026-10-10', '2026-12-10', 10000, 'icon18.jpg'),
    (3, 'ביזנס', '2026-10-10', '2026-12-10', 4000, 'icon19.jpg'),
    (1, 'ארץ הקודש', '2026-10-10', '2026-10-29', 3000, 'icon21.jpg'),
    (10, 'נופים מרהיבים בסלובקיה', '2026-09-10', '2026-10-10', 5000, 'icon22.jpg'),
    (5, 'מסע בעיקבות השורשים הצרפתיים', '2026-10-01', '2026-10-10', 6000, 'icon23.jpg'),
    (9, 'מסע להודו', '2026-10-01', '2026-10-20', 4000, 'icon24.jpg'),
    (8, 'טיול למדינה הגדולה בעולם', '2026-09-10', '2026-09-29', 8000, 'icon26.jpg'),
    (3, 'חופשה על הים', '2026-11-01', '2026-11-09', 9000, 'back1_2.jpg'),
    (4, 'טיול עם נוף הררי', '2026-10-10', '2026-12-10', 9000, 'icon21.jpg'),
    (7, 'הכי קר', '2026-07-10', '2026-12-10', 5500, 'icon21.jpg'),
    (4, 'צאו לגלות בעלי חיים מרהיבים וטבע פראי', '2026-10-10', '2026-12-10', 100, 'icon21.jpg'),
    (4, 'חופשת אקסטרים', '2026-10-10', '2026-11-10', 200, 'icon26.jpg');
