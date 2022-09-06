# gene-variant-annot-ETL
Gene Variant Annotation - ETL for database integration

# Associated GitHub Repositories
The main analysis will take place in `https://github.com/kellrott/bmeg-etl-alchemist` but here are the full list of associated repos

+ https://github.com/bmeg/sifter
+ https://github.com/bmeg/bmeg-dictionary/tree/gene-drug-association
+ https://github.com/bmeg/bmeg-etl

All except sifter will be added as a [Git Submodule](https://git-scm.com/book/en/v2/Git-Tools-Submodules). Instructions below on adding these submodules.

# Set up
1. Create Conda Environment - One time
```commandline
# Update base conda
conda update -n base -c defaults conda
# Create environment
conda create --prefix env-conda -y
```

2. Activate Conda Environment
```commandline
conda activate env-conda
```

3. Install deps - One time

3A. Download Go version 1.18 or higher https://go.dev/

3B. JDK for Java
```commandline
conda install -c conda-forge openjdk
```
Note that JDK 12 or higher required for running SNPEff. Installed JDK version 17


# Build Required Binaries
Clone and build binaries for Lathe and Sifter. Then add to $PATH (ex. working environment bin).

Git clone via ssh protocol:

Sifter (`flame` branch as of 9/2/22, or use `main` branch)
```commandline
git clone git@github.com:bmeg/sifter.git
cd sifter
git checkout flame
go build ./
```

# Download MAF from GDC
Get an example MAF from GDC AWG portal (protected access) https://portal.awg.gdc.cancer.gov/ or use any MAF file. We will use a MuTect2 MAF (details in `gdc_manifest_brca-maf.txt`) 373dfc1d-8e9f-4132-9d23-81bd0a513e36.wxs.MuTect2.aliquot.maf.gz

```commandline
tar -xf gdc_download_20220825_214206.583463.tar.gz
```

# Convert MAF to VCF
```commandline
python scripts/maf2vcf.py data/maf/7478e5e1-7714-4b81-b098-1800964a9962/373dfc1d-8e9f-4132-9d23-81bd0a513e36.wxs.MuTect2.aliquot.maf.gz data/vcf/wxs.MuTect2.aliquot.vcf
```

# Run SnpEff - Input VCF into SnpEff
Install SnpEff https://pcingola.github.io/SnpEff/download/ where the directions from the url include:
```commandline
# Download latest version
wget https://snpeff.blob.core.windows.net/versions/snpEff_latest_core.zip

# Unzip file
unzip snpEff_latest_core.zip
```

> Make sure that conda environment has been activated

> JDK v12 or higher required to run Java commands for SNPEff

Now run SnpEff
```commandline
java -Xmx8g -jar snpEff/snpEff.jar GRCh38.86 data/vcf/wxs.MuTect2.aliquot.vcf > data/vcf/wxs.MuTect2.aliquot.ann.vcf
```

### Alternative genome build versions for SNPEff
We used GR38.86 for our reference genome. To view other builds run `java -Xmx4g -jar snpEff.jar databases | grep GRCh38`

# Adding BMEG ETL Submodule
```commandline
git submodule add https://github.com/bmeg/bmeg-etl
cd bmeg-etl
git checkout flow
git checkout -b allele
cd ..
git submodule update --init --recursive
```

Which should output similar lines:
```
Submodule path 'bmeg-etl': checked out '1bad97678888c5228eec07c9fc1c6f4cd3439eb4'
Submodule 'src/bmeg/bmeg-dictionary' (https://github.com/bmeg/bmeg-dictionary.git) registered for path 'bmeg-etl/src/bmeg/bmeg-dictionary'
Submodule 'tools/vcf2maf-tools' (https://github.com/OpenGenomics/vcf2maf-tools.git) registered for path 'bmeg-etl/tools/vcf2maf-tools'
Cloning into '/Users/leejor/Ellrott_Lab/11_ALCHEMIST/gene-variant-annot-ETL/bmeg-etl/src/bmeg/bmeg-dictionary'...
Cloning into '/Users/leejor/Ellrott_Lab/11_ALCHEMIST/gene-variant-annot-ETL/bmeg-etl/tools/vcf2maf-tools'...
Submodule path 'bmeg-etl/src/bmeg/bmeg-dictionary': checked out 'e30176b8448d4cf95cf4d8a8b8c5310b36e2c4b5'
Submodule path 'bmeg-etl/tools/vcf2maf-tools': checked out '7ba1342728c6e31d296a6d18853c93f2f7a883b1'
```

# Allele ETL
First we will need to add the data model (data dictionary) as a [submodule](https://git-scm.com/book/en/v2/Git-Tools-Submodules).

Add `bmeg-dictionary` as a submodule and track the main branch `develop` (as of 9/2/22)
```commandline
git submodule add https://github.com/bmeg/bmeg-dictionary
git submodule update --init --recursive
```

Run SNPEff transform. Create JSON strings containing harmonized data ready for database import.

Create output JSON file location
```
output/snpeff
```

Transform and harmonize data
```commandline
sifter/sifter run transform/allele/allele_transform.yaml
```

# VCF Background
Purpose: format into json files the relevant data to be imported into BMEG. This will create the format expected by BMEG.

First, understand the VCF format fields:
```
1 Chromosome

2 Co-ordinate - The start coordinate of the variant.

3 Identifier

4 Reference allele - The reference allele is whatever is found in the reference genome. It is not necessarily the major allele.

5 Alternative allele - The alternative allele is the allele found in the sample you are studying.

6 Score - Quality score out of 100.

7 Pass/fail - If it passed quality filters.

8 Further information - Allows you to provide further information on the variants. Keys in the INFO field can be defined in header lines above the table.

9 Information about the following columns - The GT in the FORMAT column tells us to expect genotypes in the following columns.

10 Individual identifier (optional) - The previous column told us to expect to see genotypes here. The genotype is in the form 0|1, where 0 indicates the reference allele and 1 indicates the alternative allele, i.e it is heterozygous. The vertical pipe | indicates that the genotype is phased, and is used to indicate which chromosome the alleles are on. If this is a slash / rather than a vertical pipe, it means we don’t know which chromosome they are on.
```

## WIP - BMEG Authenticate - Only for testing purposes to see examples

Create BMEG credential file from [bmeg.io](https://bmeg.io/) under Analyze > Getting Started > Authentication

Store credential file as `secrets/bmeg_credentials.json`
