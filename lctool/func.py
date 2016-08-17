import re
import json
import urllib
import requests
import os.path
import textwrap
import time
import shutil
from collections import defaultdict
from BeautifulSoup import BeautifulSoup

class lctool:
    def __init__(self):
        self.baseurl = 'https://leetcode.com/'
        self.loginurl = 'https://leetcode.com/accounts/login/'
        self.basepath = '.'
        self.username = ''
        self.password = ''

    def get_tag_list(self):
        url = self.baseurl + 'problemset/algorithms/'
        f = urllib.urlopen(url)
        soup = BeautifulSoup(f)
        taglistinfo = soup.findAll('a', href=re.compile('^/tag/.*'))
        taglist = []
        for info in taglistinfo:
            tmp = info.attrMap['href'].split('/')
            taglist.append(tmp[-2])
        return taglist

    def get_problem_list(self, tag=None):
        if not tag:
            return
        url = self.baseurl + '/tag/' + tag
        f = urllib.urlopen(url).read()
        pattern = re.compile('.*/problems/.*')
        found = re.findall(pattern, f)
        problem_list = [tt.split('/problems/')[-1].split(u'/')[0] for tt in found if "Pick" not in tt]
        return list(set(problem_list))

    def get_problem(self, problem):
        url = self.baseurl + '/problems/' + problem
        f = urllib.urlopen(url)
        soup = BeautifulSoup(f)
        try:
            mydiv = soup.findAll("div", { "class" : "question-content" }).pop()
        except:
            return None
        newlines = re.compile(r'[\r\n|\r|\n]\s+')
        txt = mydiv.getText(' ')
        txt = newlines.sub('\n', txt).split('\n')
        res = ''
        for tx in txt:
            res += '\n'.join(textwrap.wrap(tx, 80))
            res += '\n'
        return res

    def get_problem_source(self, problem, language='C++'):
        url = self.baseurl + '/problems/' + problem
        f = urllib.urlopen(url)
        soup = BeautifulSoup(f)
        mydivs = soup.findAll("div", { "class" : "container" })
        codes = []
        for div in mydivs:
            if 'ng-init' in div.attrMap:
                codes = div.attrMap['ng-init']
        qid = int(codes.split('[{')[1].split('},],')[1].split(',')[1])
        codesj = ("{%s}" % codes.split('[{')[1].split('},],')[0]).split('},{')
        res = ''
        lang = ''
        for cj in codesj:
            if not cj.endswith('}'):
                cj += '}'
            if not cj.startswith('{'):
                cj = '{' + cj;
            js = str(cj).replace("'", "\"")
            codeinfo = defaultdict(str)
            try:
                codeinfo = json.loads(js)
            except:
                pass
            if codeinfo['text'] == language:
                res = codeinfo[u'defaultCode']
                lang = codeinfo[u'value']
                break
        return res, qid, lang

    def submit_problem(self, problem_path):
        abspath = os.path.abspath(problem_path)
        problem = abspath.split('/')[-1].split('.')[0]
        url = self.baseurl + '/problems/' + problem
        client = requests.session()
        tmp = client.get(self.loginurl)
        payloadl = {'csrfmiddlewaretoken':client.cookies['csrftoken'],
                'login': self.username, 'password': self.password}
        midres = client.post(self.loginurl, data = payloadl, headers = dict(referer=self.loginurl))
        url_submit = url + '/submit'
        payload = {}
        _, qid, lang = self.get_problem_source(problem)
        payload['question_id'] = qid
        payload['lang'] = lang
        payload['judge_type'] = 'large'
        payload['typed_code'] = 'dummy'
        with open(abspath) as f:
            payload['typed_code'] = f.read()
        tmp = client.get(url_submit)
        headers = {'X-CSRFToken': client.cookies['csrftoken'], 'Referer': url, 'Cookie': client.cookies}
        midres1 = client.post(url_submit, data = json.dumps(payload), headers=headers)
        submission = midres1.json()
        sid = submission[u'submission_id']
        url_check = 'https://leetcode.com/submissions/detail/' + str(sid) + '/check'
        res = {u'state': u'PENDING'}
        while (res[u'state'] != u'SUCCESS'):
            res = client.get(url_check, headers = headers)
            time.sleep(1)
            res = res.json()
        if res[u'status_runtime'] != 'N/A':
            tmp = abspath.split('/')
            dst = '/'.join(tmp[:-1]) + '/' + '-DONE.'.join(tmp[-1].split('.'))
            shutil.move(abspath, dst)
        return res
