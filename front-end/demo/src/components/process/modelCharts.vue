<template>
  <div style="display: flex; width: 100%; height: 450px">
    <div
      style="
        flex: 3;
        margin-left: 10px;
        border-radius: 1%;
        border-color: #378dd6;
        border-width: 1px;
      "
    >
      <div style="margin-top: 2%">
        <el-select
          @change="switchDataset"
          v-model="dataset.id"
          style="width: 96%; margin-left: 2%"
        >
          <el-option
            v-for="item in dataset"
            :key="item.id"
            :label="item.name"
            :value="item.id"
          >
          </el-option>
        </el-select>
        <p style="font-size: 16px; margin-left: 2%">
          训练用数据集：{{ currentData.name }}
        </p>
        <p style="font-size: 16px; margin-left: 2%">
          总数据量：{{ currentData.total }}
        </p>
      </div>
      <div>
        <div
          ref="datasetChart"
          style="width: 96%; height: 300px; margin-left: 2%"
        ></div>
      </div>
    </div>
    <div
      style="
        flex: 3;
        margin-left: 10px;
        border-radius: 1%;
        border-color: #378dd6;
        border-width: 1px;
      "
    >
      <span class="demonstration">混淆矩阵</span>
      <el-image
        :src="require(`../../assets/pic/test_confusion/${currentCMSrc}`)"
        :fit="fill"
        style="margin-top: 15px"
      >
        <efficient
      /></el-image>
    </div>
    <div style="flex: 3; margin-left: 10px">
      <el-image
        :src="require(`../../assets/pic/process/${currentAccSrc}`)"
        :fit="fill"
      >
      </el-image>
      <el-image
        :src="require(`../../assets/pic/process/${currentLossSrc}`)"
        :fit="fill"
      >
      </el-image>
    </div>
  </div>
</template>
<script>
import { ElOption, ElSelect, ElImage } from "element-plus";
import * as echarts from "echarts";

export default {
  name: "modelCharts",
  components: { ElSelect, ElOption, ElImage },
  props: {
    modelName: { type: String },
    modelId: { type: String },
  },
  data() {
    return {
      currentCMSrc: "logo.png",
      currentAccSrc: "logo.png",
      currentLossSrc: "logo.png",
      currentData: {},
      currentModel: {},
      pieChartData: [
        {
          name: "angry",
          value: "",
        },
        {
          name: "disgust",
          value: "",
        },
        {
          name: "fear",
          value: "",
        },
        {
          name: "happy",
          value: "",
        },
        {
          name: "netrual",
          value: "",
        },
        {
          name: "sad",
          value: "",
        },
        {
          name: "surprise",
          value: "",
        },
      ],
      dataset: [
        {
          id: "1",
          name: "FETD",
          total: "26171",
          angryTrain: "3218",
          disgustTrain: "2477",
          fearTrain: "3176",
          happyTrain: "5044",
          netrualTrain: "5126",
          sadTrain: "3091",
          surpriseTrain: "4039",
        },

        {
          id: "2",
          name: "FERplus",
          total: "23251",
          angryTrain: "3315",
          disgustTrain: "3367",
          fearTrain: "3346",
          happyTrain: "3334",
          netrualTrain: "3376",
          sadTrain: "3192",
          surpriseTrain: "3321",
        },
      ],
      ProcessData: [
        {
          id: "1",
          modelName: "efficientNet",
          CMName: ["FETD_efficient.png", "plus_efficient.png"],
          accSrc: ["efficient_FETD_val_acc.png", "efficient_plus_val_acc.png"],
          lossSrc: [
            "efficient_FETD_val_loss.png",

            "efficient_plus_val_loss.png",
          ],
        },
        {
          id: "2",
          modelName: "SimCLR",
          CMName: ["FETD_efficient.png", "plus_efficient.png"],
          accSrc: ["efficient_FETD_val_acc.png", "efficient_plus_val_acc.png"],
          lossSrc: [
            "efficient_FETD_val_loss.png",

            "efficient_plus_val_loss.png",
          ],
        },
        {
          id: "3",
          modelName: "MoCo",
          CMName: ["FETD_efficient.png", "plus_efficient.png"],
          accSrc: ["efficient_FETD_val_acc.png", "efficient_plus_val_acc.png"],
          lossSrc: [
            "efficient_FETD_val_loss.png",

            "efficient_plus_val_loss.png",
          ],
        },
        {
          id: "4",
          modelName: "SimSiam",
          CMName: ["FETD_simsiam.png", "plus_simsiam.png"],
          accSrc: ["efficient_FETD_val_acc.png", "simsiam_plus_val_acc.png"],
          lossSrc: ["efficient_FETD_val_loss.png", "simsiam_plus_val_loss.png"],
        },
        {
          id: "5",
          modelName: "BYOL",
          CMName: ["FETD_efficient.png", "plus_efficient.png"],
          accSrc: ["efficient_FETD_val_acc.png", "efficient_plus_val_acc.png"],
          lossSrc: [
            "efficient_FETD_val_loss.png",

            "efficient_plus_val_loss.png",
          ],
        },
        {
          id: "6",
          modelName: "MoCoV2",
          CMName: ["FETD_mocov2.png", "plus_mocov2.png"],
          accSrc: ["mocov2_FETD_val_acc.png", "mocov2_plus_val_acc.png"],
          lossSrc: ["mocov2_FETD_val_loss.png", "mocov2_plus_val_loss.png"],
        },
        {
          id: "7",
          modelName: "MoCoV3",
          CMName: ["FETD_mocov3.png", "plus_mocov3.png"],
          accSrc: ["mocov3_FETD_val_acc.png", "mocov3_plus_val_acc.png"],
          lossSrc: ["mocov3_FETD_val_loss.png", "mocov3_plus_val_loss.png"],
        },
        {
          id: "8",
          modelName: "MoCoV3 aug+",
          CMName: ["FETD_mocov3.png", "plus_mocov3aug.png"],
          accSrc: ["mocov3_FETD_val_acc.png", "mocov3aug_plus_val_acc.png"],
          lossSrc: ["mocov3_FETD_val_loss.png", "mocov3aug_plus_val_loss.png"],
        },
      ],
    };
  },

  methods: {
    onOpen() {
      //数据集赋值
      this.currentData = this.dataset[0];
      this.pieChartData[0].value = this.currentData.angryTrain;
      this.pieChartData[1].value = this.currentData.disgustTrain;
      this.pieChartData[2].value = this.currentData.fearTrain;
      this.pieChartData[3].value = this.currentData.happyTrain;
      this.pieChartData[4].value = this.currentData.netrualTrain;
      this.pieChartData[5].value = this.currentData.sadTrain;
      this.pieChartData[6].value = this.currentData.surpriseTrain;
      this.initPieCharts();
      this.initImage(this.currentData.id);
    },
    switchDataset(id) {
      this.currentData = this.dataset[id - 1];
      this.pieChartData[0].value = this.currentData.angryTrain;
      this.pieChartData[1].value = this.currentData.disgustTrain;
      this.pieChartData[2].value = this.currentData.fearTrain;
      this.pieChartData[3].value = this.currentData.happyTrain;
      this.pieChartData[4].value = this.currentData.netrualTrain;
      this.pieChartData[5].value = this.currentData.sadTrain;
      this.pieChartData[6].value = this.currentData.surpriseTrain;
      //console.log(this.pieChartData);
      this.initPieCharts();
      this.initImage(id);
    },
    initPieCharts() {
      const chart = echarts.init(this.$refs.datasetChart);
      const option = {
        tooltip: {
          trigger: "item",
        },
        legend: {
          orient: "vertical",
          left: "left",
        },
        title: {
          text: this.currentData.name,
          left: "center",
        },
        series: [
          {
            name: "train dataset",
            type: "pie",
            radius: ["40%", "70%"],
            itemStyle: {
              borderRadius: 10,
              borderColor: "#fff",
              borderWidth: 2,
            },
            label: {
              show: false,
              position: "center",
            },
            emphasis: {
              label: {
                show: true,
                fontSize: 28,
                fontWeight: "bold",
              },
            },
            labelLine: { show: false },
            data: this.pieChartData,
          },
        ],
      };
      chart.setOption(option);
    },
    initImage(id) {
      this.currentModel = this.ProcessData[this.modelId - 1];
      const name = this.currentModel.CMName[id - 1];
      this.currentAccSrc = this.currentModel.accSrc[id - 1];
      this.currentLossSrc = this.currentModel.lossSrc[id - 1];
      this.currentCMSrc = name;
    },
  },
};
</script>

<style scoped>
.demonstration {
  display: block;
  color: var(--el-text-color-secondary);
  font-size: 14px;
  margin-top: 20px;
}
</style>
