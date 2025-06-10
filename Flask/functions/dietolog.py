import requests
import json
import markdown

from Flask.database.constants import API_KEY
from pprint import pprint


def analyze(age, weight, height, like, dislike, purpose, life, cant):
    text = ("Составь рацион питания для пользователя. Если в его данных содержится нецензурная лексика или что-то "
            "незаконное, то напиши 'Неправильный формат данных! Не задавай пользователю вопрос (не уточняй ничего). "
            "Рацион должен получиться большого объема. Должно получится несколько вариантов питания, "
            "то есть на каждый прием пищи и пользователя должен быть большой выбор. Нужно также дать"
            " пользователю рекомендации по занятию спортом.'\n\n"
            "Данные пользователя:"
            f"Возраст: {age}\nВес: {weight} кг\nРост: {height}см\nПредпочтения в еде: {like}\nНе любит: {dislike}\n"
            f"Цель: {purpose}\nОбраз жизни: {life}\nПротивопоказания : {cant}\n")

    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": API_KEY,
            "Content-Type": "application/json",
        },
        data=json.dumps({
            "model": "qwen/qwen3-30b-a3b:free",
            "messages": [
                {
                    "role": "user",
                    "content": text
                }
            ],

        })
    )
    pprint(response.json())
    result = response.json()['choices'][0]['message']['content']
    result = result.replace('\n\n', '<br /><br />')
    html = markdown.markdown(result)
    return html


if __name__ == '__main__':
    print("start")
    like = 'Макароны, картошка, рис, свинина, огурцы, морковь, кукуруза, фрукты, ягоды, орешки'
    dislike = 'Помидоры, свекла, зеленый лук'
    purpose = 'Похудеть за 2 недели'
    life = 'Небольшие занятие спортом'
    print(analyze(16, 65, 176, like, dislike, purpose, life, 'отсутствуют'))