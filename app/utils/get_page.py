def get_page(total,p):
    show_page = 5   # ��ʾ��ҳ����
    pageoffset = 2  # ƫ����
    start = 1    #��ҳ����ʼ
    end = total  #��ҳ������

    if total > show_page:
        if p > pageoffset:
            start = p - pageoffset
            if total > p + pageoffset:
                end = p + pageoffset
            else:
                end = total
        else:
            start = 1
            if total > show_page:
                end = show_page
            else:
                end = total
        if p + pageoffset > total:
            start = start - (p + pageoffset - end)
    #����ģ����ѭ��
    dic = range(start, end + 1)
    return dic