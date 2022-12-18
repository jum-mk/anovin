import openai
import json
from ast import literal_eval

openai.api_key = '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'


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


def create_city(name, country):
    content = "Create a tourism seo friendly blog with 700 word in html. In the tourism blog reference the text: " + \
              "Tours to Balkans," + " while considering the name of city: " + \
              name + ' and ' + country + '. ' + ' Do it in HTML.' + ' At the end add list useful links for the post.' + \
              ' Do it in HTML5, write an SEO friendly article.' + \
              ' use <a> tags to link to external websites in the context of the tutorial blog post.' + \
              ' When using <a> tags make sure the href (url) is accessible and striped.' + \
              ' Try to use <a> as much as you can, seo wise. Start with h1 tag.'

    content = get_ai_text(content, 3500)
    content = content.replace('\n', '')
    meta_description = 'response text based on your SEO knowledge for articles, ' \
                       'consider the city_name "{0}" value and the content value of: {1} when writing. ' \
                       'Output maximum of 225 characters in plain text. Consider that this needs to be placed inside' \
                       'html meta description tag. Escape adding the content in new lines'.format(name, content)
    meta_description = meta_description.strip(' ')
    content = get_ai_text(meta_description, 512)
    places_to_visit = get_ai_text(
        'Output HTML5 list of places to visit in city: ' + name + ' format it considering: ' + content, 512)
    foods_to_eat = get_ai_text(
        'Output HTML5 list of foods to eat in city: ' + name + ' format it considering: ' + content, 512)

    obj = {'meta_description': meta_description, 'content': content, 'places_to_visit': places_to_visit,
           'foods_to_eat': foods_to_eat}
    print(obj)
    return obj


create_city('Ohrid', 'North Macedonia')
