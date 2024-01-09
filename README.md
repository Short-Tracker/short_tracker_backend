# short_tracker_backend
Backend short tracker app

В requirements добавлен линтер ruff и pre-commit для гита.

## Ruff Линтер

Настройки линтера лежат в файле pyproject

Чтобы проверить все файлы в репозитории из корневой дириктории необходимо вызвать

```bash
ruff .
```

Чтобы сразу исправить ошибки импортов необходимо вызвать

```bash
ruff . --fix
```

## Prehook commit

Настройки pre-commit лежат в файл .pre-commit-config

Чтобы применить pre-commit необходимо сделать следующее:

1. Вызвать команду инициализации

```bash
pre-commit init
```

2. Вызвать команду установки

```bash
pre-commit install
```

Теперь при попытке пуша коммита сперва сработает скрипты проверки описанные в .pre-commit-config, в данном случае пока только проверка на PEP8.

