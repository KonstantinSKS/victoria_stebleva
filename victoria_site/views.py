from flask import render_template, request, redirect, url_for  # flash
from werkzeug.utils import secure_filename
import os

from . import app, db
from .models import Project, Tag, Blog
from .forms import ProjectForm, BLogForm

DESCRIPTION = (
    'My name is Victoria Stebleva,\n'
    'I am an international published illustrator and author-illustrator currently living in Serbia.\n'
    'My portfolio includes non-fiction, middle-grade, activity books, graphic novel, wimmelbuch,\n'
    'editorial illustrations and even more.\n'
    'I am fond of motorbike traveling, nonfiction literature, rock music, and pets.\n'
    'Select clients include: Scholastic, Penguin Random House, Magic Cat, Usborne, Highlights,\n'
    'Yoyo Books, Wonderbly.'
)


@app.route('/')
def index_view():
    tag_filter = request.args.get('tag')
    if tag_filter and tag_filter != 'all':
        projects = Project.query.join(Project.tags).filter(
            Tag.name == tag_filter).all()
    else:
        projects = Project.query.all()
    tags = Tag.query.all()
    return render_template('index.html',
                           projects=projects,
                           tags=tags,
                           current_tag=tag_filter)


@app.route('/projects/<int:id>')
def project_view(id):
    project = Project.query.get_or_404(id)
    return render_template('project.html', project=project)


@app.route('/about')
def about_view():
    user_info = {
        "name": "Victoria Stebleva",
        "description": DESCRIPTION,  # Вынести в админку
        "image_path": "/static/img/avatar885138196.jpg",
        "email": "vikastebleva@gmail.com",
        "instagram": "https://www.instagram.com/vika_stebleva/",
        "behance": "https://www.behance.net/vika_stebleva"
    }
    return render_template('about.html', user=user_info)


# ДОРАБОТАТЬ БЛОГИ!!!!! название вью, шаблоны!!!


@app.route('/blogs')
def all_blogs_view():
    blogs = Blog.query.all()
    return render_template('all_blogs.html', blogs=blogs)


@app.route('/blogs/<int:id>')
def blog_view(id):
    blog = Blog.query.get_or_404(id)
    return render_template('blog.html', blog=blog)


@app.route('/add_blog', methods=['GET', 'POST'])
def add_blog():
    form = BLogForm()
    if form.validate_on_submit():
        filename = None
        if form.image.data:
            # filename = secure_filename(form.image.data.filename)
            # filename = os.path.join('static/media/', secure_filename(form.image.data.filename))  # пока оставить
            filename = secure_filename(form.image.data.filename)
            form.image.data.save(os.path.join(
             os.path.join(app.static_folder,
                          app.config['UPLOAD_FOLDER']), filename))
            # filepath = os.path.join('static/media/', filename)

        # file = form.image.data
        # filename = secure_filename(file.filename)
        # file.save(os.path.join(
        #     os.path.join(app.static_folder,
        #                  app.config['UPLOAD_FOLDER']), filename))
        # filepath = os.path.join('static/media/', filename)
        blog = Blog(
            title=form.title.data,
            image=filename,
            text=form.text.data,
        )
        db.session.add(blog)
        db.session.commit()
        return redirect(url_for('all_blogs_view'))
    return render_template('add_blog.html', form=form)


@app.route('/add_project', methods=['GET', 'POST'])
def add_project():
    form = ProjectForm()
    form.tags_select.choices = [(tag.id, tag.name) for tag in Tag.query.all()]
    if form.validate_on_submit():
        file = form.image_path.data
        filename = secure_filename(file.filename)  # Надо сделать уникальность имени!!!!
        file.save(os.path.join(
            os.path.join(app.static_folder,
                         app.config['UPLOAD_FOLDER']), filename))
        # filepath = os.path.join('static/media/', filename)
        # рабочий вариант, но лучше без этой строки

        project = Project(
            title=form.title.data,
            image_path=filename,
            text=form.text.data,
        )
        selected_tags = Tag.query.filter(
            Tag.id.in_(form.tags_select.data)).all()
        project.tags.extend(selected_tags)
        db.session.add(project)
        db.session.commit()
        return redirect(url_for('index_view'))
    return render_template('add_project.html', form=form)
