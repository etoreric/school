from app.extensions import db
from app.models.user import User
from app.models.site import Setting
from app.models.cms import Page, HomeSection, Category

def seed_database():
    """
    Initialize default settings, pages, sections, categories, and admin user if they don't exist.
    """
    # 1. Seed default Settings
    default_settings = {
        'school_name': 'Sunny High School',
        'primary_color': '#2563eb',
        'secondary_color': '#f59e0b',
        'footer_bg_color': '#0f172a',
        'contact_email': 'info@sunnyhigh.edu',
        'contact_phone': '+1 (555) 789-0123',
        'contact_address': '742 Evergreen Terrace, Springfield',
        'footer_text': '© 2026 Sunny High School. All rights reserved.',
    }
    
    for k, v in default_settings.items():
        s = Setting.query.filter_by(key=k).first()
        if not s:
            s = Setting(key=k, value=v)
            db.session.add(s)
    db.session.commit()

    # 2. Seed core static pages
    default_pages = [
        ('About Us', 'about', '<h1>About Sunny High School</h1><p>Sunny High School is a leading school dedicated to education.</p>'),
        ('Contact', 'contact', '<h1>Contact Us</h1><p>Get in touch with us for more information.</p>'),
    ]
    for title, slug, content in default_pages:
        p = Page.query.filter_by(slug=slug).first()
        if not p:
            p = Page(title=title, slug=slug, content=content, is_published=True)
            db.session.add(p)
    db.session.commit()

    # 3. Seed Homepage Sections
    default_sections = [
        ('hero', 'Where Excellence Meets Opportunity', 'Nurturing Future Leaders', 'We provide a holistic educational environment that balances academic rigor with creative expression, character growth, and athletic skills.', 1),
        ('welcome', 'A Warm Welcome From Our Campus', 'Welcome to our School', 'At Sunny High School, we focus on empowering young minds to reach their full potential. Through specialized learning tracks, hands-on science research labs, dynamic arts courses, and active sports programs, we help every child excel.', 2),
        ('principal', "Principal's Message to the Community", 'Leadership Note', 'Dear Students, Parents, and Friends,\n\nAs the Principal of Sunny High School, it is my privilege to welcome you to our community portal. We strive to create a warm atmosphere where education goes beyond reading textbooks to solving real-life challenges.\n\nWe encourage our students to think critically, communicate articulately, and lead with empathy. Together with our faculty, we look forward to guide another year of discovery and transformation.', 3),
        ('stats', 'A place to learn, grow, and belong.', 'Sunny High School', 'Discover a welcoming campus built around curiosity, character, and opportunity.', 4),
        ('news', 'School News & Announcements', 'Stay Updated', '', 5),
        ('events', 'Upcoming Campus Events', 'School Calendar', '', 6),
        ('gallery', 'Campus Gallery & Media', 'Visual Tour', '', 7),
        ('videos', 'Video Gallery', 'Watch & Learn', '', 8),
        ('testimonials', 'What Parents & Students Say', 'Endorsements', '', 9),
        ('contact', 'Have Questions? Contact Us', 'Get In Touch', '', 10),
    ]
    for name, title, subtitle, content, order in default_sections:
        sec = HomeSection.query.filter_by(name=name).first()
        if not sec:
            sec = HomeSection(name=name, title=title, subtitle=subtitle, content=content, order=order, is_enabled=True)
            db.session.add(sec)
    db.session.commit()

    # 4. Seed Default Categories
    default_categories = [
        ('Academics', 'academics', 'Academic news and announcements'),
        ('Campus Life', 'campus-life', 'Events and student life activities'),
        ('Sports', 'sports', 'Athletic games and achievements'),
        ('Announcements', 'announcements', 'General school notifications'),
    ]
    for name, slug, desc in default_categories:
        cat = Category.query.filter_by(slug=slug).first()
        if not cat:
            cat = Category(name=name, slug=slug, description=desc)
            db.session.add(cat)
    db.session.commit()
    
    # 5. Seed default Admin User
    admin_user = User.query.filter_by(username='admin').first()
    if not admin_user:
        admin_user = User(
            username='admin',
            email='admin@sunnyhigh.edu',
            is_admin=True,
            is_active=True
        )
        admin_user.set_password('admin123')
        db.session.add(admin_user)
        db.session.commit()
        print("Default Admin created: admin / admin123")

