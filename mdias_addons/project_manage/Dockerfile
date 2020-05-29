From registry-vpc.cn-hangzhou.aliyuncs.com/odoomaster/super_odoo12_docker

# 拷贝项目本地文件到docker
COPY . /mnt/extra-addons/project_manage

COPY funenc_wechat /mnt/extra-addons/funenc_wechat
COPY funenc_theme /mnt/extra-addons/funenc_theme
COPY vue_template_manager /mnt/extra-addons/vue_template_manager

# 安装其它依赖
ADD extra_pip.txt /opt/sources/extra_pip.txt
RUN pip3 install -r /opt/sources/extra_pip.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

RUN rm -rf /mnt/extra-addons/project_manage/funenc_wechat
RUN rm -rf /mnt/extra-addons/project_manage/funenc_theme
RUN rm -rf /mnt/extra-addons/project_manage/vue_template_manager

COPY odoo.conf /odoo/
RUN python3 /etc/entrypoint.py
CMD ["/usr/bin/supervisord"]