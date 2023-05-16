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
- ЙОГЪАРГЪЫЛЫГЪ

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
python3 shlakoblokun.py [-h] [-i [INFILE ...]] [-w1 [W1 ...]] [-w2 [W2 ...]]
                        [-o [OUTFILE]] [-r] [-n NUMBER] [-d DEPTH] [-f MINFREE]
                        [-l MINLENGTH] [-L MAXLENGTH] [-u] [-c] [-p]

опции:
  -h, --help                              вывести подсказку и выйти;
  -i [INFILE ...], --infile [INFILE ...]  словарь (текстовый файл) / папка со словарями;
  -w1 [W1 ...]                            словарь только для 1-го слова из пары;
  -w2 [W2 ...]                            словарь только для 2-го слова из пары;
  -e [EXCLUDE_OVERLAPS], --exclude-overlaps [EXCLUDE_OVERLAPS]
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
python3 shlakoblokun.py -i data/ru/n.txt -w2 data/ru/adj.txt data/ru/adv.txt data/ru/v.txt -o output.txt
```
Здесь в качестве общего словаря указан файл `data/ru/n.txt` (существительные), в то время как `data/ru/adj.txt`, `data/ru/adv.txt`, `data/ru/v.txt` указаны как словари для второго слова. Т.е. при генерации словослияний первое слово будет браться из `data/ru/n.txt`, а второе — из всех перечисленных словарей.

Того же результата можно добиться и короче:
```
python3 shlakoblokun.py -w1 data/ru/n.txt -w2 data/ru/ -o output.txt
```

Примеры с `stdin` / `stdout`:
```
cat input.txt | python3 shlakoblokun.py
python3 shlakoblokun.py < input.txt > output.txt
```

Словари извлечены из [дампа ру-Викисловаря](https://dumps.wikimedia.org/) с помощью [wiktion](https://github.com/roadkell/wiktion).

### Важное ###

[Квiр Свiт](https://queersvit.taplink.ws/) — организация, которая помогает квир- и небелым людям, пострадавшим от войны в Украине, и тем, чьим жизням угрожает растущий авторитаризм в России и Беларуси. Мы — группа волонтеров, предоставляющих финансовую помощь, жилье и транспорт нуждающимся ЛГБТК+ и небелым людям, а также рекомендации и связи с дополнительными ресурсами.
Каждый донат важен, и мы всегда благодарны людям, которые распространяют информацию о нашем деле. Спасибо!

[Queer Svit](https://queersvit.taplink.ws/) is an organization that helps queer and BAME people impacted by the war in Ukraine, and those whose lives are threated by rising authoritarianism in Russia and Belarus. We are a group of volunteers, providing financial assistance, housing, and transportation to LGBTQ+ and BAME people in need, along with guidance and connections to further resources.
Any donation helps, and we are always grateful to people who spread the word about our cause. Thank you!

### Лицензия ###

[Hippocratic License 3.0](https://firstdonoharm.dev/version/3/0/core.html)

[Викисловарь](https://ru.wiktionary.org/): [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/)

[tqdm](https://github.com/tqdm/tqdm): [MIT](https://github.com/tqdm/tqdm/blob/master/LICENCE)

[^1]: Но это неточно
