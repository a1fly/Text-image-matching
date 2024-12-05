import pymysql
import pymysql.cursors
import ast


class ReadInfo:
    def __init__(self):
        self.description = ""
        self.location = ""
        self.imageUrl=""
        self.contactmethod = ""
        self.contact = ""
        self.contactNum = ""
        self.designatePlace = ""
        self.PlaceimageUrl=""
        self.haveplaceimg = False
        self.findtime=[]

        self.config = {
            'host': 'localhost',
            'user': 'root',
            'password': '123456',
            'db': 'lossdata',
        }

    def todirt(self,item):
        d={}
        d['description']=item[1]
        d['location']=item[2]
        d['imageUrl']=self.mkURL(item[9])
        d['contactmethod']=item[4]
        d['contact']=item[5]
        d['contactNum']=item[6]
        d['designatePlace']=item[7]
        d['PlaceimageUrl']=self.mkURL(item[10])
        findtime=item[3]

        d['findtime'] = ast.literal_eval(findtime)




        print("======================================================")
        print("发现时间：")
        print(d['findtime'])
        print("类型：")
        print(type(d['findtime']))
        print("======================================================")

        return d




    def mkURL(self,findtime):
        """
        flag为0表示失物图片，为1表示地点图片
        """
        url="http://localhost:5001/static/uploads/"

        return url+findtime



    def readdata(self,page,pagesize):
        res=[]
        # MySQL 连接配置
        connection = pymysql.connect(**self.config)

        print("============================================")
        print("第几页：",page)
        print("页的大小：",pagesize)


        offset = (page - 1) * pagesize
        print("offset",offset)
        print("============================================\n\n")

        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM lost_items LIMIT %s OFFSET %s"
                cursor.execute(sql, (pagesize, offset))
                items = cursor.fetchall()
        finally:
            connection.close()

        for item in items:
            res.append(self.todirt(item))

        return res





if __name__ == '__main__':
    readinfo = ReadInfo()
    items=readinfo.readdata(1,5)
    print(items)



