# -*- coding: utf-8 -*-
"""Sección pública, incluyendo la página principal y el registro."""
from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import login_required, login_user, logout_user

from bloodlink.extensions import login_manager
from bloodlink.public.forms import LoginForm
from bloodlink.user.forms import RegisterForm, DonateForm
from bloodlink.user.models import User, Donor
from bloodlink.utils import flash_errors

blueprint = Blueprint("public", __name__, static_folder="../static")


@login_manager.user_loader
def load_user(user_id):
    """Cargar usuario por ID."""
    return User.get_by_id(int(user_id))


@blueprint.route("/", methods=["GET", "POST"])
def home():
    """Página principal."""
    form = LoginForm(request.form)
    current_app.logger.info("¡Hola desde la página principal!")
    # Manejar inicio de sesión
    if request.method == "POST":
        if form.validate_on_submit():
            login_user(form.user)
            flash("Has iniciado sesión.", "success")
            redirect_url = request.args.get("next") or url_for("user.members")
            return redirect(redirect_url)
        else:
            flash_errors(form)
    return render_template("public/home.html", form=form)


@blueprint.route("/logout/")
@login_required
def logout():
    """Cerrar sesión."""
    logout_user()
    flash("Has cerrado sesión.", "info")
    return redirect(url_for("public.home"))


@blueprint.route("/register/", methods=["GET", "POST"])
def register():
    """Registrar nuevo usuario."""
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        User.create(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
            active=True,
        )
        flash("Gracias por registrarte. Ahora puedes iniciar sesión.", "success")
        return redirect(url_for("public.home"))
    else:
        flash_errors(form)
    return render_template("public/register.html", form=form)


@blueprint.route("/about/")
def about():
    """Página Acerca de."""
    form = LoginForm(request.form)
    return render_template("public/about.html", form=form)


@blueprint.route('/donate', methods=['GET', 'POST'])
@login_required
def donate():
    """Donar sangre."""
    form = DonateForm()
    if form.validate_on_submit():
        Donor.create(
            id_card=form.cedula.data,
            name=form.nombre.data,
            address=form.direccion.data,
            gender=form.sexo.data,
            orientation=form.orientacion.data,
            donation_for=form.donacion_para.data,
            phone=form.telefono.data,
            email=form.email.data,
            illness=form.enfermedad_donante.data,
            blood_group=form.grupo_sanguineo.data,
            cold=form.resfriado.data == 'S',
            vaccine=form.vacuna.data == 'S',
            cancer=form.cancer.data == 'S',
            tattoo=form.tatuaje.data == 'S',
            rehabilitation=form.rehabilitacion.data == 'S',
            surgery=form.cirugia.data == 'S'
        )
        flash('¡Donación registrada con éxito!', 'success')
        return redirect(url_for('public.home'))
    return render_template('public/donate.html', form=form)


@blueprint.route("/solicitud/")
def solicitud():
    """Página de Solicitud."""
    form = LoginForm(request.form)
    return render_template("public/solicitud.html", form=form)


@blueprint.route("/info/")
def info():
    """Página de Información."""
    form = LoginForm(request.form)
    return render_template("public/info.html", form=form)
