var pathname = location.pathname.split('/');
var barChart = [],
    barChartData = [],
    lineChartData = [],
    isResize = false;

//bar
function generBar(elem, dataBar, con = 0){
    let canvas = document.getElementById(elem)
        ctx = canvas.getContext('2d'),
        fontSize = parseInt($('html').css('font-size')) * 1.2;
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    if(barChart[con])
        barChart[con].destroy();

    barChart[con] = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: dataBar['month'],
            datasets: [{
                data: dataBar['count'],
                backgroundColor: '#634FED',
                borderRadius: 20,
                barPercentage: 0.9,
                hoverBackgroundColor: '#7664f0'
            }]
        },
        options: {
            title: {
                display: false
            },
            scales: {
                x: {
                    ticks: {
                        font: {
                            size: fontSize
                        },
                        color: '#6E6598'
                    }
                },
                y: {
                    ticks: {
                        font: {
                            size: fontSize
                        },
                        color: '#6E6598'
                    },
                    display: false,
                }
            },
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    enabled: true,
                    mode: 'index',
                    intersect: false,
                    backgroundColor: '#453F64',
                    titleFont: {
                        size: fontSize,
                        weight: 'bold'
                    },
                    bodyFont: {
                        size: fontSize
                    },
                    xPadding: 15,
                    yPadding: 15,
                    caretPadding: 5,
                    caretSize: 5,
                    cornerRadius: 8,
                    borderWidth: 0,
                    borderColor: '#6E6598',
                    callbacks: {
                        label: function(tooltipItem) {
                            return 'Количество: ' + tooltipItem.raw;
                        },
                        labelColor: function(tooltipItem) {
                            return {
                                borderColor: '#6E6598', // прозрачная граница
                                backgroundColor: '#6E6598' // прозрачный фон
                            };
                        },
                        labelPointStyle: function() {
                            return {
                                pointStyle: 'line' // задаем стиль точки, чтобы квадрат не отображался
                            };
                        }
                    }
                }
            }
        }
    });
    barChartData[con] = {
        'elem': elem,
        'dataBar': dataBar,
        'con': con
    }
}

window.addEventListener('resize', (e) => {
    if(window.innerWidth == vw && window.innerHeight == vh) return;
    vw = window.innerWidth;
    vh = window.innerHeight;
    barChartData.forEach((item) => generBar(item.elem, item.dataBar, item.con));
    lineChartData.forEach((item) => generLine(item.elem, item.dataLine));
    isResize = true;
});

//круговая диаграмма
function generPie(elem, dataPie){
    var ctx = document.getElementById(elem).getContext('2d');
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            datasets: [{
            data: dataPie.map(obj => obj.count),
            backgroundColor: dataPie.map(obj => obj.color),
            borderWidth: 0,
            borderRadius: 1000,
            }]
        },
        options: {
            cutout: '90%',
            rotation: -10 * Math.PI,
            onHover: (event, chartElement) => {
                const items = document.querySelectorAll('.legend-item');
                items.forEach(item => item.classList.remove('highlight'));
                $('.hportfolio_proc_names').removeClass('pieHoverGraphParent');

                if (chartElement.length > 0) {
                    const index = chartElement[0].index;
                    $('.pie_item_chart').removeClass('pieHoverGraph');
                    $('.hportfolio_proc_names').addClass('pieHoverGraphParent');
                    $('.pie_item-' + index).addClass('pieHoverGraph');
                }
            }
        }
    });
}

//линейная диаграмма
function generLine(elem, dataLine){
    var canvas = document.getElementById(elem),
        ctx = canvas.getContext('2d'),
        fontSize = parseInt($('html').css('font-size')) * 1.2;
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    if(lineChart[0])
        lineChart[0].destroy();

    let bwidth = 7*vw/1000;
    if(bwidth > 7) bwidth = 7;

    lineChart[0] = new Chart(ctx, {
        type: 'line',
        data: {
            labels: dataLine.days,
            datasets: [{
                data: dataLine.count,
                borderColor: '#634FED',
                borderWidth: bwidth,
                pointRadius: dataLine.count.map((value, index) => index === dataLine.count.length - 1 ? bwidth : bwidth / 2),
                pointBackgroundColor: '#3AA1FF',
                pointBorderColor: '#3AA1FF'
            }]
        },
        options: {
            responsive: true,
            scales: {
                x: {
                    ticks: {
                        font: {
                            size: fontSize,
                        },
                        color: '#F1EDFD'
                    },
                    grid: {
                        color: 'rgba(0, 0, 0, 0)'
                    }
                },
                y: {
                    ticks: {
                        font: {
                            size: fontSize
                        },
                        color: '#F1EDFD',
                        callback: function(value) {
                            return value === 0 ? '' : value;
                        },
                    },
                    grid: {
                        color: '#453F64'
                    },
                    beginAtZero: true
                }
            },
            plugins: {
                legend: {
                    display: false // Убираем легенду, если она мешает
                }
            }
        }
    });
    
    lineChartData[0] = {
        'elem': elem,
        'dataLine': dataLine
    }
}



$('.canvas_pie').on('mouseout', function() {
    $('.hportfolio_proc_names').removeClass('pieHoverGraphParent');
    $('.pie_item_chart').removeClass('pieHoverGraph');
});

if(pathname[1] == 'analytic'){
    $('.analytic_slick').slick({
        dots: false,
        infinite: true,
        slidesToShow: 1,
        slidesToScroll: 1
    });

    $(window).on("scroll", function(e){
        $('.slick-arrow').css('top', 'calc(50vh + ' + ($(window).scrollTop() - $('.header').height() - $('nav').height())  + 'px');
    });
    $(window).scroll();
}

let val_sum = '';
$('.inputSpaces').on('keyup. input', function(e){
    let input = $(this),
        val = input.val(),
        pris = (input.hasClass('inputRub')) ? ' ₽' : ' шт',
        maxCount = $(this).attr('data-count');
    if(maxCount != '' && maxCount != undefined && Number(val.replace(/[^0-9]/g, '')) > Number(maxCount.replace(/[^0-9]/g, ''))){
        input.val(val_sum);
        return;
    }
    if(val != val_sum){
        let formatted = val.replace(/[^0-9]/g, '').replace(/\B(?=(\d{3})+(?!\d))/g, ' ');
        formatted = formatted ? formatted + pris : '';
        input.prop("selectionStart");
        input.val(formatted);
        if (formatted.endsWith(' ₽') || formatted.endsWith(' шт')) {
            let newCursorPosition = formatted.length - (formatted.endsWith(' ₽') ? 2 : 3);
            input.prop("selectionStart", newCursorPosition);
            input.prop("selectionEnd", newCursorPosition);
        }
    }
    val_sum = val;
});

if(pathname[1] == 'profile'){
    $('#deleteProfile').on('click', function(){
        if(blocked_button) return;
        blocked_button = true;
        
        if(blocked_button && !errs){
            $('#success_message, #error_message').text('');
            let params = new URLSearchParams();
            if(pathname[2] != undefined)
                params.append('id', pathname[2]);
            request("/deleteProfile/", params, function(result){
                try{
                    response = JSON.parse(result);
                    if(response.result == 'fail'){
                        $('#error_message').text(response.message);
                        $('#success_message').text('');
                        return;
                    }
                    res = JSON.parse(response.result);
                    if(res['status'] == 'success'){
                        $('#success_message').text(res.message);
                        $('#error_message').text('');
                        setTimeout(() => window.location.href = '/auth/', 1500);
                        return;
                    }
                    
                    $('#error_message').text(res.message);
                    blocked_button = false;
                }
                catch(e){
                    err('form', 'Неожиданная ошибка');
                }
            });
        }
        blocked_button = false;
    });
}