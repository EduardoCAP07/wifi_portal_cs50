-- Script Criação User Table --

/* CABEÇALHO

	- Projeto: Portal Wifi CS50
	- Autor: Eduardo Carvalho
    - Data: 11/08/26
    - Objetivo: Criar a tabela user_account de forma reexecutável e limpa,
    garantindo que funcionará de forma impecável com
    o backend do projeto.

*/

-- SCRIPT --

-- Mostra todas as bases de dados
SHOW DATABASES;

-- Seleciona a base de dados do portal_wifi
USE portal_wifi;

-- Cria tabela de user account
CREATE TABLE IF NOT EXISTS user_account(
	id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    phone VARCHAR(14) NOT NULL UNIQUE,
    tos_accepted_at DATETIME NOT NULL,
    is_active BOOL NOT NULL,
    session_version INT UNSIGNED DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    metadata JSON


);


-- MENSAGEM FINAL
SELECT 'TABELA CRIADA/EXISTENTE';

-- FIM SCRIPT --
