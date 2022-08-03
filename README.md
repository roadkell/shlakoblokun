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

[ШЛАКОБЛОКУНЬ](https://memepedia.ru/shlakoblokun-i-ego-druzya/)
КОНДИЦИОНЕРПА
ГУСТОТАЛИТАРИЗМ
БРЕВНОСТЬ
АРХИЕРЕЙВ
БАНДИТЯТКО
ХРЕНОВАЦИЯ
ДЕДЛАЙНЕР
КАНФЕРЭНЦЫЯНІЗАЦЫЯ
ЙОГЪАРГЪЫЛЫГЪ

Исходные слова импортируются из текстового файла, в нём ищутся такие пары слов, чтобы из них могло получиться словослияние (portmanteau): шлакоблок + окунь = шлакоблокунь. Результаты выводятся в текстовый файл.

По умолчанию программа ищет по всему словарю в алфавитном порядке и выводит все найденные словослияния. Чтобы предварительно перемешать словарь, используйте опцию `--randomize`.

### Как ###

1. Скачать содержимое репозитория любым удобным способом.
2. Если не установлен Python 3 — [установить](https://www.python.org/downloads/).
3. Запустить из командной строки с желаемыми опциями:
```
python3 shlakoblokun.py [-h] [-i [INFILE ...]] [-w1 [W1 ...]] [-w2 [W2 ...]]
                        [-o [OUTFILE]] [-r] [-n NUMBER] [-d DEPTH] [-f MINFREE]
                        [-l MINLENGTH] [-L MAXLENGTH] [-u] [-c] [-p]

опции:
  -h, --help                              вывести подсказку и выйти;
  -i [INFILE ...], --infile [INFILE ...]  словарь (текстовый файл) / папка со словарями;
  -w1 [W1 ...]                            словарь только для 1-го слова из пары;
  -w2 [W2 ...]                            словарь только для 2-го слова из пары;
  -o [OUTFILE], --outfile [OUTFILE]       выходной текстовый файл;
  -r, --randomize                         перемешать словарь перед генерацией;
  -n NUMBER, --number NUMBER              число генерируемых словослияний
                                          (по умолчанию: неограниченно);
  -d DEPTH, --depth DEPTH                 мин. глубина наложения (по умолчанию: 2);
  -f MINFREE, --minfree MINFREE           мин. число непересекающихся букв
                                          в каждом слове (по умолчанию: 1);
  -l MINLENGTH, --minlength MINLENGTH     мин. длина исходных слов (по умолчанию: 3);
  -L MAXLENGTH, --maxlength MAXLENGTH     макс. длина исходных слов
                                          (по умолчанию: неограниченно);
  -u, --uppercase                         капитализировать общие буквы ("шлакоблОКунь");
  -c, --capitalized                       также включать слова с заглавной буквы;
                                          (имена/названия/аббревиатуры);
  -p, --phrases                           также включать словосочетания (с пробелами);
```
В качестве словарей-исходников можно указать один или несколько текстовых файлов или папок.

Пример использования:
```
python3 shlakoblokun.py -i ru/n.txt -w2 ru/adj.txt ru/adv.txt ru/v.txt -o output.txt
```
Здесь в качестве общего словаря указан файл `ru/n.txt` (существительные), в то время как `ru/adj.txt`, `ru/adv.txt`, `ru/v.txt` указаны как словари для второго слова. Т.е. при генерации словослияний первое слово будет браться из `ru/n.txt`, а второе — из всех перечисленных словарей.

Словари извлечены из [дампа ру-Викисловаря](https://dumps.wikimedia.org/) с помощью [wiktio](https://github.com/roadkell/wiktio).

### Важно ###

Куда донатить ЛГБТК+ организациям в Украине?

- [Инсайт](https://linktr.ee/Insight.ngo), делают шелтеры в разных городах, психологическая и гуманитарная помощь

- [Точка Опорі](https://lnk.bio/fulcrumua), делают шелтеры во Львове, сервисная и гуманитарная помощь на границе

- [Когорта](https://instagram.com/p/CapTETkIuPH/?igshid=YmMyMTA2M2Y=), транс-организация, помощь с лекарствами, продуктами, эвакуацией

- [Сфера](https://shor.by/6T5P), сервисная и гуманитарная помощь в Харькове и Харьковской области

- [ГендерЗед](https://shor.by/ukrainehelp), гуманитарная и сервисная помощь в Запорожье и Запорожской области

- [GenderStream](https://linktr.ee/gender_stream), помощь транс-людям на границе

- [КиевПрайд](https://linktr.ee/kyivpride), шелтер в Киеве и психологическая помощь

- [ГАУ](https://upogau.org/donate-ua/), присылают продуктовые наборы и помогают с экстренными нуждами

А также:

- [Квир за мир!](https://twitter.com/queeragainstwar), низовое антивоенное движение и фонд взаимопомощи для ЛГБТК+ людей из Украины, России и Беларуси

- [Тред](https://twitter.com/antilashden/status/1551903998202052609) о том, почему это важно (спасибо [лашден](https://twitter.com/antilashden) и [Мире](https://twitter.com/ttt_mir_no) за информацию 🫶)

### Лицензия ###

[Hippocratic License 3.0](https://firstdonoharm.dev/)

[Викисловарь](https://ru.wiktionary.org/): [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/)

[^1]: Но это неточно
