#import json
import time
import psycopg2
import psycopg2.extras
from connector import connect_DB as connect
from builder import build_JSON as build
from selector import report_selector as selector
from constructor import report_construction
from file_check import check_file
from report_list import report_list_maker

connection = connect() #connects to the DB
selector = selector() #holds lists of reports to be generated for each MSA
cur = connection.connect() #creates cursor object connected to HMDAPub2013 sql database, locally hosted postgres
selector.get_report_lists('MSAinputs2013.csv') #fills the dictionary of lists of reports to be generated
build_msa = build() #instantiate the build object for file path, jekyll files
build_msa.msas_in_state(cur, selector, 'aggregate') #creates a list of all MSAs in each state and places the file in the state's aggregate folder
#build_msa.msas_in_state(cur, selector, 'disclosure')#creates a list of all MSAs in each state and places the file in the state's disclosure folder

#List of Alabama MSAs for test state case
'''
AL_MSAs =[
'29260', '47900', '31980', '11820', '20700', '36740', '36860', '43740', '49380', '42780', '39940', '46860', '11780', '18220', '37700', '40380', '43940', '12900',
'42140', '46700', '36420', '33340', '39380', '38380', '39740', '42340', '39060', '26260', '10620', '32580', '39220', '42900', '41580', '36780', '20140', '15500',
'46460', '25340', '17260', '36060', '16180', '40740', '26940', '26900', '16260', '14260', '29340', '11460', '45460', '32820', '29860', '35580', '25820', '26220',
'34660', '38940', '46140', '31660', '48140', '27100', '12620', '16100', '32740', '49420', '44020', '37300', '47920', '29100', '36380', '16300', '24220', '17540',
'10580', '20460', '41540', '20540', '44180', '26740', '39340', '49300', '46100', '36660', '24860', '48300', '32340', '48100', '13940', '17580', '13540', '34060',
'25020', '31700', '19860', '38540', '19260', '32860', '28740', '18020', '38860', '22520', '47020', '28860', '18460', '18980', '33620', '14860', '43380', '28780',
'13900', '32220', '15820', '20380', '36620', '11100', '44860', '26780', '43780', '30100', '36460', '29220', '32460', '29620', '13100', '32060', '32420', '16340',
'27540', '45380', '33700', '32780', '47080', '46660', '15140', '38580', '48700', '29020', '17700', '16580', '44260', '41460', '27860', '29780', '14740', '17900',
'17820', '26380', '28940', '28580', '22980', '44540', '29500', '49700', '43660', '21740', '26340', '33820', '47620', '30300', '34340', '41820', '39540', '29300',
'46260', '47540', '17780', '12540', '35740', '42680', '30860', '40100', '36580', '18260', '21540', '25620', '37780', '46300', '43140', '44660', '28820', '33100',
'19220', '25220', '39580', '26820', '17140', '48660', '47700', '30620', '27220', '42700', '38460', '40220', '19020', '16420', '27420', '12940', '38420', '46500',
'41100', '21380', '43180', '47940', '17980', '35380', '15260', '33860', '20420', '26140', '30280', '48740', '30580', '24700', '28380', '32280', '34900', '21020',
'35500', '12740', '49180', '35020', '44300', '37380', '31260', '31820', '10380', '32380', '20820', '32100', '46740', '11340', '10260', '27020', '16540', '17220',
'12980', '13460', '44420', '14380', '42940', '44700', '28260', '14460', '15340', '17020', '40060', '24260', '12660', '14140', '30340', '33780', '24900', '13700',
'43860', '41060', '10420', '41260', '31500', '42300', '47180', '19340', '12140', '38820', '42580', '25180', '30700', '27740', '36220', '20060', '11420', '47580',
'28180', '14420', '23620', '29820', '24580', '36900', '15620', '34260', '31340', '41660', '43420', '45300', '34500', '48940', '10820', '21420', '36180', '10020',
'10660', '16620', '19820', '17300', '14620', '29700', '16980', '13660', '39900', '11380', '47300', '33220', '39140', '29060', '11540', '35900', '43340', '33540',
'33460', '21060', '26300', '10780', '25100', '31420', '13180', '30060', '26420', '43460', '25580', '42060', '40700', '23900', '29940', '14060', '22840', '42820',
'48460', '23380', '37820', '33180', '31380', '13620', '27460', '38900', '34700', '46180', '23340', '27580', '12020', '26540', '35820', '14100', '40760', '35460',
'23580', '40260', '31140', '22500', '46340', '48980', '31100', '19780', '22580', '33260', '29460', '18300', '22280', '33980', '44740', '18820', '34220', '14700',
'46380', '43900', '37140', '33380', '11900', '31540', '11580', '45540', '39500', '23940', '22020', '32940', '44060', '19060', '27180', '40940', '39260', '45980',
'19460', '31740', '24500', '30460', '30420', '25500', '25300', '48220', '37420', '30740', '43300', '11660', '22620', '31460', '21460', '48820', '11020', '42420',
'43100', '21340', '35860', '25900', '35980', '21660', '13300', '19660', '28020', '26660', '29900', '36260', '25380', '25780', '21940', '37800', '47340', '42380',
'43320', '14180', '47380', '31920', '40980', '35260', '10500', '26620', '24660', '41740', '18900', '47220', '46220', '45060', '32300', '20020', '40420', '44340',
'42100', '35420', '29660', '46060', '22220', '32980', '28140', '43700', '49540', '10220', '34980', '17420', '23240', '16060', '30820', '47500', '12220', '12460',
'13860', '11060', '37460', '40080', '29420', '16220', '34300', '35840', '12100', '44220', '29580', '47660', '22420', '29740', '37540', '47460', '25980', '37620',
'11140', '13500', '38740', '42740', '10540', '25260', '32140', '32260', '10900', '21580', '46540', '34540', '20220', '36540', '36500', '24780', '42500', '37220',
'39100', '25940', '18580', '32660', '35700', '27340', '36340', '40140', '17340', '13220', '40820', '24140', '49460', '45740', '22900', '48180', '46980', '23780',
'29380', '29980', '31180', '13980', '45620', '10100', '41620', '31060', '28900', '25420', '34020', '34860', '31860', '38660', '33020', '24940', '37580', '29180',
'47420', '45340', '43060', '47820', '26480', '34140', '17740', '25760', '44100', '36940', '13140', '20500', '45140', '33060', '12060', '10880', '18060', '34420',
'27260', '11620', '20620', '28340', '41700', '42220', '45780', '13380', '24340', '22340', '25860', '34460', '18740', '44500', '35220', '13020', '24820', '37060',
'40500', '37020', '39780', '48900', '40780', '12580', '10460', '21140', '27140', '16500', '24460', '33500', '19760', '18620', '11940', '25540', '16860', '35300',
'30500', '19580', '24420', '45500', '46900', '47260', '18380', '17200', '19300', '35060', '48500', '12300', '26020', '15180', '19540', '35340', '14020', '22180',
'30380', '33300', '10940', '17860', '22780', '26500', '43580', '19980', '22380', '36980', '18180', '34100', '10860', '19380', '41900', '25460', '16380', '49620',
'40660', '18940', '20660', '28300', '43980', '34740', '21260', '42620', '39980', '37100', '22140', '45640', '28660', '23300', '12260', '21300', '41500', '18660',
'49100', '22540', '43540', '37740', '44940', '41220', '24380', '42460', '45220', '28540', '18420', '46820', '34780', '30260', '15060', '24540', '34380', '46020',
'32620', '12380', '39820', '45900', '41940', '21500', '18140', '24620', '48020', '20100', '45820', '48060', '35140', '14500', '15860', '11180', '26100', '31020',
'19940', '20900', '38020', '31900', '41140', '33660', '15380', '15740', '37340', '42860', '34620', '48620', '19700', '18860', '27700', '14220', '33740', '20260',
'44140', '44980', '23420', '43620', '11300', '13780', '27500', '23060', '17500', '23700', '31300', '42020', '12780', '15780', '27660', '13740', '30980', '15660',
'33940', '11260', '11700', '12180', '35620', '29140', '20980', '14580', '15460', '32500', '16660', '38100', '30940', '45180', '42540', '26700', '14540', '10140',
'35660', '21980', '15980', '14780', '36020', '47980', '49260', '22800', '30140', '16700', '14340', '19740', '29540', '13420', '11740', '10300', '40300', '32020',
'15420', '21120', '15940', '18880', '18700', '37900', '41860', '15020', '10980', '32900', '15540', '40860', '11980', '30660', '38700', '36700', '45000', '44580',
'45020', '14660', '40620', '32180', '14940', '16940', '23460', '32270', '45940', '19180', '20180', '41420', '39420', '20740', '11860', '10700', '39020', '48780',
'36140', '28620', '35100', '25700', '46620', '16900', '38220', '22660', '39860', '33580', '40180', '40540', '45520', '16020', '46420', '46780', '38060', '10740',
'22100', '20940', '15580', '42980', '26180', '45260', '15700', '43260', '36300', '23540', '23820', '45660', '26980', '26860', '21700', '26460', '17060', '44620',
'49500', '21860', '33140', '46580', '38180', '27300', '10760', '39300', '22060', '39660', '38260', '23980', '18100', '23660', '18500', '16740', '26580', '24100',
'38300', '20340', '37260', '18340', '38500', '13060', '45700', '24300', '34180', '39460', '40580', '28700', '48540', '37500', '42180', '23500', '44380', '34820',
'48580', '44780', '28500', '49740', '24020', '12820', '23860', '31940', '23140', '34580', '45580', '20780', '27900', '30780', '17940', '17620', '17380', '20300',
'39700', '27780', '19620', '40340', '22820', '38200', '14820', '30900', '37860', '34940', '19900', '36100', '12700', '24740', '47780', '35940', '15220', '17660',
'41980', '38340', '16460', '22260', '25060', '22700', '21900', '28100', '12860', '27940', '36820', '49340', '20580', '11500', '25740', '44600', '13820', '11220',
'49020', '43220', '43500', '42660', '33420', '24180', '21780', '49060', '25660', '21640', '28420', '45860', '27060', '31620', '21220', '38780', '37940', '12420',
'22860', '13340', '38620', '44900', '49660', '37980', '14300', '17460', '41780', '25720', '49780', '15100', '27620', '27980', '28980', '13260', '19140', '32540',
'21820', '31580', '28060', '30020', '16820', '30220', '32700', '24980', '23180', '10180', '15900', '40460', '37660', '19100', '27380', '40900', '19500', '22300',
'41180', '40484', '41884', '31084', '15764', '47644', '19804', '35084', '19124', '15804', '35644', '16974', '22744', '20764', '48864', '13644', '33124', '45104',
'14484', '23844', '42644', '37964', '23104', '36084', '35004', '47894', '42044', '29404', '37764', '48424']
'''

#AL_MSAs = ['45180', '45980', '11500', '10760', '42460', '13820', '19460', '23460', '46740', '17980', '12220', '20020', '18980', '33860', '46260', '33660', '19300', '22840', '21460','10700','21640','42820','26620','22520','46220']
#setting MSAs for reports for testing
AL_MSAs = ['33660']
selector.report_list['A 3-1'] = AL_MSAs
#selector.report_list['A 3-1'] = ['11500']
selector.report_list['A 3-2'] = AL_MSAs
#selector.report_list['A 3-2'] = ['11500']
selector.report_list['A 4-1'] = AL_MSAs
selector.report_list['A 4-2'] = AL_MSAs
selector.report_list['A 4-3'] = AL_MSAs
selector.report_list['A 4-4'] = AL_MSAs
selector.report_list['A 4-5'] = AL_MSAs
selector.report_list['A 4-6'] = AL_MSAs
selector.report_list['A 4-7'] = AL_MSAs
selector.report_list['A 4-1'] = AL_MSAs
selector.report_list['A 5-1'] = AL_MSAs
selector.report_list['A 5-2'] = AL_MSAs
selector.report_list['A 5-3'] = AL_MSAs
selector.report_list['A 5-4'] = AL_MSAs
selector.report_list['A 5-5'] = AL_MSAs
selector.report_list['A 5-6'] = AL_MSAs
selector.report_list['A 5-7'] = AL_MSAs
selector.report_list['A 7-1'] = AL_MSAs
selector.report_list['A 7-2'] = AL_MSAs
selector.report_list['A 7-3'] = AL_MSAs
selector.report_list['A 7-4'] = AL_MSAs
selector.report_list['A 7-5'] = AL_MSAs
selector.report_list['A 7-6'] = AL_MSAs
selector.report_list['A 7-7'] = AL_MSAs
selector.report_list['A 8-1'] = AL_MSAs
selector.report_list['A 8-2'] = AL_MSAs
selector.report_list['A 8-3'] = AL_MSAs
selector.report_list['A 8-4'] = AL_MSAs
selector.report_list['A 8-5'] = AL_MSAs
selector.report_list['A 8-6'] = AL_MSAs
selector.report_list['A 8-7'] = AL_MSAs
selector.report_list['A 9'] = AL_MSAs
selector.report_list['A 11-1'] = AL_MSAs
selector.report_list['A 11-2'] = AL_MSAs
selector.report_list['A 11-3'] = AL_MSAs
selector.report_list['A 11-4'] = AL_MSAs
selector.report_list['A 11-5'] = AL_MSAs
selector.report_list['A 11-6'] = AL_MSAs
selector.report_list['A 11-7'] = AL_MSAs
selector.report_list['A 11-8'] = AL_MSAs
selector.report_list['A 11-9'] = AL_MSAs
selector.report_list['A 11-10'] = AL_MSAs
selector.report_list['A 12-1'] = AL_MSAs
selector.report_list['A 12-2'] = AL_MSAs
selector.report_list['A A-1'] = AL_MSAs
selector.report_list['A A-2'] = AL_MSAs
selector.report_list['A A-3'] = AL_MSAs
selector.report_list['A A-4'] = AL_MSAs
selector.report_list['A B'] = AL_MSAs

#selector.report_list['A 7-1'] = ['33660']
#selector.report_list['A 3-1'] = ['33660']

#report lists for testing
#selector.reports_to_run = ['A 9']
#selector.reports_to_run = ['A 11-1']
#selector.reports_to_run = ['A 4-1', 'A 4-2', 'A 4-3', 'A 4-4', 'A 4-6', 'A 4-7']
#selector.reports_to_run = ['A 5-1', 'A 5-2', 'A 5-3', 'A 5-4', 'A 5-5', 'A 5-7']
#selector.reports_to_run = ['A 7-1', 'A 7-2', 'A 7-3', 'A 7-4', 'A 7-5', 'A 7-6', 'A 7-7']
#selector.reports_to_run = ['A 8-1', 'A 8-2', 'A 8-3', 'A 8-4', 'A 8-5', 'A 8-6', 'A 8-7']
#selector.reports_to_run = ['A 11-1', 'A 11-2', 'A 11-3', 'A 11-4', 'A 11-5', 'A 11-6', 'A 11-7', 'A 11-8', 'A 11-9', 'A 11-10']
#selector.reports_to_run = ['A 12-1', 'A 12-2']
selector.reports_to_run = ['A A-1', 'A A-2', 'A A-3', 'A A-4']
#selector.reports_to_run = ['B']

#complete report list
#selector.reports_to_run = ['A 3-1', 'A 3-2', 'A 4-1', 'A 4-2', 'A 4-3', 'A 4-4', 'A 4-5', 'A 4-6', 'A 4-7', 'A 5-1', 'A 5-2', 'A 5-3', 'A 5-4', 'A 5-5', 'A 5-7', 'A 7-1', 'A 7-2', 'A 7-3', 'A 7-4', 'A 7-5', 'A 7-6', 'A 7-7', 'A 8-1', 'A 8-2', 'A 8-3', 'A 8-4', 'A 8-5', 'A 8-6', 'A 8-7', 'A 9', 'A 11-1', 'A 11-2', 'A 11-3', 'A 11-4', 'A 11-5', 'A 11-6', 'A 11-7', 'A 11-8', 'A 11-9', 'A 11-10', 'A 12-1', 'A 12-2', 'A A-1', 'A A-2', 'A A-3', 'A A-4', 'A-B'] #this needs to be changed to read from the input file

#control loop
total_time_start2 = time.time()
total_time_start = time.clock() #set start time for total report batch
logfile = open('processing_log.txt', 'w')
for report in selector.reports_to_run: #loop over a list of report names
	#if len(selector.report_list[report]) >0:
	start = time.clock() #set start for one report
	start2 = time.time()
	for MSA in selector.report_list[report]: #loop through MSAs flagged for report generation
		report_x = report_construction(report, selector) #instantiate class and set function strings
		report_x.report_x(MSA, cur) #variabalize funciton inputs!!!!
	end = time.clock() #set end for one report
	end2 = time.time()

	cpu_report_time = end-start
	clock_report_time = end2-start2
	logfile.write('{time} CPU time to run report {report} on {date}\n'.format(report=report, time=cpu_report_time, date=time.asctime()))
	logfile.write('{time} human time to run {report} on {date}\n'.format(report=report, time=clock_report_time, date=time.asctime()))
	print '{time} CPU time to run report {report} on {date}'.format(report=report, time=clock_report_time, date=time.asctime())
	print '{time} human time to run {report} on {date}'.format(report=report, time=clock_report_time, date=time.asctime())

total_time_end = time.clock() #set end time for total batch
total_time_end2 = time.time()
cpu_selection_time = total_time_end - total_time_start
clock_selection_time = total_time_end2 - total_time_start2
logfile.write('{time} time to run entire report selection on {date}\n'.format(time=cpu_selection_time, date=time.asctime()))
logfile.write('{time} human time to run entire report selection on {date}\n'.format(time=clock_selection_time, date=time.asctime()))
logfile.close()
print total_time_end-total_time_start, 'time to run entire report selection on\n', time.asctime()
print total_time_end2 - total_time_start2, 'human time to run entire report selection\n', time.asctime()
#check_file must be run after reports are generated
#report_list = ['A 3-1', 'A 3-2', 'A 4-1', 'A 4-2', 'A 4-3', 'A 4-4', 'A 4-5', 'A 4-6', 'A 4-7', 'A 5-1', 'A 5-2', 'A 5-3', 'A 5-4', 'A 5-5', 'A 5-7', 'A 7-1', 'A 7-2', 'A 7-3', 'A 7-4', 'A 7-5', 'A 7-6', 'A 7-7', 'A 8-1', 'A 8-2', 'A 8-3', 'A 8-4', 'A 8-5', 'A 8-6', 'A 8-7', 'A 11-1', 'A 11-2', 'A 11-3', 'A 11-4', 'A 11-5', 'A 11-6', 'A 11-7', 'A 11-8', 'A 11-9', 'A 11-10', 'A 12-1', 'A 12-2'] #this needs to be changed to read from the input file
#check_file = check_file(build_msa) #needs a report list, state list, and msa list
#check_file.is_file('aggregate', selector.report_list['year'][0], report_list) #creates msa-mds.json files showing which MSAs have reports in the sub folders
#report_lists = report_list_maker(build_msa) #takes a build object
#report_lists.report_lists('aggregate', selector.report_list['year'][0], report_list) #produces a list of all reports available for an MSA

