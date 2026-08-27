-- Script Criação Visits Table --

/* CABEÇALHO

    - Projeto: Portal Wifi
    - Autor: Eduardo Carvalho
    - Data: 17/08
    - Objetivo: Criar a tabela visit de forma reexecutável e limpa,
    garantindo que funcionará de forma impecável com
    o backend do projeto.

*/

-- SCRIPT --

-- Mostra todas as bases de dados
SHOW DATABASES;

-- Seleciona a base de dados do portal_wifi
USE portal_wifi;

-- Cria tabela de visits
CREATE TABLE IF NOT EXISTS visit(
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    ssid VARCHAR(100) NOT NULL,
    mac VARCHAR(17) NOT NULL,
    tos_accepted_at DATETIME NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    metadata JSON,

    lead_id INT UNSIGNED NOT NULL,

    CONSTRAINT fk_visit_lead
    FOREIGN KEY (lead_id) REFERENCES leads(id)
);

-- MENSAGEM FINAL
SELECT 'TABELA CRIADA/EXISTENTE';

-- FIM SCRIPT --
