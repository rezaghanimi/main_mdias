/**
 * Created by artorias on 2018/9/21.
 * 添加option属性让用户决定上传文件的大小限制
 */
odoo.define("funenc.binary_field", function (require) {
  "use strict";

  var basic_fields = require("web.basic_fields");

  /**
   * 图像
   */
  basic_fields.FieldBinaryImage.include({
    init: function (parent, name, record) {
      this._super.apply(this, arguments);
      this.fields = record.fields;
      this.useFileAPI = !!window.FileReader;
      this.max_upload_size = this.attrs.max_upload_kb
        ? parseInt(this.attrs.max_upload_kb) * 1024
        : 100 * 1024 * 1024; // 25Mo
      if (!this.useFileAPI) {
        var self = this;
        this.fileupload_id = _.uniqueId("o_fileupload");
        $(window).on(this.fileupload_id, function () {
          var args = [].slice.call(arguments).slice(1);
          self.on_file_uploaded.apply(self, args);
        });
      }
    }
  });

  /**
   * 文件
   */
  basic_fields.FieldBinaryFile.include({
    init: function (parent, name, record) {
      this._super.apply(this, arguments);
      this.fields = record.fields;
      this.useFileAPI = !!window.FileReader;
      this.max_upload_size = this.attrs.max_upload_kb
        ? parseInt(this.attrs.max_upload_kb) * 1024
        : 100 * 1024 * 1024; // 25Mo
      if (!this.useFileAPI) {
        var self = this;
        this.fileupload_id = _.uniqueId("o_fileupload");
        $(window).on(this.fileupload_id, function () {
          var args = [].slice.call(arguments).slice(1);
          self.on_file_uploaded.apply(self, args);
        });
      }
      this.filename_value = this.recordData[this.attrs.filename];
    }
  });
});
