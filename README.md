## Шлакоблокунь: генератор смешных[^1] словослияний ##
```
   ┌\\───\\\\───\\┐
  >│ Shlakoblokun │°>
   └//───////───//┘
 Portmanteau Generator
```

### Што ###

Генератор [шлакоблокуней](https://memepedia.ru/shlakoblokun-i-ego-druzya/): берётся словарь, в нём ищутся такие пары слов, чтобы из них могло получиться словослияние (portmanteau): шлакоблок + окунь = шлакоблокунь. Результаты выводятся в текстовый файл.

По умолчанию программа ищет по всему словарю и выводит все найденные словослияния. Если нужно по-быстрому сгенерировать несколько случайных шлакоблокуней, используйте опцию `--random`.

### Как ###

1. Скачать содержимое репозитория любым удобным способом.
2. Если не установлен Python 3 — [установить](https://www.python.org/downloads/).
3. Запустить из командной строки с желаемыми аргументами / опциями:

```
python3 shlakoblokun.py [-h] [-r] [-n NUMBER] [-d DEPTH] [-u] [-c] [-m] [infiles] [outfile]

позиционные аргументы:
  infiles                       путь к файлу или папке со словарями (по умолчанию: ru)
  outfile                       выходной текстовый файл (по умолчанию: output.txt)

опции:
  -h, --help                    вывести подсказку и выйти
  -r, --random                  генерировать случайные словослияния
  -n NUMBER, --number NUMBER    число генерируемых словослияний (по умолчанию: неограниченно)
  -d DEPTH, --depth DEPTH       минимальная глубина наложения (по умолчанию: 2)
  -u, --uppercase               капитализировать общие буквы (шлакоБЛОКунь)
  -c, --capwords                также включать слова с Заглавной буквы (обычно имена/названия)
  -m, --multiwords              также включать словосочетания (с пробелами)
```
### Лицензия ###

[Hippocratic License 3.0](https://firstdonoharm.dev/)

Материалы [Викисловаря](https://ru.wiktionary.org/) доступны на условиях лицензии [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/deed.ru)

Материалы [проекта YARN](https://russianword.net/) доступны на условиях лицензии
[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

[^1]: Но это неточно
