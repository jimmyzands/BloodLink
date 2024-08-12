# -*- coding: utf-8 -*-
"""Public forms."""
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, IntegerField, SelectField, DateField
from wtforms.validators import DataRequired, NumberRange, Optional

from bloodlink.user.models import User


class LoginForm(FlaskForm):
    """Login form."""

    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        """Create instance."""
        super(LoginForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self, **kwargs):
        """Validate the form."""
        initial_validation = super(LoginForm, self).validate()
        if not initial_validation:
            return False

        self.user = User.query.filter_by(username=self.username.data).first()
        if not self.user:
            self.username.errors.append("Unknown username")
            return False

        if not self.user.check_password(self.password.data):
            self.password.errors.append("Invalid password")
            return False

        if not self.user.active:
            self.username.errors.append("User not activated")
            return False
        return True
    
class DonacionForm(FlaskForm):
    """Formulario para registrar una donación de sangre."""

    cantidad_ml = IntegerField("Cantidad (ml)", validators=[
        DataRequired(message="La cantidad es requerida"),
        NumberRange(min=50, max=500, message="La cantidad debe estar entre 50 y 500 ml")
    ])
    
    genero = SelectField("Género", choices=[('M', 'Masculino'), ('F', 'Femenino')], validators=[DataRequired()])
    
    fecha_donacion = DateField("Fecha de la donación", validators=[Optional()], format='%Y-%m-%d')

    def validate(self, **kwargs):
        """Validar el formulario."""
        initial_validation = super(DonacionForm, self).validate()
        if not initial_validation:
            return False
        
        # Aquí se puede agregar validaciones personalizadas si es necesario
        # Ejemplo: verificar si el usuario ya ha donado en un periodo de tiempo limitado
        return True
