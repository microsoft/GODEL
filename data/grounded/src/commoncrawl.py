#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
commoncrawl.py
Class to download web pages from Common Crawl, optionally specifying a target year and month.
Author: Michel Galley, Microsoft Research NLP Group (dstc7-task2@microsoft.com)
"""

import sys
import time
import gzip
import json
import urllib.parse
import urllib.request
import chardet
from datetime import datetime
from io import BytesIO

class CommonCrawl:

    month_keys = [ '2018-05', '2018-04', '2018-03', '2018-02', '2018-01', '2017-12', '2017-11', '2017-10', '2017-09', '2017-08', '2017-07', '2017-06', '2017-05', '2017-04', '2017-03', '2017-02', '2017-01', '2016-12', '2016-10', '2016-09', '2016-08', '2016-07', '2016-06', '2016-05', '2016-04', '2016-02', '2015-11', '2015-09', '2015-08', '2015-07', '2015-06', '2015-05', '2015-04', '2015-03', '2015-02', '2015-01', '2014-12', '2014-11', '2014-10', '2014-09', '2014-08', '2014-07', '2014-04', '2014-03', '2014-02', '2013-09' ]
    month_ids = [ '2018-22', '2018-17', '2018-13', '2018-09', '2018-05', '2017-51', '2017-47', '2017-43', '2017-39', '2017-34', '2017-30', '2017-26', '2017-22', '2017-17', '2017-13', '2017-09', '2017-04', '2016-50', '2016-44', '2016-40', '2016-36', '2016-30', '2016-26', '2016-22', '2016-18', '2016-07', '2015-48', '2015-40', '2015-35', '2015-32', '2015-27', '2015-22', '2015-18', '2015-14', '2015-11', '2015-06', '2014-52', '2014-49', '2014-42', '2014-41', '2014-35', '2014-23', '2014-15', '2014-10', '2013-48', '2013-20' ]
    index_url_prefix = 'http://index.commoncrawl.org/CC-MAIN-'
    data_url = 'https://data.commoncrawl.org/'
    index_url_suffix = '%2F&output=json'
    error_internal_server = 500
    error_bad_gateway = 502
    error_service_unavailable = 503
    error_gateway_timeout = 504
    error_not_found = 404
    max_retry = 5
    retry_wait = 3

    def __init__(self, month_offset):
        self.month_keys_dic = dict([ (self.month_keys[i], i) for i in range(0, len(self.month_keys))])
        self.month_offset = month_offset


    def get_key(self, url, month, year=None):
        if year == None:
            return f"{url}|{month}"
        return f"{url}|{year}-{month}"

    def get_match(self, cc_match, url, month_id):
        k = self.get_key(url, month_id)
        return cc_match[k]

    def _get_month_id(self, year, month):
        k = year + "-" + month
        iyear = int(year)
        imonth = int(month)
        if k in self.month_keys_dic.keys():
            idx = self.month_keys_dic[k]
        elif (iyear == 2014 and imonth <= 2) or (iyear == 2013 and imonth >= 10):
            idx = self.month_keys_dic['2014-02']
        elif int(iyear) <= 2013:
            idx = self.month_keys_dic['2013-09']
        else:
            idx = 0 # >= 2018
        idx += self.month_offset
        return max(0, min(idx, len(self.month_keys)-1))

    def download(self, url, year=None, month=None, backward=True, cc_match=None):
        """
        Returns html from a url using Common Crawl (CC).
            url = identifies page to retrieve
            year = of the page
            month = month of the page
            backward = whether to search backward in time if page isn't found (if false, search forward)
            Returns (response, date), where response is the html as a string, and the date the page
            was originally retrieved (datetime object).
        """
        idx = 0
        if cc_match:
            old_date = f'{year}-{month}'
            year, month = self.get_match(cc_match, url, year + '-' + month).split('-')
            new_date = f'{year}-{month}'
            print(f'MATCH\t{url}\t{old_date}\t{new_date}')
        if year != None and month != None:
            idx = self._get_month_id(year, month)
        step = int(backward)*2-1
        retry = 0
        while 0 <= idx and idx < len(self.month_keys):
            month_id = self.month_ids[idx]
            iurl = self.index_url_prefix + month_id + '-index?url=' + urllib.parse.quote_plus(url) + self.index_url_suffix
            #print(" --> try: %s [%s]" % (url, self.month_keys[idx]))
            try:
                # Find page in index:
                u = urllib.request.urlopen(iurl)
                pages = [json.loads(x) for x in u.read().decode('utf-8').strip().split('\n')]
                page = pages[0] # To do: if get multiple pages, find closest match in time

                # Get data from warc file:
                offset, length = int(page['offset']), int(page['length'])
                offset_end = offset + length - 1
                dataurl = self.data_url + page['filename']
                request = urllib.request.Request(dataurl)
                rangestr = 'bytes={}-{}'.format(offset, offset_end)
                request.add_header('Range', rangestr)
                u = urllib.request.urlopen(request)
                content = u.read()
                raw_data = BytesIO(content)
                f = gzip.GzipFile(fileobj=raw_data)

                data = f.read()
                enc = chardet.detect(data)
                els = data.decode(enc['encoding']).strip().split('\r\n\r\n', 2)
                if len(els) != 3:
                    idx = idx + step
                else:
                    warc, header, response = els
                    date = datetime.strptime(page['timestamp'],'%Y%m%d%H%M%S')
                    return response, self.month_keys[idx], date
            except UnicodeDecodeError:
                idx = idx + step
            except urllib.error.HTTPError as err:
                if err.code == self.error_service_unavailable or \
                   err.code == self.error_gateway_timeout or \
                   err.code == self.error_bad_gateway or \
                   err.code == self.error_internal_server:
                    if retry >= self.max_retry:
                        idx = idx + step
                        retry = 0
                    else:
                        retry += 1
                        time.sleep(self.retry_wait)
                        msg = "Common Crawl error code %d, waiting %d seconds... (retry attempt %d/%d), url: %s"
                        print(msg % (err.code, self.retry_wait, retry, self.max_retry, iurl), file=sys.stderr)
                        sys.stderr.flush()
                elif err.code == self.error_not_found:
                    idx = idx + step
                    retry = 0
                else:
                    idx = idx + step
                    retry = 0
                    print("Unexpected error code: %d" % err.code, file=sys.stderr)
                    sys.stderr.flush()
            except Exception as err:
                    print("Unexpected error: %s, waiting %d seconds" % (err, self.retry_wait), file=sys.stderr)
                    sys.stderr.flush()
                    time.sleep(self.retry_wait)
        return None, None, None

if __name__== "__main__":
    cc = CommonCrawl(-2)
    if len(sys.argv) != 2 and len(sys.argv) != 4:
        print("Usage: python %s URL [YEAR] [MONTH]\n\nArguments YEAR and MONTH must have the following format: YYYY and MM" % sys.argv[0], file=sys.stderr)
    else:
        url = sys.argv[1]
        month = None
        year = None
        if len(sys.argv) == 4:
            year = sys.argv[2]
            month = sys.argv[3]
        html, date = cc.download(url, year, month)
        if html != None:
            print(html)
            print("<!-- Retrieved on: " + str(date) + " -->")
