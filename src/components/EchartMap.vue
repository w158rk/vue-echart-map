<template>
    <div id="mapChart" class="chart"></div>
</template>
<script>
    import echarts from "echarts";
    import axios from 'axios'
    export default {
        props: {
            mapData: {
                type: Array,
                default: [],
            },
            mapOption: {
                type: Object,
            }

        },
        computed: {
            // 通过计算值，将mapOption的默认值补全
            chartOption() {
                return {
                    'title': '地图',
                    'titleColor': '#8796B0',
                    'backgroundColor': '#2B3648',
                    'areaColor': '#262C38',
                    'borderColor': '#678EE3',
                    'hoverAreaColor': '#16467B',
                    'lineColor': 'rgb(192, 158, 255)',
                    'trailColor': '#fff',
                    'endColor': 'rgb(192, 158, 255)',
                    ...this.mapOption
                }
            }
        },
        methods: {
            mapChart() {
                var myChart = echarts.init(document.getElementById('mapChart'));
                // var myChart = echarts.init(document.getElementById('mapChart'), null, {renderer: 'svg'});

                // axios.get("./static/json/map/world.json", {}).then(response => {
                axios.get("https://raw.githubusercontent.com/apache/echarts/master/test/data/map/json/world.json", {}).then(response => {
                    var worldJson = response.data;
                    echarts.registerMap("world", worldJson);
                    var series = [];
                    series.push({
                        // lines that goes from the source to the destination
                        type: 'lines',
                        zlevel: 1,
                        effect: {
                            show: true,
                            period: 6,
                            trailLength: 0.7,
                            color: this.chartOption.trailColor,
                            symbolSize: 3
                        },
                        lineStyle: {
                            normal: {
                                width: 0,
                                curveness: 0.2
                            }
                        },
                        data: this.initData1(this.mapData)
                    }, {
                        // static lines lying under the moving ones
                        type: 'lines',
                        zlevel: 2,
                        effect: {
                            show: true,
                            period: 6,
                            trailLength: 0,
                            symbolSize: 5
                        },
                        lineStyle: {
                            normal: {
                                color: this.chartOption.lineColor,
                                width: 1,
                                opacity: 0.4,
                                curveness: 0.2
                            }
                        },
                        data: this.initData1(this.mapData)
                    }, {
                        // dark scatters
                        type: 'effectScatter',
                        coordinateSystem: 'geo',
                        zlevel: 2,
                        rippleEffect: {
                            brushType: 'stroke'
                        },
                        label: {
                            normal: {
                                show: true,
                                position: 'right',
                                formatter: '{b}'
                            }
                        },
                        symbolSize: function (val) {
                            return val[2] / 8;
                        },
                        data: this.initData2(this.mapData)
                    }, {
                        // bright scatters
                        type: 'effectScatter',
                        coordinateSystem: 'geo',
                        zlevel: 2,
                        rippleEffect: {
                            brushType: 'stroke'
                        },
                        label: {
                            normal: {
                                show: true,
                                position: 'right',
                                formatter: '{b}'
                            }
                        },
                        symbolSize: function (val) {
                            return val[2] / 8;
                        },
                        itemStyle: {
                            normal: {
                                color: this.chartOption.endColor
                            }
                        },
                        data: this.initData2(this.mapData)
                    });

                    myChart.setOption({
                        backgroundColor: this.chartOption.backgroundColor,
                        title: {
                            text: this.chartOption.title,
                            left: 20,
                            top: 10,
                            textStyle: {
                                fontSize: '5px',
                                fontFamily: 'PingFangSC-Regular',
                                fontWeight: 'lighter',
                                color: this.chartOption.titleColor
                            }
                        },
                        toolbox: {
                            show : true,
                            feature : {
                                saveAsImage : {
                                    show: true,
                                    type: 'svg',
                                    pixelRatio:10
                                }
                            }
                        },
                        tooltip: {
                            trigger: 'item',
                            formatter: (param) => {
                                var data = param.data;
                                return data.fromName + ' - ' + data.toName + ' : ' + data.value;
                            }
                        },
                        legend: {
                            orient: 'vertical',
                            top: 'bottom',
                            left: 'right',
                            selectedMode: 'single'
                        },
                        geo: {
                            map: 'world',
                            // center: [115.97, 29.71],
                            label: {
                                emphasis: {
                                    show: false
                                }
                            },
                            roam: true,
                            itemStyle: {
                                normal: {
                                    areaColor: this.chartOption.areaColor,
                                    borderColor: this.chartOption.borderColor
                                },
                                emphasis: {
                                    areaColor: this.chartOption.hoverAreaColor
                                }
                            }
                        },
                        series: series
                    });

                });
            },
            initData1(data) {
                var result = [];
                for (var i = 0; i < data.length; i++) {
                    var el = data[i];
                    var fromData = `${el.from_longitude},${el.from_latitude}`.split(',')
                    var toData = `${el.to_longitude},${el.to_latitude}`.split(',')
                    var val = []
                    val.push(fromData, toData)
                    result.push({
                        fromName: el.from,
                        toName: el.to,
                        coords: val,
                        value: el.num
                    })
                }
                return result;
            },
            initData2(data) {
                var result = [];
                for (var i = 0; i < data.length; i++) {
                    var el = data[i];
                    var val = `${el.to_longitude},${el.to_latitude},30`.split(',')
                    result.push({
                        name: el.to,
                        value: val
                    })
                }
                for (var i = 0; i < data.length; i++) {
                    var el = data[i];
                    var val = `${el.from_longitude},${el.from_latitude},30`.split(',')
                    result.push({
                        name: el.from,
                        value: val
                    })
                }
                return result;
            },
            
        },
        mounted() {
            console.log("mark");
            console.log(this.mapData);
            this.mapChart();
            

        },
    }

</script>
<style scoped>


</style>
