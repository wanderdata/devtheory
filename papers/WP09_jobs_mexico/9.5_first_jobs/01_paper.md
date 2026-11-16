# First Jobs of Young Mexicans and Employment Three Quarters Later, 2005–2026

*Paul Wander. Working draft v0.2, 2026-11-16. Pre-analysis plan: [`00_pre_analysis_plan.md`](00_pre_analysis_plan.md). Generated tables: [`empirics/output/enoe/first_jobs/results.md`](../../../empirics/output/enoe/first_jobs/results.md). App: Jobs in Mexico, page 9.5.*

## Abstract

This paper identifies first jobs from respondents' own reports in Mexico's labour-force survey (ENOE). A first-job entrant is a person aged 15–24 who, at the first of five quarterly interviews, is not employed and reports never having worked, and who is employed at the second interview. Pooling 70 five-quarter panels from 2005–2019 and 2022–2026 gives 47,186 entrants, who are followed to the fifth interview, three quarters after entry. Of first jobs, 85.1% are informal, against 68.5% of all jobs held by employed 15–24-year-olds. Three quarters after entry, about half of those who entered informal jobs and 36% of those who entered formal jobs are not employed. In weighted linear probability models conditional on age, sex, schooling, school attendance, household employment, state, urban residence and quarter, entering an informal job is associated with a probability of formal employment three quarters later that is 3.4 percentage points higher (90% interval 3.0–3.7) than for never-worked young people who remained without work, whose rate is 2.5%. Entering a formal rather than an informal job is associated with a 34.0-point higher probability (32.3–35.8), an estimate that is sensitive to selection on unobservables.

## 1. Introduction

Most young Mexicans begin working in informal jobs. Whether this matters for their later employment depends on what such jobs lead to. An informal first job may provide skills, a work record and contacts that help a young person obtain formal employment later; it may also keep the person in informal work, or end in a return to inactivity.

The evidence for Latin America points in both directions. Using cohort data for Brazil, Cruces, Ham and Viollaz (2012) find that cohorts with higher youth informality have higher informality and lower wages as adults, mainly among the less educated. Using ENOE panels for workers aged 20–40, Conover, Khamis and Pearlman (2021) find that informal wage employees with at least upper-secondary schooling move into formal wage employment far more often than less-educated ones. Across countries, Donovan, Lu and Schoellman (2023) show that workers in poorer countries enter and leave jobs more often but move into better-paid jobs less often.

This paper differs from earlier work in two respects. First jobs are identified from the respondent's statement that they have never worked, rather than from age or tenure, and the job is observed within three months of its start. And entry into an informal job is compared with remaining out of work, which is the alternative open to a young person who declines an informal job. The paper tests four propositions stated in the pre-analysis plan: that first jobs are more informal than young people's jobs in general (P34); that entering an informal job raises the probability of later formal employment relative to remaining out of work (P35); that the formality of the first job persists (P36); and that, among informal first jobs, wage jobs in units with premises lead to formal employment more often than own-account or unpaid work (P37).

## 2. Data

ENOE interviews each dwelling in five consecutive quarters. The paper uses every quarter of 2005–2019 and of 2022 to mid-2026; 2020 and 2021 are excluded because fieldwork moved to the telephone and the questionnaire changed. Persons are linked across interviews by dwelling, household and person identifiers, with checks on sex and age, as in study 9.1. Of never-worked, non-employed 15–24-year-olds at a first interview, 91.5% are linked to the second interview and 76.5% to the fifth.

Question P2H asks everyone who is not employed whether they have ever worked; answer 4 means never. A first-job entrant is aged 15–24, not employed and has never worked at the first interview, and is employed at the second. The comparison group for P35 consists of persons who have never worked and are not employed at both the first and the second interview. Formality follows INEGI's labour-informality definition. Units with premises are INEGI's micro units with premises and small, medium and large establishments (codes 3–6 of `ambito2`).

The sample comprises 397,978 never-worked, non-employed persons aged 15–24 at a first interview, of whom 47,186 are employed, formally or informally, at the second.

## 3. Estimation

The outcome is formal employment at the fifth interview. Weighted linear probability models include an indicator for the type of entry and fixed effects for the quarter of the first interview, the state, single years of age, single years of schooling and the relationship to the household head, together with controls for sex, school attendance, the number of formally and of informally employed household members, and urban residence, all measured at the first interview. Weights are the survey weights at the first interview, and standard errors are clustered by primary sampling unit.

The comparisons condition on observed characteristics only. Unobserved motivation, contacts and reasons for not working could bias them in either direction. To assess this, the paper reports Oster's (2019) δ: the ratio of selection on unobservables to selection on observables that would reduce each coefficient to zero, computed with the maximum R² set at 1.3 and at 2 times the R² of the model with controls.

## 4. Results

### 4.1 Composition of first jobs

*Table 1. First jobs and all jobs of employed 15–24-year-olds (weighted shares)*

| | First jobs | All jobs, employed 15–24 |
|---|---|---|
| Informal | 85.1% | 68.5% |
| Wage employee | 63.2% | 78.9% |
| Unpaid worker | 27.9% | 13.2% |
| Own-account worker | 8.5% | 7.2% |
| Commerce | 27.4% | 22.0% |
| Restaurants and lodging | 12.7% | 9.6% |
| Manufacturing | 14.3% | 18.6% |
| Construction | 4.2% | 8.5% |

The informal share of first jobs is 16.6 percentage points higher than that of all jobs held by employed 15–24-year-olds. First jobs are more often unpaid, in commerce and in restaurants and lodging, and less often in manufacturing and construction. By type, 36.0% of first jobs are informal own-account or unpaid work, 29.1% informal wage jobs in units with premises, 19.9% other informal wage jobs and 14.9% formal jobs. Of the other informal wage jobs, 42% are in micro units without premises; most of the remainder are in units that INEGI does not classify by size.

Among entrants reporting earnings, the median formal first job pays 1.8 times the monthly minimum wage in force for a mean of 43 hours a week; informal wage jobs in units with premises pay a median of 1.0 times the minimum for 34 hours, and other informal wage jobs 0.8 times for 29 hours.

### 4.2 Employment three quarters after entry

*Table 2. Employment status at the fifth interview by type of first job (weighted shares, unadjusted)*

| Entry at the second interview | Formal | Informal | Not employed |
|---|---|---|---|
| Formal job | 47.8% | 16.6% | 35.6% |
| Informal wage job, unit with premises | 10.2% | 40.0% | 49.8% |
| Other informal wage job | 6.1% | 42.3% | 51.6% |
| Informal own-account or unpaid work | 3.9% | 39.3% | 56.9% |
| Not employed, never worked (comparison group) | 2.5% | 9.8% | 87.7% |

Between half and 57% of those who entered informal first jobs, and 36% of those who entered formal jobs, are not employed three quarters later. Formal employment at that point is reached by one in ten entrants into informal wage jobs in units with premises and by one in twenty-five entrants into informal own-account or unpaid work.

### 4.3 Conditional comparisons

*Table 3. Difference in the probability of formal employment at the fifth interview (percentage points; 90% interval; base = rate in the reference group)*

| Comparison | Estimate | 90% interval | Base | Oster δ (1.3 R², 2 R²) |
|---|---|---|---|---|
| Informal first job vs. remained without work | 3.4 | 3.0 to 3.7 | 2.5% | 14.6, 4.4 |
| Formal vs. informal first job | 34.0 | 32.3 to 35.8 | 6.5% | 3.2, 0.9 |
| Informal wage job with premises vs. informal own-account or unpaid work | 4.2 | 3.4 to 5.0 | 3.9% | 5.4, 1.6 |

Young people who entered an informal job are more likely to be formally employed three quarters later than comparable young people who remained without work. The difference of 3.4 points more than doubles a base of 2.5%, but leaves the probability at about 6%. Adding the controls reduces the difference only from 4.0 to 3.4 points, and selection on unobservables would have to be 4.4 to 14.6 times as strong as selection on observables to remove it. The difference is positive in each period, for women and men, among those not attending school, for ages 15–29 and for entry at the third interview (2.3 points over two quarters). It is larger for those with at least 12 years of schooling (6.0 points on a base of 5.0%) than for those with less (2.2 points on 1.7%), as in Conover, Khamis and Pearlman (2021).

Entrants into formal first jobs are 34.0 points more likely than entrants into informal first jobs to be formally employed three quarters later. The estimate ranges from 29.3 points (2022 onward) to 36.4 points (those not attending school) across samples, and the probit average marginal effect is 27.5 points. This comparison is the most exposed to selection: controls reduce it from 41.2 to 34.0 points, and selection on unobservables 3.2 times as strong as on observables, or 0.9 times with the higher maximum R², would remove it.

Among informal first jobs, wage jobs in units with premises are followed by formal employment 4.2 points more often than own-account or unpaid work, on a base of 3.9%. The difference is positive in every sample, from 3.0 points (2015–2019) to 6.4 points (12 or more years of schooling).

### 4.4 Propositions

Under the decision rules of the pre-analysis plan, P34 is supported (a difference of 16.6 points against a threshold of 10), P35 is supported (90% interval above zero), P36 is supported (lower bound 32.3 points against a threshold of 25) and P37 is rejected (upper bound 5.0 points, below the 10 points set as a material difference). P34 was a weak test, since the high informality of youth employment was known in advance.

## 5. Limitations

Of the never-worked persons who are still not employed at the second interview, 14.5% report having worked by then. Some had short jobs between interviews, which the survey does not observe; others answer inconsistently. Excluding them from the comparison group, as the plan specified, restricts it to people who remained out of work, and makes it somewhat less attached to the labour market than all non-entrants.

Three quarters is a short horizon. Transitions to formal employment that take longer cannot be observed in a five-quarter panel.

The comparisons are conditional associations. The Oster calculations suggest that the difference between informal entry and remaining without work is robust to substantial selection on unobservables, while the size of the difference between formal and informal entry is not.

The probit check was estimated with year rather than quarter effects and without clustered standard errors, for reasons of memory; only its point estimates are used.

## 6. Conclusions

Most first jobs of young Mexicans are informal, and many end within a year: half of informal entrants and a third of formal entrants are not employed three quarters after entry. Entering an informal job is associated with a higher subsequent probability of formal employment than remaining out of work, but from a low base, and about 6% of informal entrants are formally employed three quarters later. The largest observed difference is between formal and informal first jobs, but it is also the one most exposed to selection. If a substantial part of it reflects the jobs rather than the people who obtain them, measures that increase access to formal first jobs, such as hiring subsidies of the kind evaluated by Abel et al. (2022), would act on the margin with the largest potential effect. Administrative records that follow workers from their first formal job, or variation in access to formal first jobs unrelated to young people's characteristics, would be needed to establish this.

## Annex A. Implementation notes and further work

The analysis uses ENOE quarters through 2026Q2, the latest available. Controls that do not vary within a subsample (sex within a sex group, attendance among those not attending school) are dropped in that subsample. From 2025Q3 INEGI renamed the geographic codes (`cve_ent`, `cve_mun`); the shared reader maps them to the earlier names.

Further work could separate exits from first jobs into study, unemployment and inactivity (open question OQ-74); estimate how many first jobs fall between interviews (OQ-75); measure earnings growth over the quarters observed after entry; and link formal first jobs to IMSS records to follow them beyond a year.

## References

Abel, M., Carranza, E., Geronimo, K. and Ortega, M.E. (2022). Can temporary wage incentives increase formal employment? Experimental evidence from Mexico. IZA Discussion Paper 15740. [L149]

Conover, E., Khamis, M. and Pearlman, S. (2021). Job quality and labour market transitions: evidence from Mexican informal and formal workers. UNU-WIDER Working Paper 2021/23. [L159]

Cruces, G., Ham, A. and Viollaz, M. (2012). Scarring effects of youth unemployment and informality: evidence from Brazil. CEDLAS/IZA working paper. [L158]

Donovan, K., Lu, W.J. and Schoellman, T. (2023). Labor market dynamics and development. *Quarterly Journal of Economics* 138(4): 2287–2325. [L160]

Oster, E. (2019). Unobservable selection and coefficient stability: theory and evidence. *Journal of Business & Economic Statistics* 37(2): 187–204. [L161]
