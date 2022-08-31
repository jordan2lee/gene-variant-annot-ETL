#!/usr/bin/env python

import sys
import gzip

MAF_Hugo = 0
MAF_Gene = 1
MAF_Center = 2
MAF_Build = 3
MAF_Chrom = 4
MAF_Start = 5
MAF_Stop = 6
MAF_Strand = 7
MAF_Ref = 10
MAF_Alt1 = 11
MAF_Alt2 = 12

VCF_HEADER="#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tTUMOR\tNORMAL"

with gzip.open(sys.argv[1], "rt") as handle, open(sys.argv[2], 'w') as out:
    out.write(VCF_HEADER)
    out.write('\n')
    for line in handle:
        if not line.startswith("#") and not line.startswith("Hugo_Symbol"):
            row = line.split("\t")
            alt = row[MAF_Alt2]
            alt = alt.replace("-", ".")
            orow = "{chrom}\t{pos}\t{id}\t{ref}\t{alt}".format(
                chrom=row[MAF_Chrom],
                pos=row[MAF_Start],
                id=".",
                ref=row[MAF_Ref],
                alt=alt,
            )
            out.write(orow)
            out.write('\n')
