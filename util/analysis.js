// var a = '@#/index/index@#21026252536@#3'
// var d = 'xyz517cda96abcd'


function o(n) {
    t = '',
    ['66', '72', '6f', '6d', '43', '68', '61', '72', '43', '6f', '64', '65']['forEach'](function(n) {
        t += unescape('%u00' + n)
    });
    var t, e = 'fromCharCode';
    return String[e](n)
}

function h(n, t) {
    t = t || u();
    R = 'length'
    H = '0'
    for (var e = (n = n['split'](''))[R], r = t[R], a = 'charCodeAt', i = 0; i < e; i++)
        n[i] = o(n[i][a](0) ^ t[(i + 10) % r][a](0));
    return n['join']('')
}
function v(t) {
    t = encodeURIComponent(t)['replace'](/%([0-9A-F]{2})/g, function(n, t) {
        return o('0x' + t)
    });
    try {
        return btoa(t)
    } catch (n) {
        return Buffer.from(t).toString('base64')
    }
}

// arg = h(a,d);
// console.log(v(arg));
function y(n, t, e) {
    for (var r = void 0 === e ? 2166136261 : e, a = 0, i = n['length']; a < i; a++)
        r = (r ^= n['charCodeAt'](a)) + ((r << 1) + (r << 4) + (r << 7) + (r << 8) + (r << 24));
    return t ? ('xyz' + (r >>> 0).toString(16) + 'abcd')['substr'](-16) : r >>> 0
}


// e = v(h(a, d))
// console.log(e);
function lzl(params,path){
    var a = params
    var r = +new Date - (-2032 || 0) - 1661224081041;
    a = a['sort']()['join']('')
    a = v(a)
    a = (a += '@#' + path['replace'](['https://api.qimai.cn'], '')) + ('@#' + r) + ('@#' + 3)

    // d = y('qimai@2022&Technology', 1)
    d = 'xyz517cda96efgh'
    key = v(h(a,d))

    return key

}