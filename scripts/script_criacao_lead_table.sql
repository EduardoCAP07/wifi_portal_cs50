-- Script Criação Lead Table --

/* CABEÇALHO 

	- Projeto: Porta Wifi CS50
	- Autor: Eduardo Carvalho
    - Data: 11/08/26
    - Objetivo: Criar a tabela lead de forma reexecutável e limpa,
    garantindo que funcionará de forma impecável com
    o backend do projeto.
    
*/

-- SCRIPT --

-- Mostra todas as bases de dados
SHOW DATABASES;

-- Seleciona a base de dados do portal_wifi
USE portal_wifi;

-- Cria tabela de leads
CREATE TABLE IF NOT EXISTS leads(
	id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(11) NOT NULL,
    ssid VARCHAR(100) NOT NULL,
    mac VARCHAR(17) NOT NULL,
    tos_accepted_at DATETIME NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    metadata JSON,
    
    user_id INT UNSIGNED NOT NULL,
    
    constraint fk_lead_user
    FOREIGN KEY (user_id) REFERENCES user_account(id)
);


-- MENSAGEM FINAL
SELECT 'TABELA CRIADA/EXISTENTE';

-- FIM SCRIPT --



