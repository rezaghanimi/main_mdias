import xmlrpc.client

url = "http://funenccrax.vaiwan.com"
db = 'metro_park_0809'
username = 'admin'
password = 'admin'

common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
common.version()
uid = common.authenticate(db, username, password, {})

models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

# 根据用户查找部门信息
# rst = models.execute_kw(db, uid, password, 'metro.park.interface', 'getDepartmentUserData',
#                         [], {})
#
# # 根据电话号码查查询用户信息
# rst = models.execute_kw(db, uid, password, 'metro.park.interface', 'getPhoneUserData',
#                         [], {})

# 取得当天运行图信息
rst = models.execute_kw(db, uid, password, 'metro.park.interface', 'getTimeTableData',
                        [], {'operateDate': '2019-01-01'})

print(rst)
