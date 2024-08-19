# -*- coding: utf-8 -*-
"""User forms."""
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, RadioField, SelectField, TelField, EmailField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length

from .models import User

class RegisterForm(FlaskForm):
    """Register form."""

    username = StringField(
        "Username", validators=[DataRequired(), Length(min=3, max=25)]
    )
    email = StringField(
        "Email", validators=[DataRequired(), Email(), Length(min=6, max=40)]
    )
    password = PasswordField(
        "Password", validators=[DataRequired(), Length(min=6, max=40)]
    )
    confirm = PasswordField(
        "Verify password",
        [DataRequired(), EqualTo("password", message="Passwords must match")],
    )

    def __init__(self, *args, **kwargs):
        """Create instance."""
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self, **kwargs):
        """Validate the form."""
        initial_validation = super(RegisterForm, self).validate()
        if not initial_validation:
            return False
        user = User.query.filter_by(username=self.username.data).first()
        if user:
            self.username.errors.append("Username already registered")
            return False
        user = User.query.filter_by(email=self.email.data).first()
        if user:
            self.email.errors.append("Email already registered")
            return False
        return True
    
class DonateForm(FlaskForm):
    """Donate form."""
    
    cedula = StringField(
        "Cédula", validators=[DataRequired(), Length(min=11, max=11)]
    )
    nombre = StringField(
        "Nombre", validators=[DataRequired(), Length(min=3, max=50)]
    )
    direccion = StringField(
        "Dirección", validators=[DataRequired(), Length(min=3, max=250)]
    )
    sexo = RadioField(
        "Sexo", validators=[DataRequired()], choices=[('F', 'Femenino'), ('M', 'Masculino')]
    )
    orientacion = SelectField(
        "Orientación", validators=[DataRequired()], choices=[
            ('Hetero', 'Heterosexual'),
            ('Homo', 'Homosexual'),
            ('Trans', 'Transgénero'),
        ]
    )
    donacion_para = StringField(
        "Donación para", validators=[DataRequired(), Length(min=3, max=50)]
    )
    telefono = TelField(
        "Teléfono", validators=[DataRequired(), Length(min=9, max=10)]
    )
    email = EmailField(
        "Email", validators=[DataRequired(), Length(min=3, max=100)]
    )
    enfermedad_donante = TextAreaField("Enfermedad del donante", validators=[DataRequired()])
    grupo_sanguineo = SelectField("Grupo sanguíneo", validators=[DataRequired()], choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-')])
    
    def create_radio_field(label):
        return RadioField(label, validators=[DataRequired()], choices=[('S', 'Sí'), ('N', 'No')])

    resfriado = create_radio_field("Resfriado")
    vacuna = create_radio_field("Vacuna")
    cancer = create_radio_field("Cáncer")
    tatuaje = create_radio_field("Tatuaje")
    rehabilitacion = create_radio_field("Rehabilitación")
    cirugia = create_radio_field("Cirugía")