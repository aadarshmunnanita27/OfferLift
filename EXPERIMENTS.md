# Actual experiment log

- Source: Kevin Hillstrom's 2008 experiment, 64,000 rows, three randomized arms.
- Original download returned HTTP 503; used public CSV mirror in W-Tran/uplift-modelling. Raw SHA-256 recorded in metrics.json.
- Modeled men's email versus no email: 42,613 customers.
- Outcome: conversion. Only pre-treatment features included.
- Seed 42, stratification on assignment plus outcome: train 25,567, validation 8,523, test 8,523.
- Two T-learners compared: depth 1 and depth 2. Each uses separate arm models, 80 trees, minimum leaf 150, learning rate 0.04.
- Validation Qini: depth 1 = 0.000540, depth 2 = 0.000598. Selected depth 2.
- Held-out uplift Qini = -0.000540. Conversion ranking Qini = 0.000258.
- 300 row-bootstrap held-out uplift Qini 95% interval = [-0.001787, 0.000716].
- Held-out ATE = 0.006573 (0.657 percentage points), approximate 95% interval [0.002531, 0.010614].
- Interpretation: positive overall campaign effect; no evidence the selected uplift ranking improves on random targeting.
- No test-driven retraining was used to conceal the unfavorable ranking result.
- Deployment uses exported browser models; Streamlit alternative included. Profit is hypothetical and expressly labeled.

Future experiments, not completed claims: stronger regularization, validation-selected subgroup policies, doubly robust evaluation, prospective randomized policy comparison.
