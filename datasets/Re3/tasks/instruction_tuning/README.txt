This folder contains data splits for the four NLP tasks using instruction-tuning approaches, as described in the paper [1].
For more details about the tasks, please refer to the paper.
We use 20% of the data for training, specifically for demonstration example selection, and the remaining 80% for testing to obtain more reliable performance estimates.

[1]. Qian Ruan, Ilia Kuznetsov, and Iryna Gurevych. 2024. Re3: A holistic framework and dataset for modeling collaborative document revision. ArXiv, cs.CL/2406.00197.744 . In Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Main Long Paper).

> files in edit_intent_classification / edit_intent_classification_AD / edit_intent_classification_M
   - edit_index: the unique identifier for the edit
   - doc_name: the unique name of the document
   - node_ix_src: the unique id for the source node, i.e., the new sentence
   - node_ix_tgt: the unique id for the target node, i.e., the old sentence
   - text_src: the content of the new sentence
   - text_tgt: the content of the old sentence
   - gold: the gold label of edit action (EA) and intent (EI) aggregated through majority voting, in the format of 'EA,EI'
   - label: the intent label

> files in revision_alignment
   - edit_index: the unique identifier for the edits in edit_s.csv. Empty for negative samples.
   - doc_name: the unique name of the document
   - node_ix_src: the unique id for the source node, i.e., the sentence in the new document
   - node_ix_tgt: the unique id for the target node, i.e., the sentence in the old document
   - text_src: the content of the sentence in the new document
   - text_tgt: the content of the sentence in the old document
   - label: the label of the alignment, 'yes' for positive samples and 'no' for negative samples

> files in review_request_extraction
   - doc_name: the unique identifier for the review document
   - node_ix_src: the unique identifier for the review sentence in the ITG graph. The review documents in ITG format are available in the respective document folder in '/docs', and in the subfolder 'review'.
   - text_src: the review sentence
   - label: yes = the review sentence contains an edit request, no = the review sentence does not contain an edit request

> files in document_edit_summarization
   - doc_name: the unique identifier for the document
   - text_src: the content of the new sentence
   - text_tgt: the content of the old sentence
   - gold: the gold label of the edit action (EA) and intent (EI) aggregated through majority voting, in the format of 'EA,EI'
   - sec_title_src: the section title of the new sentence
   - sec_title_tgt: the section title of the old sentence
