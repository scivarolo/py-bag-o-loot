PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS 'Toys';
DROP TABLE IF EXISTS 'Children';

CREATE TABLE 'Children' (
  'id' INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  'name' TEXT NOT NULL
);

INSERT INTO Children values(null, 'Elyse');
INSERT INTO Children values(null, 'Nolan');
INSERT INTO Children values(null, 'Joe');

CREATE TABLE 'Toys' (
  'id' INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  'toy_name' TEXT NOT NULL,
  'child_id' INTEGER NOT NULL,
  'delivered' INTEGER NOT NULL DEFAULT 0 CHECK (Delivered BETWEEN 0 AND 1),
  FOREIGN KEY('child_id')
  REFERENCES 'Children'('id')
  ON DELETE CASCADE
);

INSERT INTO Toys values(null, 'racecar', 3, 0);
INSERT INTO Toys values(null, 'doll', 2, 0);
INSERT INTO Toys values(null, 'VR Headset', 1, 1);
INSERT INTO Toys values(null, 'Bag o Chips', 2, 0);