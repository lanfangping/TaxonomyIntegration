> edit_summary_human_txt: human-written document edit summaries in text format
> edit_summary_human_itg: human-written document edit summaries in ITG format
> summary_edits.csv: summary sentences and their corresponding edits
   - doc_name: the unique identifier for the document
   - node_ix_src: the unique identifier for the summary sentence in the ITG graph
   - text_src: the summary sentence
   - edits: the corresponding edits to the summary sentence, separated by a semicolon. The content of each edit can be found in '/data_human/revision/edit_s.csv' by the 'id' attribute.
   - edits_count: the count of edits linked to the summary sentence