from datetime import datetime
from flask import render_template, redirect, url_for, flash, request, send_from_directory, current_app
from app.main import main
from app.extensions import db
from app.models.cms import Page, Post, Event, Download

DEFAULT_SECTIONS = [
    {'name': 'hero', 'title': 'Where Excellence Meets Opportunity', 'subtitle': 'Nurturing Future Leaders', 'content': 'We provide a holistic educational environment that balances academic rigor with creative expression, character growth, and athletic skills.', 'is_enabled': True},
    {'name': 'welcome', 'title': 'A Warm Welcome From Our Campus', 'subtitle': 'Welcome to our School', 'content': 'At Sunny High School, we focus on empowering young minds to reach their full potential. Through specialized learning tracks, hands-on science research labs, dynamic arts courses, and active sports programs, we help every child excel.', 'is_enabled': True},
    {'name': 'principal', 'title': "Principal's Message to the Community", 'subtitle': 'Leadership Note', 'content': 'Dear Students, Parents, and Friends,\n\nAs the Principal of Sunny High School, it is my privilege to welcome you to our community portal. We strive to create a warm atmosphere where education goes beyond reading textbooks to solving real-life challenges.\n\nWe encourage our students to think critically, communicate articulately, and lead with empathy. Together with our faculty, we look forward to guide another year of discovery and transformation.', 'is_enabled': True},
    {'name': 'stats', 'title': 'A place to learn, grow, and belong.', 'subtitle': 'Sunny High School', 'content': 'Discover a welcoming campus built around curiosity, character, and opportunity.', 'is_enabled': True},
    {'name': 'news', 'title': 'School News & Announcements', 'subtitle': 'Stay Updated', 'content': '', 'is_enabled': True},
    {'name': 'events', 'title': 'Upcoming Campus Events', 'subtitle': 'School Calendar', 'content': '', 'is_enabled': True},
    {'name': 'gallery', 'title': 'Campus Gallery & Media', 'subtitle': 'Visual Tour', 'content': '', 'is_enabled': True},
    {'name': 'videos', 'title': 'Video Gallery', 'subtitle': 'Watch & Learn', 'content': '', 'is_enabled': True},
    {'name': 'testimonials', 'title': 'What Parents & Students Say', 'subtitle': 'Endorsements', 'content': '', 'is_enabled': True},
    {'name': 'contact', 'title': 'Have Questions? Contact Us', 'subtitle': 'Get In Touch', 'content': '', 'is_enabled': True},
]

@main.route('/')
def index():
    from app.models.cms import HomeSection, Testimonial, Media
    latest_news = Post.query.filter_by(is_published=True).order_by(Post.created_at.desc()).limit(5).all()
    upcoming_events = Event.query.filter_by(is_published=True).filter(Event.start_time >= datetime.utcnow()).order_by(Event.start_time.asc()).limit(3).all()
    
    sections = HomeSection.query.filter_by(is_enabled=True).order_by(HomeSection.order.asc()).all()
    if not sections:
        sections = DEFAULT_SECTIONS

    testimonials = Testimonial.query.filter_by(is_published=True).all()
    gallery_preview = Media.query.filter_by(media_type='image').limit(8).all()
    videos_preview = Media.query.filter_by(media_type='video').limit(6).all()

    return render_template(
        'main/index.html',
        latest_news=latest_news,
        upcoming_events=upcoming_events,
        sections=sections,
        gallery_preview=gallery_preview,
        videos_preview=videos_preview,
        testimonials=testimonials
    )

@main.route('/page/<slug>')
def page(slug):
    page_data = Page.query.filter_by(slug=slug, is_published=True).first_or_404()
    return render_template('main/page.html', page=page_data)

@main.route('/news')
def news():
    page_num = request.args.get('page', 1, type=int)
    search_query = request.args.get('q')
    
    query = Post.query.filter_by(is_published=True)
    
    if search_query:
        query = query.filter(Post.title.contains(search_query) | Post.content.contains(search_query))
        
    posts = query.order_by(Post.created_at.desc()).paginate(page=page_num, per_page=6)
    
    return render_template('main/news.html', posts=posts, search_query=search_query)

@main.route('/news/<slug>')
def news_detail(slug):
    post = Post.query.filter_by(slug=slug, is_published=True).first_or_404()
    return render_template('main/news_detail.html', post=post)

@main.route('/events')
def events():
    page_num = request.args.get('page', 1, type=int)
    upcoming = Event.query.filter_by(is_published=True).order_by(Event.start_time.asc()).paginate(page=page_num, per_page=6)
    return render_template('main/events.html', events=upcoming)

@main.route('/event/<slug>')
def event_detail(slug):
    event = Event.query.filter_by(slug=slug, is_published=True).first_or_404()
    return render_template('main/event_detail.html', event=event)

@main.route('/downloads')
def downloads():
    items = Download.query.order_by(Download.created_at.desc()).all()
    return render_template('main/downloads.html', items=items)

@main.route('/download/<int:download_id>')
def file_download(download_id):
    download_item = Download.query.get_or_404(download_id)
    filename = download_item.filename
    directory = current_app.config['UPLOAD_FOLDER']
    return send_from_directory(directory, filename, as_attachment=True)

@main.route('/contact', methods=['GET', 'POST'])
def contact():
    from app.forms.site import ContactForm
    from app.models.cms import ContactMessage
    form = ContactForm()
    if request.method == 'POST':
        # Accept both form object validation and manual POST payload (from homepage)
        name = request.form.get('name') or form.name.data
        email = request.form.get('email') or form.email.data
        phone = request.form.get('phone') or (form.phone.data if hasattr(form, 'phone') else '')
        subject = request.form.get('subject') or form.subject.data
        message_content = request.form.get('message_content') or form.message_content.data

        if name and email and message_content:
            msg = ContactMessage(
                name=name,
                email=email,
                phone=phone,
                subject=subject or 'Website Inquiry',
                message_content=message_content
            )
            db.session.add(msg)
            db.session.commit()
            flash('Thank you for your message! We will get back to you shortly.', 'success')
            return redirect(url_for('main.contact'))

    return render_template('main/contact.html', form=form)

@main.route('/gallery')
def gallery():
    from app.models.cms import Album
    albums = Album.query.order_by(Album.created_at.desc()).all()
    return render_template('main/gallery.html', albums=albums)

@main.route('/gallery/<int:album_id>')
def gallery_album(album_id):
    from app.models.cms import Album
    album = Album.query.get_or_404(album_id)
    return render_template('main/gallery_album.html', album=album)

@main.route('/videos')
def videos():
    from app.models.cms import Media
    videos = Media.query.filter_by(media_type='video').order_by(Media.created_at.desc()).all()
    return render_template('main/videos.html', videos=videos)


