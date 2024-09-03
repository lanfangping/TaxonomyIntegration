## Re3: A Holistic Framework and Dataset for Modeling Collaborative Document Revision
#### Authors: Qian Ruan, Ilia Kuznetsov, Iryna Gurevych
#### UKP Lab, Technical University of Darmstadt, Germany
#### Contact: ruan@ukp.tu-darmstadt.de
#### Refer to the GitHub repository for the latest updates: https://github.com/UKPLab/re3
#### Scripts for dataset loading and processing, as well as for the tasks, can be found in the GitHub repository.

### Data Structure
> Re3-Sci_v1
   > data_human: collection of human annotations
     > response: human-written document edit summaries and the corresponding human annotations, see README in the subfolder for more details
     > review: human annotations of alignments between review requests and related edits, see README in the subfolder for more details
     > revision: human annotations of edits and edit action and intent labels, at sentence(s), paragraph(p), section(sec) and subsentence(ss) levels, see README in the subfolder for more details
   > docs: document revisions, reviews and document edit summaries in ITG format. The corresponding human annotations can be found in the CSV files within the 'data_human' directory, identified by the 'doc_name' attribute.
     > subfolder structure:
       > v1.json: the original document in ITG format
       > v2.json: the revised document in ITG format
       > review: the review document(s) in ITG format
       > response: the document edit summary in ITG format
   > tasks: 
     > instruction_tuning: data splits for the four NLP tasks using instruction tuning approaches, read the paper [1] and the README in the subfolder for more details.
       > edit_intent_classification
       > edit_intent_classification_AD
       > edit_intent_classification_M
       > revision_alignment
       > review_request_extraction
       > document_edit_summarization

### Cite
[1]. Qian Ruan, Ilia Kuznetsov, and Iryna Gurevych. 2024. Re3: A holistic framework and dataset for modeling collaborative document revision. ArXiv, cs.CL/2406.00197.744 . In Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Main Long Paper)
@article{ruan2024re3,
      title={Re3: A Holistic Framework and Dataset for Modeling Collaborative Document Revision},
      author={Qian Ruan and Ilia Kuznetsov and Iryna Gurevych},
      year={2024},
      journal={arXiv preprint arXiv:2406.00197},
      url={https://arxiv.org/abs/2406.00197},
}

