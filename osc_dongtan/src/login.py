# -*- coding: utf8 -*-
'''
Created on 2014-1-25

@author: good-temper
'''

import urllib2
import urllib
import cookielib
import hashlib
import re

#设置用户名、密码
username = '';
password = '';
msg = '[python]测试签到';

#设置cookie
cj = cookielib.CookieJar();
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj));
urllib2.install_opener(opener);

loginPostData = {
    'email' : username,
    'pwd' : hashlib.sha1(password).hexdigest() #密码SHA1加密
    };
#不设置head直接请求发现403拒绝，所以下边所有请求都设置head，懒得一一验证了
loginRequest = urllib2.Request('https://www.oschina.net/action/user/hash_login',urllib.urlencode(loginPostData));
loginRequest.add_header('Accept','*/*');
loginRequest.add_header('Accept-Language','zh-CN,zh;q=0.8');
loginRequest.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36');
loginRequest.add_header('Content-Type','application/x-www-form-urlencoded');
sendPost = urllib2.urlopen(loginRequest);

#获取页面中的user_code和  user
#user_code应该是账号加密后的结果（用base64解码为乱码，但是可以看出是"XXXX：账号"的格式），user应该是用户唯一id，不明白这里为什么不直接用username
reqRequest =  urllib2.Request('http://www.oschina.net/');
reqRequest.add_header('Accept','*/*');
reqRequest.add_header('Accept-Language','zh-CN,zh;q=0.8');
reqRequest.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36');
reqRequest.add_header('Content-Type','application/x-www-form-urlencoded');
content = urllib2.urlopen(reqRequest).read();

#用bs4不知什么原因不能用name获取值，折腾半天直接用正则吧
matchVal = re.search(u'name=\'user_code\' value=\'(?P<user_code>.*?)\'/>',content);
usercode = matchVal.group('user_code');
matchVal = re.search(u'name=\'user\' value=\'(?P<user_id>.*?)\'/>',content);
userid =  matchVal.group('user_id');

#终于可以发动弹了
dtPostData = {
    'user_code' : usercode,
    'user' : userid,
    'msg': msg
    };
dtRequest = urllib2.Request('http://www.oschina.net/action/tweet/pub',urllib.urlencode(dtPostData));
dtRequest.add_header('Accept','*/*');
dtRequest.add_header('Accept-Language','zh-CN,zh;q=0.8');
dtRequest.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36');
dtRequest.add_header('Content-Type','application/x-www-form-urlencoded');
sendPost = urllib2.urlopen(dtRequest);

print sendPost.read();



    
    