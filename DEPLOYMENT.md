# Инструкции по развертыванию MASS Handbook

## Предварительные требования

- Node.js 18+ и npm
- Python 3.8+
- Git
- Аккаунты на GitHub и Vercel

## Локальная разработка

### 1. Клонирование репозитория

```bash
git clone https://github.com/your-org/mass-handbook.git
cd mass-handbook
```

### 2. Установка зависимостей

```bash
npm install
```

### 3. Запуск локального сервера

```bash
npm start
```

Сайт будет доступен на `http://localhost:3000`.

## Развертывание на GitHub

### 1. Инициализация Git репозитория

```bash
git init
git add .
git commit -m "Initial commit: MASS Handbook prototype"
git branch -M main
git remote add origin https://github.com/your-org/mass-handbook.git
git push -u origin main
```

### 2. Настройка GitHub Secrets

Перейдите в Settings → Secrets and variables → Actions и добавьте:

- `CROSSREF_EMAIL`: Ваш email для CrossRef API
- `VERCEL_TOKEN`: Токен Vercel (получить на https://vercel.com/account/tokens)
- `VERCEL_ORG_ID`: ID организации Vercel
- `VERCEL_PROJECT_ID`: ID проекта Vercel

## Развертывание на Vercel

### 1. Подключение репозитория

1. Перейдите на https://vercel.com
2. Нажмите "New Project"
3. Импортируйте репозиторий GitHub `mass-handbook`
4. Выберите Docusaurus как framework

### 2. Настройка переменных окружения

В Vercel Dashboard → Project Settings → Environment Variables добавьте:

```
CROSSREF_EMAIL=your-email@example.com
```

### 3. Развертывание

Нажмите "Deploy". Vercel автоматически создаст production версию.

## Автоматизация сбора статей

### 1. Настройка GitHub Actions

Workflow уже настроен в `.github/workflows/collect-papers.yml`.

Он запускается:
- По расписанию: каждый понедельник в 2:00 UTC
- Вручную: через GitHub Actions UI

### 2. Запуск вручную

```bash
# Локально
python scripts/collect_papers.py \
  --query "maritime autonomous collision avoidance" \
  --max-papers 50 \
  --email your-email@example.com
```

## Структура проекта

```
mass-handbook/
├── docs/
│   ├── intro.md
│   ├── papers/          # Автоматически генерируемые статьи
│   ├── guides/          # Практические гайды
│   └── glossary.md      # Глоссарий терминов
├── scripts/
│   └── collect_papers.py # Скрипт сбора статей
├── .github/
│   └── workflows/
│       └── collect-papers.yml # GitHub Actions workflow
├── docusaurus.config.ts # Конфигурация Docusaurus
├── package.json
└── README.md
```

## Добавление новых статей вручную

1. Создайте файл `docs/papers/my-paper.md`
2. Используйте следующий шаблон:

```markdown
---
sidebar_position: 1
tags: [Navigation, Collision Avoidance]
---

# Название статьи

**Авторы:** Имя Фамилия
**Год:** 2024
**Источник:** Журнал/Конференция
**DOI:** 10.xxxx/xxxxx

## Аннотация

Текст аннотации...

## Ключевые выводы

- Вывод 1
- Вывод 2

## Ссылки

- [Полный текст](https://doi.org/10.xxxx/xxxxx)
```

## Troubleshooting

### Ошибка: "Directory already exists"

```bash
rm -rf node_modules package-lock.json
npm install
```

### Ошибка при сборке Docusaurus

```bash
npm run build -- --out-dir build
```

### Проблемы с Vercel deployment

1. Проверьте логи в Vercel Dashboard
2. Убедитесь, что `package.json` содержит правильные скрипты
3. Проверьте переменные окружения

## Дополнительные ресурсы

- [Docusaurus Documentation](https://docusaurus.io/)
- [Vercel Documentation](https://vercel.com/docs)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [CrossRef API Documentation](https://www.crossref.org/documentation/retrieve-metadata/rest-api/)
