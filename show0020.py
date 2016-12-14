from urllib.request import urlopen, Request, HTTPCookieProcessor, build_opener
from urllib.parse import urlencode
from http.cookiejar import CookieJar, MozillaCookieJar
from datetime import date
from time import sleep
import json, re, sys


class GetPhoneCallDetails:
	def __init__(self, phone, password):
		self.basic_headers = {
			'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6)',
			'Host': 'uac.10010.com',
			'Referer': 'http://uac.10010.com/portal/hallLogin'
		}
		self.is_login = self.login(phone, password)

	def login(self, phone, password):
		login_url = 'https://uac.10010.com/portal/Service/MallLogin'
		request_data = {
			'redirectType': '03',
			'userName': phone,
			'password': password,
			'pwdType': '01',
			'productType': '01'
		}
		self.cookie = CookieJar()
		cookie_handler = HTTPCookieProcessor(self.cookie)
		opener = build_opener(cookie_handler)
		data = urlencode(request_data, encoding='utf-8')
		request = Request(login_url + '?' + data, headers=self.basic_headers)
		sleep(2)
		response = opener.open(request).read().decode('utf-8')
		response = re.sub(r'\w+(?=:(?!\/))', '"\g<0>"', response)
		return json.loads(response)

	def check_login(self):	
		if self.is_login['resultCode'] != '0000':
			raise PermissionError("you have not logged in.")

		self.headers = self.basic_headers
		self.headers.update({
			'Host': 'iservice.10010.com',
			'Referer': 'http://iservice.10010.com/e3/query/call_dan.html',
			'Origin': 'http://iservice.10010.com',
			'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
		})

		# update var e3's value in cookie
		url = 'http://iservice.10010.com/e3/static/check/checklogin'
		request = Request(url, headers=self.headers, method='POST')
		opener = build_opener(HTTPCookieProcessor(self.cookie))
		sleep(2)
		response = opener.open(request).read().decode('utf-8')
		return json.loads(response)

	def _call_details(self, page=1, page_size=20, begin_date=None, end_date=None):
		response = self.check_login()
		if response['isLogin'] is not True:
			raise PermissionError("you have not logged in.")

		url = 'http://iservice.10010.com/e3/static/query/callDetail?menuid=000100030001'
		request_data = {
			'pageNo': page,
			'pageSize': page_size
		}
		request_data['beginDate'] = begin_date or datetime.now()[:9] + '01'
		request_data['endDate'] = end_date or datetime.now()[:11]

		data = urlencode(request_data, encoding='utf-8').encode('utf-8')
		request = Request(url, data=data, headers=self.headers, method='POST')
		sleep(2)
		opener = build_opener(HTTPCookieProcessor(self.cookie))
		response = opener.open(request).read().decode('utf-8')
		return json.loads(response)

	def get_call_details(self, page=1, page_size=20, begin_date=None, end_date=None):
		today = date.today()
		begin_date = begin_date or '{year}-{month}-01'.format(
			year=today.year, month=today.month)
		end_date = end_date or '{year}-{month}-{day}'.format(
			year=today.year, month=today.month, day=today.day)
		response = self._call_details(page, page_size, begin_date, end_date)
		yield response
		for cur_page in range(2, int(response['pageMap']['totalPages']) + 1):
			response = self._call_details(cur_page, page_size, begin_date, end_date)
			yield response

if __name__ == '__main__':
	if len(sys.argv) < 5:
		raise SystemExit('Usage: %s phone_number password ' 
			'begin_date(20110908) end_date(20110930)' % sys.argv[0])
	my_phone_details = GetPhoneCallDetails(sys.argv[1], sys.argv[2])
	for response in my_phone_details.get_call_details(begin_date=sys.argv[3],
		end_date=sys.argv[4]):
		calls = response['pageMap']['result']
		print("""
			<table>
			<thead>
			<tr><th>{0}</th>
			<th>{1}</th>
			<th>{2}</th>
			<th>{3}</th>
			<th>{4}</th>
			<th>{5}</th>
			<th>{6}</th>
			<th>{7}</th>
			</tr></thead><tbody>
			""".format('起始时间', '通话时长', '呼叫类型', '对方号码', '本机通话地',
				'对方归属地', '通话类型', '通话费'))
		for c in calls:
			print('''<tr><td>{0}</td>
			<td>{1}</td>
			<td>{2}</td>
			<td>{3}</td>
			<td>{4}</td>
			<td>{5}</td>
			<td>{6}</td>
			<td>{7}</td>
			</tr>'''.format(c['calldate'] + ' ' + c['calltime'], c['calllonghour'],
				c['calltypeName'], c['othernum'], c['homeareaName'], c['calledhome'],
				c['landtype'], c['nativefee']))
		print('</tbody></table>')
