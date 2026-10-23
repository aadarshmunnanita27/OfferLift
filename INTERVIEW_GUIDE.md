# OfferLift: interview preparation

## Start with the business question

Which customers change their behavior because of a campaign? A high conversion probability alone does not answer that. A customer who would buy anyway can be a poor use of a costly promotion.

## 60-second explanation to learn, then personalize

“OfferLift studies the randomized Hillstrom email experiment. I trained separate conversion models for men's-email and control customers and ranked by their probability difference. I compared that ranking with conversion targeting and a random-policy baseline on held-out data. The campaign had a positive overall conversion effect, but my uplift ranking did not outperform random targeting on the test set. I report that limitation and bootstrap uncertainty instead of claiming business lift. The next step would be a validation-selected simpler policy and a prospective experiment.”

Use first-person language only after you understand and have worked through the implementation.

## Questions and answers

1. **Prediction versus causality?** Prediction estimates an outcome under observed conditions. A causal effect compares outcomes under two interventions. Random assignment helps identify average effects; ordinary observational associations may be confounded.
2. **Why this dataset?** It is a real randomized campaign with treatment and control, unlike fabricated promotion labels. It is still an old retail email experiment, not CRED customer data.
3. **Why only two arms?** The first version isolates men's email versus no email. Dropping the third randomized arm leaves approximately equal assignment probability, so e(X)=0.5 is used.
4. **What is the outcome?** Whether a customer converted during the two-week outcome window. Visit and spend are outcomes too and excluded from predictors.
5. **What is a T-learner?** Fit m1(X) on treated customers and m0(X) on controls. Estimate uplift as m1(X)-m0(X). Both models here are shallow gradient-boosted classifiers.
6. **Can you observe individual uplift?** No. Each customer is observed under only one assignment. You evaluate group-level or policy-level effects, not individual uplift labels.
7. **What is ATE?** Average treatment effect. In the test split, treated conversion rate minus control conversion rate is about 0.657 percentage points, with an approximate 95% interval of 0.253 to 1.061 points.
8. **What is CATE?** Conditional average treatment effect: expected outcome difference for customers with given features. It is not an observed personal counterfactual.
9. **Why not use classification accuracy to evaluate uplift?** Accurate outcome prediction does not necessarily rank treatment effects well. Evaluate incremental outcomes under targeting policies.
10. **How is the gain curve computed?** Use z=Y*T/0.5 - Y*(1-T)/0.5 = 2Y(2T-1). Sort customers by score, cumulate z and divide by the test population size. The curve estimates incremental conversions per population if the selected group were treated.
11. **What is the Qini definition here?** Trapezoidal area of the gain curve above the line from zero to the full-population gain, on 5% targeting increments. Other packages may normalize differently, so compare definitions before comparing values.
12. **How was the model selected?** Depth 1 versus depth 2, 80 trees each, validation Qini. Depth 2 won validation. The test set remained out of selection.
13. **What happened on test?** Uplift Qini was -0.000540; conversion targeting was +0.000258. The uplift bootstrap interval was approximately [-0.001787, 0.000716], including zero. No reliable targeting advantage is established.
14. **Why can the campaign work but the ranking fail?** A positive mean effect does not imply predictable heterogeneity. Rare outcomes and differences of two noisy predictions can make ranking unstable.
15. **What does the bootstrap capture?** Row-sampling variability on held-out outcomes conditional on fixed trained models. It omits training uncertainty. There are 300 percentile bootstrap replicates.
16. **Why not tune until test results improve?** That makes the test set part of model selection and biases reported performance. A new final evaluation or properly nested procedure is needed after exploration.
17. **What does simulated profit mean?** Estimated incremental conversions × assumed contribution margin − contacts × assumed contact cost. Neither margin nor email cost was measured in this dataset. It is a scenario, not observed business profit.
18. **How would you use this at CRED?** The experimental reasoning could inform a rewards or reminder study, but this email model cannot establish cashback or bill-payment treatment effects. Collect randomized data for the actual intervention.
19. **Which assumptions matter?** Random assignment, consistent treatment, no interference between customers, no relevant outcome-measurement bias, and enough data in both arms.
20. **What would you test next?** A simpler subgroup policy chosen using validation data, better-regularized effect estimation, and a prospective equal-budget policy comparison. Report guardrails like unsubscribe or complaint rates.

## Practice tasks

- Explain why a 10% purchase probability can still correspond to zero uplift.
- Manually compute IPW gain for six invented customers with known treatment and outcome.
- Recreate the overall difference in conversion rates with SQL.
- Explain the distinction between percentage points and relative percentage increase.
- Describe a prospective A/B test including randomization unit, primary metric, budget, power, and guardrails.

## Resume wording after you understand and verify it

Developed a deployed campaign-analysis app on a 64,000-customer randomized email experiment, implementing T-learner uplift modeling, held-out policy comparisons, bootstrap uncertainty and campaign-budget simulation.

Do not claim improved campaign ROI. The current test results do not support it. Discussing this honestly is a strength, not something to hide.
