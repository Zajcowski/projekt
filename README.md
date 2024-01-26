# projekt
Projekt wykonałem sam Jan Rojek: 39959
Mój projekt jest oparty o operacje CRUDowe, można je obsługiwać po przejściu do docsów, localhost:8887/docs
Strona jest połączona z bazą danych, w której znajdują się informacje o filmach, które możemy dodawać, usuwać, modyfikować i dodawać nowe.
Dostęp do zmiany w bazie danych otrzymamy po zalowaniu się poprzez przycisk authorize. Login i hasło to root/mypass123


-BAZA DANYCH
Aby aplikacja prawidłowo funkcjonowała należy wykonać poniższe kroki:
1. Wejść do phpmyadmin http://localhost:8081, root/mypass123
2. Otworzyć wiesz poleceń
3. Wkleić polecenie: CREATE DATABASE projekt;
4. Z pola po lewej stronie wybrać utworzoną bazę
5. Wkleić polecenie: 
CREATE TABLE filmy (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nazwa VARCHAR(30),
    gatunek VARCHAR(30),
    rok INT(4)
);
6. Wkleić polecenie:
INSERT INTO filmy (nazwa,gatunek,rok) VALUES
    ('Skazani na Shawshank', 'Dramat', 1994),
    ('Nietykalni', 'Biograficzny/Dramat/Komedia', 2011),
    ('Zielona mila', 'Dramat', 1999);
