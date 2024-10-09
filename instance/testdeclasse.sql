SELECT u.id, u.username, c.nomClasse 
FROM user u
LEFT JOIN classe c ON u.id_class = c.id
WHERE c.id = 0;
