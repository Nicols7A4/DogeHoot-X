CREATE TABLE IF NOT EXISTS cuestionario (
  id_cuestionario     INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  titulo              VARCHAR(160) NOT NULL,
  descripcion         TEXT NULL,
  es_publico          TINYINT(1) NOT NULL DEFAULT 0,
  id_propietario      INT NOT NULL,   -- MISMO TIPO QUE usuario.id_usuario
  fecha_creacion      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  fecha_actualizacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

  CONSTRAINT fk_c_prop FOREIGN KEY (id_propietario)
    REFERENCES usuario(id_usuario)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,

  KEY idx_propietario (id_propietario),
  KEY idx_publico (es_publico),
  KEY idx_fecha (fecha_creacion)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;