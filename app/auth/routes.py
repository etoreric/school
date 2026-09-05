from itsdangerous import URLSafeTimedSerializer
from flask import render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, login_required, current_user
from app.auth import auth
from app.extensions import db
from app.models.user import User
from app.forms.auth import LoginForm, ChangePasswordForm, ResetPasswordRequestForm, ResetPasswordForm


def generate_reset_token(user):
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return s.dumps({'user_id': user.id, 'hash': user.password_hash[:10]}, salt='password-reset-salt')


def verify_reset_token(token, max_age=3600):
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token, salt='password-reset-salt', max_age=max_age)
    except Exception:
        return None
    user = User.query.get(data.get('user_id'))
    if not user or user.password_hash[:10] != data.get('hash'):
        return None
    return user


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


@auth.route('/reset-password', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))
    form = ResetPasswordRequestForm()
    reset_link = None
    if form.validate_on_submit():
        query = form.email_or_username.data.strip()
        user = User.query.filter((User.email == query) | (User.username == query)).first()
        if user:
            token = generate_reset_token(user)
            reset_link = url_for('auth.reset_password', token=token, _external=True)
            flash(f'Password reset link generated for {user.username} ({user.email}).', 'success')
            return render_template('auth/reset_password_request.html', form=form, reset_link=reset_link, user=user)
        else:
            flash('No account found with that email address or username.', 'danger')
            return redirect(url_for('auth.reset_password_request'))
    return render_template('auth/reset_password_request.html', form=form)


@auth.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))
    user = verify_reset_token(token)
    if not user:
        flash('The password reset link is invalid or has expired. Please request a new one.', 'danger')
        return redirect(url_for('auth.reset_password_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset successfully! You can now log in with your new password.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form, user=user)


