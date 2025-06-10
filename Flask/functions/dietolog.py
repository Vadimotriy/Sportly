import requests
import json
import markdown

from Flask.database.constants import API_KEY


def analyze(age, weight, height, like, dislike, purpose):
    text = ("Составь рацион питания для пользователя. Если в его данных содержится нецензурная лексика "
            "напиши 'Неправильный формат данных!'\n\n"
            "Данные пользователя:"
            f"Возраст: {age}\nВес: {weight} кг\nРост: {height}см\nПредпочтения в еде: {like}\nНе любит: {dislike}\n"
            f"Цель: {purpose}")

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

    result = response.json()['choices'][0]['message']['content']
    html = markdown.markdown(result)
    return html


if __name__ == '__main__':
    print("start")
    like = 'Макароны, картошка, рис, свинина, огурцы, морковь, кукуруза, фрукты, ягоды, орешки'
    dislike = 'Помидоры, свекла, зеленый лук'
    purpose = 'Похудеть за 2 недели'
    print(analyze(16, 65, 176, like, dislike, purpose))