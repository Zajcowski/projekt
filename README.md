# projekt

Aby aplikacja prawidłowo funkcjonowała należy wykonać poniższe kroki:
1. Wejść do phpmyadmin http://localhost:8081, root/mypass123
2. Otworzyć wiesz poleceń
3. Wkleić polecenie: CREATE DATABASE IF NOT EXISTS samochody;
4. Z pola po lewej stronie wybrać utworzoną bazę
5. Wkleić polecenie: 
CREATE TABLE IF NOT EXISTS marki (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nazwa VARCHAR(50)
);
6. Wkleić polecenie lub zrobić to ręcznie przez interfejs aplikacji:
INSERT INTO marki (nazwa) VALUES
    ('Vw'),
    ('Nissan'),
    ('Ford');



jinja2