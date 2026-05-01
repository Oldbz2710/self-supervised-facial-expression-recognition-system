<template>
  <div class="common-layout">
    <el-container style="width: 100%">
      <el-main style="width: 100%">
        <div style="width: 100%; background-color: #378dd6; height: 50px"></div>
        <h1 style="text-align: center; margin-top: 4%">
          基于自监督学习的人脸识别算法研究与实现
        </h1>
        <div style="display: flex; flex-wrap: nowrap; margin-top: 3%">
          <el-card
            shadow="hover"
            style="width: 25%; margin-left: 6%; height: 35%"
          >
            <template #header>
              <div class="cardHeader">
                <h3>01 特征展示</h3>
              </div>
            </template>
            <p>
              此模块通过表格的方式对各模型的特点进行展示，并对各基于对比自监督学习方法的模型优势，学习方式，骨干网络，损失函数以及模型结构进行详细介绍
            </p>
            <template #footer>
              <div class="cardFooter" style="text-align: center">
                <el-button type="plain" @click="goToContrast">
                  <span style="margin-left: 3px; margin-right: 3px">
                    前往页面
                  </span></el-button
                >
              </div>
            </template>
          </el-card>
          <el-card shadow="hover" style="width: 25%; margin-left: 6%">
            <template #header>
              <div class="cardHeader">
                <h3>02 训练详情</h3>
              </div>
            </template>
            <p>
              此模块将通过折叠面板的方式对模型详细训练过程进行展示，包括模型训练数据集，验证混淆矩阵，训练详细参数，准确率损失函数折线图等
            </p>
            <template #footer>
              <div class="cardFooter" style="text-align: center">
                <el-button type="plain" @click="goToProccess">
                  <span style="margin-left: 3px; margin-right: 3px">
                    前往页面
                  </span>
                </el-button>
              </div>
            </template>
          </el-card>
          <el-card shadow="hover" style="width: 25%; margin-left: 6%">
            <template #header>
              <div class="cardHeader">
                <h3>03 调用测试</h3>
              </div>
            </template>
            <p>
              此模块将提供模型测试接口，用户调用浏览器摄像机或直接导入图片，对包含表情的人脸图像进行识别分类以验证模型的准确率
            </p>
            <template #footer>
              <div class="cardFooter" style="text-align: center">
                <el-button type="plain" @click="goToTest">
                  <span style="margin-left: 3px; margin-right: 3px">
                    前往页面
                  </span></el-button
                >
              </div>
            </template>
          </el-card>
        </div>
      </el-main>
    </el-container>
  </div>
</template>
<script>
import { ElButton, ElCard, ElContainer } from "element-plus";

export default {
  name: "mainPage",
  components: { ElButton, ElCard, ElContainer },
  data() {
    return {};
  },
  methods: {
    goToContrast() {
      this.$router.push("/contrast");
    },
    goToProccess() {
      this.$router.push("/process");
    },
    goToTest() {
      this.$router.push("/test");
    },
  },
};
</script>
<style lang="css" scoped>
* {
  margin: 0;
  padding: 0;
}
body {
  overflow: hidden;
}
</style>
