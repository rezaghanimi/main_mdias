require('./common');

import { vueWidgetRegister } from '../base/__init_'
import EarlyWaringSetting from './park_production/early_waring/EarlyWaringSetting'
import EarlyWaringPage from './park_production/early_waring/EarlyWaringPage'
import BI from './park_production/BI/BI'


vueWidgetRegister.actionRegister('EarlySetting', EarlyWaringSetting);
vueWidgetRegister.actionRegister('EarlyWaringPage', EarlyWaringPage);
vueWidgetRegister.actionRegister('BIClient', BI);

