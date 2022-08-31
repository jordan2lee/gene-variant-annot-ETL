# gene-variant-annot-ETL
Gene Variant Annotation - ETL for database integration

# Set up
```
python3 -m venv venv
```
```
. venv/bin/activate
pip install -r requirements.txt
```

# Download MAF from GDC
Get an example MAF from GDC AWG portal (protected access) https://portal.awg.gdc.cancer.gov/ or use any MAF file. We will use a MuTect2 MAF (details in `gdc_manifest_brca-maf.txt`) 373dfc1d-8e9f-4132-9d23-81bd0a513e36.wxs.MuTect2.aliquot.maf.gz

```
tar -xf gdc_download_20220825_214206.583463.tar.gz
```

# Convert MAF to VCF
```
python scripts/maf2vcf.py data/maf/7478e5e1-7714-4b81-b098-1800964a9962/373dfc1d-8e9f-4132-9d23-81bd0a513e36.wxs.MuTect2.aliquot.maf.gz data/vcf/wxs.MuTect2.aliquot.vcf
```

# WIP - Run SnpEff - Input VCF into SnpEff

Install SnpEff https://pcingola.github.io/SnpEff/download/ where the directions from the url include:
```
# Download latest version
wget https://snpeff.blob.core.windows.net/versions/snpEff_latest_core.zip

# Unzip file
unzip snpEff_latest_core.zip
```

Install Java JDK
Go to https://docs.oracle.com/en/java/javase/16/install/installation-jdk-macos.html#GUID-2FE451B0-9572-4E38-A1A5-568B77B146DE and follow instractions
```
```

Now run SnpEff
```
docker build -t java .
docker run --rm -v `pwd`:/ java
java -Xmx8g -jar snpEff/snpEff.jar GRCh38 data/vcf/wxs.MuTect2.aliquot.vcf > data/vcf/wxs.MuTect2.aliquot.ann.vcf
```
