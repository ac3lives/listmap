from argparse import RawTextHelpFormatter
import sys, time, os
import re
import argparse
import argcomplete
import csv

timestr = time.strftime("%Y%m%d-%H%M")


class colors:
    white = "\033[1;37m"
    normal = "\033[0;00m"
    red = "\033[1;31m"
    blue = "\033[1;34m"
    green = "\033[1;32m"
    lightblue = "\033[0;34m"


banner = colors.red + r"""
     _             _                            
    (_ )  _       ( )_                          
     | | (_)  ___ | ,_)  ___ ___     _ _  _ _   
     | | | |/',__)| |  /' _ ` _ `\ /'_` )( '_`\ 
     | | | |\__, \| |_ | ( ) ( ) |( (_| || (_) )
    (___)(_)(____/`\__)(_) (_) (_)`\__,_)| ,__/'
                                         | |    
                                         (_)    
                                               
"""+'\n' \
+ '\n listmap.py v1.1' \
+ '\n Created by: Shane Young/@x90skysn3k' + '\n' + colors.normal + '\n'


def ip_by_port():
    for port in port_list:
        with open(args.file, 'r') as nmap_file:
            iplist = []
            for line in nmap_file:
                if ' '+port+'/open' in line:
                    ip = re.findall( r'[0-9]+(?:\.[0-9]+){3}', line)
                    iplist += ip
             
            output = 'listmap-data/' + args.prefix + '-' + port + '_' + timestr + '.txt'
            with open(output, 'w+') as f:
                f.write('\n'.join(iplist))
                f.write('\n')
                print "\nThe Port: " + colors.green + port + colors.normal + " is open on these IP's: "
                print iplist
                print "\nWritten list to: " + "[" + colors.green + "+" + colors.normal + "] " + colors.green + output + colors.normal


def port_by_ip():
    for ip in ip_list:
        with open(args.file, 'r') as nmap_file:
            portlist = []
            for line in nmap_file:
                if ' '+ip+' ' in line:
                    port = re.findall( '(\d+)\/open', line)
                    portlist += port
            
            output = 'listmap-data/' + args.prefix + '-' + ip + '_' + timestr + '.txt'
            with open(output, 'w+') as f:
                f.write('\n'.join(portlist))
                f.write('\n')
                print "\nThe IP: " + colors.green + ip + colors.normal + " has these open ports: "
                print portlist
                print "\nWritten list to: " + "[" + colors.green + "+" + colors.normal + "] " + colors.green + output + colors.normal

#CSV code thanks to @ac3lives!
def do_csv():
    output = 'listmap-data/' + args.csv + '-' + timestr + '.csv' 
    outputfile = csv.writer(open(output, 'w+'), delimiter='\t')
    with open(args.file, 'r') as nmap_file:
        for line in nmap_file:
            ip = None
            try:
                ip = re.findall( r'[0-9]+(?:\.[0-9]+){3}', line)[0]
            except: 
                pass 
            openports = re.findall( '(\d+)\/open', line)
            ports = ', '.join(map(str, openports)) 
            if ip and ports:
                outputlist = [ip, ports]
                outputfile.writerow(outputlist)
                
    print "\nWritten list to: " + "[" + colors.green + "+" + colors.normal + "] " + colors.green + output + colors.normal                

def parse_args():
    
    parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter, description=\

    banner + 
    "Usage: python listmap.py <OPTIONS> \n")

    menu_group = parser.add_argument_group(colors.lightblue + 'Menu Options' + colors.normal)
    
    menu_group.add_argument('-f', '--file', help="Gnmap file to parse", required=True)
    
#    menu_group.add_argument('-t', '--top-ports', help="Parse out top interesting ports")

    menu_group.add_argument('-p', '--port', help="Define single port to parse out", default=None)

    menu_group.add_argument('-o', '--prefix', help="Specify prefix for output file i.e. company name", default="listmap")
    
    menu_group.add_argument('-i', '--ip', help="Parse out ports by ip", default=None)

    menu_group.add_argument('-c', '--csv', help="output ip and port to csv", default=None)

    argcomplete.autocomplete(parser)    
   
    args = parser.parse_args()

    output = None

    return args,output


if __name__ == "__main__":
    print(banner)
    args,output = parse_args()
    if not os.path.exists("listmap-data/"):
        os.mkdir("listmap-data/")
        
    if args.port:
        port_list = args.port.split(',')
    elif args.ip:
        ip_list = args.ip.split(',')
    elif not args.csv:
        print colors.lightblue + "\nNo IP or Port Given!" + colors.normal
   
    if args.port:
        ip_by_port()
    elif args.ip:
        port_by_ip()
    elif args.csv:
        do_csv() 
        




