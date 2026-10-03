from app.models.usuario import TokenRevocados

def token_revocado(jti, db): 
    resultado = db.query(TokenRevocados.jti).filter_by(jti=jti).first()

    if resultado is not None:
        return True

    else:
        return False


def revocar_token(jti, db):
    try:
        jti_anulado = TokenRevocados(
            jti = jti
        )

        db.add(jti_anulado)
        db.commit()

        return True

    except Exception:
        db.rollback()
        raise
