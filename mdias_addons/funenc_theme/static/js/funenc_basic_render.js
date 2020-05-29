odoo.define("funenc.basic_render", function (require) {
  "use strict";

  var BasicRenderer = require("web.BasicRenderer");

  BasicRenderer.include({

    _applyModifiers: function (modifiersData, record, element) {
      var self = this;
      var modifiers = modifiersData.evaluatedModifiers[record.id] || {};

      if (element) {
        _apply(element);
      } else {
        // Clone is necessary as the list might change during _.each
        _.each(_.clone(modifiersData.elementsByRecord[record.id]), _apply);
      }

      function _apply(element) {
        // If the view is in edit mode and that a widget have to switch
        // its "readonly" state, we have to re-render it completely
        if ('readonly' in modifiers && element.widget) {
          var mode = modifiers.readonly ? 'readonly' : modifiersData.baseModeByRecord[record.id];
          if (mode !== element.widget.mode) {
            self._rerenderFieldWidget(element.widget, record, {
              keepBaseMode: true,
              mode: mode,
            });
            return; // Rerendering already applied the modifiers, no need to go further
          }
        }

        // Toggle modifiers CSS classes if necessary
        element.$el.toggleClass("o_invisible_modifier", !!modifiers.invisible);
        element.$el.toggleClass("o_readonly_modifier", !!modifiers.readonly);
        element.$el.toggleClass("o_required_modifier", !!modifiers.required);

        if (element.widget && element.widget.updateModifiersValue) {
          element.widget.updateModifiersValue(modifiers);
        }

        if ("disable" in modifiers) {
          if (self.mode != "readonly") {
            var input = element.$el.find("input, select");
            if (input.length > 0) {
              input.attr("disabled", modifiers.disable);
            } else {
              element.$el.attr("disabled", modifiers.disable);
            }
          }
        }

        // Call associated callback
        if (element.callback) {
          element.callback(element, modifiers, record);
        }
      }
    }
  })

})

