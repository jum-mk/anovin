import openai
import json
import requests
from ast import literal_eval
from .models import *

openai.api_key = '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'

meta_description = 'response text based on your SEO knowledge for articles, ' \
                   'consider the title "Kali Linux for Wireless Pentesting" value when writing.'


def get_ai_text(prompt, max_tokens):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.9,
        max_tokens=max_tokens,
        top_p=0.1,
        frequency_penalty=0,
        presence_penalty=0
    )

    response_data = response['choices'][0]['text']
    return response_data


def create_tutorial(title):
    meta_description = 'response text based on your SEO knowledge for articles, ' \
                       'consider the title "{0}" value when writing. ' \
                       'Output maximum of 300 characters, trim the text. Consider that this needs to be placed inside' \
                       'html meta description tag. Escape adding the content in new lines'.format(title)
    introduction = 'Write a tutorial introduction for the title "{0}",' \
                   ' use HTML5 when writing,'.format(title)

    title = title

    meta_description = get_ai_text(meta_description, 256)
    introduction = get_ai_text(introduction, 512)

    print(meta_description)
    print(introduction)

    steps = 'Write a how to tutorial in steps considering that the title is {0}' \
            'write in plain text, make it seo friendly'.format(title)

    steps = get_ai_text(steps, 512)
    print(steps)
    python_step_list = "write python list for the steps in '{0}' and output just the value without variable assignment".format(
        steps)
    python_step_list = literal_eval(get_ai_text(python_step_list, 256))
    print(python_step_list)

    python_tag_list = "write python list of tags considering it is a blog post with title {0} and introduction '{1}'" \
                      " write the tags in plain python list without markup and output just the value without variable assignment. Trim whitespaces!".format(
        title, introduction)

    tags = get_ai_text(python_tag_list, 256)
    print(tags)
    python_tag_list = literal_eval(tags)

    print(python_tag_list)

    content = ''

    content_query = 'Write around of 700 words tutorial article in the context and title of' \
                    + title + ' for ' + ' list of steps are: ' + str(python_step_list) + \
                    ' . Context' + str(python_step_list) + '. Do it in HTML5 considering that you are starting to ' \
                                                           'write after the introduction of a blog post after the body tag, start with h tags, create <a> links to external sites whenever you can' \
                                                           ' use <code> tags when you write code and add <br> before and after the <code> tag,' \
                                                           ' when using <a> tags make sure the href (url) is accessible and striped,' \
                                                           ' make sure all <a> href links are accessible, make sure ' \
                                                           ' to place <br> before and after all <code>, output only the HTML. Write in UTF-8 all the time:'

    content += get_ai_text(content_query, 4096)

    content = content.replace('\n', '')

    category = get_ai_text('Name a tech category for the title: {0}'.format(title))
    obj = {
        'title': title,
        'meta_description': meta_description,
        'introduction': introduction,
        'steps': steps,
        'python_step_list': python_step_list,
        'python_tag_list': python_tag_list,
        'content': content,
        'category': category
    }

    tut = Tutorial()

    for item in python_tag_list:
        try:
            tag = Tag.objects.get(name=item)
            tut.tags.add(tag)
        except:
            tag = Tag.objects.create(name=item)
            tag.save()
            tut.tags.add(tag)

    try:
        category = Category.objects.get(category=category)
    except:
        category = Category.objects.create()

    tut.title = title
    tut.meta_description = meta_description
    tut.content = content
    tut.category = category
    print(tut.tags)

    print(tut)

    print(json.dumps(obj, sort_keys=False, indent=2))
    tut.save()
    return obj


create_tutorial('Kali Linux for Wireless Pentesting')
