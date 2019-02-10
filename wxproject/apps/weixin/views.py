from django.shortcuts import render,redirect,reverse
from django.views import View
from django.http import HttpResponse
from w3lib.html import remove_tags #去掉网页标签
import collections
import jieba
import re
import itchat, time, sys
from django.views.decorators.cache import cache_page
# Create your views here.

def get_code():
    """
    获取UUID
    :return:
    """

    uuid = itchat.get_QRuuid()
    if not uuid:
        uuid = itchat.get_QRuuid()
        time.sleep(2)
    code = itchat.get_QR(uuid)
    return code,uuid


class WxCode(View):
    """
    获取二维码图片
    """
    def get(self,request):
        global Code
        code,uuid = get_code()
        return render(request, 'index.html', {
            "code_image":code,
            "uuid":uuid
        })


class Staus(View):
    """
    检查是否确定登录
    """
    def post(self,request):
        uuid = request.POST.get("uuid")
        status = itchat.check_login(uuid)
        if status == "200":
            return HttpResponse("success")

        else:
            return HttpResponse("fail")

class FriendsInfo(View):
    def get(self,request,uuid):
        #未登录情况下，会报错,捕捉错误，返回首页扫二维码
        try:
            status = itchat.check_login(uuid)
            if status == "200":


                Signature = []


                userInfo = itchat.web_init() #初始化微信


                # 使用一个字典统计好友男性和女性的数量
                sex_dict = {'male': 0, 'female': 0, "unknown": 0}

                # 省份统计表
                province_dict = {'北京': 0, '上海': 0, '天津': 0, '重庆': 0,
                                 '河北': 0, '山西': 0, '吉林': 0, '辽宁': 0, '黑龙江': 0,
                                 '陕西': 0, '甘肃': 0, '青海': 0, '山东': 0, '福建': 0,
                                 '浙江': 0, '台湾': 0, '河南': 0, '湖北': 0, '湖南': 0,
                                 '江西': 0, '江苏': 0, '安徽': 0, '广东': 0, '海南': 0,
                                 '四川': 0, '贵州': 0, '云南': 0,
                                 '内蒙古': 0, '新疆': 0, '宁夏': 0, '广西': 0, '西藏': 0,
                                 '香港': 0, '澳门': 0}

                friends_list = itchat.get_friends(update=True)[1:] #获取好友列表
                for friends in friends_list:
                    # 统计性别
                    if friends["Sex"] == 1:
                        sex_dict['male'] += 1
                    elif friends["Sex"] == 2:
                        sex_dict['female'] += 1
                    else:
                        sex_dict["unknown"] += 1


                        #省份统计
                    #判断省份是否在字典内
                    if friends["Province"] in province_dict.keys():
                        province_dict[friends["Province"]] +=1
                    else:
                        province_dict[friends["Province"]] = 1


                    Signature.append(friends["Signature"])

                #把好友个性签名连接
                Signature_str = "".join(Signature)
                #去掉html标签
                Signature_str = remove_tags(Signature_str)

                # 文本预处理
                pattern = re.compile(u'\t|\n|\.|-|:|;|\)|\(|\?|"')  # 定义正则表达式匹配模式
                Signature_data = re.sub(pattern, '', Signature_str)  # 将符合模式的字符去除

                # 文本分词
                seg_list_exact = jieba.cut(Signature_data, cut_all=False)  # 精确模式分词

                object_list = []

                remove_words = [u'的', u'，',u'和', u'是', u'随着', u'对于', u'对',u'等',u'能',u'都',u'。',u' ',u'、',u'中',u'在',u'了',
                u'通常',u'️',u'✝',u'你'] # 自定义去除词库

                for word in seg_list_exact:  # 循环读出每个分词
                    if word not in remove_words:  # 如果不在去除词库中
                        object_list.append(word)  # 分词追加到列表

                # 词频统计
                word_counts = collections.Counter(object_list)  # 对分词做词频统计
                word_counts_top20 = word_counts.most_common(60)  # 获取前60最高频的词

                all_word_counts_dict = {}
                for word_counts in word_counts_top20:
                    all_word_counts_dict[word_counts[0]] = int(word_counts[1])



                return render(request, "firends.html", {
                    "male":sex_dict['male'],
                    "female":sex_dict['female'],
                    "unknown":sex_dict["unknown"],
                    "all_province":province_dict,
                    "all_word_counts_dict":all_word_counts_dict
                })
            else:
                return redirect(reverse("wx"))
        except:
            return redirect(reverse("wx"))

class WxLoginOut(View):
    def post(self,request):
        itchat.logout()
        return HttpResponse("success")