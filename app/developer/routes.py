import secrets
import hashlib
from datetime import datetime
from flask import render_template, redirect, url_for, flash, request, session, abort
from flask_login import login_required, current_user, login_user
from app.developer import developer
from app.extensions import db
from app.models.school import School, SchoolInvite
from app.models.user import User
from app.forms.developer import SchoolOnboardingForm

def super_admin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_super_administrator:
            flash('Developer access required.', 'danger')
            return redirect(url_for('admin.dashboard'))
        return f(*args, **kwargs)
    return decorated_function

@developer.route('/')
@developer.route('/dashboard')
@login_required
@super_admin_required
def dashboard():
    schools = School.query.order_by(School.created_at.desc()).all()
    invites = SchoolInvite.query.filter_by(used_at=None).order_by(SchoolInvite.created_at.desc()).all()
    generated_link = session.pop('generated_link', None)
    return render_template('developer/dashboard.html', schools=schools, invites=invites, generated_link=generated_link)

@developer.route('/invite', methods=['POST'])
@login_required
@super_admin_required
def create_invite():
    token = secrets.token_urlsafe(32)
    token_hash = hashlib.sha256(token.encode()).hexdigest()
    invite = SchoolInvite(token_hash=token_hash, created_by_id=current_user.id)
    db.session.add(invite)
    db.session.commit()
    
    generated_link = url_for('developer.onboard', token=token, _external=True)
    session['generated_link'] = generated_link
    flash('New school invitation link created.', 'success')
    return redirect(url_for('developer.dashboard'))

@developer.route('/schools/<int:school_id>/administrators/<int:user_id>/toggle', methods=['POST'])
@login_required
@super_admin_required
def toggle_administrator(school_id, user_id):
    admin_user = User.query.filter_by(id=user_id, school_id=school_id).first_or_404()
    if admin_user.id == current_user.id:
        flash('You cannot deactivate your own developer administrator account.', 'danger')
    else:
        admin_user.is_active = not admin_user.is_active
        db.session.commit()
        state = 'activated' if admin_user.is_active else 'deactivated'
        flash(f'Administrator {admin_user.username} {state}.', 'success')
    return redirect(url_for('developer.dashboard'))

@developer.route('/onboard/<token>', methods=['GET', 'POST'])
def onboard(token):
    token_hash = hashlib.sha256(token.encode()).hexdigest()
    invite = SchoolInvite.query.filter_by(token_hash=token_hash, used_at=None).first_or_404()
    
    form = SchoolOnboardingForm()
    if form.validate_on_submit():
        existing_user = User.query.filter((User.username == form.username.data) | (User.email == form.email.data)).first()
        if existing_user:
            flash('A user with that username or email already exists.', 'danger')
            return render_template('developer/onboard.html', form=form)
            
        school = School(name=form.school_name.data)
        db.session.add(school)
        db.session.flush()
        
        admin_user = User(
            username=form.username.data,
            email=form.email.data,
            is_admin=True,
            is_active=True,
            school_id=school.id
        )
        admin_user.set_password(form.password.data)
        db.session.add(admin_user)
        
        invite.used_at = datetime.utcnow()
        db.session.commit()
        
        login_user(admin_user)
        flash(f'Welcome! School {school.name} created successfully.', 'success')
        return redirect(url_for('admin.dashboard'))
        
    return render_template('developer/onboard.html', form=form)
