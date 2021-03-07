# -*- coding:utf-8 -*-
import re
import os
from crawler_utils import crawl_url_by_get
from lxml import etree
import json
import sys
import csv
import pandas as pd

class Contract_Detail(object):
    
    def __init__(self, contract_addr):
        columns = ['contract_addr','contract_name','eth_balance','eth_usd_value','no_of_trans','creator_address','creator_transaction','source_code','contract_abi','byte_code']
        self.contract_addr = contract_addr
        self.base_dir = './' + str(contract_addr)
        self.api_key = 'NXR4MP72TG297DXPDSUGZMVXJTBGNN2BX2'
        self.parse_html = self.get_parse_html()
        '''with open("./crawl_info.csv","wb") as csvfile:
            dict_writer = csv.writer(csvfile)
            dict_writer.writerow(columns)   
            csvfile.close()
        '''
        pass

    def get_parse_html(self, write2file=False):
        '''
            get details of a given smart contract
            Parameters : contract_addr, smart contract address 
            return : parse_html
        '''

        '''
        if os.path.exists(self.base_dir + '/parse.html'):
            with open(self.base_dir + '/parse.html', 'r') as pt:
                raw_html = pt.read() 
                parse_html = etree.HTML(raw_html)
                return parse_html
        '''
        try:
            base_url = 'https://cn.etherscan.com/address/'
            target_url = str(base_url) + str(self.contract_addr) + str('#code') 
            raw_html = crawl_url_by_get(target_url, proxy=None)
            parse_html = etree.HTML(raw_html)
        except:
            self.success = False
            return None
        else:
            self.success = True
            return parse_html
    
    def get_basic_info(self):
        '''
            extract basic info from a given html
            Parameters : 
            return : basic_info, dict, 
                     {
                        'contract_name' : ..., 
                        'eth_balance' : ...,
                        'eth_usd_value' : ...,
                        'no_of_trans' : ...,
                     }
        '''
        basic_info = {}
        csv_info = []
        basic_info['contract_addr'] = self.contract_addr
        csv_info.append(self.contract_addr)
        tmp = self.parse_html.xpath("//*[@id='ContentPlaceHolder1_contractCodeDiv']/div[2]/div[1]/div[1]/div[2]/span")
        
        contract_name = tmp[0].xpath('text()')[0]
        basic_info['contract_name'] = contract_name
        csv_info.append(contract_name)
        tmp = self.parse_html.xpath("//*[@id='ContentPlaceHolder1_divSummary']/div[1]/div[1]/div/div[2]/div[1]/div[2]")
        eth_balance = tmp[0].xpath('text()')[0]
        basic_info['eth_balance'] = eth_balance
        csv_info.append(eth_balance)
        tmp = self.parse_html.xpath("//*[@id='ContentPlaceHolder1_divSummary']/div[1]/div[1]/div/div[2]/div[2]/div[2]")
        eth_usd_value = tmp[0].xpath('text()')[0]
        basic_info['eth_usd_value'] = eth_usd_value
        csv_info.append(eth_usd_value)
        tmp = self.parse_html.xpath("//*[@id='transactions']/div[1]/p/a[1]")
        if len(tmp) == 0:
            no_of_trans = 0
        else:
            no_of_trans = tmp[0].xpath('text()')[0]
        basic_info['no_of_trans'] = no_of_trans
        csv_info.append(no_of_trans)
        tmp = self.parse_html.xpath("//*[@id='ContentPlaceHolder1_trContract']/div/div[2]/a")
        creator_address = tmp[0].xpath('text()')[0]
        basic_info['creator_address'] = creator_address
        csv_info.append(creator_address)
        tmp  = self.parse_html.xpath("//*[@id='ContentPlaceHolder1_trContract']/div/div[2]/span/a")
        creator_transaction = tmp[0].xpath('text()')[0]
        basic_info['creator_transaction'] = creator_transaction
        csv_info.append(creator_transaction)
        
        
        
        return csv_info
        

    def get_source_code(self):
        '''
            extract source code from a given html and write into a file
            Parameters : contract_addr
            return : file of source code
        '''
        # parse_html = self.get_parse_html()
        #         source_code = self.parse_html.xpath('//pre[@class = "js-sourcecopyarea"]/text()')
        source_code = self.parse_html.xpath('//pre[@class = "js-sourcecopyarea editor"]/text()')
        #         with open(self.base_dir + '/source_code', 'w') as sc:
        #             for e in source_code:
        #                 sc.write(e)
        return source_code

    def get_contract_abi(self):
        '''
            get contract ABI from api call 'https://api.etherscan.io/api?module=contract&action=getabi&address='
            Parameters : contract_addr 
            return : file of contract abi
            https://api-cn.etherscan.com/api?module=contract&action=getsourcecode&address=0xBB9bc244D798123fDe783fCc1C72d3Bb8C189413&apikey=YourApiKeyToken
        '''
        target_url = 'https://api-cn.etherscan.com/api?module=contract&action=getabi'\
                        + '&address=' + str(self.contract_addr)\
                        + '&apikey=' + str(self.api_key)
        result = crawl_url_by_get(target_url, proxy=None, enable_proxy=True)
        # print result, type(result)
        return result

    def get_byte_code(self):
        '''
            get byte code from api call 'https://api.etherscan.io/api?module=proxy&action=eth_getCode&address=0xf75e354c5edc8efed9b59ee9f67a80845ade7d0c&tag=latest&apikey=YourApiKeyToken'
            Parameters : contract_addr
            return : file of byte code
        '''
        target_url = 'https://api-cn.etherscan.com/api?module=proxy&action=eth_getCode&address=' + str(self.contract_addr)
        result = crawl_url_by_get(target_url, proxy=None, enable_proxy=True)
        # print result, type(result)
        return result

    def get_op_code(self):
        '''
            get op codes from api call 'https://etherscan.io/api?module=opcode&action=getopcode&address=0xDa65eed883A48301D0EcF37465f135A7a0C9d978'
            Parameters : contract_addr
            return : file of op code
        '''
        target_url = 'https://etherscan.io/api?module=opcode&action=getopcode&address=' + str(self.contract_addr)
        result = crawl_url_by_get(target_url, proxy=None, enable_proxy=True)
        # print result, type(result)
        with open(self.base_dir + '/op_code', 'w') as oc:
            oc.write(result)

        parse_op_code = json.loads(result)['result'].split('<br>')
        # print parse_op_code, type(parse_op_code)
        with open(self.base_dir + '/parse_op_code', 'w') as poc:
            for e in parse_op_code:
                poc.write(e + '\n')

    def get_contract_detail(self):
        try:
            # self.get_parse_html(write2file=True )
            # self.get_contract_abi()
            # self.get_byte_code()
            # self.get_op_code()
            csv_info =  self.get_basic_info()
            if self.success:
                csv_info.append( self.get_source_code())
                csv_info.append( self.get_contract_abi())
                csv_info.append( self.get_byte_code())
                # return basic_info, True
                with open("./crawl_info.csv","ab") as csvfile:
                    dict_writer = csv.writer(csvfile)
                    dict_writer.writerow(csv_info)   
                    csvfile.close()
               
                return True
            else:
                return False
        except Exception, ex:
#             print 'get_contract_detail（） -------- ', str(ex) 
            # return None, False
            return False
 

def mainss():
    num = 5
    with open("./contract_addresses","r") as address:
        while num > 0:
            line = address.readline()
            if not line:
                break
            line = line.strip("\n")
            print line
            contract_detailer = Contract_Detail(line)
            contract_detailer.get_contract_detail()
            num -=1
    
def main():
    contract_detailer = Contract_Detail("0x0bc61dded5f6710c637cf8288eb6058766ce1921")
    contract_detailer.get_contract_detail()

def mainss():
    filename = "ARS.csv"
    odata = pd.read_csv(filename)
    y = odata['fileName']
    csvfile =  open("./contract_address_ARS","ab")
        
    for index in range(len(y)):
        csvfile.write(y[index]+"\n")
if __name__ == '__main__':
    main()
