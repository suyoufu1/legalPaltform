        $.fn.pageList = function (arg, methodName) {
            if (typeof methodName === "string" && $.trim(methodName) != "") {
                switch (methodName) {
                    case 'refresh'://刷新当前页,一般用于删除或者更新后
                        $(this).each(function () {
                            var arg = $(this).data('pageListArg');
                            if (arg != null && typeof arg.clickCallback === "function") {
                                arg.clickCallback(arg.currentPage);
                            }
                        });
                        break;
                }
            }
            else {
                var defaultSettings = {
                    prevText: 'Prev',//显示的前一页文本
                    nextText: 'Next',//显示的下一页文本
                    showGoLink: 'auto',//是否显示快速跳转，可能的值为auto 自动判断；true 永远显示；false 永不显示
                    goInputType: 'select',//如何显示快速跳转输入，可能的值为select 下拉列表；text 输入框，默认值为select
                    goText: 'Go',//显示的快速跳转文本
                    recordText: '',//显示记录数，为空时不显示，否则按照占位符显示文本，{0}表示总页数，{1}表示总记录数
                    clickCallback: function (currentPage) { },//链接被点击时触发的事件，currentPage表示当前点击的是第几页，索引从1开始
                    renderPerCall: true,//是否每次点击都重新绘制，如果每次clickCallback事件中都会重新绘制pageList，此处请设置为false减少绘制消耗
                    pageSize: 10,//每页显示的数据条数
                    currentPage: 1,//当前第几页，索引从1开始
                    totalCount: 0,//总记录数
                    currentPageCenter: true,//当前页是否居中，true表示居中,false表示按showPageRange倍率范围显示,注意此值会导致完全不同的显示方式
                    showPageRange: 5//允许最小值3，当currentPageCenter设置为true时，表示去除第一页，最后一页后，还需显示的页面数量；为false时,表示在倍率范围内应当显示的页面链接数量,
                };
                arg = $.extend({}, defaultSettings, arg);
                var totalPages = ~~(arg.totalCount / arg.pageSize) + (~~(arg.totalCount % arg.pageSize) == 0 ? 0 : 1);//获取总页数
                if (arg.currentPage < 1) {//修正当前页页码为第一页
                    arg.currentPage = 1;
                }
                if (arg.currentPage > totalPages) {//修正当前页页码为最后一页
                    arg.currentPage = totalPages;
                }
                if (!(arg.showPageRange > 2)) {
                    arg.showPageRange = 3;
                }
                $(this).data('pageListArg', arg);
                $(this).each(function () {
                    $(this).empty();//无数据
                    if (totalPages > 0) {
                        var ul = $('<ul class="pager"></ul>');
                        var startPage = 2, endPage = totalPages - 1;//排除首页最后一页后显示的第一个超链接，最后一个超链接
                        var prevS = false, nextS = false;//是否需要显示…对应的超链接
                        if (arg.showPageRange + 4 < totalPages) {//因为页面链接最多包含arg.showPageRange + 4个，所以如果总页数大于时，才显示对应的…
                            if (!arg.currentPageCenter) {
                                var rangeIdx = ~~(arg.currentPage / arg.showPageRange) + (~~(arg.currentPage % arg.showPageRange) == 0 ? 0 : 1);
                                startPage = (rangeIdx - 1) * arg.showPageRange + 1;
                                endPage = rangeIdx * arg.showPageRange;
                                if (startPage < 2) { startPage = 2; }//修正
                                if (endPage >= totalPages) { endPage = totalPages - 1; }//修正
                                if (startPage >= endPage) { startPage = startPage - arg.showPageRange; }//修正
                                if (endPage == totalPages - 2) { endPage++; }//修正
                                prevS = startPage >= arg.showPageRange;
                                nextS = endPage < totalPages - 1;
                            }
                            else {
                                var prevReduce = ~~(arg.showPageRange / 2);
                                var nextAdd = prevReduce;
                                if (~~(arg.showPageRange % 2) == 0) {
                                    prevReduce--;//showPageRange为偶数时，currentPage前面显示的页码链接数比后面显示的链接数少一个
                                }
                                if (prevReduce < 0) {//修正当showPageRange被设置为1导致的负数
                                    prevReduce = 0;
                                }
                                startPage = arg.currentPage - prevReduce;
                                if (startPage < 2) { startPage = 2; }//修正startPage
                                endPage = arg.currentPage + nextAdd;
                                if (endPage - startPage < arg.showPageRange) { endPage = startPage + arg.showPageRange - 1; }//根据startPage修正endPage
                                if (endPage > totalPages - 1) { endPage = totalPages - 1; startPage = endPage - arg.showPageRange + 1; }//修正endPage,并同步修正startPage
                                if (startPage <= 3) {//再次修正startPage
                                    startPage = 2;
                                }
                                if (endPage > totalPages - 3) {//再次修正endPage
                                    endPage = totalPages - 1;
                                }
                                prevS = startPage - 1 > 1;
                                nextS = endPage + 1 < totalPages;
                            }
                        }
                        var li = renderDoms(arg.prevText, arg.currentPage == 1, false, arg.currentPage - 1, arg);//前一页
                        li.addClass("prev");
                        ul.append(li);
                        ul.append(renderDoms("1", arg.currentPage == 1, arg.currentPage == 1, 1, arg));//第一页
                        if (prevS) {
                            ul.append(renderDoms('…', false, false, startPage - 1, arg));//…页
                        }
                        for (var i = startPage; i <= endPage; i++) {
                            ul.append(renderDoms(i, arg.currentPage == i, arg.currentPage == i, i, arg));//第i页
                        }
                        if (nextS) {
                            ul.append(renderDoms('…', false, false, endPage + 1, arg));//…页
                        }
                        if (totalPages > 1) {
                            ul.append(renderDoms(totalPages, arg.currentPage == totalPages, arg.currentPage == totalPages, totalPages, arg));//最后一页
                        }
                        li = renderDoms(arg.nextText, arg.currentPage == totalPages, false, arg.currentPage + 1, arg);//下一页
                        li.addClass("next");
                        ul.append(li);
                        var showGo;
                        switch ((arg.showGoLink + '').toLowerCase()) {
                            case "true":
                                showGo = true; break;
                            case "false":
                                showGo = false; break;
                            default:
                                showGo = arg.showPageRange + 4 < totalPages; break;
                        }
                        if (showGo) {
                            li = $('<li class="text"><span class="go">' + arg.goText + '</span></li>');
                            var sel;
                            if (arg.goInputType.toLowerCase() != 'text') {
                                sel = $('<select class="go"></select>');//<input tyle="text" class="go" />
                                for (var i = 1; i <= totalPages; i++) {
                                    sel.append('<option value="' + i + '">' + i + '</option>');
                                }
                                sel.val(arg.currentPage);
                            }
                            else {
                                sel = $('<input tyle="text" class="go" />');
                                sel.focus(function () {
                                    $(this).val('');
                                }).change(function () {
                                    var num = parseInt($(this).val());
                                    if (num && num > 0) {
                                        if (num > totalPages) {
                                            num = totalPages;
                                        }
                                        $(this).val(num);
                                    }
                                    else {
                                        $(this).val('');
                                    }
                                }).keyup(function () { $(this).change(); });
                            }
                            var sp = li.find('span');
                            sel.insertBefore(sp);
                            sp.click(function () {
                                var pageNumber = ~~$(this).parent().find('.go:eq(0)').val();
                                if (pageNumber > 0) {
                                    clickEvent($(this).parent(), arg, pageNumber);
                                }
                            });
                            ul.append(li);
                        }
                        if (typeof arg.recordText === "string" && $.trim(arg.recordText) != "") {
                            ul.append('<li class="text">' + arg.recordText.replace(/\{0\}/g, totalPages).replace(/\{1\}/g, arg.totalCount) + '</li>');
                        }
                        $(this).append(ul);
                    }
                });
            }
            function renderDoms(text, disable, active, pageNumber, arg) {
                var li = $('<li><a style="cursor:' + (disable ? "" : "pointer") + ';">' + text + '</a></li>');
                if (active) {
                    li.addClass("active");
                }
                if (disable) {
                    li.addClass("disable");
                }
                else {
                    li.click(function () {
                        clickEvent(this, arg, pageNumber);
                    });
                }
                return li;
            }
            function clickEvent(dom, arg, pageNumber) {
                if (typeof arg.clickCallback === "function") {
                    arg.clickCallback(pageNumber);
                }
                if (arg.renderPerCall) {
                    arg.currentPage = pageNumber;
                    $(dom).parent().parent().pageList(arg);
                }
            }
        };