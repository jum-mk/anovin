import openai
from ast import literal_eval
from . import models
from django.http import HttpResponse
from openai.error import ServiceUnavailableError

openai.api_key = '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'


def get_ai_text(prompt, max_tokens):
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


def get_social_media_posts(request):
    tutorials = models.Tutorial.objects.all()
    f = open('/Users/yellowflash/PycharmProjects/anovin/anovin/social_media_posts.txt', 'w')
    for t in tutorials:
        while True:
            try:
                title = str(t.title)
                url = str(t.get_absolute_url())

                snippet = title + str(t.hashtags) + '\n' + 'https://anovin.mk' + url + '\n' + '------------------------------------------------------------------' + '\n'
                print(snippet)
                f.write(snippet)

            except ServiceUnavailableError:
                continue

            break
    return HttpResponse(request, 'Ok')
