<template>
    <div class="w-96 sm:w-[28rem]">
        <Doughnut v-if="chartToShow == 'doughnut'" id="my-chart-id" :options="chartOptions" :data="chartData" />
        <Bar v-else-if="chartToShow == 'bar'" id="my-chart-id" :options="chartOptions" :data="chartData" />
        <PolarArea v-else-if="chartToShow == 'polar'" id="my-chart-id" :options="chartOptions" :data="chartData" />
        <Pie v-else-if="chartToShow == 'pie'" id="my-chart-id" :options="chartOptions" :data="chartData" />
    </div>
</template>

<script setup>
import { Doughnut, Bar, PolarArea, Pie, Scatter } from 'vue-chartjs'
import { Chart as ChartJS, BarController, BubbleController, DoughnutController, LineController, PieController, PolarAreaController, RadarController, ScatterController, ArcElement, BarElement, LineElement, PointElement, Filler, Legend, SubTitle, Title, Tooltip, CategoryScale, LinearScale, LogarithmicScale, RadialLinearScale, TimeScale, TimeSeriesScale } from 'chart.js'

ChartJS.register(BarController, BubbleController, DoughnutController, LineController, PieController, PolarAreaController, RadarController, ScatterController, ArcElement, BarElement, LineElement, PointElement, Filler, Legend, SubTitle, Title, Tooltip, CategoryScale, LinearScale, LogarithmicScale, RadialLinearScale, TimeScale, TimeSeriesScale)

defineProps({
    chartToShow: {
        type: String,
        default: 'doughnut'
    },
    labels: {
        type: Array,
        required: true
    },
    chartData: {
        type: Object,
        required: true
    },
    chartOptions: {
        type: Object,
        default: {
            responsive: true
        }
    }
})
</script>