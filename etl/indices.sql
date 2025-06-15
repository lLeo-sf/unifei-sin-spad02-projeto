-- Busca por cidade
CREATE INDEX idx_organizations_city ON Organizations(city);

-- Busca por estado
CREATE INDEX idx_organizations_state ON Organizations(state);

-- Busca por tipo do animal
CREATE INDEX idx_animals_species ON Animals(species);

-- Busca por status (adotado, disponível, etc.)
CREATE INDEX idx_animals_status ON Animals(status);

-- Índice na tabela de Animals por organizationId
CREATE INDEX idx_animals_organizationId ON Animals(organizationId);

-- Índice na tabela Organizations por id (opcional, mas por segurança)
CREATE INDEX idx_organizations_id ON Organizations(id);

CREATE INDEX idx_statuses_name ON statuses(name);
CREATE INDEX idx_animals_organizationid ON animals(organizationid);
CREATE INDEX idx_animals_speciesid ON animals(speciesid);
CREATE INDEX idx_animals_statusid ON animals(statusid);
CREATE INDEX idx_animals_patternid ON animals(patternid);

