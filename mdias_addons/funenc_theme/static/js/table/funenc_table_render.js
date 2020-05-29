odoo.define('funenc.fnt_table_render', function (require) {
    "use strict";

    /**
     * render for fnt_table
     */
    var core = require('web.core');
    var ListRenderer = require('web.ListRenderer');
    var qweb = core.qweb
    var config = require('web.config');
    var core = require('web.core');
    var dom = require('web.dom');
    var field_utils = require('web.field_utils');
    var pyUtils = require('web.py_utils');

    var _t = core._t;

    // Allowed decoration on the list's rows: bold, italic and bootstrap semantics classes
    var DECORATIONS = [
        'decoration-bf',
        'decoration-it',
        'decoration-danger',
        'decoration-info',
        'decoration-muted',
        'decoration-primary',
        'decoration-success',
        'decoration-warning'
    ];

    var FIELD_CLASSES = {
        float: 'o_list_number',
        integer: 'o_list_number',
        monetary: 'o_list_number',
        text: 'o_list_text',
    };

    var table_id = 1;
    var fnt_table_render = ListRenderer.extend({
        main_box: undefined,
        default_check_col_width: 40, // checkbox 列默认宽度,
        default_button_col_width: 60,
        cur_table_id: undefined,
        autoColNums: 0,
        height: 400,
        resizing: null,
        render_option: {},
        flags: {
            resizeStart: false
        }, // 用于记录拖动事件相关信息

        options: {
            cellMinWidth: 30,
            index: undefined
        },

        events: _.extend({}, ListRenderer.prototype.events, {
            'scroll .': '_onScroll',
            'resize': '_onResize',
            'mousemove th': "_onThMousemove",
            'mouseleave th': "_onThMouseleave",
            'mousedown th': "_onThMouseDown",
            'click .add_record': '_onAddRecord',
            'click tr .o_list_record_remove': '_onRemoveIconClick',
            'contextmenu tr': 'on_context_menu_click'
        }),

        _getRenderOption: function () {
            return this.arch.attrs.options || {}
        },

        /**
         * 右键点击, 触发消息
         */
        on_context_menu_click: function (event) {
            var target = event.target
            var id = $(target).attr('id')
            var parent = this.getParent()
            var record = parent.model.get(id, {raw: true})
            this.trigger_up('table_row_right_click', {
                event: event,
                record: record
            })
        },

        /**
         * 重写，绑定拖动事件
         */
        start: function () {
            // 渲染属性, 通attrs的options获取
            if (this.arch.attrs.options) {
                this.render_option = pyUtils.py_eval(this.arch.attrs.options)
                // 设置百分比高度
                if (this.render_option.height && /^full-\d+$/.test(this.render_option.height)) {
                    this.fullHeightGap = this.render_option.height.split('-')[1];
                    this.height = $(window).height() - this.fullHeightGap;
                } else if (this.render_option.height) {
                    this.height = this.render_option.height;
                }
            }

            // 这里注意了, 这里要父级完成以后这里才调用resize，否则self.parent无效
            var self = this;
            this._super.apply(this, arguments).then(function () {
                // 监听窗口大小改变  
                $(window).on('resize', _.bind(self.on_resize, self));
                //拖拽中
                $(document).on('mousemove', _.bind(self._on_doc_mouse_move, self))
                    .on('mouseup', _.bind(self._on_doc_mouse_up, self));
            })
        },

        on_resize: function (e) {
            this._onResize()
        },

        destroy: function () {
            this._super.apply(this, arguments);
        },

        _on_doc_mouse_move: function (e) {
            if (this.flags.resizeStart) {
                // 防止对话框弹出时mouse_up消息没有收到
                if (e.buttons == 1) {
                    e.preventDefault();
                    if (this.flags.rule) {
                        var setWidth = this.flags.ruleWidth + e.clientX - this.flags.offset[0];
                        if (setWidth < this.flags.minWidth) setWidth = this.flags.minWidth;
                        this.flags.rule.style.width = setWidth + 'px';
                    }
                    this.resizing = 1;
                } else {
                    this.flags = {};
                    this.scrollPatch();
                    $('body').css('cursor', '');
                }
            }
        },

        _on_doc_mouse_up: function (e) {
            if (this.flags.resizeStart) {
                this.flags = {};
                this.scrollPatch();
                $('body').css('cursor', '');
            }
            if (this.resizing === 2) {
                this.resizing = null;
            }
        },

        /**
         * 重写，添加自动计算宽度属性
         * @constructor
         * @param {Widget} parent
         * @param {any} state
         * @param {Object} params
         * @param {boolean} params.hasSelectors
         */
        init: function (parent, state, params) {
            this._super.apply(this, arguments);

            table_id++;
            this.cur_table_id = table_id;
            this.options.index = table_id;

            // if addTrashIcon is true, there will be a small trash icon at the end
            // of each line, so the user can delete a record.
            this.addTrashIcon = params.addTrashIcon;

            // This attribute lets us know if there is a handle widget on a field,
            // and on which field it is set.
            this.handleField = null;
            // 通过 columnInvisibleFields 可以获取要隐藏的列, 
            // this.arch.children 可以取得所有的列信息
            this._processColumns(params.columnInvisibleFields || {});

            // 计算行属性
            this.rowDecorations = _.chain(this.arch.attrs)
                .pick(function (value, key) {
                    return DECORATIONS.indexOf(key) >= 0;
                }).mapObject(function (value) {
                    return py.parse(py.tokenize(value));
                }).value();

            // 是否有checkbox
            this.hasSelectors = params.hasSelectors;

            // 初始选中的项
            this.selection = params.selectedRecords || [];
            // groups的pager
            this.pagers = []; // instantiated pagers (only for grouped lists)
            // 是否可编辑
            this.editable = params.editable;
            // 分组, 暂时没有启用
            this.isGrouped = this.state.groupedBy.length > 0;
            // 是否有序号列
            this.has_serial = params.arch.attrs.has_serial;
        },

        _clear_content: function () {
            this.layHeader.empty();
            this.layBody.empty();
            this.pagerBox.empty();
        },

        _init_boxes: function () {
            // 主框子
            this.main_box = $(qweb.render('funenc.fnt_table', {
                widget: this
            }));
            this.$el.append(this.main_box);

            // 各个容器
            this.layHeader = this.$('.layui-table-header table');
            this.layBody = this.$('.layui-table-body table');
            this.layFixed = this.$('.layui-table-fixed');

            this.layMain = this.$('.layui-table-main');
            this.layMainHeader = this.$('.layui-table-header-main table');
            this.layMainBody = this.$('.layui-table-body-main table');

            this.layFixLeft = this.$('.layui-table-fixed-l');
            this.layFixLeftHeader = this.layFixLeft.find('.layui-table-header table');
            this.layFixLeftBody = this.layFixLeft.find('.layui-table-body table');

            this.layFixRight = this.$('.layui-table-fixed-r');
            this.layFixRightHeader = this.layFixRight.find('.layui-table-header table');
            this.layFixRightBody = this.layFixRight.find('.layui-table-body table');

            this.pagerBox = this.$('.pager_box')
            this.fullSize(); //让表格铺满

            var self = this;
            this.layMain.on('scroll', function () {
                var othis = $(this)

                var scrollLeft = othis.scrollLeft()
                var scrollTop = othis.scrollTop();

                self.$('.layui-table-header').scrollLeft(scrollLeft);
                self.layFixed.find('.layui-table-body').scrollTop(scrollTop);
            });

            // 行事件
            this.layBody.on('mouseenter', 'tr', function () { //鼠标移入行
                var othis = $(this)
                    , index = othis.index();
                self.layBody.find('tr:eq(' + index + ')').addClass('layui-table-hover')
            }).on('mouseleave', 'tr', function () { //鼠标移出行
                var othis = $(this)
                var index = othis.index();
                self.layBody.find('tr:eq(' + index + ')').removeClass('layui-table-hover')
            }).on('click', 'tr', function () { //单击行
                var index = $(this).parents('tr').eq(0).data('index')
                var tr = self.layBody.find('tr[data-index="' + index + '"]')
                tr.trigger("click");
            }).on('dblclick', 'tr', function () { //双击行
                var index = $(this).parents('tr').eq(0).data('index')
                var tr = self.layBody.find('tr[data-index="' + index + '"]')
                tr.trigger("dbclick");
            });
        },

        _renderAggregateCells: function (aggregateValues, isHeader) {
            var self = this;

            return _.map(this.columns, function (column, index) {
                if (isHeader && index === 0) {
                    return;
                }
                var $cell = $('<td></td>');
                var $div = $('<div/>');
                $div.addClass('layui-table-cell')
                if (config.debug) {
                    $cell.addClass(column.attrs.name);
                }
                if (column.attrs.name in aggregateValues) {
                    var field = self.state.fields[column.attrs.name];
                    var value = aggregateValues[column.attrs.name].value;
                    var help = aggregateValues[column.attrs.name].help;
                    var formatFunc = field_utils.format[column.attrs.widget];
                    if (!formatFunc) {
                        formatFunc = field_utils.format[field.type];
                    }
                    var formattedValue = formatFunc(value, field, {escape: true});

                    $div.addClass('o_list_number').attr('title', help).html(formattedValue);

                }
                $cell.append($div)
                return $cell;
            });
        },

        _renderFooter: function () {
            if (this.state.data.length === 0) {
                return false
            }

            var aggregates = {};
            _.each(this.columns, function (column) {
                if ('aggregate' in column) {
                    aggregates[column.attrs.name] = column.aggregate;
                }
            });
            var $cells = this._renderAggregateCells(aggregates, false);
            if (this.hasSelectors) {
                $cells.unshift($('<td>'));
            }
            var is_empty = true;
            _.each($cells, function ($cell) {

                if (!!$cell.find('div').html()) {
                    is_empty = false;
                    return false
                }
            });

            if (!is_empty) {
                $cells[0].find('div').html('合计').css({'float': 'right', 'font-weight': 'bold'});
                return $('<tfoot>').append($('<tr>').append($cells)).css({'font-weight': 'bold'});
            }
        }
        ,

        /**
         * 渲染视图
         */
        _renderView: function () {
            if (!this.main_box) {
                this._init_boxes();
            } else {
                this._clear_content();
            }
            this._computeAggregates();
            // 渲染头部
            var header_content = this._renderHeader();
            this.layMainHeader.append(header_content);

            // 主体body部份
            var body_content = this._renderBody();
            this.layMainBody.append(body_content);
            this.layMainBody.append(this._renderFooter());

            // fix_left部份header
            if (this.hasLeftFixedPart()) {
                var header_content_l = this._renderFixedHeader(true);
                this.layFixLeftHeader.append(header_content_l);

                // fixe_left body部份
                var body_content_body_l = this._renderFixedBody(true)
                this.layFixLeftBody.append(body_content_body_l)
            }

            if (this.hasRightFixedPart()) {
                // fix_left部份header
                var header_content_r = this._renderFixedHeader(false);
                this.layFixRightHeader.append(header_content_r);

                // fixe_left body部份
                var body_content_body_r = this._renderFixedBody(false)
                this.layFixRightBody.append(body_content_body_r)
            }

            this.setColsWidth(); // 自适应列宽

            var self = this;
            setTimeout(function () {
                self.scrollPatch(); // 滚动条补丁
            }, 0);

            // basic render 这样返回的
            return $.when();
        }
        ,

        //重置表格尺寸结构
        _onResize: function () {
            this.fullSize(); //让表格铺满
            this.setColsWidth(); //自适应列宽
            this.scrollPatch(); //滚动条补丁
        }
        ,

        _onThMousemove: function (e) {
            var othis = $(e.target)
            var oLeft = othis.offset().left
            var pLeft = e.clientX - oLeft;
            if (othis.data('unresize') || this.flags.resizeStart) {
                return;
            }

            //是否处于拖拽允许区域
            this.flags.allowResize = othis.width() - pLeft <= 10;
            $('body').css('cursor', (this.flags.allowResize ? 'col-resize' : ''));
        }
        ,

        _onThMouseleave: function (e) {
            if (this.flags.resizeStart)
                return;
            $('body').css('cursor', '');
        }
        ,

        /**
         * 鼠标按扭按下
         * @param {*} e
         */
        _onThMouseDown: function (e) {
            var self = this;
            var target = $(e.target);
            if (this.flags.allowResize) {
                var key = $(e.target).data('key');
                e.preventDefault();
                this.flags.resizeStart = true; //开始拖拽
                this.flags.offset = [e.clientX, e.clientY]; //记录初始坐标

                this.getCssRule(key, function (item) {
                    var width = item.style.width || target.outerWidth();
                    self.flags.rule = item;
                    self.flags.ruleWidth = parseFloat(width);
                    self.flags.minWidth = target.data('minwidth') || self.options.cellMinWidth;
                });
            }
        }
        ,

        /**
         * 设置表格高度，子表等可以设置为
         */
        fullSize: function () {
            if (!this.render_option.auto_height) {
                var height = this.height

                if (this.fullHeightGap) {
                    height = $(window).height() - this.fullHeightGap;
                    if (height < 135) {
                        height = 135;
                    }
                }

                if (!height) return;

                // 减去列头区域的高度, 如果是有分页还要减去分页的高度
                // 此处的数字常量是为了防止容器处在隐藏区域无法获得高度的问题，暂时只对默认尺寸的表格做支持。
                var bodyHeight = parseFloat(height) - (this.layMainHeader.outerHeight() || 38);
                if (this._has_pager()) {
                    bodyHeight -= 51;
                }

                // 这里还要考虑是否有分页的情况
                this.layMain.css('height', bodyHeight);
            } else {
                this.$el.css('height', 'auto');
            }
        }
        ,

        /**
         * 判断是否显示分页
         */
        _has_pager: function () {
            var controller = this.getParent();
            if (controller && controller.model && controller.model.get) {
                var data = controller.model.get(controller.handle, {raw: true});
                if (data.count <= data.limit) {
                    return false;
                } else {
                    return true;
                }
            } else {
                return false
            }
        }
        ,

        // 添加序列号列头
        _render_serial_header: function ($tr) {
            if (this.has_serial) {
                $tr.prepend($('<th class="o_list_row_number_header serial">').html('#'));
            }
        }
        ,

        // 添加序列号列内容
        _render_serial_row: function ($tr, record) {
            if (this.mode !== 'edit' && this.state.groupedBy.length == 0 && this.has_serial) {
                var index = this.state.data.findIndex(function (e) {
                    return record.id === e.id
                })
                if (index !== -1) {
                    $tr.prepend($('<th class="serial">').html(index + 1));
                }
            }
        }
        ,

        /**
         * 渲染头部, 表格头有可能会渲染多级，之前没有处理这个
         * @param {} isGrouped
         */
        _renderHeader: function (isGrouped) {
            var $tr = $('<tr>')
                .append(_.map(this.columns, this._renderHeaderCell.bind(this)));
            if (this.hasSelectors) {
                var selector = this._renderSelector('th');
                $tr.prepend(selector);
            }
            if (this.addTrashIcon) {
                var $th = $('<th><div></div></th>')
                $th.find('div').addClass('o_list_record_selector lay-table-trash layui-table-cell');
                $tr.append($th);
            }
            this._render_serial_header($tr)
            return $('<thead>').append($tr);
        }
        ,

        /**
         * 只渲染需要渲染的部份
         * @param {} bLeft
         */
        _renderFixedBody: function (bLeft) {
            var $rows = this._renderFixedRows(bLeft);
            return $('<tbody>').append($rows);
        }
        ,

        /**
         * 重写，去掉4行
         */
        _renderBody: function () {
            var $rows = this._renderRows();
            return $('<tbody>').append($rows);
        }
        ,

        /**
         * 固定列需要过滤
         * @param {} b_left
         */
        _renderFixedRows: function (b_left) {
            var self = this;
            return _.map(this.state.data, function (record) {
                return self._renderFixedRow(record, b_left)
            });
        }
        ,

        /**
         * 只渲染fixed的数据
         * @param {} record
         * @param {*} b_left
         */
        _renderFixedRow: function (record, b_left) {
            var self = this;
            var $cells = _.map(this.columns, function (node, index) {
                if (b_left && node.attrs.fixed_left) {
                    return self._renderBodyCell(record, node, index, {mode: 'readonly', 'fixed': true});
                } else if (!b_left && node.attrs.fixed_right) {
                    return self._renderBodyCell(record, node, index, {mode: 'readonly', 'fixed': true});
                }
            });
            var $tr = $('<tr/>', {class: 'o_data_row o_fixed_row'})
                .data('id', record.id)
                .append($cells);

            if (b_left && this.hasSelectors) {
                $tr.prepend(this._renderSelector('td', !record.res_id));
            }
            this._render_serial_row($tr, record);
            this._setDecorationClasses(record, $tr);

            return $tr;
        }
        ,

        /**
         * 重写，添加width属性
         *
         * @private
         * @param {Object} node
         * @returns {jQueryElement} a <th> element
         */
        _renderHeaderCell: function (node) {
            var name = node.attrs.name;
            var order = this.state.orderedBy;
            var isNodeSorted = order[0] && order[0].name === name;
            var field = this.state.fields[name];
            // 添加样式
            var thClassName = ' layui-table-cell laytable-cell-' + node.key
            var $th = $('<th><div></div></th>');
            var $div = $th.find('div').addClass(thClassName);
            if (node.tag === 'widget') {
                $div.text(node.attrs.string)
                    .data('name', name)
                    .data('key', node.key)
            }

            if (!field) {
                return $th;
            }
            // 描述, 居然是通过组件的描述来的
            var description;
            if (node.attrs.widget) {
                description = this.state.fieldsInfo.list[name].Widget.prototype.description;
            }
            if (description === undefined) {
                description = node.attrs.string || field.string;
            }
            $div.text(description)
                .data('name', name)
                .data('field', name)
                .data('key', node.key)
                .toggleClass('o-sort-down', isNodeSorted ? !order[0].asc : false)
                .toggleClass('o-sort-up', isNodeSorted ? order[0].asc : false)
                .addClass(field.sortable && 'o_column_sortable');

            if (isNodeSorted) {
                $div.attr('aria-sort', order[0].asc ? 'ascending' : 'descending');
            }

            if (field.type === 'float' || field.type === 'integer' || field.type === 'monetary') {
                $div.css({textAlign: 'right'});
            }

            // 调试模式下输出更多信息
            if (config.debug) {
                var fieldDescr = {
                    field: field,
                    name: name,
                    string: description || name,
                    record: this.state,
                    attrs: node.attrs,
                };
                this._addFieldTooltip(fieldDescr, $div);
            }

            return $th;
        }
        ,

        /**
         * 重写，添加class
         * @param {} record
         * @param {*} node
         * @param {*} colIndex
         * @param {*} options
         */
        _renderBodyCell: function (record, node, colIndex, options) {
            var tdClassName = 'o_data_cell';

            if (node.tag === 'button') {
                tdClassName += ' o_list_button';
            } else if (node.tag === 'field') {
                var typeClass = FIELD_CLASSES[this.state.fields[node.attrs.name].type];
                if (typeClass) {
                    tdClassName += (' ' + typeClass);
                }
                if (node.attrs.widget) {
                    tdClassName += (' o_' + node.attrs.widget + '_cell');
                }
            }

            // 添加新的类，用于控制宽度
            tdClassName += ' layui-table-cell laytable-cell-' + node.key

            var $td = $('<td><div></div></td>', {class: tdClassName});
            var $div = $td.find('div').addClass(tdClassName)

            // We register modifiers on the <td> element so that it gets the correct
            // modifiers classes (for styling)
            var modifiers = this._registerModifiers(node, record, $div, _.pick(options, 'mode'));
            // If the invisible modifiers is true, the <td> element is left empty.
            // Indeed, if the modifiers was to change the whole cell would be
            // rerendered anyway.
            if (modifiers.invisible && !(options && options.renderInvisible)) {
                return $td;
            }

            if (node.tag === 'button') {
                $div.append(this._renderButton(record, node));
                return $td;
            } else if (node.tag === 'widget') {
                $div.append(this._renderWidget(record, node));
                return $td;
            }

            if (node.attrs.widget || (options && options.renderWidgets)) {
                var $el = this._renderFieldWidget(node, record, _.pick(options, 'mode', 'fixed'));
                this._handleAttributes($el, node);
                $div.append($el);
                return $td;
            }

            var name = node.attrs.name;
            var field = this.state.fields[name];
            var value = record.data[name];
            var formattedValue = field_utils.format[field.type](value, field, {
                data: record.data,
                escape: true,
                isPassword: 'password' in node.attrs,
            });
            this._handleAttributes($div, node);
            $div.html(formattedValue)
            return $td;
        }
        ,

        /**
         * 重写，添加fixed标识
         * @param {*} node
         * @param {*} record
         * @param {*} options
         */
        _renderFieldWidget: function (node, record, options) {
            options = options || {};
            var fieldName = node.attrs.name;
            // Register the node-associated modifiers
            var mode = options.mode || this.mode;
            var modifiers = this._registerModifiers(node, record, null, options);
            // Initialize and register the widget
            // Readonly status is known as the modifiers have just been registered
            var Widget = record.fieldsInfo[this.viewType][fieldName].Widget;
            var widget = new Widget(this, fieldName, record, {
                mode: modifiers.readonly ? 'readonly' : mode,
                viewType: this.viewType,
            });

            // 标识为fixed
            if (options.fixed) {
                widget.fixed = true
            }

            // Register the widget so that it can easily be found again
            if (this.allFieldWidgets[record.id] === undefined) {
                this.allFieldWidgets[record.id] = [];
            }
            this.allFieldWidgets[record.id].push(widget);

            widget.__node = node; // TODO get rid of this if possible one day

            // Prepare widget rendering and save the related deferred
            var def = widget._widgetRenderAndInsert(function () {
            });
            var async = def.state() === 'pending';
            var $el = async ? $('<div>') : widget.$el;
            if (async) {
                this.defs.push(def);
            }

            // Update the modifiers registration by associating the widget and by
            // giving the modifiers options now (as the potential callback is
            // associated to new widget)
            var self = this;
            def.then(function () {
                if (async) {
                    $el.replaceWith(widget.$el);
                }
                self._registerModifiers(node, record, widget, {
                    callback: function (element, modifiers, record) {
                        element.$el.toggleClass('o_field_empty', !!(
                            record.data.id
                            && (modifiers.readonly || mode === 'readonly')
                            && !element.widget.isSet()
                        ));
                    },
                    keepBaseMode: !!options.keepBaseMode,
                    mode: mode,
                });
                self._postProcessField(widget, node);
            });

            return $el;
        }
        ,

        /**
         * 重写，过滤到fixed的情况
         * @param {*} record
         * @param {*} currentIndex
         * @param {*} options
         */
        _activateFieldWidget: function (record, currentIndex, options) {
            options = options || {};
            _.defaults(options, {inc: 1, wrap: false});
            currentIndex = Math.max(0, currentIndex); // do not allow negative currentIndex

            var recordWidgets = _.filter(this.allFieldWidgets[record.id] || [], function (widget) {
                return !widget.fixed
            })

            for (var i = 0; i < recordWidgets.length; i++) {
                var widget = recordWidgets[currentIndex]
                if (widget && widget.fixed) {
                    currentIndex += options.inc;
                    if (currentIndex >= recordWidgets.length) {
                        if (options.wrap) {
                            currentIndex -= recordWidgets.length;
                            continue;
                        } else {
                            return -1;
                        }
                    }
                }
                var activated = recordWidgets[currentIndex].activate(
                    {
                        event: options.event,
                        noAutomaticCreate: options.noAutomaticCreate || false
                    });
                if (activated) {
                    return currentIndex;
                }

                currentIndex += options.inc;
                if (currentIndex >= recordWidgets.length) {
                    if (options.wrap) {
                        currentIndex -= recordWidgets.length;
                    } else {
                        return -1;
                    }
                } else if (currentIndex < 0) {
                    if (options.wrap) {
                        currentIndex += recordWidgets.length;
                    } else {
                        return -1;
                    }
                }
            }
            return -1;
        }
        ,

        /**
         * 遍历表头，取得表头信息，对要显示的字段添加index和key的信息, 如果是有选择框的话则在前边添加一列
         * @param {*} columnInvisibleFields
         */
        _processColumns: function (columnInvisibleFields) {
            var self = this;
            self.handleField = null;

            // 取得所有要显示的列
            this.columns = _.reject(this.arch.children, function (c) {
                if (c.tag === 'control') {
                    return true;
                }
                var reject = c.attrs.modifiers.column_invisible;

                // width
                if (c.attrs.width) {
                    c.width = c.attrs.width
                } else {
                    c.width = 100;
                }

                if (c.attrs.name in columnInvisibleFields) {
                    reject = columnInvisibleFields[c.attrs.name];
                }

                if (!reject && c.attrs.widget === 'handle') {
                    self.handleField = c.attrs.name;
                }

                return reject;
            });

            var index = 0;
            if (this.hasSelectors) {
                index += 1
            }

            // 设置index和key
            _.each(this.columns, function (column) {
                column.index = index
                column.key = self.cur_table_id + '-' + index
                index++
            })
        }
        ,

        /**
         * 取得button列的数量，这个还要补齐header的
         */
        button_col_count: function () {
            var count = 0;
            _.map(this.columns, function (node, index) {
                if (node.tag == 'button') {
                    count++;
                }
            });
            return count;
        }
        ,

        /**
         * 取得widget col 的数里
         * @param {*} bLeft
         */

        /**
         * 渲染固定部份head
         * @param {*} bLeft
         */
        _renderFixedHeader: function (bLeft) {
            var tmp_columns = this.columns.filter(function (column) {
                if (bLeft && column.attrs.fixed_left) {
                    return true
                } else if (!bLeft && column.attrs.fixed_right) {
                    return true
                }
                return false
            })
            // 如果是左侧则添加selector
            var $tr = $('<tr>')
                .append(_.map(tmp_columns, this._renderHeaderCell.bind(this)));
            if (bLeft && this.hasSelectors) {
                $tr.prepend(this._renderSelector('th'));
            }
            this._render_serial_header($tr)
            return $('<thead>').append($tr);
        }
        ,

        /**
         *
         * @param {*} tag
         * @param {*} Input
         */
        _renderSelector: function (tag, disableInput) {
            var $content = dom.renderCheckbox();
            if (disableInput) {
                $content.find("input[type='checkbox']").prop('disabled', disableInput);
            }
            var $th = $('<th><div></div></th>')
            $th.find('div').addClass('o_list_record_selector layui-table-cell').append($content);
            return $th;
        }
        ,

        /**
         * 取得客户区宽度
         */
        get_box_width: function () {
            var self = this
            var getWidth = function (parent) {
                var width, isNone;
                parent = parent || self.getParent()
                try {
                    width = parent.$el.width();
                    isNone = parent.$el.css('display') === 'none';
                } catch (e) {
                }
                if (parent && parent[0] && (!width || isNone))
                    return getWidth(parent.getParent());
                return width;
            };
            return getWidth();
        }
        ,

        //获取滚动条宽度
        getScrollWidth: function (elem) {
            var width = 0;
            if (elem) {
                width = elem.offsetWidth - elem.clientWidth;
            } else {
                elem = document.createElement('div');
                elem.style.width = '100px';
                elem.style.height = '100px';
                elem.style.overflowY = 'scroll';

                document.body.appendChild(elem);
                width = elem.offsetWidth - elem.clientWidth;
                document.body.removeChild(elem);
            }
            return width;
        }
        ,

        //滚动条补丁
        scrollPatch: function () {
            var self = this;
            var layMainTable = this.layMain.children('table')

            window.layMain = this.layMain

            var scollWidth = this.layMain.width() - this.layMain.prop('clientWidth') // 纵向滚动条宽度
            var scollHeight = this.layMain.height() - this.layMain.prop('clientHeight') // 横向滚动条高度

            var outWidth = layMainTable.outerWidth() - self.layMain.width() //表格内容器的超出宽度

            //添加补丁
            var addPatch = function (elem) {
                if (scollWidth && scollHeight) {
                    elem = elem.eq(0);
                    if (!elem.find('.layui-table-patch')[0]) {
                        var patchElem = $('<th class="layui-table-patch"><div class="layui-table-cell"></div></th>'); //补丁元素
                        patchElem.find('div').css({
                            width: scollWidth
                        });
                        elem.find('tr').append(patchElem);
                    }
                } else {
                    elem.find('.layui-table-patch').remove();
                }
            }

            // header 打补丁
            addPatch(self.layHeader);

            // 固定列区域高度
            var mainHeight = self.layMain.height();
            var fixHeight = mainHeight - scollHeight;
            self.layFixed.find('.layui-table-body').css('height', layMainTable.height() >= fixHeight ? fixHeight : 'auto');

            // 表格宽度小于容器宽度时，隐藏固定列
            self.layFixRight[outWidth > 0 ? 'removeClass' : 'addClass']('layui-hide');

            // 操作栏
            self.layFixRight.css('right', scollWidth - 1);
        }
        ,

        /**
         * 自动计算宽度，要考虑selection才对
         */
        setColsWidth: function () {
            var self = this;
            var colNums = 0;//列个数
            var autoColNums = 0; //自动列宽的列个数
            var autoWidth = 0; //自动列分配的宽度
            var countWidth = 0; //所有列总宽度和
            var cntrWidth = this.get_box_width();

            // 统计列个数，本身已经隐藏了个数
            colNums = this.columns.length;

            // 减去边框差和滚动条宽
            cntrWidth = cntrWidth - function () {
                return colNums + 1;
            }() - self.getScrollWidth(self.layMain[0]) - 1;

            // 计算自动分配的宽度
            var getAutoWidth = function (back) {
                // 遍历所有列
                _.each(self.columns, function (column) {
                    var width = 0
                    var minWidth = column.attrs.minWidth || self.options.cellMinWidth; //最小宽度

                    if (!back) {
                        width = column.attrs.width || 0;
                        if (/\d+%$/.test(width)) { //列宽为百分比
                            width = Math.floor((parseFloat(width) / 100) * cntrWidth);
                            width < minWidth && (width = minWidth);
                        } else if (!width) { //列宽未填写
                            column.width = width = 0;
                            autoColNums++;
                        }
                    } else if (autoWidth && autoWidth < minWidth) {
                        autoColNums--;
                        width = minWidth;
                    }

                    if (column.hide) width = 0;
                    countWidth = countWidth + width;
                });

                // 如果未填充满，则将剩余宽度平分
                (cntrWidth > countWidth && autoColNums) && (
                    autoWidth = (cntrWidth - countWidth) / autoColNums
                );
            }

            getAutoWidth();
            getAutoWidth(true); //重新检测分配的宽度是否低于最小列宽

            // 记录自动列数
            self.autoColNums = autoColNums;

            // 设置列宽
            _.each(self.colNums, function (column) {
                var minWidth = column.minWidth || self.options.cellMinWidth;

                // 给位分配宽的列平均分配宽
                if (column.width === 0) {
                    self.getCssRule(self.options.index + '-' + column.key, function (item) {
                        item.style.width = Math.floor(autoWidth >= minWidth ? autoWidth : minWidth) + 'px';
                    });
                }
                // 给设定百分比的列分配列宽
                else if (/\d+%$/.test(column.width)) {
                    self.getCssRule(self.options.index + '-' + column.key, function (item) {
                        item.style.width = Math.floor((parseFloat(column.width) / 100) * cntrWidth) + 'px';
                    });
                }
            })

            // 填补 Math.floor 造成的数差
            var patchNums = self.layMain.width() - self.getScrollWidth(self.layMain[0])
                - self.layMain.children('table').outerWidth();

            if (self.autoColNums && patchNums >= -colNums && patchNums <= colNums) {
                var getEndTh = function (th) {
                    var field;
                    th = th || self.layHeader.eq(0).find('thead th:last-child')
                    field = th.data('field');
                    if (!field && th.prev()[0]) {
                        return getEndTh(th.prev())
                    }
                    return th
                }
                var th = getEndTh()
                var key = th.data('key');

                self.getCssRule(key, function (item) {
                    var width = item.style.width || th.outerWidth();
                    item.style.width = (parseFloat(width) + patchNums) + 'px';

                    // 二次校验，如果仍然出现横向滚动条（通常是 1px 的误差导致）
                    if (self.layMain.height() - self.layMain.prop('clientHeight') > 0) {
                        item.style.width = (parseFloat(item.style.width) - 1) + 'px';
                    }
                });
            }
        }
        ,

        /**
         * 取得css样式, 对有特定属性的元素调用
         * @param {*} key
         * @param {*} callback
         */
        getCssRule: function (key, callback) {
            var that = this
                , style = that.$el.find('style')[0]
                , sheet = style.sheet || style.styleSheet || {}
                , rules = sheet.cssRules || sheet.rules;
            _.each(rules, function (item, index) {
                if (item.selectorText === ('.laytable-cell-' + key)) {
                    return callback(item), true;
                }
            })
        }
        ,

        /**
         * 取得
         */
        getTotalWidth: function () {
            var that = this
            var style = that.$el.find('style')[0]
            var sheet = style.sheet || style.styleSheet || {}
            var rules = sheet.cssRules || sheet.rules;
            var total_width = 0;
            _.each(rules, function (item, index) {
                total_width += item.style.width;
            })
            return total_width;
        }
        ,

        /**
         * check have fixed left
         */
        hasLeftFixedPart: function () {
            var self = this
            return _.find(this.arch.children, function (item) {
                if (item.attrs.fixed_left || self.hasSelectors) {
                    return true;
                }
                return false;
            })
        }
        ,

        /**
         * check have fixed right column
         */
        hasRightFixedPart: function () {
            return _.find(this.arch.children, function (item) {
                if (item.attrs.fixed_right) {
                    return true;
                }
                return false;
            })
        }
        ,

        /**
         * 重写，删除除最后一行
         */
        _renderRows: function () {
            var $rows = this._super();
            if (this.addCreateLine) {
                $rows.pop()
            }
            return $rows;
        }
        ,

        /**
         * 这里由于被 edit listrender 改掉, 所以这里要还原回来
         */
        _renderRow: function (record, index) {
            var self = this;
            this.defs = []; // TODO maybe wait for those somewhere ?
            var $cells = _.map(this.columns, function (node, index) {
                return self._renderBodyCell(record, node, index, {mode: 'readonly'});
            });
            delete this.defs;

            var $tr = $('<tr/>', {class: 'o_data_row'})
                .data('id', record.id)
                .append($cells);

            if (this.hasSelectors) {
                $tr.prepend(this._renderSelector('td', !record.res_id));
            }
            this._render_serial_row($tr, record);
            this._setDecorationClasses(record, $tr);
            var condition_delete = eval("(" + this.arch.attrs.condition_delete + ")");
            var force_delete = true;
            _.each(condition_delete, function (value, key) {
                if (record.data[key] === value && force_delete) {
                    force_delete = false;
                }
            });
            if (this.addTrashIcon && force_delete) {
                var $icon = this.isMany2Many ?
                    $('<button>', {
                        class: 'fa fa-times',
                        name: 'unlink',
                        'aria-label': _t('Unlink row ') + (index + 1)
                    }) :
                    $('<button>', {
                        class: 'fa fa-trash-o',
                        name: 'delete',
                        'aria-label': _t('Delete row ') + (index + 1)
                    });
                var $td = $('<td><div></div></td>');
                $td.addClass('o_list_record_remove');
                var $div = $td.find('div').append($icon);
                $div.addClass('layui-table-cell lay-table-trash')
                $tr.append($td);
            }
            return $tr;
        }
        ,

        _onRemoveIconClick: function (event) {
            event.stopPropagation();
            var $row = $(event.target).closest('tr');
            var id = $row.data('id');
            if ($row.hasClass('o_selected_row')) {
                this.trigger_up('list_record_remove', {id: id});
            } else {
                var self = this;
                this.unselectRow().then(function () {
                    self.trigger_up('list_record_remove', {id: id});
                });
            }
        }
        ,

        /**
         * 渲染分布
         */
        _render_pager: function () {
            var totalNumber = this.state.count || 0;
            if (totalNumber <= this.state.limit) {
                var $pager = $('<div class="funenc_pager light-theme simple-pagination" style="height:31px"></div>')
                $pager.appendTo(this.pagerBox)
                return;
            }
            var start_index = this.state.offset;
            var pageSize = this.state.limit;
            var currentPage = start_index / pageSize + 1;
            var pager = new FunencPager(this, totalNumber, currentPage, pageSize);
            this.funenc_pager = pager;

            pager.on('funenc_pager_changed', this, function (info) {
                this.funenc_pager.disable();

                var offset = info.data.offset;
                var limitChanged = info.data.limitChanged;

                var controller = this.getParent();
                var data = controller.model.get(controller.handle, {raw: true});

                controller.reload({limit: data.limit, offset: offset})
                    .then(function () {
                        // Reset the scroll position to the top on page changed only
                        if (!limitChanged) {
                            controller.trigger_up('scrollTo', {top: 0});
                        }
                    })
                    .then(this.funenc_pager.enable.bind(this.funenc_pager));
            })

            pager.appendTo(this.pagerBox);
        }
        ,

        /**
         * 更新分页, 扩展在底部增加分页
         */
        _updatePager: function () {
            this._super.apply(this, arguments);

            if (this.funenc_pager) {
                var data = this.model.get(this.handle, {raw: true});

                var totalNumber = data.count || 0;
                var start_index = data.count.offset;
                var currentPage = start_index / data.limit;

                this.funenc_pager.updateState({
                    totalNumber: totalNumber,
                    currentPage: currentPage,
                    pageSize: data.limit
                });

                var isRecord = data.type === 'record';
                var hasData = !!data.count;
                var isGrouped = data.groupedBy ? !!data.groupedBy.length : false;
                var isNew = this.model.isNew(this.handle);
                var isPagerVisible = isRecord ? !isNew : (hasData && !isGrouped);

                this.funenc_pager.do_toggle(isPagerVisible);
            }
        }
        ,

        /**
         * 编辑行
         * @param {*} recordID
         */
        editRecord: function (recordID) {
            var rowIndex = _.findIndex(this.state.data, {id: recordID});
            this._selectCell(rowIndex, 0);
        }
        ,

        /**
         * 移除行
         */
        removeLine: function (state, recordID) {
            // var rowIndex = _.findIndex(this.state.data, {id: recordID});
            // this.state = state;
            // if (rowIndex === -1) {
            //     return;
            // }

            // if (rowIndex === this.currentRow) {
            //     this.currentRow = null;
            // }

            // // remove the row
            // var $row = this.$('.o_data_row:nth(' + rowIndex + ')');
            // if (this.state.count >= 4) {
            //     $row.remove();
            // } else {
            //     $row.replaceWith(this._renderEmptyRow());
            // }

            // this._destroyFieldWidgets(recordID);
        }
    });

    return fnt_table_render;

});
