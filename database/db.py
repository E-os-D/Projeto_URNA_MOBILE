import sqlite3

conn = sqlite3.connect("urna_eletronica.db")
cursor = conn.cursor()

# # Criação das tabelas
# cursor.execute("""
# CREATE TABLE IF NOT EXISTS Partidos (
#     id_partido INTEGER PRIMARY KEY,
#     nome TEXT,
#     sigla VARCHAR(10)
# )
# """)

# cursor.execute("""
# CREATE TABLE IF NOT EXISTS Governador (
#     id_número_governador INTEGER PRIMARY KEY,
#     nome TEXT,
#     foto BLOB,
#     id_partido INTEGER,
#     descrição TEXT,
#     FOREIGN KEY (id_partido) REFERENCES Partidos(id_partido)
# )
# """)

# cursor.execute("""
# CREATE TABLE IF NOT EXISTS Presidente (
#     id_número_presidente INTEGER PRIMARY KEY,
#     nome TEXT,
#     foto BLOB,
#     id_partido INTEGER,
#     descrição TEXT,
#     FOREIGN KEY (id_partido) REFERENCES Partidos(id_partido)
# )
# """)

# cursor.execute("""
# CREATE TABLE IF NOT EXISTS Prefeito (
#     id_número_prefeito INTEGER PRIMARY KEY,
#     nome TEXT,
#     foto BLOB,
#     id_partido INTEGER,
#     descrição TEXT,
#     FOREIGN KEY (id_partido) REFERENCES Partidos(id_partido)
# )
# """)

# cursor.execute("""
# CREATE TABLE IF NOT EXISTS Votação_governador (
#     idvotos INTEGER PRIMARY KEY AUTOINCREMENT,
#     id_número_governador INTEGER,
#     FOREIGN KEY (id_número_governador) REFERENCES Governador(id_número_governador)
# )
# """)

# cursor.execute("""
# CREATE TABLE IF NOT EXISTS Votação_presidente (
#     idvotos INTEGER PRIMARY KEY AUTOINCREMENT,
#     id_número_presidente INTEGER,
#     FOREIGN KEY (id_número_presidente) REFERENCES Presidente(id_número_presidente)
# )
# """)

# cursor.execute("""
# CREATE TABLE IF NOT EXISTS Votação_prefeito (
#     idvotos INTEGER PRIMARY KEY AUTOINCREMENT,
#     id_número_prefeito INTEGER,
#     FOREIGN KEY (id_número_prefeito) REFERENCES Prefeito(id_número_prefeito)
# )
# """)

# cursor.execute("""
# CREATE TABLE IF NOT EXISTS Admin (
#     idadmin INTEGER PRIMARY KEY AUTOINCREMENT,
#     nome TEXT,
#     email VARCHAR(100),
#     senha TEXT
# )
# """)

# cursor.execute("""
# CREATE TABLE IF NOT EXISTS Eleitor (
#     idRG VARCHAR(20) PRIMARY KEY,
#     nome TEXT
# )
# """)

# # Salva e fecha
# conn.commit()
# conn.close()

# print("Banco de dados criado com sucesso!")