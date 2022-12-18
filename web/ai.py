import openai
import json
from ast import literal_eval
from . import models

openai.api_key = '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'

meta_description = 'response text based on your SEO knowledge for articles, ' \
                   'consider the title "Kali Linux for Wireless Pentesting" value when writing.'


def get_ai_text(prompt, max_tokens):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.2,
        max_tokens=max_tokens,
        top_p=0.1,
        frequency_penalty=0,
        presence_penalty=0
    )

    response_data = response['choices'][0]['text']
    return response_data


def create_tutorial(title, category):
    meta_description = 'response text based on your SEO knowledge for articles, ' \
                       'consider the title "{0}" value when writing. ' \
                       'Output maximum of 300 characters in plain text. Consider that this needs to be placed inside' \
                       'html meta description tag. Escape adding the content in new lines. Use only plain text without formatting'.format(
        title)

    title = title
    print(title)
    meta_description = get_ai_text(meta_description, 256)

    print(meta_description)

    steps = 'Write a how to tutorial in steps considering that the title is {0}' \
            'write in plain text, make it seo friendly'.format(title)

    steps = get_ai_text(steps, 512)
    python_step_list = "write python list for the steps in '{0}' and output just the value without variable assignment".format(
        steps)
    python_step_list = literal_eval(get_ai_text(python_step_list, 256))

    python_tag_list = "write python list of a maximum 8 tags considering it is a blog post with title {0} and introduction '{1}'" \
                      " write the tags in plain python list without markup and hashtag and output just the value without variable assignment. Trim whitespaces!".format(
        title, meta_description)

    tags = get_ai_text(python_tag_list, 256)
    python_tag_list = literal_eval(tags)

    content = ''

    content_query = 'Write about tutorial article of minimum 900 words in the context and title of ' + title + \
                    'for the steps in this list: ' + str(python_step_list) + \
                    'The tutorial belongs to the category: ' + category + '.' \
                                                                          ' Do it in HTML5, write an SEO frieldy article.' + \
                    ' Try to write code when you can. Format the code in the HTML.' + \
                    ' Use <code> tags when you write code and always add <br> before and after the <code> tag,' + \
                    ' Format the code lines appropriately, like in IDE according to the programming language' + \
                    ' use <a> tags to link to external websites in the context of the tutorial blog post.' + \
                    ' When using <a> tags make sure the href (url) is accessible and striped.' + \
                    ' Try to use <a> as much as you can, seo wise.' + \
                    'output only the HTML. Do not use the <pre> tag.  Write in UTF-8 all the time. Start with h1 title.' + title + \
                    ' from wikipedia or some other open source image library.' + \
                    ' At the end add list useful links for the post. Write many code examples.' + \
                    'It is very important that you beautify and style the code inside the <code> tag.'

    content += get_ai_text(content_query, 3800)


    category_input = category

    obj = {
        'title': title,
        'meta_description': meta_description,
        'introduction': meta_description,
        'steps': steps,
        'python_step_list': python_step_list,
        'python_tag_list': python_tag_list,
        'content': content,
        'category': category
    }
    print('AI FINISHED')

    tut = models.Tutorial()

    tut.title = title
    tut.meta_description = meta_description
    tut.content = content
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

    return obj
