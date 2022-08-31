# gene-variant-annot-ETL
Gene Variant Annotation - ETL for database integration

# Set up
Create Conda Environment - One time```
# Update base conda
conda update -n base -c defaults conda
# Create environment
conda create --prefix env-conda -y
```

Activate Conda Environment```
conda activate env-conda
```

Install deps - One time```
conda install -c conda-forge openjdk
```
Note that JDK 12 or higher required for running SNPEff. Installed JDK version 17

# Download MAF from GDC
Get an example MAF from GDC AWG portal (protected access) https://portal.awg.gdc.cancer.gov/ or use any MAF file. We will use a MuTect2 MAF (details in `gdc_manifest_brca-maf.txt`) 373dfc1d-8e9f-4132-9d23-81bd0a513e36.wxs.MuTect2.aliquot.maf.gz

```
tar -xf gdc_download_20220825_214206.583463.tar.gz
```

# Convert MAF to VCF
```
python scripts/maf2vcf.py data/maf/7478e5e1-7714-4b81-b098-1800964a9962/373dfc1d-8e9f-4132-9d23-81bd0a513e36.wxs.MuTect2.aliquot.maf.gz data/vcf/wxs.MuTect2.aliquot.vcf
```

# Run SnpEff - Input VCF into SnpEff
Install SnpEff https://pcingola.github.io/SnpEff/download/ where the directions from the url include:
```
# Download latest version
wget https://snpeff.blob.core.windows.net/versions/snpEff_latest_core.zip

# Unzip file
unzip snpEff_latest_core.zip
```

> Make sure that conda environment has been activated

> JDK v12 or higher required to run Java commands for SNPEff

Now run SnpEff
```
java -Xmx8g -jar snpEff/snpEff.jar GRCh38.86 data/vcf/wxs.MuTect2.aliquot.vcf > data/vcf/wxs.MuTect2.aliquot.ann.vcf
```

### Alternative genome build versions for SNPEff
We used GR38.86 for our reference genome. To view other builds run `java -Xmx4g -jar snpEff.jar databases | grep GRCh38`
