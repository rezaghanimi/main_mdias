From registry.cn-hangzhou.aliyuncs.com/odoomaster/super_odoo12_docker
# 拷贝项目本地文件到docker
COPY . /mnt/extra-addons/mdias_addons

# 安装其它依赖
ADD extra_pip.txt /opt/sources/extra_pip.txt
RUN pip3 install -r /opt/sources/extra_pip.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY odoo.conf /odoo/

EXPOSE 8099

RUN python3 ./etc/entrypoint.py


CMD ["/usr/bin/supervisord"]

