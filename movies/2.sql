SELECT birth
FROM people
WHERE id =
(
    SELECT id
    WHERE name = 'Emma Stone'
);
