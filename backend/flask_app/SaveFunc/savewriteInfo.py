import pymysql


class SaveInfo:
    def __init__(self):
        self.description = ""
        self.location = ""
        self.savetime = []
        self.contactmethod = ""
        self.contact = ""
        self.contactNum = ""
        self.designatePlace = ""
        self.imgname = ""
        self.Placeimgname = ""
        self.haveplaceimg = False

    def save(self, description, location, savetime, contactmethod, contact, contactNum, designatePlace, haveplaceimg):
        """
        description：失物描述
        location：发现地点
        savetime：上传时间 如：[2022,10,12,16,17,23]
        contactmethod：方式，放在发现地点，联系本人，放在指定地点
        contact：联系方式，微信，QQ，钉钉
        contactNum：联系号码
        designatePlace：指定地点的位置
        haveplaceimg：是否有指定地点的图片
        """

        self.description = description
        self.location = location
        self.savetime = savetime
        if contactmethod == 1:
            self.contactmethod = "放在发现地点"
        elif contactmethod == 2:
            self.contactmethod = "联系本人"
        else:
            self.contactmethod = "放在指定地点"

        self.contact = contact
        self.contactNum = contactNum
        self.designatePlace = designatePlace
        self.haveplaceimg = haveplaceimg

        self.imgname = ""
        for i in range(len(self.savetime)):
            self.imgname += (str(savetime[i]) + "-")
        self.imgname += "0.png"

        if haveplaceimg:
            self.Placeimgname = ""
            for i in range(len(self.savetime)):
                self.Placeimgname += (str(savetime[i]) + "-")
            self.Placeimgname += "1.png"

        self.save_to_db()

    def create_db_and_table(self):
        # MySQL 连接配置
        connection = pymysql.connect(
            host='localhost',  # MySQL 服务器地址
            user='root',  # 数据库用户名
            password='123456',  # 数据库密码
        )

        try:
            with connection.cursor() as cursor:
                cursor.execute("CREATE DATABASE IF NOT EXISTS lossdata")
                print("数据库创建或已存在")

                cursor.execute("USE lossdata")

                # 创建表格
                create_table_sql = """
                    CREATE TABLE IF NOT EXISTS lost_items (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        description VARCHAR(255),
                        location VARCHAR(255),
                        savetime VARCHAR(255),
                        contactmethod VARCHAR(50),
                        contact VARCHAR(50),
                        contactNum VARCHAR(50),
                        designatePlace VARCHAR(255),
                        haveplaceimg BOOLEAN,
                        imgname VARCHAR(255),
                        Placeimgname VARCHAR(255)
                    )
                """
                cursor.execute(create_table_sql)
                print("表格创建或已存在")
        except Exception as e:
            print(f"创建数据库或表格时发生错误: {e}")
        finally:
            connection.close()

    def save_to_db(self):
        # MySQL 连接配置
        connection = pymysql.connect(
            host='localhost',  # MySQL 服务器地址
            user='root',  # 数据库用户名
            password='123456',  # 数据库密码
            database='lossdata'  # 数据库名称
        )

        try:
            with connection.cursor() as cursor:
                # 插入数据的 SQL 语句
                sql = """
                    INSERT INTO lost_items (description, location, savetime, contactmethod, contact, contactNum, designatePlace, haveplaceimg, imgname, Placeimgname)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                # 将数据作为元组传入
                cursor.execute(sql, (
                    self.description,
                    self.location,
                    str(self.savetime),  # 将时间列表转为字符串存储
                    self.contactmethod,
                    self.contact,
                    self.contactNum,
                    self.designatePlace,
                    self.haveplaceimg,
                    self.imgname,
                    self.Placeimgname
                ))
                # 提交事务
                connection.commit()
                print("数据保存成功")
        except Exception as e:
            print(f"保存数据时发生错误: {e}")
        finally:
            connection.close()


if __name__ == '__main__':
    saveinfo = SaveInfo()
    saveinfo.create_db_and_table()

    saveinfo.save("雨伞",
                  "学校里面",
                  [2022, 10, 12, 16, 17, 23],
                  1,
                  "微信",
                  "123456",
                  "寝室",
                  True)

