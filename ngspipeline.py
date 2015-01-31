import sys
import os

config = {}

#read config
def read_config():
	#configfile = sys.argv[1]
	configfile = 'ngsconfig'
	f = open(configfile, 'r')
	for line in f:
		if '#' not in line and len(line) > 2:
			line = line.strip().split(':')
			config[line[0]] = line[1]
	f.closed
	
#fast qc
def fastqc():
	try:
		cmd1 = 'fastqc %s' %(config['rawfile'])
		print cmd1
		os.system(cmd1)
	except KeyError:
		print 'No raw file specified'

#cut adapter
def cutadapt():
	try:
		cmd1 = 'cutadapt -a %s %s > %s' %(config['adapter'], config['rawfile'], config['cutadaptout'])
		print cmd1
		os.system(cmd1)
	except KeyError:
		print 'No raw file or adapter specified'

#assembly and map to reference
def tophat2():
	try:
		cmd1 = 'tophat2 -o %s %s %s' %(config['tophatout'], config['refindex'], config['cutadaptout'])
		print cmd1
		os.system(cmd1)
	except KeyError:
		print 'No ref genome specified or invalid output from cutadapt'
		
#sort and index bam file
def samtools():
	try:
		cmd1 = 'samtools sort %s/accepted_hits.bam %s' %(config['tophatout'], config['sortedfile'])
		print cmd1
		os.system(cmd1)
		cmd2 = 'samtools index %s.bam' %(config['sortedfile'])
		print cmd2
		os.system(cmd2)
	except KeyError:
		print 'Invalid tophat output folder'

#mark duplicates
def picard():
	#need to preset java home and class path for picard
	try:
		cmd1 = 'MarkDuplicates.jar INPUT=%s.bam OUTPUT=%s METRICS_FILE=%s_matrics' %(config['sortedfile'],  config['markdup'], config['markdup'])
		print cmd1
		os.system(cmd1)
	except KeyError:
		print 'Invalid setting for marking duplicate'
	
def run():
	read_config()
	try:
		fastqc() if config['quality_checking'] == '1' else 0
		cutadapt() if config['cutting_adapter'] == '1' else 0
		tophat2() if config['assembly'] == '1' else 0
		samtools() if config['sort_index_bamfile'] == '1' else 0
		picard() if config['mark_duplicate'] == '1' else 0
	except KeyError:
		print 'Error configuring modules'
	
run()
	

