import openai
from ast import literal_eval
from . import models
from openai.error import ServiceUnavailableError, InvalidRequestError


def get_ai_text(prompt, max_tokens):
    openai.api_key = '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'
    while True:
        try:

            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=prompt,
                temperature=0.2,
                max_tokens=max_tokens,
                top_p=0.1,
                frequency_penalty=0,
                presence_penalty=0,
            )
            response_data = response['choices'][0]['text']
            return response_data
        except ServiceUnavailableError or InvalidRequestError:
            print("An error occurred. Restarting the job.")
            continue


def create_tutorial(title, category):
    try:
        models.Tutorial.objects.get(title=title)
    except:
        meta_description = 'response one sentence text based on your SEO knowledge for articles. ' \
                           ' Consider the title "{0}" value when writing. ' \
                           'Output maximum of 160 characters in plain text. Consider that this needs to be placed inside' \
                           'html meta description tag. Use only plain text without formatting.'.format(
            title)

        title = title
        meta_description = get_ai_text(meta_description, 356)

        print('meta_description -DONE')

        steps = 'Write a how to tutorial in steps considering that the title is {0}' \
                'write in plain text, make it seo friendly'.format(title)

        steps = get_ai_text(steps, 400)
        python_step_list = "output python list of strings for the tutorial step parts in '{0}'. Output only the list value, do not assign it to a variable.!".format(
            steps)

        python_step_list = literal_eval(get_ai_text(python_step_list, 512))
        print('step list -DONE')

        python_tag_list = "write python list of a maximum 8 tags for the blog post with title {0} and introduction '{1}'" \
                          " write the tags in a python list of strings in plain text. Output only the value, without variable assignment!".format(
            title, meta_description)

        tags = get_ai_text(python_tag_list, 512)
        python_tag_list = literal_eval(tags)
        print('tags and step list -DONE')

        content = ''

        for step in python_step_list:
            content_query = 'Write <p> tutorial part of minimum of 300  words in the context of: ' + str(
                title) + '. The parts of the tutorial are: ' + str(
                python_step_list) + '. You are writing for the part: ' + str(
                step) + '. The h2 title is {0}'.format(
                step) + 'The tutorial belongs to the category: ' + category + '.' + ' Do it in HTML5, write an SEO friendly paragraph.' + ' Write code inside <pre> tags. Write commands inside <pre> tags. Format the code in the HTML.' + ' Always add <br> before and after <pre> and <code> tags.' + ' Format the code inside <pre> tag lines appropriately, like in IDE according to the programming language' + ' . Use <a> tags to link to external websites in the context of the step.' + ' When using <a> tags make sure the href (url) is accessible and striped.' + ' Try to use <a> as much as you can, seo wise.' + ' Output only the HTML! Use the <pre> tag whenever you can. ' + ' Write in UTF-8 all the time. ' + ' Write code examples inside <pre> tag. ' + 'Do not style the HTML inline!' + ' Do not repeat sentences from the previous step!.'
            print(len(content_query))

            content += get_ai_text(content_query, 2600)

        content = '<h1>' + title + '</h1>' + content
        useful_links = get_ai_text(
            'Write valid HTML5 list of useful correctly formatted links for the tutorial with title: ' + title + ' . The title of the useful links is h3. Do not make syntax errors!',
            512)
        content += useful_links
        category_input = category

        print('AI FINISHED')

        tut = models.Tutorial()

        tut.title = title
        tut.meta_description = str(meta_description).strip(' ').replace('\n', '')
        tut.content = content

        tut.slug = str(tut.title).strip(' ').replace(' ', '-').lower()
        tut.save()
        for item in python_tag_list:
            try:
                tag = models.Tag.objects.get(name=item)
                tut.tags.add(tag)
                tut.save()
            except:
                tag = models.Tag.objects.create(name=item)
                tag.slug = str(tag.name).strip(' ').replace('\n', '').replace(' ', '-').lower()
                tag.save()
                tut.tags.add(tag)

        try:
            category = models.Category.objects.get(name=category)
            tut.category = category
            tut.save()
        except:
            category = models.Category.objects.create(name=category_input)
            category.slug = str(category.name).strip(' ').replace('\n', '').replace(' ', '-').lower()
            category.save()
            tut.category = category
            tut.save()
        print('TUTORIAL SAVED')

        return tut
