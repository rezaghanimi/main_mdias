From registry-vpc.cn-hangzhou.aliyuncs.com/odoomaster/super_odoo12_docker

# 拷贝项目本地文件到docker
COPY . /mnt/extra-addons/metro_park_base

COPY funenc_wechat /mnt/extra-addons/funenc_wechat
COPY funenc_theme /mnt/extra-addons/funenc_theme
COPY metro_park_maintenance /mnt/extra-addons/metro_park_maintenance
COPY odoo_groups_manage /mnt/extra-addons/odoo_groups_manage
COPY vue_template_manager /mnt/extra-addons/vue_template_manager
COPY metro_park_dispatch /mnt/extra-addons/metro_park_dispatch
COPY metro_park_production /mnt/extra-addons/metro_park_production
COPY metro_park_interlock /mnt/extra-addons/metro_park_interlock
COPY driver_plan /mnt/extra-addons/driver_plan
COPY metro_park_maintance_hz /mnt/extra-addons/metro_park_maintance_hz
RUN mkdir -p /mnt/extra-addons/metro_park_dispatch/static/route_management/
COPY rout_management /mnt/extra-addons/metro_park_dispatch/static/route_management/

#RUN python3 -m pip install --upgrade pip

#RUN apt-get install -y gcc
#RUN apt-get install python3.7-dev

# 安装其它依赖
ADD extra_pip.txt /opt/sources/extra_pip.txt
RUN pip3 install -r /opt/sources/extra_pip.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

RUN rm -rf /mnt/extra-addons/metro_park_base/funenc_wechat
RUN rm -rf /mnt/extra-addons/metro_park_base/funenc_theme
RUN rm -rf /mnt/extra-addons/metro_park_base/metro_park_maintenance
RUN rm -rf /mnt/extra-addons/metro_park_base/odoo_groups_manage
RUN rm -rf /mnt/extra-addons/metro_park_base/vue_template_manager
RUN rm -rf /mnt/extra-addons/metro_park_base/metro_park_dispatch
RUN rm -rf /mnt/extra-addons/metro_park_base/metro_park_production
RUN rm -rf /mnt/extra-addons/metro_park_base/driver_plan
RUN rm -rf /mnt/extra-addons/metro_park_base/metro_park_maintance_hz

COPY odoo.conf /odoo/
RUN python3 ./etc/entrypoint.py
CMD ["/usr/bin/supervisord"]