odoo.define('funenc.SideBarMenu', function (require) {
    "use strict";

    /**
     * 侧边栏菜单
     */
    var Widget = require('web.Widget');
    var ThemeColorPicker = require('funenc.ThemeColorPicker')
    var ThemeColor = require('funenc.ThemeColor');
    var core = require('web.core');

    var SideBarMenu = Widget.extend({
        template: 'funenc_side_bar_menu',
        cur_main_menu: undefined,
        side_bar_open: true,
        side_bar_close_duaration: 500,

        /**
         * init menuData
         * @param {*} parent
         * @param {*} menuData
         */
        init: function (parent, menuData) {
            this.menuData = menuData
            this._super.apply(this, arguments);
        },

        /**
         * start
         */
        start: function () {
            this._super.apply(this, arguments);
            // 绑定事件
            var self = this;

            this.$('.sidebarnavSec a').on('click', function (e) {
                // 折叠展示
                e.preventDefault()
                var clicked_item = $(this)
                // 移除所有的展开项
                var this_active = clicked_item.hasClass("active");
                $("ul", clicked_item.parents("ul:first")).removeClass("in");
                // 移除所有的active
                if (clicked_item.hasClass('has-arrow')) {
                    var sub_active = clicked_item.next("ul").find('.active')
                    $("a", clicked_item.parents("ul:first")).removeClass("active");
                    $(sub_active).addClass('active');
                } else {
                    $("a", clicked_item.parents("ul:first")).removeClass("active");
                    setTimeout(function () {
                        var menu_id = clicked_item.data('menu_id');
                        var action_id = clicked_item.data('action-id');
                        if (action_id) {
                            self._trigger_menu_clicked(menu_id, action_id);
                            // 暂时没有使用这个状态
                            self.current_secondary_menu = menu_id;
                        }
                    }, 0);
                }
                // 如果本身是激活状态则不作处理切换为收起，否则添加展开状态
                if(!this_active){
                    clicked_item.next("ul").addClass("in");
                    clicked_item.addClass("active");
                }
            });

            self.$('.sidebarnavSec >li >a.has-arrow').on('click', function (e) {
                e.preventDefault();
            });

            // 美化滚动条
            this.$(".scroll-sidebar").perfectScrollbar({})

            // 初始化数据 
            this.sections = this.$('.funenc_sub_menu_section');
//            core.bus.on('show_sidebar', this, this._show.bind(this));
//            core.bus.on('hide_sidebar', this, this._hide.bind(this));
        },

        _trigger_menu_clicked: function (menu_id, action_id) {
            this.trigger_up('menu_clicked', {
                id: menu_id,
                action_id: action_id,
                previous_menu_id: this.current_secondary_menu || this.current_primary_menu,
            });
        },

        /**
         * 选择菜单项
         */
        select_menu_item: function (menu_id) {
            var menu_item = this.$('.sidebar-link[data-menu=' + menu_id + ']')
            if (menu_item) {
                // close all the 
                this.$('li.active').removeClass("active")
                this.$('li.in').removeClass("in");
                menu_item.parents("ul.collapse").addClass("in");
                menu_item.parent('li').parents("li.sidebar-item").find("a:first").addClass("active");
                menu_item.addClass('active')
            }
        },

        /**
         * 选中第一个子级菜单
         */
        open_first_menu_item: function (menu_id) {
            var section = _.find(this.sections, function (section) {
                return $(section).attr("id") == "funenc_tabs_" + menu_id;
            })
            if (section) {
                var link = $(section).find('.sidebar-link:not(.has-arrow)')
                if (link && link.length > 0) {
                    var menu_id = $(link[0]).data("menu");
                    if (menu_id) {
                        $(link[0]).find('span').click()
                        this.select_menu_item(menu_id);
                    }
                }
            }
        },

        _onToggleClick: function (event) {
            var self = this
            if (!self.side_bar_open) {
                this.$el.animate({
                    left: 0
                }, {
                    duration: self.side_bar_close_duaration,
                    done: function () {
                        self.switchArrow("right");
                        $('.o_main').css('padding-left', self.$el.width())
                        self.side_bar_open = true
                    }
                });
                $('.o_main').animate({
                    'padding-left': this.$el.width()
                }, {
                    duration: self.side_bar_close_duaration,
                });
            } else {
                this.$el.animate({
                    left: -this.$el.width()
                }, {
                    duration: self.side_bar_close_duaration,
                    done: function () {
                        self.switchArrow('left');
                        $('.o_main').css('padding-left', '0px')
                        self.side_bar_open = false
                    }
                });
                $('.o_main').animate({
                    'padding-left': 0
                }, {
                    duration: self.side_bar_close_duaration,
                });
            }
        },

        /**
         * 切换箭头符号
         * @param {} direction
         */
        switchArrow: function (direction) {
            var $icon = this.$(".toggler span");
            $icon.removeClass();
            if (direction === "left") {
                $icon.addClass('fa-angle-double-right');
            } else if (direction === "right") {
                $icon.addClass('fa-angle-double-left');
            }
            $icon.addClass('fa');
        },
        _hide: function(){
            this.$el.show();
        },
        _show: function(){
            this.$el.hide()
        }
    });

    /**
     * 菜单颜色选择
     */
    var SideBarThemeColor = ThemeColorPicker.extend({
        title: '侧边栏:',
        color: 'transparent',
        cls_key: 'left-sidebar',
        css_key: 'background',
        sequence: 51,  // 用于排序
    })

    // 注册颜色设置
    ThemeColor.Items.push(SideBarThemeColor);

    return SideBarMenu;
});