from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.auth import auth
from app.extensions import db
from app.models.user import User
from app.forms.auth import LoginForm, ChangePasswordForm

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))
        
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password.', 'danger')
            return redirect(url_for('auth.login'))
            
        if not user.is_active:
            flash('Your account has been deactivated.', 'danger')
            return redirect(url_for('auth.login'))
            
        login_user(user, remember=form.remember_me.data)
        db.session.commit()
        
        next_page = request.args.get('next')
        if not next_page or not next_page.startswith('/'):
            next_page = url_for('admin.dashboard')
        return redirect(next_page)
        
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))

@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if not current_user.check_password(form.old_password.data):
            flash('Incorrect current password.', 'danger')
            return redirect(url_for('auth.change_password'))
            
        current_user.set_password(form.new_password.data)
        db.session.commit()
        
        flash('Your password has been updated.', 'success')
        return redirect(url_for('admin.dashboard'))
        
    return render_template('auth/change_password.html', form=form)

