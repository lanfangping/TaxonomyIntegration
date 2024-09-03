> review_edits.csv: review request sentences and their corresponding edits
   - doc_name: the unique identifier for the document
   - node_ix_src: the unique identifier for the request sentence in the ITG graph. The review documents in ITG format are available in the respective document folder in '/docs', and in the subfolder 'review'.
   - text_src: the request sentence
   - label: the type of the request sentence (i.e., 'Weakness', 'Edit suggestion_explicit', 'Edit suggestion_implicit')
   - edits: the realized edits related to the request sentence, separated by a semicolon. The content of each edit can be found in '/data_human/revision/edit_s.csv' by the 'id' attribute.
   - edits_count: the count of edits related to the request sentence

> review_sents_1000_binary.csv: 1000 samples for the review request extraction task (formulated as a binary classification problem). 
   - doc_name: the unique identifier for the review document
   - node_ix_src: the unique identifier for the review sentence in the ITG graph. The review documents in ITG format are available in the respective document folder in '/docs', and in the subfolder 'review'.
   - text_src: the review sentence
   - label: yes = the review sentence contains an edit request, no = the review sentence does not contain an edit request

> review_sents_1000.csv: same samples as in the review_sents_1000_binary.csv file, with the request type in 'label'.
   - doc_name: the unique identifier for the review document
   - node_ix_src: the unique identifier for the review sentence in the ITG graph. The review documents in ITG format are available in the respective document folder in '/docs', and in the subfolder 'review'.
   - text_src: the review sentence
   - label: No = the review sentence does not contain an edit request; 'Weakness'; 'Explicit edit suggestion'; 'Implicit edit suggestion'