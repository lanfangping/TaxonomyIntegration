> edits_s.csv: sentence-level edit annotations with edit action and intent labels. See partition groups and further details in 'stats/edits_s_stat.json'.
   - edit_index: int, the unique identifier for the edit
   - id: str, the unique id for the edit in the format of 'N===O', where N is the new sentence ix and O is the old sentence ix. In cases of additions or deletions, O or N is 'nan'.
   - doc_name: the unique name of the document
   - node_ix_src: the unique id for the source node, i.e., the new sentence
   - node_ix_tgt: the unique id for the target node, i.e., the old sentence
   - text_src: the content of the new sentence
   - text_tgt: the content of the old sentence
   - a: the first human annotation of edit action (EA) and intent (EI), in the format of 'EA,EI'
   - b: the second human annotation of edit action (EA) and intent (EI), in the format of 'EA,EI'
   - c: the third human annotation of edit action (EA) and intent (EI), in the format of 'EA,EI'
   - gold: the gold label of edit action (EA) and intent (EI) aggregated through majority voting, in the format of 'EA,EI'
   - parent_node_src: id and node type of the parent node of the source node
   - parent_node_tgt: id and node type of the parent node of the target node
   - sec_node_src: id and node type of the section node containing the source node
   - sec_node_tgt: id and node type of the section node containing the target node
   - sec_id_src: the linear index of the section node containing the source node
   - sec_id_tgt: the linear index of the section node containing the target node
   - sec_title_src: the title of the section node containing the source node
   - sec_title_tgt: the title of the section node containing the target node

> edits_p.csv: paragraph-level edit annotations with lists of edit action and intent labels. See alignment groups and further details in 'stats/edits_p_stat.json'.
   - edit_index: int, the unique identifier for the paragraph-level edit
   - doc_name: the unique name of the document
   - node_ix_src: the unique id for the source node, i.e., the new paragraph
   - node_ix_tgt: the unique id for the target node, i.e., the old paragraph
   - gold: the list of sentence-level gold labels of edit action (EA) and intent (EI), separated by ';'
   - s_index: the list of sentence-level edit indices in the paragraph separated by ';', refer to 'edit_index' in edits_s.csv
   - node_type_src: the type of the source node, e.g., 'p' for paragraph
   - node_type_tgt: the type of the target node, e.g., 'p' for paragraph
   - sec_node_src: id and node type of the section node containing the source node
   - sec_node_tgt: id and node type of the section node containing the target node
   - sec_id_src: the linear index of the section node containing the source node
   - sec_id_tgt: the linear index of the section node containing the target node
   - sec_title_src: the title of the section node containing the source node
   - sec_title_tgt: the title of the section node containing the target node

> edits_sec.csv: section-level edit annotations with lists of edit action and intent labels. See alignment groups and further details in 'stats/edits_sec_stat.json'.
   - edit_index: int, the unique identifier for the section-level edit
   - doc_name: the unique name of the document
   - node_ix_src: the unique id for the source node, i.e., the new section
   - node_ix_tgt: the unique id for the target node, i.e., the old section
   - gold: the list of sentence-level gold labels of edit action (EA) and intent (EI), separated by ';'
   - s_index: the list of sentence-level edit indices in the section separated by ';', refer to 'edit_index' in edits_s.csv
   - p_index: the list of paragraph-level edit indices in the section separated by ';', refer to 'edit_index' in edits_p.csv
   - node_type_src: the type of the source node, e.g., 'title' for the node of the section title, which is used as the source node
   - node_type_tgt: the type of the target node, e.g., 'title' for the node of the section title, which is used as the source node
   - sec_id_src: the linear index of the section node 
   - sec_id_tgt: the linear index of the section node 
   - sec_title_src: the title of the section node 
   - sec_title_tgt: the title of the section node 

> edits_ss.csv: subsentence-level edit annotations for 1453 sentence revision pairs, with 3 annotations per sample.
   - edit_index: int, the unique identifier for the edit
   - doc_name: the unique name of the document
   - node_ix_src: the unique id for the source node, i.e., the new edit span. The values after '==' in the node ixs are the beginning and ending character offsets of the subsentence edit spans.
   - node_ix_tgt: the unique id for the target node, i.e., the old edit span. The values after '==' in the node ixs are the beginning and ending character offsets of the subsentence edit spans.
   - text_src: the content of the new edit span
   - text_tgt: the content of the old edit span
   - a: the first human annotation of edit action (EA) and intent (EI), in the format of 'EA,EI'
   - b: the second human annotation of edit action (EA) and intent (EI), in the format of 'EA,EI'
   - c: the third human annotation of edit action (EA) and intent (EI), in the format of 'EA,EI'
   - gold: the gold label of edit action (EA) and intent (EI) aggregated through majority voting, in the format of 'EA,EI'
   - node_type_src: the type of the source node, e.g., 'ss' for subsentence-level
   - node_type_tgt: the type of the target node, e.g., 'ss' for subsentence-level
   - parent_node_src: ix of the parent node of the source node, i.e., ix of the new sentence
   - parent_node_tgt: ix of the parent node of the target node, i.e., ix of the old sentence
   - s_index: the index of the corresponding sentence-level edit, refer to 'edit_index' in edits_s.csv

> edits_s_align.csv: the alignment of the sentence revision pairs. Data used for the revision alignment task. Negative samples are constructed by sentences from the same document but not aligned as a revision pair.
   - edit_index: the unique identifier for the edits in edit_s.csv. Empty for negative samples.
   - doc_name: the unique name of the document
   - node_ix_src: the unique id for the source node, i.e., the sentence in the new document
   - node_ix_tgt: the unique id for the target node, i.e., the sentence in the old document
   - text_src: the content of the sentence in the new document
   - text_tgt: the content of the sentence in the old document
   - label: the label of the alignment, 'yes' for positive samples and 'no' for negative samples