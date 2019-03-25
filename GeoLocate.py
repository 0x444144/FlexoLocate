#!/usr/bin/python3

import socket
import pygeoip
import sys

# function to determine if ip address is valid
# socket considers digits like '10' as ip addresses for some reason
def valid_ip(address):
    try: 
        socket.inet_aton(address)
        try:
            host_bytes = address.split('.')
            valid = [int(b) for b in host_bytes]
            valid = [b for b in valid if b >= 0 and b<=255]
            return len(host_bytes) == 4 and len(valid) == 4
        except:
                return False
    except:
        return False

# Testing different inputs:
# print valid_ip('10.1.1.1')
# print valid_ip('999.10.20.30')
# print valid_ip('13')
# print valid_ip('gibberish')

# getting ip addresses from file
def parse_ips(file_location):
    addresses = list()
    with open (file_location, 'r') as f:
        for line in f.readlines():
            for word in line.split():
                if valid_ip(word):
                    #print word + " is a valid ip"
                    addresses.append(word)
    return addresses

# ip = sys.argv[1]

# database downloaded from:
# https://dev.maxmind.com/geoip/geoip2/geolite2/
# city.dat from https://dev.maxmind.com/geoip/legacy/geolite/
def ipLocator(ip):
    GeoIPDatabase = '/root/geo-locate/GeoLiteCity.dat'
    ipData = pygeoip.GeoIP(GeoIPDatabase)
    record = ipData.record_by_name(ip)
    print("The geolocation for IP Address %s is:" % ip)
    print("Accurate Location: %s, %s, %s" % (record['city'], record['region_code'], record['country_name']))
    print("General Location: %s" % (record['metro_code']))

def countryLocator(ip):
    GeoIPDatabase = '/root/geo-locate/GeoLiteCity.dat'
    ipData = pygeoip.GeoIP(GeoIPDatabase)
    record = ipData.record_by_addr(ip)
    print("The geolocation for IP Address %s is:" % ip)
    print("Accurate Location: %s, %s, %s" % (record['city'], record['region_code'], record['country_name']))
    print("General Location: %s" % (record['metro_code']))

ip_list = (parse_ips(sys.argv[1]))
for ip in ip_list:
    try:
        #print("search by name: ")
        ipLocator(ip)
    except:
        continue
#    print("search by addr: ")
#    countryLocator(ip)
