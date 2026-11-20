-- Ejecutar una sola vez en la base PostgreSQL del sistema.
-- No modifica ni elimina registros existentes.
CREATE TABLE IF NOT EXISTS usuario_credencial (
    id_usuario INTEGER PRIMARY KEY REFERENCES usuario(id_usuario) ON DELETE CASCADE,
    password_hash TEXT NOT NULL,
    actualizado TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
