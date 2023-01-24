import pyfastaq
import itertools

from cluster_vcf_records import vcf_clusterer


class Error(Exception):
    pass


class SimpleVcfMerger:
    """Merges samtools and cortex vcf files by filtering on samtools SNP QUAL score, minimum DP4 read depth, and minimum cortex GT confidence. Also filters for homozygous only before masking samtools calls by positions of cortex indels."""

    def __init__(
        self,
        samtools_vcf,
        cortex_vcf,
        output_vcf,
        reference_fasta,
        source="simple_vcf_merger",
        homozygous_only=False,
        max_REF_len=None,
        min_SNP_qual=None,
        min_dp4=None,
        min_GT_conf=None,
    ):
        self.samtools_vcf = samtools_vcf
        self.cortex_vcf = cortex_vcf
        self.output_vcf = output_vcf
        self.reference_seqs = {}
        pyfastaq.tasks.file_to_dict(reference_fasta, self.reference_seqs)
        for seq in self.reference_seqs.values():
            seq.seq = seq.seq.upper()
        self.source = source
        self.homozygous_only = homozygous_only
        self.max_REF_len = max_REF_len
        self.min_SNP_qual = min_SNP_qual
        self.min_dp4 = min_dp4
        self.min_GT_conf = min_GT_conf

    @classmethod
    def _merge_vcf_records(cls, vcf_records, ref_seq):
        """Merges VCF record dict, as made by cluster_vcf_records.vcf_file_read.vcf_file_to_dict()"""
        # for paranoia, should check that keys are same in each dict
        # and handle if they are not...
        for record in vcf_records:
            keys = vars(record)
            check = [
                "CHROM",
                "POS",
                "ID",
                "REF",
                "ALT",
                "QUAL",
                "FILTER",
                "INFO",
                "FORMAT",
            ]
            flag = False
            for key in check:
                if key not in keys:
                    flag = True
            if flag == True:
                raise Error("Error! At least 1 key is missing from vcf_records!")

        """This section creates a mask of the genome by creating a list of 1's where cortext indel postions are coded as zero.
        Samtools calls in this region are then thrown out."""

        mask = [1] * len(ref_seq)  # create mask vector of 1's
        indel_positions = (
            []
        )  # intialize variables and assign indel positions and lengths
        indel_lengths = {}

        for vcf_record in vcf_records:
            if vcf_record.FILTER == "PASS":
                indel_positions.append(vcf_record.POS)
                if vcf_record.INFO.get("SVTYPE") == "COMPLEX":
                    if int(len(vcf_record.REF)) >= int(len(vcf_record.ALT[0])):
                        indel_lengths[vcf_record.POS] = (
                            len(vcf_record.REF) - 1
                        )  # -1 adjusts for useless preceding nucleotide that is not removed
                    else:
                        indel_lengths[vcf_record.POS] = len(vcf_record.ALT[0]) - 1
                else:
                    indel_lengths[vcf_record.POS] = abs(
                        len(vcf_record.ALT[0]) - len(vcf_record.REF)
                    )

        for position in indel_positions:  # adds in cortex indel regions as [0] to mask
            mask[position : position + indel_lengths[position]] = itertools.repeat(
                0, ((position + indel_lengths[position]) - (position))
            )

        new_record = []
        odd_record = []
        for record in vcf_records:
            if (
                record.QUAL != None and mask[record.POS] == 0
            ):  # filters out samtools calls in masked regions
                pass
            elif "INDEL" in record.INFO:
                for position in indel_positions:
                    if position < record.POS:
                        check_start = position
                if (
                    record.POS - check_start > 1000
                ):  ##filters out samtools indels not located near with cortex indels
                    chuck = True
                else:
                    homopolymer = ref_seq[check_start + 1 : record.POS + 1]
                    chuck = all(
                        [i == homopolymer[0] for i in homopolymer]
                    )  ##checks for homopolymer between samtools call and cortex call
                if chuck == True:
                    pass
                else:
                    odd_record.append(record)
            else:
                new_record.append(record)  # creates new vcf of combined calls

        return new_record, odd_record

    def run(self):
        vcf_files = [self.samtools_vcf, self.cortex_vcf]
        sample_name, vcf_headers, vcf_records = vcf_clusterer.VcfClusterer._load_vcf_files(
            vcf_files,
            self.reference_seqs,
            homozygous_only=self.homozygous_only,
            max_REF_len=self.max_REF_len,
            min_SNP_qual=self.min_SNP_qual,
            min_dp4=self.min_dp4,
            min_GT_conf=self.min_GT_conf,
        )

        f_out = pyfastaq.utils.open_file_write(self.output_vcf)
        print("##fileformat=VCFv4.2", file=f_out)
        print("##source=", self.source, sep="", file=f_out)
        print(
            "#CHROM",
            "POS",
            "ID",
            "REF",
            "ALT",
            "QUAL",
            "FILTER",
            "INFO",
            "FORMAT",
            sample_name,
            sep="\t",
            file=f_out,
        )

        for ref_name in vcf_records:
            ref_seq = self.reference_seqs[ref_name]
            final_record, checks = SimpleVcfMerger._merge_vcf_records(
                vcf_records[ref_name], ref_seq
            )
            for row in final_record:
                print(row, file=f_out)
        pyfastaq.utils.close(f_out)
