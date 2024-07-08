DROP DATABASE IF EXISTS padrao;

CREATE DATABASE padrao;

USE padrao;

CREATE TABLE `POKEMON_INFO` (
  `id_pokedex` int NOT NULL,
  `name_pokemon` varchar(100) NOT NULL,
  PRIMARY KEY (`id_pokedex`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;