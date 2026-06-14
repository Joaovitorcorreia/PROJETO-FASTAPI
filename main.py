from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import Usuario
from schemas import UsuarioCreate, UsuarioResponse
 # para rodar o código: uvicorn main:app --reload

Base.metadata.create_all(bind=engine)

app = FastAPI()

#definir o banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#criar usuario
@app.post("/usuarios/", response_model=UsuarioResponse)
def criar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    novo_usuario = Usuario(nome=usuario.nome, email=usuario.email)
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    return novo_usuario

#listar usuarios
@app.get("/usuarios/", response_model=list[UsuarioResponse])
def listar_usuarios(db: Session = Depends(get_db)):
    usuarios = db.query(Usuario).all()
    return usuarios

#alterar usuario
@app.put("/usuarios/{usuario_id}", response_model=UsuarioResponse)
def alterar_usuario(usuario_id: int, usuario: UsuarioCreate, db: Session = Depends(get_db)):
    usuario_db = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario_db:
        return {"error": "Usuário não encontrado"}
    usuario_db.nome = usuario.nome
    usuario_db.email = usuario.email
    db.commit()
    db.refresh(usuario_db)
    return usuario_db

#deletar usuario
@app.delete("/usuarios/{usuario_id}")
def deletar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario_db = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario_db:
        return {"error": "Usuário não encontrado"}
    db.delete(usuario_db)
    db.commit()
    return {"message": "Usuário deletado com sucesso"}