from enum import Enum


class CommandEnum(Enum):
    start = "start"
    auth = "auth"
    stats = "stats"
    get_question = "Ешё вопрос ➡"
    answer_again = "🔄 Повторить вопрос"
    llm_answer = "🤖 Помощь бота"
    go_back = "⏮ Главное меню"
    me = "👤 Мой профиль"
    select_stack = "✅ Выбор стека"
    start_interview = "⏳ Начать собеседование"
    start_training = "🧠 Начать тренировку"
    leaders = "👑 Лидеры"
    run_training = "✅ Готово"

    @classmethod
    def get_commands(cls) -> str:
        return (
            "Выберите желаемое действие:\n\n"
            # f"*{CommandEnum.start_interview.value}* \- мок собеседование с \~20 вопросами по выбранному стеку\. Фидбек в конце собеседования \n\n"  # noqa: E501
            f"*{CommandEnum.start_training.value}* \- бесконечная тренировка с выбранным стеком \n\n"  # noqa: E501
            f"*{CommandEnum.me.value}* \- перейти в свой профиль \n\n"
            # f"*{CommandEnum.leaders.value}* \- посмотреть лидеров \n\n"
        )


class StackEnum(Enum):
    python = "python"
    django = "django"
    fastapi = "fastapi"
    sql = "sql"
    javascript = "javascript"
    react = "react"
    vue = "vue"
    angular = "angular"
    git = "git"
    docker = "docker"
    linux = "linux"
    network = "сети"
    algorithm = "алгоритмы"
    computer_science = "computer science"

    @classmethod
    def get_stacks(cls) -> list[str]:
        return cls._member_names_
