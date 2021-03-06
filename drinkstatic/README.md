
# drinkStatic

drinkStatic is a minimalist static blog engine for Django on Google App Engine. It's aimed at developers and designers
to be as unobtrusive as possible.

The blog entries are defined in Django templates but decorated with tags to provide metadata to provide data to the
rest of the site. drinkStatic only uses the datastore for storing generated entities so the content and structure of
the site should be identical locally as when deployed.

## Getting started

Add the /drinkstatic directory to your Django application and add the application to its settings file:

   INSTALLED_APPS = (
       ...
       'drinkstatic',
   )

drinkstatic should come after your main site application.

Add the directory where your blog files will be kept to the settings file:

    DRINKSTATIC_TEMPLATE_DIRS =(os.path.join(os.path.dirname(__file__), '../templates/cinemas'),)

Add the url prefix (if any) that you'd like to use for your blog urls:

    BLOG_URL = 'cinemas'

Add 'drinkstatic.context_processors.drinkstatic' to TEMPLATE_CONTEXT_PROCESSORS:

    TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS + (
        'drinkstatic.context_processors.drinkstatic',
    )

## Writing blog entries

Load the drinkStatic tags in all of your blog files: {% load drinkstatic_tags %}

Use the drinkStatic tags to define the blog. At a minimum, the blog should have a title:

    {% titletext %}4U at Theatr Gwaun, Fishguard{% endtitletext %}

Each drinkstatic tag takes an optional 'render' argument. This defaults to True which means that the contents of the tag will be output to the screen.
If you want to use the tag simply to define meta rather than have the data hit the screen you can override this by passing False. I.e.

    {% datestamp 2012-08-13 False %}

Drinkstatic defines the following tags:

    - titletext
        - Defines the blog title. This title is used for the url slug unless a urlslug is defined
        - It works as a block tag so it will read everything from {% titletext %} to {% endtitletext %}.
            It will render its content by default but pass False to the render parameter to inhibit this. I.e.

            {% titletext False %}4U at Theatr Gwaun, Fishguard{% endtitletext %}

    - datestamp
        - Defines the blog date.
        - This reads the argument in y-m-d format and stores the datetime object. I.e.
            {% datestamp 2012-08-13 False %}
        - TODO: allow a parsing format to be passed in, allow a datetime object to be passed in.

    - thumbnail
        - Defines the blogs thumbnail image url.
        - Simply reads the argument and stores the path. Can be combined with an img tag to prevent repetition I.e.

            <img src="{% thumbnail /static/img/cinemas/4u_fishguard_1.jpg %}" />

Adding context data to nodes:

    TODO: add convention to add this in and remove current settings.NODE_GET_CONTEXT_DATA use

XML sitemap:

   drinkStatic generates a basic XML sitemap for the blog entries. This can be found in (settings.BLOG_URL)/sitemap.xml.
   You might want to add this to your robots.txt if you aren't generating your own sitemap.

Archive:

   To set an entry as archived then simply add {% archived %} to an entry.
