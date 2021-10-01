import sys
from Bio.Seq import Seq
from Bio import SeqIO

from os import listdir, mkdir
from os.path import join, isdir


def remove_Condons(file):
    """Removes stop codons

    This function takes a file as input and removes stop codons 
    (TAG, TGA, TAA) from each sequence in a fasta file.
    
    Parameters
    ----------
    file : str
        fasta name file

    Returns
    -------
    record
        a sequence with stop codons removed
    """

    codon_stop_array = ["TAG", "TGA", "TAA"]

    for record in SeqIO.parse(file, "fasta"):
        tempRecordSeq = list(record.seq)
        for index in range(0, len(record.seq), 3):
            codon = record.seq[index:index+3]
            if codon in codon_stop_array:
                del tempRecordSeq[index:index+3]
        record.seq = Seq("".join(tempRecordSeq))
    return record


def processDirectory(path):
    """Creates a fasta file with stop codons removed 

    It takes a folder path and retrieves all fasta files in it.
    Then, removes stop codons from each file and concatenates them
    in a single sequence. 
    When the process is done is creates a fasta file named "output.fasta"
    
    Parameters
    ----------
    path : str
        path of the folder containing the fasta files
    """
    
    record_list = []
    for file in listdir(path):
        if file.lower().endswith(".fasta"):
            sequence = remove_Condons(join(path, file))
            record_list.append(sequence)

    SeqIO.write(record_list, join(join(path, "output"), "results.fasta"), 'fasta')
    print("Files sucesfully processed!")



def main():
    argv = sys.argv[1:]
    # check if passed arguments are correct
    if len(argv) == 1:
        directory = argv[0]
        # create a folder to hold the results
        folder_Output = join(directory, "output")
        CHECK_FOLDER = isdir(folder_Output)
        if not CHECK_FOLDER:
            mkdir(folder_Output)
        else:
            print(directory, "folder already exists.")

        # process the files
        processDirectory(directory)

    else:
        print("Bad Usage:\nExample usage: python main.py <folder-path>")


if __name__ == '__main__':
    main()
