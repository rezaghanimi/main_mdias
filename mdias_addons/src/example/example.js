import {vueWidgetRegister} from '../base/__init_';
import example_action from "./example_action";
import StationSelectBoxs from "./StationSelectBoxs";

//第一个是odoo widget组件注册名字
//第二个是odoo 对应单文本组件
//第三个是odop域(模块名)
vueWidgetRegister.actionRegister('example_action', example_action, 'example');


//这是施工调度使用的完全示例。
vueWidgetRegister.fieldRegister('LineBoxs', StationSelectBoxs);


