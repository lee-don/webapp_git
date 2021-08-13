# localhost/zzmlevel?rc=较软岩&kv=破碎&is_fault=&water=喷出&crustal_stress=高地应力
# 其中
# rc和kv可以传标准str或者数值，rc“硬岩与软岩互层”情况，rc输入30，或者“硬岩与软岩互层”
# rc_dic={'极硬岩':(60,1000),'硬岩':(30.001,60),'硬岩与软岩互层':(29.999,30.001),'较软岩':(15,29.999),'软岩':(5,15),'极软岩':(-1000,5)}
# [is_fault]标记断层泥情况，基本分级6
# water修正参数逻辑字典，也可以传入数值(L/(min*10m))
# water_dic_str={('无','干','燥','渗'):1,('整体浸润','润'):2,('喷','涌','特别大'):3}
# 包含key中的任意字符即确定为该分级：不传将不做修正
# crustal_stress:地应力字符中包含高/极高分别确定为高地应力/极高地应力，包含字符即确定为该分级：不传将不做修正
# 返回结果为content中level为最终分级等级，msg为过程及说明
# 示例：{"content": "{"level": 6, "msg": "掌子面情况为"较软岩|破碎"，围岩基本分级5。地应力情况为高地应力，修正前分级为5，根据规范，修正为6。"}", "suc": true}





class ZzmResult:
    def __init__(self):
        self.level = -1
        self.msg = ''

    def append_msg(self,msg):
        self.msg += msg

# 初始化环境start
# 坚硬程度
# 硬岩与软岩互层情况 rc输入30
rc_dic={'极硬岩':(60,1000),'硬岩':(30.001,60),'硬岩与软岩互层':(29.999,30.001),'较软岩':(15,29.999),'软岩':(5,15),'极软岩':(-1000,5)}
def get_rc_str(rc_digit):
    for re in rc_dic.keys():
        val = rc_dic[re]
        if rc_digit >=  val[0] and rc_digit < val[1]:
            return re
    return None

# 完整程度
kv_dic={'完整':(0.75,1000),'较完整':(0.55,0.75),'较破碎':(0.35,0.55),'破碎':(0.15,0.35),'极破碎':(-1000,0.15)}
def get_kv_str(kv_digit):
    for re in kv_dic.keys():
        val = kv_dic[re]
        if kv_digit >=  val[0] and kv_digit < val[1]:
            return re
    return None

# 基本等级表
def get_level_dic():
    level1 = ('极硬岩|完整',)
    level2 = ('极硬岩|较完整', '硬岩|完整')
    level3 = ('极硬岩|较破碎', '硬岩|较完整', '较软岩|完整', '硬岩与软岩互层|较完整', '硬岩与软岩互层|完整')
    level4 = ('极硬岩|破碎', '硬岩|破碎', '硬岩|较破碎', '较软岩|较完整', '较软岩|较破碎', '软岩|完整', '软岩|较完整', '硬岩与软岩互层|较破碎')  # ,'硬岩与软岩互层|较完整'软岩为主
    # level5 = ('较软岩|破碎','软岩|较破碎','软岩|破碎','*|极破碎','极软岩|*','硬岩与软岩互层|破碎')
    level5 = ('较软岩|破碎', '软岩|较破碎', '软岩|破碎', '极破碎', '极软岩', '硬岩与软岩互层|破碎')

    level6 = ('断层泥',)
    return {1:level1,2:level2,3:level3,4:level4,5:level5,6:level6}
level_dic = get_level_dic()

# 地下水矫正
water_dic_str={('无','干','燥','渗'):1,('整体浸润','润'):2,('喷','涌','特别大'):3}
water_dic_digit={(0,10):1,(10,25):2,(25,125):3}#（L/（min*10m））
def get_waterlv_fdigit(water_digit):
    for key in water_dic_digit.keys():
        if water_digit >=  key[0] and water_digit < key[1]:
            return water_dic_digit[key]
    return None

def get_waterlv_fstr(water_str):
    for key in water_dic_str.keys():
        for item in key:
            if  water_str.find(item) is not -1:
                return water_dic_str[key]
    return None

def correct_level_by_water(zzmResult,water_level):
    if water_level == None:
        return zzmResult
    if zzmResult.level == 6:
        return zzmResult
    msgformat = '地下水分级为{}，修正前分级为{}，根据规范，修正为{}。'
    tmp = zzmResult.level
    if water_level == 3:
        zzmResult.level += 1
        zzmResult.append_msg(msgformat.format(water_level,tmp,zzmResult.level))
        return zzmResult
    if water_level == 2:
        if zzmResult.level > 2:
            zzmResult.level += 1
            zzmResult.append_msg(msgformat.format(water_level, tmp, zzmResult.level))
            return zzmResult
    return zzmResult



# 地应力
def get_crustal_stress_case(comment):
    if comment == None:
        return 0
    if comment.find('极高') is not -1:
        return 1
    if comment.find('高') is not -1:
        return 2
    return 0

def correct_level_by_crustal_stress(zzm,crus_str_str):
    zzmResult = zzm.zzmResult
    crus_str_case = get_crustal_stress_case(crus_str_str)
    if crus_str_case == 0 or zzmResult.level < 3:
        return zzmResult
    if crus_str_case == 2 and zzmResult.level == 3:
        return zzmResult
    msgformat = '地应力情况为{}，修正前分级为{}，根据规范，修正为{}。'
    tmp = zzmResult.level
    if crus_str_case == 1 and zzmResult.level == 4:
        zzmResult.level += 1
        zzmResult.append_msg(msgformat.format(crus_str_str, tmp, zzmResult.level))
        return zzmResult
    if crus_str_case == 1 and zzmResult.level == 3:
        if is_standard_comment1(zzm):
            msgformat = '地应力情况为{}，修正前分级为{}，属于规范注释1中需要修正的情况，修正为{}。'
            zzmResult.level += 1
            zzmResult.append_msg(msgformat.format(crus_str_str, tmp, zzmResult.level))
            return zzmResult
        else:
            return zzmResult
    if crus_str_case == 2 and zzmResult.level == 4:
        if is_standard_comment2(zzm):
            msgformat = '地应力情况为{}，修正前分级为{}，属于规范注释2需要修正的情况，修正为{}。'
            zzmResult.level += 1
            zzmResult.append_msg(msgformat.format(crus_str_str, tmp, zzmResult.level))
            return zzmResult
        else:
            return zzmResult
    if zzmResult.level == 5:
        zzmResult.level += 1
        zzmResult.append_msg(msgformat.format(crus_str_str, tmp, zzmResult.level))
    return zzmResult

# 规范P61注释1需要调整的情况：！（'极硬岩|较破碎', '硬岩|较完整'）
def is_standard_comment1(zzm):
    ss = zzm.get_kvrc_str()
    li = ('极硬岩|较破碎', '硬岩|较完整')
    return ss not in li

# 规范P61注释2情况需要调整的情况：！（'极硬岩|破碎', '硬岩|破碎', '硬岩|较破碎'）
def is_standard_comment2(zzm):
    ss = zzm.get_kvrc_str()
    li = ('极硬岩|破碎', '硬岩|破碎', '硬岩|较破碎')
    return ss not in li

# 初始化环境ok


class Zzm:
    def __init__(self,rc_d_or_s,kv_d_or_s,is_fault=False,water_d_or_s=None,crustal_stress_str=None):
        rc_d = rc_d_or_s
        kv_d = kv_d_or_s
        water_level = water_d_or_s
        try:
            rc_d = float(rc_d)
            kv_d = float(kv_d)
            if water_level != None:
                water_level = float(water_level)
        except:
            pass
        if type(rc_d) is str:
            try:
                tu = rc_dic[rc_d]
                rc_d = (tu[0] + tu[1]) / 2
            except:
                self.zzmResult = ZzmResult()
                msgformat = '掌子面模型创建失败，"{}"不符合掌子面Rc参数格式。'
                self.zzmResult.append_msg(msgformat.format(rc_d_or_s))
                return
        if water_level is None:
            pass
        elif type(water_level) is str:
            try:
                water_level = get_waterlv_fstr(water_level)
            except:
                self.zzmResult = ZzmResult()
                msgformat = '掌子面模型创建失败，"{}"不符合掌子面地下水（water）参数格式。'
                self.zzmResult.append_msg(msgformat.format(water_d_or_s))
                return
        else:
            try:
                water_level = get_waterlv_fdigit(water_level)
            except:
                self.zzmResult = ZzmResult()
                msgformat = '掌子面模型创建失败，"{}"不符合掌子面地下水（water）参数格式。'
                self.zzmResult.append_msg(msgformat.format(water_d_or_s))
                return
        if type(kv_d) is str:
            try:
                tu = kv_dic[kv_d]
                kv_d = (tu[0] + tu[1]) / 2
            except:
                self.zzmResult = ZzmResult()
                msgformat = '掌子面模型创建失败，"{}"不符合掌子面Kv参数格式。'
                self.zzmResult.append_msg(msgformat.format(kv_d_or_s))
                return
        self.rc = rc_d
        self.kv = kv_d
        self.rc_str = get_rc_str(rc_d)
        self.kv_str = get_kv_str(kv_d)
        self.is_fault = is_fault
        self.zzmResult = Zzm.basic_level_str(self.rc_str,self.kv_str,self.is_fault)
        self.crustal_stress_str = crustal_stress_str
        self.zzmResult = correct_level_by_crustal_stress(self, self.crustal_stress_str)
        self.water_level = water_level
        self.zzmResult = correct_level_by_water(self.zzmResult,self.water_level)

    def get_kvrc_str(self):
        return self.rc_str + '|' + self.kv_str

    @staticmethod
    def basic_level_str(rc_str,kv_str,is_fault=False,result=None):
        if result is None:
            result = ZzmResult()
        if is_fault:
            result.level = 6
            return result
        ss = rc_str + '|' + kv_str
        msgformat = '掌子面情况为"{}"，围岩基本分级{}。'
        for key in level_dic:
            for value in level_dic[key]:
                if ss.find(value) is not -1:
                    result.level = key
                    result.append_msg(msgformat.format(ss, result.level))
                    return result
        return result

    @staticmethod
    def basic_level_digit(rc_digit,kv_digit,is_fault=False,result=None):
        if result is None:
            result = ZzmResult()
        if is_fault:
            result.level = 6
            return result
        rc_str = get_rc_str(rc_digit)
        kv_str = get_kv_str(kv_digit)
        return Zzm.basic_level_str(rc_str, kv_str,result)

#test
if __name__ == '__main__':
    zzm = Zzm('较软岩', '完整', False, '喷出', '极高地应力')
    zzm2 = Zzm(16, 0.6, False, None, '高地应力')
    print(type('11') is str)
    print()
