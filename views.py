from __init__ import *
from forms.forms import *
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date
# from fpdf import FPDF, HTMLMixin 

def index():
    return make_response(render_template('index.html'))

def login():
    form = login_form()
    if form.validate_on_submit():
        try:
            user = Users.query.filter_by(email=form.email.data).first()
            if user:
                if check_password_hash(user.pwd, form.pwd.data):
                    user.id = user.email
                    login_user(user)
                    if request.args.get('next'):
                        return redirect(request.args.get('next'))
                    else:
                        return redirect(url_for('dashboard'))
                else:
                    flash("Invalid Username or password!", "danger")
            else:
                flash("User does not exist!", "danger")
        except Exception as e:
            flash(e, "danger")
    return make_response(render_template('auth.html', form = form))
def register():
    form = register_form()
    if form.validate_on_submit():
        try:
            email = form.email.data
            pwd = form.pwd.data
            username = form.username.data
            
            newuser = Users(
                username=username,
                email=email,
                pwd=generate_password_hash(pwd),
            )
    
            db.session.add(newuser)
            db.session.commit()
            flash(f"Account Succesfully created", "success")
            return redirect(url_for("login"))

        except Exception as e:
            flash(e, "danger")
    return make_response(render_template('auth.html', form = form))

@login_required
def dashboard():
    print(current_user.email)
    return make_response(render_template('admin/ndc/index.html'))


@login_required
def settings():
    return render_template('admin/ndc/settings.html')
@login_required
def logs():
    return render_template('admin/ndc/logs.html')
@login_required
def new():
    return render_template('admin/ndc/new.html')

@login_required
def dc_white_space():
    return render_template('admin/ndc/dc_white_space.html')
@login_required
def comments():
    midnight = datetime.combine(date.today(), datetime.min.time())
    generators = Generators.query.filter(Generators.date <= datetime.now()).filter(Generators.date >= midnight).first()
    whitespace = WhiteSpace.query.filter(WhiteSpace.date <= datetime.now()).filter(WhiteSpace.date >= midnight).first()
    power_rooms =  PowerRooms.query.filter(PowerRooms.date <= datetime.now()).filter(PowerRooms.date >= midnight).first()

    
    if not generators:
        flash('No generators information available today', 'error')
        return redirect(url_for('generator'))
    if not whitespace:
        flash('No DC white space information available today', 'error')
        return redirect(url_for('dc_white_space'))
    if not power_rooms:
        flash('No power room information available today', 'error')
        return redirect(url_for('power_rooms'))
    
    t,h = 0,0
    for key, value in power_rooms.data.items():
        t += int(value.get('temperature'))
        h += int(value.get('humidity'))
    avg_tempPw = t/(len(power_rooms.data))
    avg_humPw = h/(len(power_rooms.data))
    
    today = date.today()
    
    return render_template('admin/ndc/comments.html', 
                           generators=generators, 
                           whitespace = whitespace, 
                           power_rooms = power_rooms,
                           avg_tempPw = avg_tempPw, 
                           avg_humPw = avg_humPw, today = today)
@login_required
def power_rooms():
    return render_template('admin/ndc/power_rooms.html')
@login_required
def generators():
    return render_template('admin/ndc/generators.html')

@login_required
def urlf(urls):
    return render_template(f'admin/pages/{urls}.html')

def generate_pdf():
    data = request.json
    date = datetime.now()
    rendered_template = render_template('admin/ndc/generate_pdf-min.html', data = data,date = date.strftime('%c'))

    return make_response(rendered_template)


@login_required
def containment_data():
    data = request.json
    try:
        new = WhiteSpace(
            data = data,
            user = current_user.id,
            
        )
        db.session.add(new)
        db.session.commit()
        return make_response(jsonify({'success': True, 'message': 'Data saved successfully', 'data': data}))
    except Exception as e:
        return make_response(jsonify({'success': False, 'message': 'Error saving your data'}))
@login_required
def generators_data():
    data = request.json
    try:
        new = Generators(
            data = data,
            user = current_user.id,
            
        )
        db.session.add(new)
        db.session.commit()
        return make_response(jsonify({'success': True, 'message': 'Data saved successfully', 'data': data}))
    except Exception as e:
        return make_response(jsonify({'success': False, 'message': 'Error saving your data'}))
    
@login_required
def power_rooms_data():
    data = request.json
    try:
        new = PowerRooms(
            data = data,
            user = current_user.id,
            
        )
        db.session.add(new)
        db.session.commit()
        return make_response(jsonify({'success': True, 'message': 'Data saved successfully', 'data': data}))
    except Exception as e:
        return make_response(jsonify({'success': False, 'message': 'Error saving your data'}))

@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))