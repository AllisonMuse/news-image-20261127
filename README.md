# news-image-20261127 — second edition

[![make.fun · news-image-20261127](https://make.fun/badge/news-image-20261127.svg)](https://make.fun/bounty/news-image-20261127?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127)
[![rank](https://make.fun/badge/news-image-20261127/AllisonMuse/news-image-20261127/rank.svg)](https://make.fun/bounty/news-image-20261127/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127)
[![reward](https://make.fun/badge/news-image-20261127/AllisonMuse/news-image-20261127/reward.svg)](https://make.fun/bounty/news-image-20261127?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127)

The World in One Day — 27 November 2026, second edition. An entry for
make.fun's [Sum up 27 November's world news in one image](https://make.fun/bounty/news-image-20261127)
bounty ($100 in USDC, top 50 paid).

The first edition ranked 160 of 5,304. This edition is rebuilt on the shape
of the 25 November winner: a newspaper front page with a masthead and ticker
strip, a stats strip, twelve large illustrated feature stories (each with a
hand-drawn scene, a dateline, a verification tag, a headline and a two-line
summary), a story-locator map with numbered pins, a compact "Also on Friday"
index of the remaining stories, a UTC timeline, a DATE CHECK box and a
verification legend. `draw_day.py` (Python 3, Pillow) draws `entry.png` — a
1024×1024 picture of the day with 40 verified stories across 11 region
groups. `main.ts` (Node 22, standard library only) validates `entry.png`
(PNG, at most 1 MiB, at most 1024×1024) and copies it into the output
directory the grader provides.

## Run it

```sh
python3 draw_day.py
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## The stories

Every story below was reported on 27 November 2026. Events that happened
on 26 November but were first reported on 27 November are noted as such.
Claims that are unconfirmed are marked as claims, not facts. Tags:
OFFICIAL = stated by an authority; CLAIM = attributed, unconfirmed;
CLOSE = final reported price; REPORT = press report.

### North America
1. Trump lashes out in Thanksgiving message — foes, immigrants and the federal government in the firing line. Source: AP, via Deccan Chronicle (https://www.deccanchronicle.com/world).
2. Trump calls GDP figures "fake", demands probe — Q3 growth revised up to 4.3% after the midterms. Source: AP, via ETV Bharat (https://www.etvbharat.com/en/international/trump-calls-the-pre-election-gdp-figures-fake-and-demands-an-investigation-of-commerce-department-enn26112700617) and Malay Mail (https://www.malaymail.com/news/world/2026/11/27/massive-and-purposeful-error-trump-wants-investigation-into-gdp-revision-released-after-midterms/244945).
3. Trump defends Huang's return as Nvidia chief — "Everybody's replaceable". Source: The Economic Times (https://economictimes.indiatimes.com/news/international?from=mdr).
4. Trump: Putin "would like to make a deal" — says Putin can attend the G20 in Miami. Source: Deccan Chronicle (https://www.deccanchronicle.com/world).
5. Storm batters the US on Thanksgiving — holiday travel hit as a nor'easter moves in. Source: Deccan Chronicle (https://www.deccanchronicle.com/world).
6. King tides flood the California coast — Pacifica Pier collapses; records fall. The record water levels were set on 25 November and reported through 27 November. Source: weather.com (https://weather.com/2026/11/26/forecast/regional/king-tides-record-coastal-flooding-west-coast) and USA Today (https://www.usatoday.com/story/news/state/california/2026/11/25/california-coast-braces-for-king-tides-dangerous-surf/92959926007/).
7. Eagles' 21-point Thanksgiving comeback — 59-yard field goal sinks the Cowboys. Source: AP, via sports roundups of 27 November 2026.
8. Black Friday: $12.9bn expected online — Adobe forecasts a record day; 126m Americans to shop. Source: Adobe, via The World Data (https://theworlddata.com/biggest-black-friday-deals/).

### Middle East
9. Kuwait drone attack kills two Italians — Iran calls it "suspicious" and denies any role. Source: Al Jazeera live blog (https://www.aljazeera.com/news/liveblog/2026/11/27/iran-war-live-irans-araghchi-calls-deadly-kuwait-attack-suspicious?traffic_source=rss) and Dawn (https://www.dawn.com/live/iran-israel-war).
10. Houthis hit Saudi Jazan refinery — one worker killed; operations halted. Source: Al Jazeera (https://www.aljazeera.com/news/liveblog/2026/11/27/iran-war-live-irans-araghchi-calls-deadly-kuwait-attack-suspicious?traffic_source=rss) and Dawn (https://www.dawn.com/live/iran-israel-war).
11. Tankers "hit mines" near Khasab — IRGC claim, unverified. Source: Times Now live blog (https://www.timesnownews.com/world/middle-east/us-iran-war-live-updates-strait-of-hormuz-crisis-donald-trump-iran-tensions-oil-tanker-fires-saudi-houthi-threats-scott-bessent-global-oil-supply-fears-liveblog-156558802).
12. Israeli strikes kill 10 in Gaza — Hamas education deputy among the dead. Source: Deccan Chronicle (https://www.deccanchronicle.com/world).
13. Brent crude near $96 a barrel — first weekly gain in a month. Source: Reuters, via Al Jazeera (https://www.aljazeera.com/news/liveblog/2026/11/27/iran-war-live-irans-araghchi-calls-deadly-kuwait-attack-suspicious?traffic_source=rss) and Dawn (https://www.dawn.com/live/iran-israel-war).
14. Saudi jets strike Mocha, Yemen — nine civilians hurt in Taiz shelling. Source: Al Jazeera (https://www.aljazeera.com/news/liveblog/2026/11/27/iran-war-live-irans-araghchi-calls-deadly-kuwait-attack-suspicious?traffic_source=rss).

### Europe
15. UK net migration falls to 77,000 — lowest since 1997, excluding Covid. Figures released 26 November, reported 27 November. Source: Reuters (https://www.reuters.com/world/uk/uk-annual-net-migration-drops-77000-year-june-2026-2026-11-26/) and The Times (https://www.thetimes.com/uk/politics/article/net-migration-lowest-level-ons-gnqxc6dxb).
16. EU picks Hernandez de Cos as ECB chief — succeeds Lagarde in February 2027. Source: Reuters (https://www.reuters.com/business/finance/ecb-turns-crisis-veteran-de-cos-new-strains-loom-2026-11-26/).
17. Depardieu to stand trial over rape claim — Paris court orders trial; he denies wrongdoing. Source: Al Jazeera (https://www.aljazeera.com/news/2026/11/26/paris-court-orders-gerard-depardieu-to-stand-trial-for-rape-sexual-assault?traffic_source=rss).
18. Sweden summons Russian envoy — over Polish airspace breach and Denmark plot. The summons was issued 26 November. Source: Government of Sweden (https://www.government.se/statements/2026/11/statement-from-the-ministry-for-foreign-affairs-on-the-summoning-of-the-russian-ambassador/).
19. Russian drones kill 3 in Ukraine — at least 10 injured overnight. Source: Kyiv Post (https://www.kyivpost.com/post/91254).
20. Besiktas–Hapoel halted 30 minutes — Palestine banner, pepper spray in Batumi; Besiktas won 2–1. The match was played 26 November and reported 27 November. Source: Al Jazeera (https://www.aljazeera.com/news/liveblog/2026/11/27/iran-war-live-irans-araghchi-calls-deadly-kuwait-attack-suspicious?traffic_source=rss).
21. Davis Cup: Britain beats Germany 2–1 — first semi-final in seven years. The tie was played 26 November and reported 27 November. Source: Devdiscourse (https://www.devdiscourse.com/article/international/4012832-tennis-patten-skupski-send-britain-past-germany-into-davis-cup-semi-finals?amp).

### East Asia
22. Taiwan votes on Saturday — cyberattacks surge ahead of local polls. Source: Nikkei Asia (https://asia.nikkei.com/spotlight/cybersecurity/taiwan-weathers-wave-of-cyberattacks-ahead-of-saturday-s-elections) and Deccan Chronicle (https://www.deccanchronicle.com/amp/world/taiwans-local-elections-whats-at-stake-and-why-china-is-watching-2008272).
23. Kim vows more nuclear weapons — after ignoring US talks. Source: Deccan Chronicle (https://www.deccanchronicle.com/world).
24. China protests Japan over Diaoyu waters — vessels' "illegal intrusion" draws a solemn protest. Source: Xinhua (http://english.scio.gov.cn/pressroom/2026-11/27/content_118791382.html) and China Daily Asia (https://www.chinadailyasia.com/hk/article/643326).

### South Asia
25. Hasina aide arrested in Bangladesh — ex-deputy press secretary held. Source: The Economic Times (https://economictimes.indiatimes.com/news/international?from=mdr).
26. Afghan women renamed "Bibi", "goat" — Taliban-ruled Balkh registers new names. Source: Moneycontrol (https://www.moneycontrol.com/world/taliban-strips-afghan-women-of-their-names-replaces-them-with-bibi-goat-cow-article-14090108.html), reporting a Zan Times / Guardian / El País investigation.
27. India, UAE fast-track defence tech — co-development of next-gen equipment. Source: Deccan Chronicle (https://www.deccanchronicle.com/world).
28. Sri Lanka A reach Asia Cup final — beat India A by eight wickets. Source: Apex Sports News (https://apexsportsnews.in/match-reports).

### South-East Asia
29. Indonesia mine flood: 13 dead — thirteen more still missing. Source: Al Jazeera (https://www.aljazeera.com/news/2026/11/26/at-least-13-dead-in-indonesia-gold-mine-flood-as-rescue-efforts-intensify).
30. Hong Kong warns over fire remembrance — memorial for 168 killed in blaze. Source: SCMP (https://www.scmp.com/news/hong-kong/society/article/3375868/youre-not-alone-hongkongers-return-mourn-tai-po-blaze-victims-year).

### Oceania
31. NZ coalition loses its majority — Luxon now needs the Opportunity Party. Source: The Economic Times (https://economictimes.indiatimes.com/news/international?from=mdr) and Deccan Chronicle (https://www.deccanchronicle.com/world).
32. Five women "buried alive" in PNG — sorcery claims spark outrage. Source: RNZ (https://www.rnz.co.nz/news/pacific/2768470/agents-of-the-devil-outrage-in-png-after-five-women-allegedly-buried-alive-over-sorcery-claims) and The National (https://www.thenational.com.pg/buried-alive-8/).

### Africa
33. Zambia: treason trial over "coup plot" — prosecutors allege Russia training. The plot itself is alleged, not proven. Source: Reuters, via CNBC Africa (https://www.cnbcafrica.com/2026/zambia-opposition-leader-charged-with-attempting-to-overthrow-government).
34. Kenya court halts Ebola centre — US-backed quarantine build stopped. The court ruled 26 November. Source: Reuters health summary, via Devdiscourse (https://www.devdiscourse.com/article/international/4012854-reuters-health-news-summary).
35. DRC summons Uganda diplomat — over general's Walikale posts. Source: OkayAfrica (https://www.okayafrica.com/today-in-africa-nov-26-2026-kenyan-court-rules-ebola-quarantine-facility-breached-the-constitution-dr-congo-summons-ugandas-top-diplomat-over-military-chiefs-posts/1442300).

### Latin America
36. Argentina bans money printing — central bank barred from funding government. Source: The Economic Times (https://economictimes.indiatimes.com/news/international?from=mdr).
37. Brazil snubs Milei from Lula inauguration — ambassador recalled as ties sour. Source: Firstpost (https://www.firstpost.com/world/argentinas-javier-milei-receives-no-invite-to-lulas-inauguration-amid-tensions-14062930.html), reporting Reuters.

### Sport
38. NZ 131–4 at tea in Christchurch Test — Latham 59 on day one v India. Source: Reuters (https://www.reuters.com/sports/cricket/new-zealand-131-4-tea-second-test-v-india-2026-11-27/).
39. Chess: rest day in Geneva — Game 3 drawn; Gukesh–Sindarov 1½–1½. Game 3 was played 26 November; 27 November is the rest day. Source: The Guardian, via World Chess (https://worldchess.com/news/gukesh-vs-sindarov-everything-you-need-to-know-about-the-2026-world-chess-championship).

### World & Tech
40. FIFA confirms hackers got in — limited personal, business data accessed. Source: Reuters (https://www.reuters.com/sports/soccer/fifa-victim-cyber-attack-files-related-world-cup-stake-selloff-unaffected-2026-11-26/).

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
