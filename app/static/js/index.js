// JavaScript Document
// echarts
// create for AgnesXu at 20161115


//环状图
var ring = echarts.init(document.getElementById('ring'));
var labelTop = {
    normal : {
        label : {
            show : true,
            position : 'center',
            formatter : '{b}',
            textStyle: {
                baseline : 'bottom'
            }
        },
        labelLine : {
            show : false
        }
    }
};

var labelFromatter = {
    normal : {
        label : {
            formatter : function (params){
                return 100 - params.value + '%'
            },
            textStyle: {
                baseline : 'top'
            }
        }
    },
}
var labelBottom = {
    normal : {
        color: '#ccc',
        label : {
            show : true,
            position : 'center'
        },
        labelLine : {
            show : false
        }
    },
    emphasis: {
        color: 'rgba(0,0,0,0)'
    }
};
var radius = [40, 55];
ring.setOption({
    color:["#33bb9f","#ffa259","#4cbbe6"],
    series : [
        {
            type : 'pie',
            center : ['15%', '58%'],
            radius : radius,
            x: '0%', // for funnel
            itemStyle : labelFromatter,
            data : [
                {name:'other', value:26, itemStyle : labelBottom},
                {name:'完成', value:84,itemStyle : labelTop}
            ]
        },
        {
            type : 'pie',
            center : ['45%', '58%'],
            radius : radius,
            x:'20%', // for funnel
            itemStyle : labelFromatter,
            data : [
                {name:'other', value:76, itemStyle : labelBottom},
                {name:'退回', value:24,itemStyle : labelTop}
            ]
        },
        {
            type : 'pie',
            center : ['75%', '58%'],
            radius : radius,
            x:'40%', // for funnel
            itemStyle : labelFromatter,
            data : [
                {name:'other', value:35, itemStyle : labelBottom},
                {name:'未完成', value:65,itemStyle : labelTop}
            ]
        }
    ]
}) ;





//折线图
var line = echarts.init(document.getElementById('line'));
line.setOption({
    color:["#32d2c9"],
    title: {
        x: 'left',
        text: '成绩统计',
        textStyle: {
            fontSize: '18',
            color: '#4c4c4c',
            fontWeight: 'bolder'
        }
    },
    tooltip: {
        trigger: 'axis'
    },
    toolbox: {
        show: true,
        feature: {
            dataZoom: {
                yAxisIndex: 'none'
            },
            dataView: {readOnly: false},
            magicType: {type: ['line', 'bar']}
        }
    },
    xAxis:  {
        type: 'category',
        boundaryGap: false,
        data: ['周一','周二','周三','周四','周五','周六','周日'],
        axisLabel: {
            interval:0
        }
    },
    yAxis: {
        type: 'value'
    },
    series: [
        {
            name:'成绩',
            type:'line',
            data:[23, 42, 18, 45, 48, 49,100],
            markLine: {data: [{type: 'average', name: '平均值'}]}
        }
    ]
}) ;



//柱状图
var pillar1 = echarts.init(document.getElementById('pillar1'));
pillar1.setOption({
    color:["#ce6e73","#ee804b","#ffc668"],
    title : {
        subtext: '平均分（分）'
    },
    tooltip : {
        trigger: 'axis'
    },
    legend: {
        x: 'right',
        data:['您的班级','全市','全国']
    },
    calculable : true,
    xAxis : [
        {
            type : 'category',
            data : ['语言','词汇','词汇1','词汇2','词汇3','词汇4',
            '词汇5','词汇6','词汇7','词汇8','词汇9','词汇10']
        }
    ],
    yAxis : [
        {
            type : 'value'
        }
    ],
    series : [
        {
            name:'您的班级',
            type:'bar',
            data:[74, 62, 56, 79, 80, 30, 55, 35, 38, 41, 75, 89]
        },
        {
            name:'全市',
            type:'bar',
            data:[70, 65, 80, 71, 70, 40, 35, 46, 58, 40, 56, 30]
        },
        {
            name:'全国',
            type:'bar',
            data:[60, 55, 70, 61, 60, 30, 45, 36, 48, 50, 56, 40]
        }
    ]
}) ;



//柱状图2
var pillar2 = echarts.init(document.getElementById('pillar2'));
pillar2.setOption({
    color:["#00afff"],
    tooltip : {
        trigger: 'axis'
    },
    calculable : true,
    xAxis : [
        {
            type : 'category',
            data : ['语言','词汇','词汇1','词汇2','词汇3','词汇4',
            '词汇5','词汇6','词汇7']
        }
    ],
    yAxis : [
        {
            type : 'value'
        }
    ],
    series : [
        {
            name:'您的班级',
            type:'bar',
            data:[74, 62, 56, 79, 80, 30, 55, 35, 38]
        }
    ]
});
