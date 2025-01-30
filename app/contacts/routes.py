from flask import abort, redirect,  url_for, flash, Response, request
from jinja2 import TemplateNotFound
from app import db
from app.models import Contact, Page
from app.helpers import t_path
from app.contacts import bp
import os.path

@bp.route('/contacts', methods=['GET'])
def contact_list() -> str: 
    search: str | None = request.args.get("q")
    pg: int = int(request.args.get("page", 1))
    
    page = Page(dict(title="Contacts", template="list.html", page=pg, contacts=Contact.all(page=pg)))
    page.total = Contact.count()
   
    if search is not None:
        page.title = f"Search results for '{search}'"
        page.contacts = Contact.search(search)
        if request.headers['HX-Trigger'] == 'search':
            page.template = "rows.html"

    try:
        return page.render()
    except TemplateNotFound:
        abort(404)

@bp.route("/contacts/count")
def contacts_count() -> str:
    count: int = Contact.count()
    return f"({str(count)} total Contacts)"


@bp.route('/contacts/<int:id>', methods=['GET'])
def contact_show(id):
    c = db.get_or_404(Contact, id)
    page = Page(dict(title=f"{c.fname} {c.lname}", template="view.html", contact=c))
    return page.render()


@bp.route('/contacts/new', methods=['GET'])
def contact_new():
    page = Page(dict(title="New Contact", template="new.html", contact=Contact()))
    return page.render()


@bp.route('/contacts/new', methods=['POST'])
def contact_new_post() -> str | Response:
    c = Contact(
        name=request.form.get('name'),
        fname=request.form.get('fname'),
        lname=request.form.get('lname'),
        email=request.form.get('email'),
        phone=request.form.get('phone'),
        address=request.form.get('address')
    )
    if c.save():
        flash('Contact created successfully', 'success')
        return Response(headers={"hx-redirect": url_for('contacts.contact_list')})
    
    page = Page(dict(title="New Contact", template="new.html", contact=c))
    return page.render()


@bp.route('/contacts/<int:id>/edit', methods=['GET'])
def contact_edit(id) -> str | Response:
    c = db.get_or_404(Contact, id)
    page = Page(dict(title="Edit Contact", template="edit.html", contact=c))
    return page.render()

@bp.route('/contacts/<int:id>/edit', methods=['PUT'])
def contact_edit_put(id) -> str | Response:
    c = db.get_or_404(Contact, id)
    c.name = request.form.get('name')
    c.fname = request.form.get('fname')
    c.lname = request.form.get('lname')
    c.email = request.form.get('email')
    c.phone = request.form.get('phone')
    c.address = request.form.get('address')
    if c.save():
        flash('Contact updated successfully', 'success')
        return Response(headers={"hx-redirect": url_for('contacts.contact_list')})

    page = Page(dict(title="Edit Contact", template="edit.html", contact=c))
    return page.render()


@bp.route('/contacts/<int:id>/delete', methods=['DELETE'])
def contact_delete(id):
    c = db.get_or_404(Contact, id)
    db.session.delete(c)
    db.session.commit()
    flash('Contact deleted successfully', 'success')
    return redirect(url_for('contacts.contact_list'), code=303)

    
        
