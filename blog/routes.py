from flask import render_template, request, flash, redirect, url_for
from blog import app
from blog.models import Entry, db
from blog.forms import EntryForm


def edit_db_entry(form, entry_id=0):
    errors = None
    if request.method == 'POST':
        if entry_id == 0:
            if form.validate_on_submit():
                entry = Entry(
                    title=form.title.data,
                    body=form.body.data,
                    is_published=form.is_published.data
                )
                db.session.add(entry)
            else:
                errors = form.errors
        else:
            entry = Entry.query.filter_by(id=entry_id).first_or_404()
            if form.validate_on_submit():
                form.populate_obj(entry)
            else:
                errors = form.errors
    if not errors:
        db.session.commit()
        flash(f'Zmodyfikowano bazę!')
        return errors


@app.route("/")
def index():
    all_posts = Entry.query.filter_by(is_published=True).order_by(Entry.pub_date.desc())
    return render_template("homepage.html", all_posts=all_posts)


@app.route("/new-post/", methods=["GET", "POST"])
def create_entry():
    form = EntryForm()
    errors = None
    if request.method == 'POST':
        edit_db_entry(form=form)
        return redirect(url_for('index'))
    return render_template("entry_form.html", form=form, errors=errors)


@app.route("/edit-post/<int:entry_id>", methods=["GET", "POST"])
def edit_entry(entry_id):
    entry = Entry.query.filter_by(id=entry_id).first_or_404()
    form = EntryForm(obj=entry)
    errors = None
    if request.method == 'POST':
        edit_db_entry(form=form, entry_id=entry_id)
        return redirect(url_for('index'))
    return render_template("entry_form.html", form=form, errors=errors)
