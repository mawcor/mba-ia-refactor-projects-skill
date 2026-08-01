class UsuarioModel:
    @staticmethod
    def get_todos_usuarios(db):
        cursor = db.cursor()
        cursor.execute("SELECT * FROM usuarios")
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

    @staticmethod
    def get_usuario_por_id(db, id):
        cursor = db.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE id = ?", (id,))
        row = cursor.fetchone()
        return dict(row) if row else None

    @staticmethod
    def login_usuario(db, email, senha):
        cursor = db.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE email = ? AND senha = ?", (email, senha))
        row = cursor.fetchone()
        if row:
            return {
                "id": row["id"],
                "nome": row["nome"],
                "email": row["email"],
                "tipo": row["tipo"]
            }
        return None

    @staticmethod
    def criar_usuario(db, nome, email, senha, tipo="cliente"):
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO usuarios (nome, email, senha, tipo) VALUES (?, ?, ?, ?)",
            (nome, email, senha, tipo)
        )
        db.commit()
        return cursor.lastrowid
