# OODREB
The out-of-distribution relation extraction dataset and the source code of paper (OODREB: Benchmarking State-of-the-Art methods for Out-Of-Distribution Generalization on Relation Extraction) accepted by WWW2024.

## Datasets and Processing
The dataset consists of samples from 7 human-annotated datasets, including DocRED, CoNLL04, FewRel, TACRED, KBP-37, SciERC, SemEval, 2010 Task 8, and TACRED. The dataset is stored in the `data` folder. The `source` folder contains the files resulting from partitioning the `general_red.json` file according to respective datasets.

## How to Analyze the SOTA Models through OODREB
We conducted experiments on five different models, namely SciBERT, ATLOP, DocuNet, KD, and EIDER. To test the robustness and generalization ability, we applied entity adversarial attacks, primarily consisting of three methods: mask entity attack(EM), randomly shuffled entity attack(ER), and unseen entity substitution attack(ES).