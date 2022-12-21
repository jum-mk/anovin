import openai
from ast import literal_eval
from . import models

openai.api_key = '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'


def get_ai_text(prompt, max_tokens):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.3,
        max_tokens=max_tokens,
        top_p=0.3,
        frequency_penalty=0.2,
        presence_penalty=0.1,
    )

    response_data = response['choices'][0]['text']
    return response_data


def create_tutorial(title, category):
    try:
        title = title.strip()
        models.Tutorial.objects.get(title=title)
        print('Tutorial already exists')

    except:
        meta_description = 'response text based on your SEO knowledge for articles, ' \
                           'consider the title "{0}" value when writing. ' \
                           'Output maximum of 300 characters in plain text. Consider that this needs to be placed inside' \
                           'html meta description tag. Escape adding the content in new lines. Use only plain text without formatting'.format(
            title)

        title = title
        print(title)
        meta_description = get_ai_text(meta_description, 356)

        print('meta_description -DONE')

        steps = 'Write a how to tutorial in steps considering that the title is {0}' \
                'write in plain text, make it seo friendly'.format(title)

        steps = get_ai_text(steps, 512)
        python_step_list = "write python list for the tutorial steps in '{0}'. Output only the value of the variable!".format(
            steps)

        python_step_list = literal_eval(get_ai_text(python_step_list, 256))
        print(python_step_list)
        print('step list -DONE')

        python_tag_list = "write python list of a maximum 8 tags considering it is a blog post with title {0} and introduction '{1}'" \
                          " write the tags in a python list in plain text. Output only the value!".format(
            title, meta_description)

        tags = get_ai_text(python_tag_list, 256)
        python_tag_list = literal_eval(tags)
        print('tags and step list -DONE')
        print(python_step_list)
        print(python_tag_list)

        content = ''

        for step in python_step_list:
            content_query = 'Write <p> tutorial part of minimum 200 words in the context and title of ' + str(
                title) + ' The steps in the tutorial are: ' + str(python_step_list) + \
                            'You are writing for the step:' + str(step) + \
                            'the h2 title is {0}'.format(step) + \
                            'The tutorial belongs to the category: ' + category + '.' + \
                            ' Do it in HTML5, write an SEO friendly paragraph.' \
                            ' Try to write code when you can. Format the code in the HTML.' + \
                            ' Use <pre> tag instead of <code> tags when you write code and always add' \
                            ' <br> before and after the <pre> tag.' \
                            ' Format the code lines appropriately, like in IDE according to the programming language' \
                            ' use <a> tags to link to external websites in the context of the step.' \
                            ' When using <a> tags make sure the href (url) is accessible and striped.' \
                            ' Try to use <a> as much as you can, seo wise.' \
                            'output only the HTML. Use  the <pre> tag whenever you can, ' \
                            ' Write in UTF-8 all the time. ' \
                            ' Write code examples. ' \
                            'Do not style the HTML inline! '
            print(len(content_query))

            content += get_ai_text(content_query, 2600)


        content = '<h1>' + title + '</h1>' + content
        useful_links = get_ai_text(
            'Write HTML list of useful links for the tutorial with title: ' + title + ' . The title of the useful links is h3.',
            512)
        content += useful_links
        category_input = category

        print('AI FINISHED')

        tut = models.Tutorial()

        tut.title = title
        tut.meta_description = meta_description
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
                tag.save()
                tut.tags.add(tag)

        try:
            category = models.Category.objects.get(name=category)
            tut.category = category
            tut.save()
        except:
            category = models.Category.objects.create(name=category_input)
            category.save()
            tut.category = category
            tut.save()
        print('TUTORIAL SAVED')

        return tut