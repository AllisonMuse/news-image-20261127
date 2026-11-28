# news-image-20261127 — third edition

[![make.fun · news-image-20261127](https://make.fun/badge/news-image-20261127.svg)](https://make.fun/bounty/news-image-20261127?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127)
[![rank](https://make.fun/badge/news-image-20261127/AllisonMuse/news-image-20261127/rank.svg)](https://make.fun/bounty/news-image-20261127/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127)
[![reward](https://make.fun/badge/news-image-20261127/AllisonMuse/news-image-20261127/reward.svg)](https://make.fun/bounty/news-image-20261127?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127)

The World in One Day — 27 November 2026, third edition. An entry for
make.fun's [Sum up 27 November's world news in one image](https://make.fun/bounty/news-image-20261127)
bounty ($100 in USDC, top 50 paid).

The second edition's live development rank fell to 3,955 of 14,175, and the
26 November final proved development scores collapse on re-judging (97.84%
in development, 52.6% in the final). This edition is rebuilt to the
26 November winner's craft: a four-column newspaper broadsheet, 40 verified
stories across 11 regions and 27 fields, 12 large illustrated headlines
(each with a dateline, a verification tag, a headline, a two-line summary
and a WHY IT MATTERS line), a story-locator map with numbered pins, a
round-the-world strip, a DATE CHECK box, a HOW SURE source column, a stats
strip, and an "Also on Friday" index of the remaining 28 stories.
`draw_v3.py` (Python 3, Pillow) draws `entry.png` — a 1024×1024 picture.
`main.ts` (Node 22, standard library only) validates `entry.png` (PNG, at
most 1 MiB, at most 1024×1024) and copies it into the output directory the
grader provides.

## Run it

```sh
python3 draw_v3.py
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## The stories

Every story below was reported on 27 November 2026. Events that happened
on 26 November but were first reported on 27 November are noted as such.
Claims that are unconfirmed are marked as claims, not facts. Tags:
OFFICIAL = stated by an authority; CLAIM = attributed, unconfirmed;
CLOSE = final reported price; REPORT = press report.

### North America
1. Trump lashes out in Thanksgiving message — foes, immigrants and the federal government. Source: AP, via Deccan Chronicle.
2. Trump calls GDP figures "fake", demands probe — Q3 growth revised up to 4.3% after the midterms. Source: AP, via ETV Bharat and Malay Mail.
3. Trump defends Huang's return as Nvidia chief — "Everybody's replaceable". Source: The Economic Times.
4. Trump: Putin "would like to make a deal" — says Putin can attend the G20 in Miami. Source: Deccan Chronicle.
5. Storm batters the US on Thanksgiving — holiday travel hit as a nor'easter moves in. Source: Deccan Chronicle.
6. King tides flood the California coast — Pacifica Pier collapses; records set 25 November, reported through 27 November. Source: weather.com and USA Today.
7. Eagles' 21-point Thanksgiving comeback — 59-yard field goal sinks the Cowboys. Source: AP, via sports roundups of 27 November 2026.
8. Black Friday: $12.9bn expected online — Adobe forecasts a record day; 126m Americans to shop. Source: Adobe, via The World Data.

### Middle East
9. Kuwait drone attack kills two Italians — Iran calls it "suspicious" and denies any role. Source: Al Jazeera live blog and Dawn.
10. Houthis hit Saudi Jazan refinery — one worker killed; operations halted. Source: Al Jazeera and Dawn.
11. Tankers "hit mines" near Khasab — IRGC claim, unverified. Source: Times Now live blog.
12. Israeli strikes kill 10 in Gaza — Hamas education deputy among the dead. Source: Deccan Chronicle.
13. Brent crude near $96 a barrel — first weekly gain in a month. Source: Reuters, via Al Jazeera and Dawn.
14. Saudi jets strike Mocha, Yemen — nine civilians hurt in Taiz shelling. Source: Al Jazeera.

### Europe
15. UK net migration falls to 77,000 — lowest since 1997, excluding Covid. Figures released 26 November, reported 27 November. Source: Reuters and The Times.
16. EU picks Hernandez de Cos as ECB chief — succeeds Lagarde in February 2027. Source: Reuters.
17. Depardieu to stand trial over rape claim — Paris court orders trial; he denies wrongdoing. Source: Al Jazeera.
18. Sweden summons Russian envoy — over Polish airspace breach and Denmark plot. Summons issued 26 November. Source: Government of Sweden.
19. Russian drones kill 3 in Ukraine — at least 10 injured overnight. Source: Kyiv Post.
20. Besiktas–Hapoel halted 30 minutes — Palestine banner, pepper spray in Batumi; Besiktas won 2–1. Match played 26 November, reported 27 November. Source: Al Jazeera.
21. Davis Cup: Britain beats Germany 2–1 — first semi-final in seven years. Tie played 26 November, reported 27 November. Source: Devdiscourse.

### East Asia
22. Taiwan votes on Saturday — cyberattacks surge ahead of local polls. Source: Nikkei Asia and Deccan Chronicle.
23. Kim vows more nuclear weapons — after ignoring US talks. Source: Deccan Chronicle.
24. China protests Japan over Diaoyu waters — vessels' "illegal intrusion" draws a solemn protest. Source: Xinhua and China Daily Asia.

### South Asia
25. Hasina aide arrested in Bangladesh — ex-deputy press secretary held. Source: The Economic Times.
26. Afghan women renamed "Bibi", "goat" — Taliban-ruled Balkh registers new names. Source: Moneycontrol, reporting a Zan Times / Guardian / El País investigation.
27. India, UAE fast-track defence tech — co-development of next-gen equipment. Source: Deccan Chronicle.
28. Sri Lanka A reach Asia Cup final — beat India A by eight wickets. Source: Apex Sports News.

### South-East Asia
29. Indonesia mine flood: 13 dead — thirteen more still missing. Source: Al Jazeera.
30. Hong Kong warns over fire remembrance — memorial for 168 killed in blaze. Source: SCMP.

### Oceania
31. NZ coalition loses its majority — Luxon now needs the Opportunity Party. Source: The Economic Times and Deccan Chronicle.
32. Five women "buried alive" in PNG — sorcery claims spark outrage. Source: RNZ and The National.

### Africa
33. Zambia: treason trial over "coup plot" — prosecutors allege Russia training. The plot is alleged, not proven. Source: Reuters, via CNBC Africa.
34. Kenya court halts Ebola centre — US-backed quarantine build stopped. Court ruled 26 November. Source: Reuters health summary, via Devdiscourse.
35. DRC summons Uganda diplomat — over general's Walikale posts. Source: OkayAfrica.

### Latin America
36. Argentina bans money printing — central bank barred from funding government. Source: The Economic Times.
37. Brazil snubs Milei from Lula inauguration — ambassador recalled as ties sour. Source: Firstpost, reporting Reuters.

### Sport
38. NZ 131–4 at tea in Christchurch Test — Latham 59 on day one v India. Source: Reuters.
39. Chess: rest day in Geneva — Game 3 drawn; Gukesh–Sindarov 1½–1½. Game 3 played 26 November; 27 November is the rest day. Source: The Guardian, via World Chess.

### World & Tech
40. FIFA confirms hackers got in — limited personal, business data accessed. Source: Reuters.

## Timing notes

The competition's day is the events that happened, or were first reported,
on 27 November 2026 in any time zone. A few stories above happened late on
26 November in the Americas or Europe and were first reported on 27 November
(the UK migration figures, the Sweden summons, the Kenya court ruling, the
Besiktas–Hapoel halt and the Davis Cup tie); they are noted in place. The
king-tide records were set on 25 November and the flooding continued through
Thanksgiving week, reported on 27 November.

Left out on purpose — not 27 November news: FIFA's 2031 host announcement
(23 November); England's heat-death toll and Senegal's Afcon reinstatement
(first reported on earlier days); the North Korea aircraft story (the
aircraft was Russian, not North Korean).

## License

MIT — see LICENSE.
