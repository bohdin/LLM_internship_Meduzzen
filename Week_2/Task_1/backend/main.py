from agent import agent

def run_test(prompt: str):
    print(f"🧪 Prompt: {prompt}")
    try:
        response = agent.invoke(prompt)
        print(f"🤖 Response: {response}")
    except Exception as e:
        print(f"❌ Error: {e}")
    print("=" * 60)

if __name__ == "__main__":
    test_prompts = [
        # 1. Простий запит без тулза
        "Hi my name Bohdan!",

        # 2. Виклик тулзу get_weather
        "What's my name?",

        # 3. Виклик тулзу calculate_area_rectangle (новий формат)
        "Please calculate the area of a rectangle: height=4.5, width=6.2",

        # 4. Виклик тулзу Wikipedia
        "Find some information about neural networks.",

        # 5. Комбінований запит з двома тулзами
        "What is the capital of Ukrain?",

        # 6. Перевірка памʼяті (follow-up без уточнення)
        "Can you remind me what city I just asked about?",

        # 7. Довший діалог
        "Now tell me something else about that city.",

        # 8. Спроба обробити некоректне введення для тулзу
        "Calculate area of rectangle: 5 by something wrong",
    ]

    for prompt in test_prompts:
        run_test(prompt)
