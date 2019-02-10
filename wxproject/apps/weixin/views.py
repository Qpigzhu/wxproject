from django.shortcuts import render,redirect,reverse
from django.views import View
from django.http import HttpResponse
import itchat, time, sys
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




                userInfo = itchat.web_init() #初始化微信
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

                #将数据变为元组[('北京', 0), ('上海', 1), ('天津', 0)】
                # province = []
                # for key,value in province_dict.items():
                #     province.append((key,value))







                return render(request, "firends.html", {
                    "male":sex_dict['male'],
                    "female":sex_dict['female'],
                    "unknown":sex_dict["unknown"],
                    "all_province":province_dict,
                })
            else:
                return redirect(reverse("wx"))
        except:
            return redirect(reverse("wx"))

class WxLoginOut(View):
    def post(self,request):
        itchat.logout()
        return HttpResponse("success")