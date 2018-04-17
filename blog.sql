CREATE TABLE authors (
  id SERIAL NOT NULL PRIMARY KEY,
  name VARCHAR(70)
);

CREATE TABLE post (
  id SERIAL NOT NULL PRIMARY KEY,
  title VARCHAR(70),
  slug VARCHAR(70),
  body VARCHAR,
  author_id INTEGER REFERENCES authors (id)
);

CREATE TABLE comments (
  id SERIAL NOT NULL PRIMARY KEY,
  title VARCHAR(70),
  body VARCHAR,
  post_id INTEGER REFERENCES post (id),
  author_id INTEGER REFERENCES authors (id)
);