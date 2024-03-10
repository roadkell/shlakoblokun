## Шлакоблокунь: генератор смешных[^1] словослияний ##

```
        \\\\\\\\
  ┌────────────────┐__
\\│ ШЛАКОБЛ⎛⎞⎟⎠    │ °_\
//│        ⎝⎠⎟⎞УНЬ │___/
  └────────────────┘
 Portmanteau Generator
```

### Што ###

- [ШЛАКОБЛОКУНЬ](https://memepedia.ru/shlakoblokun-i-ego-druzya/)
- КОНДИЦИОНЕРПА
- ГУСТОТАЛИТАРИЗМ
- БРЕВНОСТЬ
- АРХИЕРЕЙВ
- БАНДИТЯТКО
- ХРЕНОВАЦИЯ
- ДЕДЛАЙНЕР
- КАНФЕРЭНЦЫЯНІЗАЦЫЯ

Исходные слова импортируются из текстового файла, в нём ищутся такие пары слов, чтобы из них могло получиться словослияние (portmanteau): шлакоблок + окунь = шлакоблокунь. Результаты выводятся в текстовый файл.

По умолчанию программа ищет по всему словарю в алфавитном порядке и выводит все найденные словослияния. Чтобы предварительно перемешать словарь, используйте опцию `--randomize`.

### Как ###

- Если не установлен Python 3 — [установить](https://www.python.org/downloads/).
- Скачать содержимое репозитория любым удобным способом.
- Запустить `shlakoblokun-ru.sh`, по желанию отредактировав.
- Остановить генерацию, нажав `Ctrl-C`, когда надоест ждать.
- Посмеяться (поплакать) над результатами в `output-ru.txt`.

Также можно запустить скрипт непосредственно из папки `shlakoblokun/` с желаемыми опциями:

```
python3 shlakoblokun.py [-h] [-i [INFILE ...]] [-a [AAA ...]] [-b [BBB ...]]
                        [-e [OVERLAPS]] [-o [OUTFILE]] [-r] [-n NUMBER] [-d DEPTH]
                        [-f MINFREE] [-l MINLENGTH] [-L MAXLENGTH] [-u] [-c] [-p]

опции:
  -h, --help                              вывести подсказку и выйти;
  -i [INFILE ...], --infile [INFILE ...]  словарь (текстовый файл) / папка со словарями;
  -a [AAA ...]                            словарь только для 1-го слова из пары;
  -b [BBB ...]                            словарь только для 2-го слова из пары;
  -e [OVERLAPS], --exclude-overlaps [OVERLAPS]
                                          словарь суффиксов/окончаний, на которых не следует генерировать наложения;
  -o [OUTFILE], --outfile [OUTFILE]       выходной текстовый файл;
  -r, --randomize                         перемешать словарь перед генерацией;
  -n NUMBER, --number NUMBER              число генерируемых словослияний (по умолчанию: неограниченно);
  -d DEPTH, --depth DEPTH                 мин. глубина наложения (по умолчанию: 2);
  -f MINFREE, --minfree MINFREE           мин. число непересекающихся букв в каждом слове (по умолчанию: 1);
  -l MINLENGTH, --minlength MINLENGTH     мин. длина исходных слов (по умолчанию: 3);
  -L MAXLENGTH, --maxlength MAXLENGTH     макс. длина исходных слов (по умолчанию: неограниченно);
  -u, --uppercase                         капитализировать общие буквы ("шлакоблОКунь");
  -c, --capitalized                       также включать слова с заглавной буквы;
  -p, --phrases                           также включать словосочетания (с пробелами);
```

В качестве словарей-исходников можно указать один или несколько текстовых файлов или папок, или даже направить поток из `stdin`.

Пример использования:

```
python3 shlakoblokun.py -i data/ru/n.txt -b data/ru/adj.txt data/ru/adv.txt data/ru/v.txt -o output.txt
```

Здесь в качестве общего словаря указан файл `data/ru/n.txt`, в то время как `data/ru/adj.txt`, `data/ru/adv.txt`, `data/ru/v.txt` указаны как словари для второго слова. Т.е. при генерации словослияний первое слово будет браться из `data/ru/n.txt`, а второе — из всех перечисленных словарей.

Того же результата можно добиться и короче:

```
python3 shlakoblokun.py -a data/ru/n.txt -b data/ru/ -o output.txt
```

Примеры с `stdin` / `stdout`:

```
cat input.txt | python3 shlakoblokun.py
python3 shlakoblokun.py < input.txt > output.txt
```

Словари извлечены из [дампа ру-Викисловаря](https://dumps.wikimedia.org/) с помощью [wiktion](https://github.com/roadkell/wiktion).

### Важное ###

[Queer Svit](https://queersvit.org/) — независимая команда волонтёров со всего мира. С вашей поддержкой мы помогаем ЛГБТК+ сообществу и небелым* людям из Украины, России, Беларуси и других стран региона ВЕЦА. Мы помогаем людям, пострадавшим от войны и/или политических репрессий, оказываем поддержку при переезде — проводим консультации, приобретаем билеты, находим бесплатное жильё и предоставляем гуманитарную помощь.

Война, как и всякая катастрофа, сильнее всего бьет по наиболее уязвимым членам общества. Так, маргинализированные группы (включая ЛГБТК+ и небелых* людей) находятся в большей опасности, но об их проблемах общество почти не слышит. Но так как наша команда и состоит из квир- и небелых* людей, мы не понаслышке знаем о трудностях, с которыми сталкиваются наши бенефициары, и хорошо понимаем, как им помочь.

Ваши пожертвования имеют значение; Queer Svit существует в значительной степени за счет небольших пожертвований индивидуальных жертвователей. Мы благодарны за любую помощь — спасибо!

[Queer Svit](https://queersvit.org/) is a black queer-run independent team of volunteers from all over the world. With your support we help LGBTQ+ and BAME people affected by the war and/or political repressions get to safety by providing consultations, purchasing tickets, finding free accommodation and providing humanitarian aid.

‌‌Just like any other catastrophe, war affects the most those who are most vulnerable, including LGBTQ+ and BAME people while at the same time their troubles are often rendered invisible. But because our own team comprises LGBTQ+ and BAME people we see the specific challenges our beneficiaries face and understand how to help them.

‌Your donations make a difference; Queer Svit is run in large part on small donations from individual donors. We are grateful for any and all help to continue our work — thank you!

### Лицензия ###

[Hippocratic License 3.0 (HL3-CORE)](https://github.com/roadkell/shlakoblokun/blob/main/LICENSE.md)

[Викисловарь](https://ru.wiktionary.org/): [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/)

[tqdm](https://github.com/tqdm/tqdm): [MIT](https://github.com/tqdm/tqdm/blob/master/LICENCE)

[^1]: Но это неточно
