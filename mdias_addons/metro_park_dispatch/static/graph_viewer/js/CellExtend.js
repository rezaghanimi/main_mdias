
/**
 * 扩展mxCell, 添加findSubCell函数, 做了缓存处理
 */
mxCell.prototype.getSubCell = function (name) {
    var result = []
    var cells = this.children || []
    for (var index = 0; index < cells.length; index++) {
        var subCell = cells[index]
        if ((subCell.children || []).length > 0) {
            result = result.concat(subCell.getSubCell(name));
        } else if (subCell.getAttribute('name') == name) {
            result.push(subCell)
        }
    }
    return result
}

/*
* 取得带有uid属性的cell
*/
mxCell.prototype.getParkElement = function () {
    if (this.getAttribute('uid')) {
        return this
    } else {
        if (this.parent != null) {
            return this.parent.getParkElement()
        } else {
            return null
        }
    }
}

mxCell.prototype.elementStatus = undefined;

/**
 * 取得元素的站场地图状态
 */
mxCell.prototype.getParkStatus = function () {
    return this.elementStatus;
}

/**
 * 取得元素的站场地图状态
 */
mxCell.prototype.setParkStatus = function (status) {
    this.elementStatus = status;
}
