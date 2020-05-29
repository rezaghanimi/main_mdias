odoo.define('funenc.ActWindowActionManager', function (require) {
    "use strict";

    var ActionManager = require('web.ActionManager');
    var Context = require('web.Context');

    ActionManager.include({
        /**
         * 重主，form直接弹出，而不是切换视图
         * @param {*} ev
         */
        _onSwitchView: function (ev) {
            ev.stopPropagation();
            var viewType = ev.data.view_type;
            var currentController = this.getCurrentController();
            if (currentController.jsID === ev.data.controllerID) {
                // only switch to the requested view if the controller that
                // triggered the request is the current controller
                var action = this.actions[currentController.actionID];
                if ('res_id' in ev.data) {
                    action.env.currentId = ev.data.res_id;
                }
                var options = {};
                if (viewType === 'form' && !action.env.currentId) {
                    options.mode = 'edit';
                } else if (ev.data.mode) {
                    options.mode = ev.data.mode;
                }
                if (viewType === 'form') {
                    var _views = action._views

                    var view = _.find(_views, function (_view) {
                        return _view && _view[1] && _view[1] == viewType
                    });

                    if (!view) {
                        view = [false, "form"]
                    }

                    // 从新窗口弹出, 添加list_pop_form作为标识
                    this.do_action({
                        type: 'ir.actions.act_window',
                        view_type: 'form',
                        view_mode: 'form',
                        target: 'new',
                        context: _.extend({}, action.context, {
                            'list_pop_form': true
                        }),
                        res_model: action.res_model,
                        res_id: action.env.currentId,
                        views: [view],
                        flags: {
                            mode: options.mode
                        }
                    }, {
                        'title': action.name,
                        'on_close': function () {
                            currentController.widget.reload();
                        }
                    });
                } else {
                    this._switchController(action, viewType, options);
                }
            }
        },

        /**
         * 正常的切换视图, bug need fix
         * @param {*} action
         * @param {*} viewType
         * @param {*} viewOptions
         */
        _switchController: function (action, viewType, viewOptions) {
            var self = this;

            var newController = function () {
                return self
                    ._createViewController(action, viewType, viewOptions)
                    .then(function (controller) {
                        // AAB: this will be moved to the Controller
                        var widget = controller.widget;
                        if (widget.need_control_panel) {
                            // set the ControlPanel bus on the controller to allow it to
                            // communicate its status
                            widget.set_cp_bus(self.controlPanel.get_bus());
                        }
                        return self._startController(controller);
                    });
            };

            var controllerDef = action.controllers[viewType];
            if (!controllerDef || controllerDef.state() === 'rejected') {
                // if the controllerDef is rejected, it probably means that the js
                // code or the requests made to the server crashed.  In that case,
                // if we reuse the same deferred, then the switch to the view is
                // definitely blocked.  We want to use a new controller, even though
                // it is very likely that it will recrash again.  At least, it will
                // give more feedback to the user, and it could happen that one
                // record crashes, but not another.
                controllerDef = newController();
            } else {
                controllerDef = controllerDef.then(function (controller) {
                    if (!controller.widget) {
                        // lazy loaded -> load it now
                        return newController().done(function (newController) {
                            // replace the old controller (without widget) by the new one
                            var index = self.controllerStack.indexOf(controller.jsID);
                            self.controllerStack[index] = newController.jsID;
                            delete self.controllers[controller.jsID];
                        });
                    } else {
                        viewOptions = _.extend(viewOptions || {}, action.env);
                        return $.when(controller.widget.willRestore()).then(function () {
                            return controller.widget.reload(viewOptions).then(function () {
                                return controller;
                            });
                        });
                    }
                });
            }

            return this.dp.add(controllerDef).then(function (controller) {
                var view = _.findWhere(action.views, {type: viewType});
                var currentController = self.getCurrentController();
                var index;
                if (currentController.actionID !== action.jsID) {
                    index = _.indexOf(self.controllerStack, controller.jsID);
                } else if (view.multiRecord) {
                    // remove other controllers linked to the same action from the stack
                    index = _.findIndex(self.controllerStack, function (controllerID) {
                        return self.controllers[controllerID].actionID === action.jsID;
                    });
                } else if (!_.findWhere(action.views, {type: currentController.viewType}).multiRecord) {
                    // replace the last controller by the new one if they are from the
                    // same action and if they both are mono record
                    index = self.controllerStack.length - 1;
                }
                return self._pushController(controller, {index: index});
            });
        },

        _handleAction: function (action, options) {
            for (var controller in this.controllers) {
                var this_controller = this.controllers[controller];
                if (this_controller.actionID === action.jsID) {
                    this_controller.widget.destroy()
                }
            }
            return this._super.apply(this, arguments)
        },
        
        _onExecuteAction: function (ev) {
            ev.stopPropagation();
            var self = this;
            var actionData = ev.data.action_data;
            var env = ev.data.env;
            var context = new Context(env.context, actionData.context || {});
            var recordID = env.currentID || null; // pyUtils handles null value, not undefined
            var def = $.Deferred();

            // determine the action to execute according to the actionData
            if (actionData.special) {
                def = $.when({type: 'ir.actions.act_window_close', infos: 'special'});
            } else if (actionData.type === 'object') {
                // call a Python Object method, which may return an action to execute
                var args = recordID ? [[recordID]] : [env.resIDs];
                if (actionData.args) {
                    try {
                        // warning: quotes and double quotes problem due to json and xml clash
                        // maybe we should force escaping in xml or do a better parse of the args array
                        var additionalArgs = JSON.parse(actionData.args.replace(/'/g, '"'));
                        args = args.concat(additionalArgs);
                    } catch (e) {
                        console.error("Could not JSON.parse arguments", actionData.args);
                    }
                }
                args.push(context.eval());
                def = this._rpc({
                    route: '/web/dataset/call_button',
                    params: {
                        args: args,
                        method: actionData.name,
                        model: env.model,
                    },
                });
            } else if (actionData.type === 'action') {
                // execute a given action, so load it first
                def = this._loadAction(actionData.name, _.extend(pyUtils.eval('context', context), {
                    active_model: env.model,
                    active_ids: env.resIDs,
                    active_id: recordID,
                }));
            }

            // use the DropPrevious to prevent from executing the handler if another
            // request (doAction, switchView...) has been done meanwhile ; execute
            // the fail handler if the 'call_button' or 'loadAction' failed but not
            // if the request failed due to the DropPrevious,
            def.fail(ev.data.on_fail);
            this.dp.add(def).then(function (actions) {
                if (!(actions instanceof Array)) {
                    actions = [actions]
                }
                _.each(actions, function (action) {
                    // show effect if button have effect attribute
                    // rainbowman can be displayed from two places: from attribute on a button or from python
                    // code below handles the first case i.e 'effect' attribute on button.

                    var effect = false;
                    if (actionData.effect) {
                        effect = pyUtils.py_eval(actionData.effect);
                    }
                    if (action && action.constructor === Object) {
                        // filter out context keys that are specific to the current action, because:
                        //  - wrong default_* and search_default_* values won't give the expected result
                        //  - wrong group_by values will fail and forbid rendering of the destination view
                        var ctx = new Context(
                            _.object(_.reject(_.pairs(env.context), function (pair) {
                                return pair[0].match('^(?:(?:default_|search_default_|show_).+|' +
                                    '.+_view_ref|group_by|group_by_no_leaf|active_id|' +
                                    'active_ids|orderedBy)$') !== null;
                            }))
                        );
                        ctx.add(actionData.context || {});
                        ctx.add({active_model: env.model});
                        if (recordID) {
                            ctx.add({
                                active_id: recordID,
                                active_ids: [recordID],
                            });
                        }
                        ctx.add(action.context || {});
                        action.context = ctx;
                        // in case an effect is returned from python and there is already an effect
                        // attribute on the button, the priority is given to the button attribute
                        action.effect = effect || action.effect;
                    } else {
                        // if action doesn't return anything, but there is an effect
                        // attribute on the button, display rainbowman
                        action = {
                            effect: effect,
                            type: 'ir.actions.act_window_close',
                        };
                    }
                    var options = {on_close: ev.data.on_closed};
                    return self.doAction(action, options).then(ev.data.on_success, ev.data.on_fail);
                });
            });
        }
    });

});
