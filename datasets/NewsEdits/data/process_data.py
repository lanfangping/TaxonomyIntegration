import difflib

class DiffExtractor:
    def __init__(self) -> None:
        pass

    def tokenize(self, seq):
        return seq.split()

    def extract_diff(self, sentence1, sentence2):
        tokens1 = self.tokenize(sentence1)
        tokens2 = self.tokenize(sentence2)
        
        matcher = difflib.SequenceMatcher(None, tokens1, tokens2)
        diff_results = []

        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag == 'replace':
                diff_in_seq1 = ' '.join(tokens1[i1:i2])
                diff_in_seq2 = ' '.join(tokens2[j1:j2])
                diff_in_seq1_indices = [i1, i2]
                diff_in_seq2_indices = [j1, j2]

                diff_results.append({
                    'diff_in_seq1': diff_in_seq1,
                    'diff_in_seq2': diff_in_seq2,
                    'diff_in_seq1_indices': diff_in_seq1_indices,
                    'diff_in_seq2_indices': diff_in_seq2_indices
                })
            elif tag == 'delete':
                diff_in_seq1 = ' '.join(tokens1[i1:i2])
                diff_in_seq2 = ''
                diff_in_seq1_indices = [i1, i2]
                diff_in_seq2_indices = None

                diff_results.append({
                    'diff_in_seq1': diff_in_seq1,
                    'diff_in_seq2': diff_in_seq2,
                    'diff_in_seq1_indices': diff_in_seq1_indices,
                    'diff_in_seq2_indices': diff_in_seq2_indices
                })
            elif tag == 'insert':
                diff_in_seq1 = ''
                diff_in_seq2 = ' '.join(tokens2[j1:j2])
                diff_in_seq1_indices = None
                diff_in_seq2_indices = [j1, j2]

                diff_results.append({
                    'diff_in_seq1': diff_in_seq1,
                    'diff_in_seq2': diff_in_seq2,
                    'diff_in_seq1_indices': diff_in_seq1_indices,
                    'diff_in_seq2_indices': diff_in_seq2_indices
                })

        return diff_results

    def parse_edits_in_revision(sentence1, sentence2):

        return 


if __name__ == '__main__':
    sentence1 = """< p > A Massachusetts police officer described as a " great family man and officer " died Sunday after a man attacked him with a rock , then took the cop 's gun and shot him in the head and chest , officials said ."""
    sentence2 = """< p > A Massachusetts police officer and an elderly woman were killed Sunday after a suspect attacked the officer with a rock , took his gun and shot him in the head and chest , officials said ."""

    # sentence1 = """< p > According to the letter , a uniformed Border Patrol agent noticed a group on the Rio Grande River flood plain south of the Tornillo , Texas , Port of Entry , taking photos of the holding facility ."""
    # sentence2 = """The mayor and his security detail were spotted taking photos by a Border Patrol agent on the Rio Grande River flood plain south of the Tornillo , Texas , Port of Entry ."""

    # sentence1 = """< p > Lopes was arrested and rushed to a hospital with injuries that were not life - threatening ."""
    # sentence2 = """< p > Lopes was arrested and taken to a hospital with injuries that were not life - threatening ."""

    extractor = DiffExtractor()
    diff_results = extractor.extract_diff(sentence1, sentence2)
    for diff in diff_results:
        print(diff)