# 视倾角接口 localhost/view_angle?att_str=232°∠32&section_dir=180
# 正常情况返回结果位于"content": "21.04"
# 产状换算接口 localhost/att_strs?att_str=232°∠32
# 正常情况返回结果位于"content": "21.04"
# "content": "{"str_dz": "232.0°∠32.0°", "str_rw": "N38°W/32°SW"}"


import math
import json
import re

pattern1 = r'[S|E|W|N]'
pattern2 = r'[\d|\.]+'

class AttstrResult:
    def __init__(self):
        self.str_dz = ''
        self.str_rw = ''


class Atti:
    def __init__(self,qingxiang=0.0,qingjiao=0.0):
        self.qingxiang = round(qingxiang,2)
        self.qingjiao = round(qingjiao,2)

    @staticmethod
    def get_a_Atti_from_str(s):
        qx=-1000.0
        qj=-1000.0
        try:
            if s.find('∠') is not -1:  # 地质写法情况
                s = s.replace('°', '')
                ss = s.split('∠')
                qx = float(ss[0])
                qj = float(ss[1])
            else:  # 象限写法情况，逻辑：4*字母+2 数值,否则出错！
                s = s.upper()
                match1 = re.findall(pattern1, s)
                match2 = re.findall(pattern2, s)
                zx_str = match1[0] + match1[1]
                qx_str = match1[2] + match1[3]
                qj = float(match2[1])
                zx = float(match2[0])
                # 走向换算
                if zx_str == 'NE':
                    zx = zx
                elif zx_str == 'SE':
                    zx = 180 - zx
                elif zx_str == 'SW':
                    zx = 180 + zx
                elif zx_str == 'NW':
                    zx = 360 - zx
                else:
                    return Atti(qx, qj)  # 错误
                if zx > 180:
                    zx -= 180
                if qx_str == 'NE':
                    if zx < 90:
                        return Atti(qx, qj)  # 错误
                    else:
                        qx = zx - 90
                elif qx_str == 'SE':
                    if zx < 90:
                        qx = zx + 90
                    else:
                        return Atti(qx, qj)  # 错误
                elif qx_str == 'SW':
                    if zx < 90:
                        return Atti(qx, qj)  # 错误
                    else:
                        qx = zx + 90
                elif qx_str == 'NW':
                    if zx < 90:
                        qx = zx + 270
                    else:
                        return Atti(qx, qj)  # 错误
        except:
            pass
        return Atti(qx,qj)
    # 视倾角换算
    def cal_view_angle(self,section_direction):
        #tanβ=tanα cosω。其中β为视倾角，α为真倾角，ω为剖面方向（即视倾向）与倾向之夹角。
        alfa = math.radians(self.qingjiao)#度数转弧度
        omega = math.radians(self.qingxiang) - math.radians(section_direction)
        beta = math.atan(math.tan(alfa)*math.cos(omega))
        beta = math.degrees(beta)
        beta = round(beta, 2)
        stus = {'code': 0, 'content': {'shiqingjiao': beta}}
        # result = json.dumps(stus)  # 先把字典转成json
        return str(beta)
    def str_dz(self):
        return str(self.qingxiang)+'°∠'+str(self.qingjiao)+'°'
    # 铁道换算
    def str_rw(self):
        # 走向
        zx = self.qingxiang + 90
        if zx > 360:
            zx -= 360
        # print('走向：'+str(zx))
        result = ''
        if 90 < zx <= 270:
            result += 'S'
            if zx <= 180:
                result += str(round(180 - zx)) + '°E/' + str(round(self.qingjiao)) + '°NE'
            else:
                result += str(round(zx - 180)) + '°W/' + str(round(self.qingjiao)) + '°SE'
        else:
            result += 'N'
            if zx > 270:
                result += str(round(360 - zx)) + '°W/' + str(round(self.qingjiao)) + '°SW'
            else:
                result += str(round(zx - 0)) + '°E/' + str(round(self.qingjiao)) + '°NW'
        # stus = {'code': 0, 'content': {'railway_atti': result}}
        # result = json.dumps(stus)  # 先把字典转成json
        return result

    def get_Attstrs(self):
        attstrResult=AttstrResult()
        try:
            attstrResult.str_dz = self.str_dz()
            attstrResult.str_rw = self.str_rw()
        except:
            pass
        return attstrResult
    #测试函数
    def print(self):
        print('倾向倾角：%s 象限：%s 视倾角（180）：%s'%(self.str_dz(),self.str_rw(),self.cal_view_angle(180)))


if __name__ == '__main__':
    # 测试代码
    at = Atti(20, 60)
    at.print()
    at = Atti.get_a_Atti_from_str('20°∠60°')
    at.print()
    at = Atti.get_a_Atti_from_str('S70°E/60°NE')
    at.print()

    at = Atti(102, 32)
    at.print()
    at = Atti.get_a_Atti_from_str('102∠32°')
    at.print()
    at = Atti.get_a_Atti_from_str('S12W32°SE')
    at.print()

    at = Atti(232, 32)
    at.print()
    at = Atti.get_a_Atti_from_str('232°∠32°')
    at.print()
    at = Atti.get_a_Atti_from_str('N38°W/32°SW')
    at.print()

    at = Atti(302, 32)
    at.print()
    at = Atti.get_a_Atti_from_str('302°∠32°')
    at.print()
    at = Atti.get_a_Atti_from_str('N32°E/32°NW')
    at.print()
