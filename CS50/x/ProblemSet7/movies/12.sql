SELECT title
  FROM movies
  JOIN stars
    ON stars.movie_id = movies.id
  JOIN people
    ON people.id = stars.person_id
  JOIN (SELECT movies.id
  FROM movies
  JOIN stars
    ON stars.movie_id = movies.id
  JOIN people
    ON people.id = stars.person_id
 WHERE people.name = "Helena Bonham Carter")
       helen
    ON helen.id = movies.id
 WHERE people.name = "Johnny Depp";

