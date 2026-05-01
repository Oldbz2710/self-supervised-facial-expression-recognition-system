<template>
  <div style="width: 100%">
    <el-header
      class="title"
      style="
        height: 50px;
        background-color: #378dd6;
        top: -15px;
        width: 100%;
        color: #e6e6e6;
      "
    >
      <span class="titleLeft">
        <el-button
          text
          @click="onBack"
          style="
            border: none;
            margin-right: 5px;
            margin-bottom: 2px;
            color: #e6e6e6;
          "
          class="backButton"
        >
          <el-icon><Back /></el-icon>
          返回主页
        </el-button>
        <span style="padding-left: 5px; border-left: #e6e6e6 solid 1px">
          训练详情
        </span>
      </span>
    </el-header>
    <div
      style="
        height: 50px;
        align-items: center;
        border-left: 1px solid #f6f6f6;
        border-right: 1px solid #f6f6f6;
      "
    >
      <span style="margin-left: 10px; margin-right: 5px; line-height: 50px"
        >当前最佳模型名称:{{ name }}</span
      >
      <span style="margin-right: 5px; line-height: 50px"
        >共执行{{ epochs }}轮次</span
      >
      <span style="color: #f66262; margin-right: 5px; line-height: 50px"
        >准确率{{ accuracy }}</span
      >
    </div>
    <el-collapse accordion>
      <el-collapse-item
        v-for="items in modelData"
        :key="items.modelName"
        style="border-left: 1px solid #f6f6f6; border-right: 1px solid #f6f6f6"
        @click="checkTrainningDetail(items)"
      >
        <template #title>
          <div
            style="width: 100%; display: flex; justify-content: space-between"
          >
            <span style="margin-left: 10px; color: #666666; width: 10%">{{
              items.modelName
            }}</span>
            <span style="margin-left: 10px; color: #666666; width: 10%"
              >共执行{{ items.epoch }}个轮次</span
            >
            <span style="margin-left: 10px; color: #666666; width: 10%"
              >耗时{{ items.runTime }}</span
            >
            <span style="margin-left: 10px; color: #666666; width: 10%"
              >最终准确率：{{ items.accuracy }}</span
            >
          </div>
        </template>
        <modelCharts
          :model-name="items.modelName"
          :modelId="items.id"
          ref="chart"
        />
      </el-collapse-item>
    </el-collapse>
  </div>
</template>

<script>
import { ElHeader, ElButton, ElCollapse, ElCollapseItem } from "element-plus";
import modelCharts from "./modelCharts.vue";

export default {
  name: "processMain",
  components: { ElHeader, ElButton, ElCollapse, ElCollapseItem, modelCharts },
  // 定义列表中的数据
  data() {
    return {
      //flag控制面板首次打开加载
      name: " MoCoV3 aug+",
      epochs: "100",
      accuracy: "65%",
      flag: [0, 0, 0, 0, 0, 0, 0, 0],
      modelData: [
        {
          modelName: "EfficientNet_b0",
          epoch: "70",
          accuracy: "65%",
          id: "1",
          runTime: "1.37hr",
        },
        {
          modelName: "SimCLR",
          epoch: "100",
          runTime: "2.3days",
          accuracy: "50.3%",
          id: "2",
        },
        {
          modelName: "MoCo",
          epoch: "100",
          runTime: "21.6min",
          accuracy: "51.5%",
          id: "3",
        },
        {
          modelName: "SimSiam",
          epoch: "200",
          runTime: "1.83days",
          accuracy: "50.8%",
          id: "4",
        },
        {
          modelName: "BYOL",
          epoch: "100",
          runTime: "28.6min",
          accuracy: "52.4%",
          id: "5",
        },
        {
          modelName: "MoCoV2",
          epoch: "100",
          runTime: "22.7min",
          accuracy: "54%",
          id: "6",
        },
        {
          modelName: "MoCoV3",
          epoch: "100",
          runTime: "1.557h",
          accuracy: "57.6%",
          id: "7",
        },
        {
          modelName: "MoCoV3 aug+",
          epoch: "100",
          runTime: "1.285h",
          accuracy: "65.35%",
          id: "8",
        },
      ],
    };
  },

  foldColomns: [
    { label: "", prop: "" },
    { label: "", prop: "" },
  ],
  methods: {
    onBack() {
      this.$router.go(-1);
    },
    checkTrainningDetail(items) {
      console.log(items.id);
      if (this.flag[items.id - 1] == 0) {
        this.$refs.chart[items.id - 1].onOpen();
        this.flag[items.id - 1] = 1;
      }
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.title {
  width: 100%;
  display: flex;
}
.titleLeft {
  float: left;
  line-height: 50px;
  font-size: 18px;
}
.backButton :hover {
  color: #378dd6;
}
</style>
