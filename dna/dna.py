import csv
import sys


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    longest_run = 0
    subseq_len = len(subsequence)
    seq_len = len(sequence)

    for i in range(seq_len):
        count = 0
        while True:
            start = i + count * subseq_len
            end = start + subseq_len
            if sequence[start:end] == subsequence:
                count += 1
            else:
                break
        longest_run = max(longest_run, count)

    return longest_run


def main():
    # TODO: Check for command-line usage
    if len(sys.argv) != 3:
        print("Usage: python dna.py data.csv sequence.txt")
        sys.exit(1)

    database_file = sys.argv[1]
    sequence_file = sys.argv[2]

    # TODO: Read database file into a variable
    with open(database_file, "r") as file:
        reader = csv.DictReader(file)
        database = list(reader)
        strs = reader.fieldnames[1:]  # skip 'name'

    # TODO: Read DNA sequence file into a variable
    with open(sequence_file, "r") as file:
        dna_sequence = file.read().strip()

    # TODO: Find longest match of each STR in DNA sequence
    def longest_match(sequence, subseq):
        max_count = 0
        i = 0
        while i < len(sequence):
            count = 0
            while sequence[i:i+len(subseq)] == subseq:
                count += 1
                i += len(subseq)
            if count > max_count:
                max_count = count
            i += 1 if count == 0 else 0
        return max_count

    # TODO: Check database for matching profiles
    # Example STRs from your CSV header
    matches = {}
    for s in strs:
        matches[s] = longest_match(dna_sequence, s)

    # Check database
    for person in database:
        if all(int(person[s]) == matches[s] for s in strs):
            print(person["name"])
            break
    else:
        print("No match")

def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
