CREATE TABLE Podróżnicy (
    Imię varchar(16) NOT NULL,
    Nazwisko varchar(64) NOT NULL,
    Ulica varchar(64) NOT NULL,
    Nr_domu NUMBER(8,0) NOT NULL,
    Nr_mieszkania NUMBER(5,0),
    Kod_pocztowy varchar(8) NOT NULL,
    Miasto varchar(64) NOT NULL,
--    Kraj varchar(32) NOT NULL,
    Telefon varchar(16), -- Maybe not a good idea, since formatting can throw it off? I assume it gets normalized before entering it
    Email varchar(64),
    Pesel char(11) NOT NULL PRIMARY KEY
    );

CREATE TABLE Przewodnicy (
    Imię varchar(16) NOT NULL,
    Nazwisko varchar(64) NOT NULL,
    Telefon varchar(16), -- Maybe not a good idea, since formatting can throw it off? I assume it gets normalized before entering it
    Pesel char(11) NOT NULL PRIMARY KEY
    );
    
CREATE TABLE Preferencje (
    Typ varchar(10) NOT NULL,
    Id_ int NOT NULL PRIMARY KEY,
    Gmt NUMBER(2, 0),
    Rodzaj_klimatu varchar(64),
    Punkty_gti NUMBER(2, 0),
    Pesel char(11) NOT NULL, -- Foreign key
    FOREIGN KEY (Pesel) REFERENCES Podróżnicy,
    CHECK (Typ in ('strefa','klimat','zagrożenie'))
    ); -- maybe a good idea to make primary key out of combination of (Pesel, Gmt, Rodzaj_klimatu, Punkty_gti)?
    -- This way there can't be duplicate values for the same user
    -- CONSTRAINT PK_Pref PRIMARY KEY (Pesel, Gmt, Rodzaj_klimatu, Punkty_gti)
    
CREATE TABLE Ubezpieczenia (
    Numer int NOT NULL PRIMARY KEY,
    Cena NUMBER(7, 0) NOT NULL,
    Opis varchar(2048) NOT NULL,
    Data_od DATE NOT NULL,
    Data_do DATE NOT NULL,
    Pesel char(11) NOT NULL,
    FOREIGN KEY (Pesel) REFERENCES Podróżnicy
    );
    
CREATE TABLE Podróże (
    Id_podróży int NOT NULL PRIMARY KEY,
    Cena NUMBER(7, 0) NOT NULL
    );
    
CREATE TABLE Jest_w (
    Data_od DATE NOT NULL,
    Data_do DATE NOT NULL,
    Id_podróży int NOT NULL,
    FOREIGN KEY (Id_podróży) REFERENCES Podróże,
    Pesel char(11) NOT NULL,
    FOREIGN KEY (Pesel) REFERENCES Podróżnicy,
    CONSTRAINT PK_Rel PRIMARY KEY (Data_od, Data_do, Id_podróży, Pesel)
    );
    
CREATE TABLE Prowadzi (
    Pesel char(11) NOT NULL,
    Id_podróży int NOT NULL,
    FOREIGN KEY (Pesel) REFERENCES Przewodnicy,
    FOREIGN KEY (Id_podróży) REFERENCES Podróże,
    CONSTRAINT PK_Prowadzi PRIMARY KEY (Pesel, Id_podróży)
    );
    
CREATE TABLE Miasta (
    Miasto varchar(128) NOT NULL PRIMARY KEY,
    Kraj varchar(64) NOT NULL,
    Gmt int NOT NULL,
    Rodzaj_klimatu varchar(64) NOT NULL,
    Punkty_gti int NOT NULL
    );
    
CREATE TABLE Atrakcje (
    Id_atrakcji int NOT NULL PRIMARY KEY,
    Nazwa varchar(128) NOT NULL,
    Miasto varchar(128) NOT NULL, -- extract to another table?
    Opis varchar(2048) NOT NULL,
    FOREIGN KEY (Miasto) REFERENCES Miasta
    );

CREATE TABLE Podczas (
    Id_podróży int NOT NULL,
    FOREIGN KEY (Id_podróży) REFERENCES Podróże,
    Id_atrakcji int NOT NULL,
    FOREIGN KEY (Id_atrakcji) REFERENCES Atrakcje,
    CONSTRAINT PK_Podczas PRIMARY KEY (Id_podróży, Id_atrakcji)
    );

    
DROP TABLE Podróżnicy;
DROP TABLE Przewodnicy;
DROP TABLE Preferencje;
DROP TABLE Ubezpieczenia;
DROP TABLE Podróże;
DROP TABLE Jest_w;
DROP TABLE Prowadzi;
DROP TABLE Podczas;
DROP TABLE Atrakcje;
DROP TABLE Kraje;
