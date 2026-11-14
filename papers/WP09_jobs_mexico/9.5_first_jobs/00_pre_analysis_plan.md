# Study 9.5 — Where careers start: first jobs of young Mexicans and where they lead

*Paul Wander. Pre-analysis plan v0.1, 2026-11-13. Written before any outcome was computed. The only data checks so far: the never-worked question exists with the same coding in 2005, 2012, 2019 and 2023, and its frequency (D-057).*

## 1. Question and propositions

Most young Mexicans' first jobs are informal. Whether that matters depends on what happens next.
- **Stepping stone.** An informal job may teach skills and signal effort, and lead to formal work.
- **Trap.** It may keep young people in informal work.

Earlier evidence:
- With Brazilian cohort data, Cruces, Ham and Viollaz (2012) find that youth informality raises later informality and lowers wages, mainly for the less educated.
- With ENOE, Conover, Khamis and Pearlman (2021) find that informal wage work leads to formal work for the better educated more than for the rest.
- Across 49 countries, Donovan, Lu and Schoellman (2023) describe a "slippery" job ladder: in poor countries workers enter and leave jobs often, but rarely reach or keep better-paid ones.

This study follows young people from the quarter in which they take their first job, on their own report, and compares where they are three quarters later by the type of that job. Taking an informal first job is also compared with continuing not to work.

**P34. First jobs are more informal than young people's jobs in general.**
- **Supported if** the informal share of first jobs (entrants aged 15–24) exceeds the informal share of all jobs held by employed 15–24-year-olds by at least 10 percentage points, pooled over the period.
- **Rejected if** the difference is below 3 points.

**P35. Informal first jobs are stepping stones, not traps.** Among young people aged 15–24 who have never worked and are not employed at their first interview, those who start an informal job by the second interview are more likely to be formally employed at the fifth interview than those still not employed at the second. The comparison conditions on observables (§3).
- **Supported if** the difference is positive with a 90% interval above zero.
- **Rejected,** in the sense that an informal first job is a trap relative to continued search, if the 90% interval is below zero.
- **Inconclusive** otherwise.

**P36. The formality of the first job persists.** Conditional on the same observables, entrants into formal first jobs are at least 25 percentage points more likely to be formally employed three quarters later than entrants into informal first jobs.
- **Supported if** the lower end of the 90% interval is at least 25 points.
- **Rejected if** the upper end is below 25.
- **Inconclusive** otherwise.

**P37. Among informal first jobs, wage jobs in established units lead to formal work more often than own-account or unpaid family work.** Wage employment in units with premises (INEGI's micro units with premises, small, medium and large establishments) is compared with own-account and unpaid family work.
- **Supported if,** conditional on observables, the probability of formal employment three quarters later is at least 10 points higher in the first group, with a 90% interval above zero.
- **Rejected if** the 90% interval excludes 10 points from above, that is if the upper end is below 10.

## 2. Data and definitions

- **Survey.** ENOE, all quarters from 2005Q1 to 2019Q4 and from 2022Q1 to the latest available. 2020–2021 are excluded because of the telephone survey and the change to ENOE^N. Panels of five consecutive quarters are built with the linkage of study 9.1 (`enoe_link`), within each of the two periods.
- **Never worked.** Answer 4 to question P2H ("¿ha trabajado alguna vez en su vida?"), asked of everyone not employed.
- **First-job entrant.** A person aged 15–24 at the first interview who is not employed and has never worked at the first interview, and is employed at the second.
  - The first job is described at the second interview: formal or informal (`emp_ppal`), position (`pos_ocu`: wage employee, employer, own-account, unpaid), INEGI size class and type of unit (`ambito2`), sector (`rama_est2`), hours and monthly earnings.
  - Outcomes are measured at the fifth interview, three quarters after the second.
- **Comparison group (P35).** Persons aged 15–24 who have never worked and are not employed at both the first and the second interview, followed to the fifth.
- **Stock of young workers (P34).** All employed persons aged 15–24, every quarter, weighted.
- **Weights.** Survey weights at the first interview.
- **Attrition.** Persons not linked to the fifth interview are dropped. Robustness: inverse-probability weights for being linked, as in study 9.1, estimated on characteristics at the second interview.

## 3. Estimation

**Outcomes at the fifth interview:**
- formally employed;
- informally employed;
- not employed;
- (among the employed) a wage employee in a unit with premises.

**Linear probability models** with survey weights:

  y_i = Σ_k γ_k · D_ik + X_i'β + δ_{quarter of first interview} + μ_state + ε_i

- **D:** indicators for the type of entry. P35 compares informal entry against no entry; P36 formal against informal entry; P37 informal wage work in units with premises against informal own-account or unpaid work.
- **X**, measured at the first interview:
  - age (single years);
  - sex;
  - years of schooling (single years) and whether attending school;
  - relationship to the household head;
  - number of household members aged 15+ who are employed, formally and informally;
  - urban (self-represented city) or not.
- **Standard errors:** clustered by primary sampling unit.

**Descriptives** (no propositions attached):
- The composition of first jobs against the stock of young workers' jobs.
- Transition matrices from entry to the fifth interview, by type of first job.
- Results by period (2005–2008, 2009–2014, 2015–2019, 2022 onward), by sex, and by schooling below or at least 12 years.
- Monthly earnings of first jobs relative to the minimum wage in force.

**What the comparison can and cannot show.** P35 compares people who take an informal job with people who do not, conditional on observables. Unobserved differences (motivation, contacts, the reason for not working) bias the difference in an unknown direction. Two checks bound the problem:
- the same comparison among people not attending school at the first interview, for whom the reason for not working is less likely to be study;
- the sensitivity of the estimate to adding the controls, reported in the manner of Oster (2019): how large selection on unobservables would have to be, relative to selection on observables, to bring the difference to zero.

## 4. Robustness

- Ages 15–29.
- Entry at the third interview, with outcomes at the fifth (two quarters).
- Attrition weights.
- Excluding 2022 onward (ENOE^N).
- Probit average marginal effects instead of linear probability models, for P35 and P36.

## 5. What would change the conclusions

- **Recall of earlier work.** If the never-worked answer is unreliable (young people with casual earlier work answering "never"), first jobs would include some later jobs. As a check, the paper reports the share of never-worked answers that switch to "has worked" without an intervening employed interview.
- **Too short a window.** Three quarters may be too short to see stepping stones that take longer. The ENOE panel cannot follow people beyond five interviews.
