odoo.define('funenc.basic_model', function (require) {
    "use strict";

    var BasicModel = require('web.BasicModel');
    var Domain = require('web.Domain');

    BasicModel.include({
        /**
         * 扩展增加disalbe修饰
         * @param {*} element 
         * @param {*} modifiers 
         */
        _evalModifiers: function (element, modifiers) {
            var result = {};
            var self = this;
            var evalContext;
            function evalModifier(mod) {
                if (mod === undefined || mod === false || mod === true) {
                    return !!mod;
                }
                evalContext = evalContext || self._getEvalContext(element);
                return new Domain(mod, evalContext).compute(evalContext);
            }
            if ('invisible' in modifiers) {
                result.invisible = evalModifier(modifiers.invisible);
            }
            if ('column_invisible' in modifiers) {
                result.column_invisible = evalModifier(modifiers.column_invisible);
            }
            if ('readonly' in modifiers) {
                result.readonly = evalModifier(modifiers.readonly);
            }
            if ('required' in modifiers) {
                result.required = evalModifier(modifiers.required);
            }
            if ('disable' in modifiers) {
                result.disable = evalModifier(modifiers.disable);
            }
            return result;
        }
    })
})