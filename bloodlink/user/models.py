# -*- coding: utf-8 -*-
"""User models."""
import datetime as dt

from flask_login import UserMixin
from sqlalchemy.ext.hybrid import hybrid_property

from bloodlink.database import Column, PkModel, db, reference_col, relationship
from bloodlink.extensions import bcrypt


class Role(PkModel):
    """Un rol asignado a un usuario."""

    __tablename__ = "roles"
    name = Column(db.String(80), unique=True, nullable=False)
    user_id = reference_col("users", nullable=True)
    user = relationship("User", backref="roles")

    def __repr__(self):
        """Representación única de la instancia."""
        return f"<Role({self.name})>"


class User(UserMixin, PkModel):
    """Un usuario de la aplicación."""

    __tablename__ = "users"
    username = Column(db.String(80), unique=True, nullable=False)
    email = Column(db.String(80), unique=True, nullable=False)
    _password = Column("password", db.LargeBinary(128), nullable=True)
    created_at = Column(
        db.DateTime, nullable=False, default=dt.datetime.now(dt.timezone.utc)
    )
    first_name = Column(db.String(30), nullable=True)
    last_name = Column(db.String(30), nullable=True)
    active = Column(db.Boolean(), default=False)
    is_admin = Column(db.Boolean(), default=False)

    @hybrid_property
    def password(self):
        """Contraseña encriptada."""
        return self._password

    @password.setter
    def password(self, value):
        """Establecer la contraseña."""
        self._password = bcrypt.generate_password_hash(value)

    def check_password(self, value):
        """Verificar la contraseña."""
        return bcrypt.check_password_hash(self._password, value)

    @property
    def full_name(self):
        """Nombre completo del usuario."""
        return f"{self.first_name} {self.last_name}"

    def __repr__(self):
        """Representación única de la instancia."""
        return f"<User({self.username!r})>"


class Donante(PkModel):
    """Modelo que representa a un donante en el sistema."""

    __tablename__ = 'donantes'
    
    # Género del donante
    genero = Column(db.String(10), nullable=False)
    
    # Fecha de la última donación
    ultima_donacion = Column(db.Date, nullable=True)
    
    # Disponibilidad del donante para donar nuevamente
    disponibilidad = Column(db.Boolean, default=True, nullable=False)
    
    # Relación con las donaciones realizadas
    donaciones = relationship('Donacion', backref='donante', lazy=True)

    def __repr__(self):
        """Representación única de la instancia."""
        return f"<Donante(id={self.id}, genero={self.genero})>"


class Donacion(PkModel):
    """Modelo que registra cada donación de sangre."""

    __tablename__ = 'donaciones'
    
    # Clave foránea al donante que realizó la donación
    donante_id = reference_col('donantes', nullable=False)
    
    # Fecha de la donación
    fecha_donacion = Column(db.Date, nullable=False)
    
    # Cantidad de sangre donada en mililitros
    cantidad_ml = Column(db.Integer, nullable=False)

    def __repr__(self):
        """Representación única de la instancia."""
        return f"<Donacion(id={self.id}, donante_id={self.donante_id}, cantidad_ml={self.cantidad_ml})>"