##odoo vue widget使用
#### 一、环境安装<Node.js和Webpack安装,已有跳过此步骤>   
#####打开终端:   

```shell
git clone  git@e.coding.net:funenc/odoo_vue_addons.git  
```

将该文件夹作为addons,并且修改package.json 相应的name,然后进入目录,输入如下命令  

```shell
brew update

brew install node
npm install webpack --save-dev
```



##### 切换到项目目录

```javascript
npm install
```

##vue widget register使用
#####step1: 在项目目录下webpack.config.js 中entry配置项目主入口文件,例如我的项目有俩个木块分别是research_management和
example,我将js分别打包至相应的static下面,其中打包目标文件分别指定


```javascript
 entry: {
        '/research_management/static/js/main':"./src/main/main_research_management.js",
        '/example/static/js/example': "./src/example/example.js"
    },

```
配置comm js打包,这会将所有模块共用的js打包到同一文件,将该js打包后我们其他模块只需要依赖与这个歌模块就可以了。如果模块仅仅只有一个就不要改配置，这样有益于代码分离  
```javascript
splitChunks: {
            chunks: 'all',
            minSize: 30000,
            maxSize: 0,
            minChunks: 1,
            maxAsyncRequests: 5,
            maxInitialRequests: 3,
            automaticNameDelimiter: '~',
            name: '/funenc_base/static/js/pack/common', //指定comm.js目标位置
            cacheGroups: {
                common: {
                    test: /[\\/]node_modules[\\/]/,
                    priority: -10
                },
                default: {
                    minChunks: 2,
                    priority: -20,
                    reuseExistingChunk: true
                }
            }
        }
```
其中字典:key是文件输出地址, value是js文件入口 


#####step2: 主文件注册odoo widget组件:
a) 创建vue 单文本组件(.vue文件),在组件中增加widget 属性，该属性和odoo中使用相应的widget方式一致，但是重写方法一定要调用 this._super.apply(this, arguments)  
```javascript
<template>

</template>

<script>
    export default {
        name: "example_action",
        data() {
            return {
                value: null,
            }
        },
        widget: {

            init: function (parent, options) {
                //this.vue 这里可以使用vue的实例

                return this._super.apply(this, arguments);
            },
            start: function () {
                this.vue; //vue实例,该实例可以访问vue
                th
                return this._super.apply(this, arguments)
            }
        },
    }
</script>

<style scoped>

</style>
```
b) 在主文件注册js

```javascript
//引入odoo vue组件注册器
import {vueWidgetRegister} from '../base/__init_'
import example_action from "./example_action"
import StationSelectBoxs from "./StationSelectBoxs";

//参数分别是：
//第一是odoo widget组件注册名字
//第二是odoo 对应单文本组件
//第三是想要依赖使用的odoo组件
//第四是odoo define域,不指定默认指定vue域
vueWidgetRegister.actionRegister('example_action', example_action, ['web.core'] 
'example');
```

例如:
```javascript
import { vueWidgetRegister } from '../base/__init_';
import AttachmentListField from './AttachmentListField'
import MenuIndex from './MenuIndex'
import ResearchManagementMenuTreeButtons from './ResearchManagementMenuTreeButtons'
//注册一个odoo field widget 
vueWidgetRegister.fieldRegister('AttachmentListField', AttachmentListField, ['web.core']);
// 注册一个odoo action widget
vueWidgetRegister.actionRegister('MenuIndex', MenuIndex, ['web.dialog']);
//注册一个普通的odoo widget组件
vueWidgetRegister.widgetRegister('ResearchManagementMenuTreeButtons',
    ResearchManagementMenuTreeButtons);
```

c) 在项目进行编译,将js编码
```bash
      webpack
```
最后在项目中引入打包后的js文件和css文件就可以了,后面就没有什么不同field widget 直接在xml使用, client在xml ir.actions.client注册就可以使用了
备注:
$widget: 可以在vue单文本组件中,对odoo widget当前实例进行访问, 在vue中通过this.$root.$widget 访问
$require: 在vue中可以通过该钩子函数,获取odoo其余组件;例如: this$root..$required('xxxxx'),在widget中可以通过this.required('xxxx')获取,例如: this.$required("web.core")获取core对象
widget.vue: 在vue单文本组件widget 键对象中,可以通this.vue 访问vue实例

其他说明:
其余odoo extend include 可以直接使用odoo.define进行自定义
```javascript
   //和odoo中使用方式一致,odoo define仅仅是一个函数
 odoo.define()
```

下面是一个完整的使用实例，其功能是实现了对Many2many('ir.accachment') 类型字段在tree增加一个附件列表,代码如下   

step1: 新建AttachmentListField.vue文件,代码如下:
```vue
<template>
    <div>
        <div>
            <el-button size="mini" type="text" @click.stop="openDialog">{{display_name}}</el-button>

            <el-dialog
                    title="附件"
                    :visible.sync="dialogVisible"
                    :modal-append-to-body="true"
                    :append-to-body="true"
                    width="60%"
            >
                <el-table
                        :data="value_data"
                        style="width: 100%"
                        border
                        height="32rem"
                        width="100%"
                >
                    <el-table-column label="文件名" prop="data">
                        <template slot-scope="scope">
                            <span>{{scope.row.data.name || scope.row.data.filename}}</span>
                        </template>
                    </el-table-column>
                    <el-table-column label="下载" prop="id">
                        <template slot-scope="scope">
                            <a :href="metadata[scope.row.id].url">
                                下载
                            </a>
                        </template>
                    </el-table-column>
                </el-table>
            </el-dialog>
        </div>

    </div>


</template>

<script>
    import WidgetMixin from '../minix/widget_minix'

    export default {
        name: "AttachmentListField",
        mixins: [WidgetMixin],
        computed: {
            display_name() {
                return this.$widget.nodeOptions.button_name || '下载'
            }
        },
        data() {
            return {
                metadata: {},
                dialogVisible: false,
                value_data: [],
            }
        },
        mounted() {
            this.metadata = this.$widget.metadata;

        },
        methods: {
            openDialog(event) {
                event.stopPropagation();
                //获取到字段当前的value 
                this.value_data = this.$widget.value.data
                this.dialogVisible = true
            }

        },
        widget: {
            fieldsToFetch: {
                name: {type: 'char'},
                datas_fname: {type: 'char'},
                mimetype: {type: 'char'},
            },

            supportedFieldTypes: ['many2many', 'many2one'],
            init() {

                let res = this._super.apply(this, arguments);
                if (this.field.type !== 'many2many' || this.field.relation !== 'ir.attachment') {
                    var msg = "The type of the field '%s' must be a many2many field with a relation to 'ir.attachment' model.";
                    throw _.str.sprintf(msg, this.field.string);
                }
                this.metadata = {};
                return res
            },
            _generatedMetadata: function () {
                var self = this;
                _.each(this.value.data, function (record) {
                    self.metadata[record.id] = {
                        url: self._getFileUrl(record.data),
                        name: record.name
                    };
                });
            },
            _getFileUrl: function (attachment) {
                return '/web/content/' + attachment.id + '?download=true';
            },
            _render: function () {
                this._generatedMetadata();
            }
        },
    }
</script>

<style scoped>

</style>
```

step2:在main.js注册:

```javascript
		import { vueWidgetRegister } from '../base/__init_';
		import AttachmentListField from './AttachmentListField'
    vueWidgetRegister.fieldRegister('AttachmentListField',       AttachmentListField);
```

step3:使用webpack编译后引入  

