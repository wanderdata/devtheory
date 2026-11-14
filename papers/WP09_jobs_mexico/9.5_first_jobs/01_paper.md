# Where Careers Start: First Jobs of Young Mexicans and Where They Lead, 2005–2026

*Paul Wander. Working draft v0.1, 2026-11-13. Pre-analysis plan: [`00_pre_analysis_plan.md`](00_pre_analysis_plan.md). Generated tables: [`empirics/output/enoe/first_jobs/results.md`](../../../empirics/output/enoe/first_jobs/results.md). App: Jobs in Mexico, page 9.5.*

## Abstract

We identify first jobs from the respondent's own report. A first job is held by someone aged 15–24 who, at their first interview in Mexico's labour-force survey (ENOE), is not working and says they have never worked, and who is working three months later. Pooling 70 five-quarter panels from 2005–2019 and 2022–2026, we observe 47,186 such entrants and follow them for three more quarters.

**What first jobs are.** First jobs are much more informal than young people's jobs in general: 85% against 68%. 28% are unpaid work, mostly in family businesses.

**Where they lead.** First jobs are short-lived. Three quarters after entry:
- half of those who started in an informal job are not working;
- so are 36% of those who started in a formal job.

**Informal first jobs.** These are stepping stones, but weak ones. Compared with young people who had never worked and were still not working, and conditional on age, sex, schooling, school attendance, household and place, taking an informal first job raises the probability of formal employment three quarters later by 3.4 percentage points (90% interval 3.0–3.7), from 2.5%.

**Formal first jobs.** Starting formally raises that probability by 34 points relative to starting informally.

**Among informal first jobs.** Wage jobs in establishments with premises lead to formal work 4.2 points more often than own-account or unpaid work. This is less than the 10-point difference we expected.

## 1. Introduction

**The question.** In Mexico, as elsewhere in Latin America, most young people start working in informal jobs. Whether that is a problem depends on what follows.
- **Stepping stone.** An informal first job may teach skills, build a record and lead to formal employment.
- **Trap.** It may leave young people in informal work or return them to inactivity.

**Earlier evidence.**
- Cruces, Ham and Viollaz (2012), with Brazilian cohort data, find that cohorts with more youth informality have more informality and lower wages as adults, mainly among the less educated.
- With ENOE, Conover, Khamis and Pearlman (2021) find that informal wage work leads to formal work far more often for workers with upper-secondary schooling than for others.
- Donovan, Lu and Schoellman (2023) document across countries a "slippery" job ladder: in poor countries workers move into and out of marginal jobs often but rarely reach or keep better ones.

**This paper.** It contributes in two ways.
- **A definition from the respondent's own answer.** It defines a first job by the respondent's statement that they had never worked, rather than by age or tenure, and observes the job within three months of its start.
- **A comparison with continuing not to work.** It compares taking an informal first job with not working. This is the margin that matters for a young person deciding whether to accept an informal job. In this programme's terms, it asks whether the first rung of the ladder leads anywhere.

## 2. Data

**Survey and periods.** ENOE, every quarter from 2005Q1 to 2019Q4 and from 2022Q1 to 2026Q2. 2020–2021 are excluded because of the telephone survey and the change to ENOE^N. Persons are linked across the five interviews of each dwelling with the method of study 9.1. Of the never-worked, non-employed 15–24-year-olds at a first interview, 91.5% are linked to the second interview and 76.5% to the fifth.

**Definitions.**
- **Never worked.** Answer 4 ("has never worked") to question P2H, asked every quarter of everyone not employed.
- **First-job entrant.** Aged 15–24 at the first interview, not employed and never worked then, and employed at the second interview.
- **Comparison group.** Never worked and not employed at both the first and the second interview.
- **Formality.** INEGI's labour-informality definition.
- **Units with premises.** INEGI's micro units with premises and small, medium and large establishments.

**Sample.** 397,978 never-worked, non-employed 15–24-year-olds at a first interview, among whom 47,186 take a formal or informal job by the second.

## 3. Method

**Model.** The outcome is formal employment at the fifth interview, three quarters after entry. Weighted linear probability models include:
- fixed effects for the quarter of the first interview, state, single years of age, single years of schooling, and relationship to the household head;
- controls for sex, school attendance, the number of formally and informally employed household members, and urban residence.

All characteristics are measured at the first interview. Standard errors are clustered by primary sampling unit.

**Selection on unobservables.** The comparisons are conditional on observables. Unobserved motivation, contacts or reasons for not working could bias them. Following Oster (2019), we report how strong selection on unobservables would have to be, relative to selection on observables, to reduce each difference to zero.

## 4. Results

### 4.1 First jobs

| | First jobs | All jobs, employed 15–24 |
|---|---|---|
| Informal | 85.1% | 68.5% |
| Wage employee | 63.2% | 78.9% |
| Unpaid | 27.9% | 13.2% |
| Own-account | 8.5% | 7.2% |
| Commerce | 27.4% | 22.0% |
| Restaurants and lodging | 12.7% | 9.6% |
| Manufacturing | 14.3% | 18.6% |
| Construction | 4.2% | 8.5% |

**Composition.** First jobs are more informal than the jobs young people hold in general, by 17 points. P34 is supported. They are more often unpaid, mostly help in family businesses, and more often in commerce, restaurants and lodging. They are less often in manufacturing and construction.

**By type.** Classified by type:
- 36% of first jobs are informal own-account or unpaid work;
- 29% are informal wage jobs in units with premises;
- 20% are other informal wage jobs, mostly in micro units without premises;
- 15% are formal.

**Pay and hours.** Formal first jobs pay a median of 1.8 times the monthly minimum wage for 43 hours a week. Informal wage jobs in units with premises pay about the minimum for 34 hours, and other informal wage jobs 0.8 times it for 29 hours.

### 4.2 Where first jobs lead

State three quarters after entry, by type of first job (weighted shares, not adjusted):

| First job | Formal | Informal | Not employed |
|---|---|---|---|
| Formal | 47.8% | 16.6% | 35.6% |
| Informal wage, unit with premises | 10.2% | 40.0% | 49.8% |
| Informal wage, other | 6.1% | 42.3% | 51.6% |
| Informal own-account or unpaid | 3.9% | 39.3% | 56.9% |
| Still not working at entry (comparison) | 2.5% | 9.8% | 87.7% |

**Fleeting jobs.** The most common destination of an informal first job, three quarters on, is no job. Even among formal entrants, a third are not working. This is the slippery ladder of Donovan, Lu and Schoellman (2023) at the start of careers.

**Formal destinations.** Among those who start informally, one in ten of those in units with premises, and one in twenty-five of those in own-account or unpaid work, are formal three quarters later.

### 4.3 Comparisons conditional on observables

Effect on the probability of formal employment three quarters after entry, percentage points:

| Comparison | Estimate | 90% interval | Base | Proposition |
|---|---|---|---|---|
| Informal first job vs. still not working | +3.4 | +3.0 to +3.7 | 2.5% | P35 supported |
| Formal vs. informal first job | +34.0 | +32.3 to +35.8 | 6.5% | P36 supported |
| Informal wage job, premises vs. informal own-account or unpaid | +4.2 | +3.4 to +5.0 | 3.9% | P37 rejected |

**Informal first jobs are stepping stones, but weak ones.** Taking one more than doubles the probability of formal employment three quarters later. That probability rises from 2.5%, for those still not working, to about 6%. The difference is positive in every period, in each sex, among those not attending school, and with entry at the third interview.
- **By schooling:** it is larger with at least 12 years of schooling (+6.0 points on a base of 5.0%) than with less (+2.2 on 1.7%), consistent with Conover, Khamis and Pearlman (2021).
- **Selection:** adding controls lowers it only from 4.0 to 3.4 points, and selection on unobservables would have to be 14.6 times as strong as selection on observables to remove it (4.4 times with a more demanding maximum R²).
- **Not a trap:** an informal first job does not reduce the chance of later formal work relative to continued search. P35 is supported.

**The formality of the first job persists.**
- **Size:** formal entrants are 34 points more likely than informal entrants to be formal three quarters later. The probit average marginal effect is 27.5 points.
- **Across samples:** the difference is 29–36 points across periods and groups. It is smallest in 2022 onward (29).
- **Selection:** this comparison is the most exposed to selection. Controls lower it from 41 to 34 points, and selection on unobservables 3.2 times as strong as on observables would remove it. With the more demanding maximum R², 0.9 times would suffice.

**The type of informal first job matters, but less than expected.** Informal wage jobs in units with premises lead to formal work 4.2 points more often than own-account or unpaid work, roughly doubling a low base. The difference is positive in every sample. Its upper bound, 5.0 points, is below the 10 points the plan set as a material difference, so P37 is rejected as stated.

## 5. Robustness and limits

- **Robustness checks.** Results hold with:
  - ages 15–29;
  - entry at the third interview (two-quarter horizon);
  - weights for attrition between the second and fifth interviews;
  - 2005–2019 only.
- **Recall.** Of the never-worked who are still not employed at the second interview, 14.5% now report having worked. Some had short jobs between interviews, which ENOE does not observe. Others give inconsistent answers. Excluding them from the comparison group, as the plan specified, keeps the group to people who stayed out of work. It also makes the comparison group somewhat more inactive than all non-entrants.
- **Horizon.** Three quarters is short. Stepping stones that take a year or more cannot be seen in a five-quarter panel.
- **Selection.** The conditional comparisons are not causal estimates. The Oster bounds show that P35 is robust to strong selection on unobservables, while the size of P36 is not.

## 6. Conclusions

**The start of careers.** Most young Mexicans' first jobs are informal, often unpaid work in a family business, and short-lived. Three quarters after starting, half of those in informal first jobs are not working.

**Informal first jobs.** They are not traps relative to staying out of work: they raise the chance of formal employment later. But from very low levels: about 6% are formal three quarters on.

**Formal first jobs.** These are the clearest route to formal employment, yet a third of formal entrants are not working three quarters later.

**Within informal work.** Wage jobs in established units do somewhat better than own-account or unpaid work, by less than expected.

**For this programme.** The first rung of the job ladder exists, but it is low and slippery. Policies that help young people into formal first jobs would act on the margin with the largest observed difference, if that difference is not mostly selection. The policies most commonly discussed for this are hiring subsidies and apprenticeships, as in the experiment of Abel et al. (2022).

**What would change these conclusions:**
- a longer panel, such as administrative records linked from the first formal job;
- a source of variation in access to formal first jobs that is unrelated to young people's characteristics.

## Annex A. Notes on implementation and further work

**A.1 Choices.**
- **Quarters.** The plan's periods were used, through 2026Q2, the latest available.
- **Probit.** The probit check (plan §4) was estimated with year instead of quarter effects and without clustered standard errors. Only its point estimates are compared, because the clustered version exceeded the workspace's memory.
- **Constant controls.** A control that does not vary within a subsample (sex within a sex group, attendance among those not attending) is dropped there.
- **Reader fixes.** From 2025Q3 INEGI renamed the geographic codes (`cve_ent`, `cve_mun`); the shared reader maps them back. No earlier study uses those quarters.

**A.2 Further work.**
- **Who returns to non-employment.** Examine whether exits from first jobs are to study, unemployment or inactivity.
- **Earnings growth in first jobs.** Use the two to four quarters observed.
- **IMSS records.** Link formal first jobs to administrative records, for durations beyond a year.

## References

- Abel, M., Carranza, E., Geronimo, K. and Ortega, M.E. (2022). Can temporary wage incentives increase formal employment? Experimental evidence from Mexico. IZA Discussion Paper 15740. [L149]
- Conover, E., Khamis, M. and Pearlman, S. (2021). Job quality and labour market transitions: evidence from Mexican informal and formal workers. UNU-WIDER Working Paper 2021/23. [L159]
- Cruces, G., Ham, A. and Viollaz, M. (2012). Scarring effects of youth unemployment and informality: evidence from Brazil. CEDLAS/IZA working paper. [L158]
- Donovan, K., Lu, W.J. and Schoellman, T. (2023). Labor market dynamics and development. *Quarterly Journal of Economics* 138(4): 2287–2325. [L160]
- Oster, E. (2019). Unobservable selection and coefficient stability: theory and evidence. *Journal of Business & Economic Statistics* 37(2): 187–204. [L161]
