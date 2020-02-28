        $.fn.pageList = function (arg, methodName) {
            if (typeof methodName === "string" && $.trim(methodName) != "") {
                switch (methodName) {
                    case 'refresh'://ˢ�µ�ǰҳ,һ������ɾ�����߸��º�
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
                    prevText: 'Prev',//��ʾ��ǰһҳ�ı�
                    nextText: 'Next',//��ʾ����һҳ�ı�
                    showGoLink: 'auto',//�Ƿ���ʾ������ת�����ܵ�ֵΪauto �Զ��жϣ�true ��Զ��ʾ��false ������ʾ
                    goInputType: 'select',//�����ʾ������ת���룬���ܵ�ֵΪselect �����б�text �����Ĭ��ֵΪselect
                    goText: 'Go',//��ʾ�Ŀ�����ת�ı�
                    recordText: '',//��ʾ��¼����Ϊ��ʱ����ʾ��������ռλ����ʾ�ı���{0}��ʾ��ҳ����{1}��ʾ�ܼ�¼��
                    clickCallback: function (currentPage) { },//���ӱ����ʱ�������¼���currentPage��ʾ��ǰ������ǵڼ�ҳ��������1��ʼ
                    renderPerCall: true,//�Ƿ�ÿ�ε�������»��ƣ����ÿ��clickCallback�¼��ж������»���pageList���˴�������Ϊfalse���ٻ�������
                    pageSize: 10,//ÿҳ��ʾ����������
                    currentPage: 1,//��ǰ�ڼ�ҳ��������1��ʼ
                    totalCount: 0,//�ܼ�¼��
                    currentPageCenter: true,//��ǰҳ�Ƿ���У�true��ʾ����,false��ʾ��showPageRange���ʷ�Χ��ʾ,ע���ֵ�ᵼ����ȫ��ͬ����ʾ��ʽ
                    showPageRange: 5//������Сֵ3����currentPageCenter����Ϊtrueʱ����ʾȥ����һҳ�����һҳ�󣬻�����ʾ��ҳ��������Ϊfalseʱ,��ʾ�ڱ��ʷ�Χ��Ӧ����ʾ��ҳ����������,
                };
                arg = $.extend({}, defaultSettings, arg);
                var totalPages = ~~(arg.totalCount / arg.pageSize) + (~~(arg.totalCount % arg.pageSize) == 0 ? 0 : 1);//��ȡ��ҳ��
                if (arg.currentPage < 1) {//������ǰҳҳ��Ϊ��һҳ
                    arg.currentPage = 1;
                }
                if (arg.currentPage > totalPages) {//������ǰҳҳ��Ϊ���һҳ
                    arg.currentPage = totalPages;
                }
                if (!(arg.showPageRange > 2)) {
                    arg.showPageRange = 3;
                }
                $(this).data('pageListArg', arg);
                $(this).each(function () {
                    $(this).empty();//������
                    if (totalPages > 0) {
                        var ul = $('<ul class="pager"></ul>');
                        var startPage = 2, endPage = totalPages - 1;//�ų���ҳ���һҳ����ʾ�ĵ�һ�������ӣ����һ��������
                        var prevS = false, nextS = false;//�Ƿ���Ҫ��ʾ����Ӧ�ĳ�����
                        if (arg.showPageRange + 4 < totalPages) {//��Ϊҳ������������arg.showPageRange + 4�������������ҳ������ʱ������ʾ��Ӧ�ġ�
                            if (!arg.currentPageCenter) {
                                var rangeIdx = ~~(arg.currentPage / arg.showPageRange) + (~~(arg.currentPage % arg.showPageRange) == 0 ? 0 : 1);
                                startPage = (rangeIdx - 1) * arg.showPageRange + 1;
                                endPage = rangeIdx * arg.showPageRange;
                                if (startPage < 2) { startPage = 2; }//����
                                if (endPage >= totalPages) { endPage = totalPages - 1; }//����
                                if (startPage >= endPage) { startPage = startPage - arg.showPageRange; }//����
                                if (endPage == totalPages - 2) { endPage++; }//����
                                prevS = startPage >= arg.showPageRange;
                                nextS = endPage < totalPages - 1;
                            }
                            else {
                                var prevReduce = ~~(arg.showPageRange / 2);
                                var nextAdd = prevReduce;
                                if (~~(arg.showPageRange % 2) == 0) {
                                    prevReduce--;//showPageRangeΪż��ʱ��currentPageǰ����ʾ��ҳ���������Ⱥ�����ʾ����������һ��
                                }
                                if (prevReduce < 0) {//������showPageRange������Ϊ1���µĸ���
                                    prevReduce = 0;
                                }
                                startPage = arg.currentPage - prevReduce;
                                if (startPage < 2) { startPage = 2; }//����startPage
                                endPage = arg.currentPage + nextAdd;
                                if (endPage - startPage < arg.showPageRange) { endPage = startPage + arg.showPageRange - 1; }//����startPage����endPage
                                if (endPage > totalPages - 1) { endPage = totalPages - 1; startPage = endPage - arg.showPageRange + 1; }//����endPage,��ͬ������startPage
                                if (startPage <= 3) {//�ٴ�����startPage
                                    startPage = 2;
                                }
                                if (endPage > totalPages - 3) {//�ٴ�����endPage
                                    endPage = totalPages - 1;
                                }
                                prevS = startPage - 1 > 1;
                                nextS = endPage + 1 < totalPages;
                            }
                        }
                        var li = renderDoms(arg.prevText, arg.currentPage == 1, false, arg.currentPage - 1, arg);//ǰһҳ
                        li.addClass("prev");
                        ul.append(li);
                        ul.append(renderDoms("1", arg.currentPage == 1, arg.currentPage == 1, 1, arg));//��һҳ
                        if (prevS) {
                            ul.append(renderDoms('��', false, false, startPage - 1, arg));//��ҳ
                        }
                        for (var i = startPage; i <= endPage; i++) {
                            ul.append(renderDoms(i, arg.currentPage == i, arg.currentPage == i, i, arg));//��iҳ
                        }
                        if (nextS) {
                            ul.append(renderDoms('��', false, false, endPage + 1, arg));//��ҳ
                        }
                        if (totalPages > 1) {
                            ul.append(renderDoms(totalPages, arg.currentPage == totalPages, arg.currentPage == totalPages, totalPages, arg));//���һҳ
                        }
                        li = renderDoms(arg.nextText, arg.currentPage == totalPages, false, arg.currentPage + 1, arg);//��һҳ
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