import glob, uuid, os, argparse, random

from datetime import date, timedelta

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--organisation",default="University of Oxford",help="the name of the organisation (the user must belong to it otherwise validation will fail)")
    parser.add_argument("--country",default="United Kingdom",help="the name of the country where the samples were collected")
    parser.add_argument("--tech",default='Illumina',help="whether to generate illumina (paired) or nanopore (unpaired) reads")
    parser.add_argument("--tag_file",default='tags.txt',help="a plaintext file with one row per tag")
    parser.add_argument("--number_of_tags",required=True,type=int,help="how many tags to give each sample. Can be zero, or up to the number of rows in <tag_file>")
    options = parser.parse_args()

    assert options.tech in ['Illumina','Nanopore']

    tags=[]
    with open(options.tag_file,'r') as INPUT:
        for line in INPUT:
            tags.append(line.rstrip())

    assert options.number_of_tags>0
    assert options.number_of_tags<=len(tags)

    if options.tech=='Illumina':
        header='name,fastq,organisation,tags,specimenOrganism,host,collectionDate,country,submissionTitle,submissionDescription,instrument_platform,instrument_model,flowcell'
        file_list = glob.glob('*_1.fastq.gz')
        file_extensions = ['_1.fastq.gz','_2.fastq.gz']
    else:
        header='name,fastq1,fastq2,organisation,tags,specimenOrganism,host,collectionDate,country,submissionTitle,submissionDescription,instrument_platform,instrument_model,flowcell'
        file_list = glob.glob('*.fastq.gz')
        file_extensions = ['.fastq.gz']

    print(header)
    
    def build_rest_of_line():
        rest_of_line = options.organisation+','
        if options.number_of_tags==0:
            rest_of_line+=','
        elif options.number_of_tags==len(tags):
            for i in tags:
                rest_of_line+=i+':'
            rest_of_line=rest_of_line[:-1]+','
        else:
            for i in random.sample(tags,options.number_of_tags):
                rest_of_line+=i+':'
            rest_of_line=rest_of_line[:-1]+','
        rest_of_line+='SARS-CoV-2,human,'

        date_collected=str(date.today()-timedelta(days=random.choice(range(7))))
        rest_of_line+=date_collected+','
        rest_of_line+=options.country+','
        rest_of_line+='covid study,study of covid,'
        if options.tech=='Illumina':
            rest_of_line+="Illumina,HiSeq,96"
        elif options.tech=='Nanopore':
            rest_of_line+="Nanopore,GridION,96"

        return(rest_of_line)

    for i in file_list:

        if options.tech=='Illumina':
            filename=i.split('_1.fastq.gz')[0]
        else:            
            filename=i.split('.fastq.gz')[0]
            
        if '_' in filename:
            lineage=i.split('_')[0]
        else:
            lineage=filename

        uid=str(uuid.uuid4())

        rest_of_line=build_rest_of_line()

        for file_extension in file_extensions:
            os.rename(filename+file_extension,lineage+"_"+uid+file_extension)

        if options.tech=='Illumina':
            line=lineage+"_"+uid+','+lineage+"_"+uid+'_1.fastq.gz,'+lineage+"_"+uid+'_2.fastq.gz,'+rest_of_line
        else:
            line=lineage+"_"+uid+','+lineage+"_"+uid+'.fastq.gz,'+rest_of_line

        print(line)

#
#
#
# header='name,fastq,organisation,tags,specimenOrganism,host,collectionDate,country,submissionTitle,submissionDescription,instrument_platform,instrument_model,flowcell'
#
# print(header)
#
# rest_of_line=',University of Oxford,University_of_Oxford:HPRU,SARS-CoV-2,human,2021-10-20,United Kingdom,covid study,study of covid,Nanopore,GridION,96'
#
# for i in glob.glob('*.fastq.gz'):
#
#     filename=i.split('.fastq.gz')[0]
#
#     lineage=i.split('_')[0]
#
#     uid=str(uuid.uuid4())
#
#     for file_extension in ['.fastq.gz']:
#         os.rename(filename+file_extension,lineage+"_"+uid+file_extension)
#
#     line=lineage+"_"+uid+','+lineage+"_"+uid+'.fastq.gz'+rest_of_line
#
#     print(line)
