# e_notice_board/routes/modify.py
@admin_bp.route('/monitors/add', methods=['GET', 'POST'])
@login_required
def add_monitor():
    if request.method == 'POST':
        name = request.form.get('name')
        location = request.form.get('location')
        screen_size = request.form.get('screen_size')

        if not name or not location or not screen_size:
            flash('All fields are required!', 'danger')
            return redirect(url_for('admin.add_monitor'))

        new_monitor = Monitor(
            name=name,
            location=location,
            screen_size=screen_size,
            is_active=True
        )
        db.session.add(new_monitor)
        db.session.commit()

        flash(f'Monitor "{name}" added successfully!', 'success')
        return redirect(url_for('admin.list_monitors'))

    return render_template('admin/add_monitor.html')

@admin_bp.route('/monitors/delete/<int:monitor_id>', methods=['POST'])
@login_required
def delete_monitor(monitor_id):
    monitor = Monitor.query.get_or_404(monitor_id)
    db.session.delete(monitor)
    db.session.commit()

    flash(f'Monitor "{monitor.name}" deleted successfully!', 'success')
    return redirect(url_for('admin.list_monitors'))

@admin_bp.route('/monitors')
@login_required
def list_monitors():
    monitors = Monitor.query.all()
    return render_template('admin/list_monitors.html', monitors=monitors)

# models.py
notice_monitor = db.Table('notice_monitor',
    db.Column('notice_id', db.Integer, db.ForeignKey('notice.id')),
    db.Column('monitor_id', db.Integer, db.ForeignKey('monitor.id'))
)

class Notice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    monitors = db.relationship('Monitor', secondary=notice_monitor,
                               backref=db.backref('assignments', lazy='dynamic'))

class Monitor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    location = db.Column(db.String(50))
    is_active = db.Column(db.Boolean, default=True)
    # assignments comes from Notice relationship
